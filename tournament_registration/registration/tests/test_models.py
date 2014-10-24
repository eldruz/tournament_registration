from datetime import date

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from registration.models import Tournament, Entry, Player

class TournamentTestCase(TestCase):
    def setUp(self):
        Tournament.utilities.create_tournament(title='Tournoi test',
                                               game='2X',
                                               date=date.today(),
                                               nb_max=64,
                                               id=5)

    def test_utilities_creation(self):
        """Tournament created with the utility creation funtion is correct"""
        tourney = Tournament.utilities.get(title='Tournoi test')
        self.assertEqual(tourney.title, 'Tournoi test')
        self.assertEqual(tourney.game, '2X')
        self.assertEqual(tourney.date, date.today())
        self.assertEqual(tourney.nb_max, 64)
        self.assertEqual(tourney.support, u'Unknown')
        self.assertEqual(tourney.nb_per_team, 1)
        self.assertEqual(tourney.price, 0)
        self.assertEqual(tourney.id, 5)

    def test_cannot_create_duplicate(self):
        self.assertRaises(ValidationError,
                          Tournament.utilities.create_tournament,
                          title='Tournoi test',
                          game='USF4',
                          date=date.today(),
                          nb_max=32)
        self.assertRaises(ValidationError,
                          Tournament.utilities.create_tournament,
                          title='Tournoi test',
                          game='2X',
                          date=date.today(),
                          nb_max=64)

    def test_game_not_in_list(self):
        """Game field of the tournament is in the authorized games list"""
        self.assertRaises(ValidationError,
                          Tournament.utilities.create_tournament,
                          title='Invalid Game Tournament',
                          game='PACMAN',
                          date=date.today(),
                          nb_max=32)


class PlayerTestCase(TestCase):
    def setUp(self):
        Player.utilities.create_player(name='Eldruz',
                                       team='3HC')

    def test_player_unicity_constraint(self):
        self.assertRaises(IntegrityError,
                          Player.utilities.create_player,
                          name='Eldruz',
                          team='3HC')

    def test_player_creation(self):
        player = Player.objects.get(name='Eldruz',
                                    team='3HC')
        self.assertIsInstance(player, Player)

    def test_player_update(self):
        player = Player.objects.get(name='Eldruz',
                                    team='3HC')
        Player.utilities.update_player(player_id=player.pk,
                                       name='The Eldruz',
                                       team='F3HC')
        # The updated player exists in the database
        player = Player.objects.get(name='The Eldruz',
                                    team='F3HC')
        self.assertIsInstance(player, Player)
        # The old one does not
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          name='Eldruz',
                          team='3HC')

    def test_player_delete(self):
        player1 = Player.utilities.create_player(name='SGwada',
                                                team='3HC')
        player2 = Player.utilities.create_player(name='Nono',
                                                team='3HC')
        self.assertIsInstance(player1, Player)
        self.assertIsInstance(player2, Player)
        # Delete player1 with name and team
        Player.utilities.delete_player(name='SGwada',
                                       team='3HC')
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          name='SGwada',
                          team='3HC')
        # Delete player2 with id
        Player.utilities.delete_player(player_id=player2.pk)
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          pk=player2.pk)


class EntryTestCase(TestCase):
    def setUp(self):
        tourney = Tournament.utilities.create_tournament(title='X-MANIA',
                                                         game='2X',
                                                         date=date.today(),
                                                         nb_max=1,
                                                         id=100)
        player = Player.utilities.create_player(name='Komoda')
        Entry.utilities.create_entry(tournament=tourney,
                                     player=player)

    def test_valid_entry_creation(self):
        """Entry created with the utility function is correct"""
        tournament = Tournament.objects.get(pk=100)
        player = Player.objects.get(name='Komoda')
        entry = Entry.objects.select_related('tournament_id').\
            get(tournament_id=tournament, player=player)
        self.assertEqual(tournament, entry.tournament_id)
        self.assertEqual(player, entry.player)

    def test_is_tournament_full(self):
        tourney = Tournament.utilities.create_tournament(
            title='MORLAIX',
            game='2X',
            date=date.today(),
            nb_max=1)
        straw_player = Player.utilities.create_player(name='Dourssin')
        self.assertEqual(tourney.get_available_spots(), 1)
        Entry.utilities.create_entry(tournament=tourney,
                                     player=straw_player)
        self.assertEqual(tourney.get_available_spots(), 0)


    def test_maximum_number_of_players_registered(self):
        tournament = Tournament.objects.get(pk=100)
        straw_player = Player.utilities.create_player(name='Boulbin')
        self.assertRaises(ValidationError,
                          Entry.utilities.create_entry,
                          tournament=tournament,
                          player=straw_player)

    def test_cannot_enter_same_player_twice(self):
        " Entering the same player twice does not create two players. "
        tourney = Tournament.utilities.create_tournament(title='Tougeki',
                                                         game='2X',
                                                         date=date.today(),
                                                         nb_max=2,
                                                         id=8)
        player = Player.utilities.create_player(name='Yamsha', team='Escroc')
        Entry.utilities.create_entry(tournament=tourney,
                                     player=player)
        Entry.utilities.create_entry(tournament=tourney,
                                     player=player)
        self.assertEqual(Entry.objects.filter(tournament_id=8).count(),1)
