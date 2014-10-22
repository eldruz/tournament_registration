from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from registration.models import Tournament, Entry, Player
from registration.views import TournamentDetail

class TournamentListTestCase(TestCase):
    def test_tournament_list_with_no_tournaments(self):
        response = self.client.get(reverse('tournament_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tournaments are available')
        self.assertQuerysetEqual(response.context['tournament_list'], [])

    def test_tournament_list_with_tournaments(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('tournament_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['tournament_list'],
            ['<Tournament: Tournoi test>']
        )


class TournamentDetailTestCase(TestCase):
    def test_tournament_detail_with_no_tournament(self):
        response = self.client.get(reverse('tournament_detail',
                                           kwargs={'slug': 'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_tournament_detail_existing_tournament(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        slug = slugify(unicode(date.today().isoformat() + '-' + 'Tournoi test'))
        response = self.client.get(
            reverse('tournament_detail', kwargs={'slug': slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournament'],
            tourney
        )


class PlayerListTestCase(TestCase):
    def test_player_list_with_no_players(self):
        response = self.client.get(reverse('player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No players are registered')
        self.assertQuerysetEqual(response.context['player_list'], [])

    def test_player_list_with_players(self):
        player = Player.utilities.create_player(name='Kurahashi')
        response = self.client.get(reverse('player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['player_list'],
            ['<Player: [] Kurahashi>']
        )


class PlayerDetailTestCase(TestCase):
    def test_player_detail_with_no_player(self):
        response = self.client.get(reverse('player_detail',
                                           kwargs={'slug': 'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_player_detail_with_existing_player(self):
        player = Player.utilities.create_player(name='Kurahashi')
        slug = slugify(unicode(player.team + '-' + player.name))
        response = self.client.get(
            reverse('player_detail', kwargs={'slug': slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['player'],
            player
        )


class PlayersPerTournamentListTestCase(TestCase):
    def test_list_no_tournament(self):
        response = self.client.get(reverse('players_per_tournament',
                                           kwargs={'slug': 'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_list_no_players(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('players_per_tournament',
                                           kwargs={'slug': tourney.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournament'],
            tourney
        )
        self.assertQuerysetEqual(
            response.context['players'],
            []
        )
        self.assertContains(response, 'No players are registered')

    def test_list_tournament_with_players(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        player = Player.utilities.create_player(name='Daigo', team='MCZ')
        Entry.utilities.create_entry(tournament=tourney, player=player)
        response = self.client.get(reverse('players_per_tournament',
                                           kwargs={'slug': tourney.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournament'],
            tourney
        )
        self.assertQuerysetEqual(
            response.context['players'],
            ['<Player: [MCZ] Daigo>']
        )


class PlayerCreateTestCase(TestCase):
    def test_cannot_create_player_with_no_tournaments(self):
        response = self.client.get(reverse('create_player'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_player'),
                                    {'name':'Tokido', 'team':'MCZ'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          name='Tokido',
                          team='MCZ')

    def test_create_player_valid_form(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('create_player'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_player'),
                                    {'name':'Tokido',
                                     'team':'MCZ',
                                     'registered_tournaments':(tourney.pk)},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse('player_detail', kwargs={'slug': 'mcz-tokido'})
        )
        self.assertIsInstance(
            Player.objects.get(name='Tokido', team='MCZ'),
            Player
        )


class PlayerUpdateTestCase(TestCase):
    def test_update_player_valid_form(self):
        # We create 1 player and 2 tournaments and register the player
        # to both tournaments
        player = Player.utilities.create_player(name='Taira')
        tourney1 = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        tourney2 = Tournament.utilities.create_tournament(
            title='NantesGeki',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        Entry.utilities.create_entry(tournament=tourney1, player=player)
        Entry.utilities.create_entry(tournament=tourney2, player=player)
        # Checking the data is correct
        response = self.client.get(reverse('update_player',
                                           kwargs={'slug':player.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['player'],
            player
        )
        # Changing the form to change the player
        response = self.client.post(reverse('update_player',
                                            kwargs={'slug':player.slug}),
                                    {'name':'YuVega',
                                     'team':'DICTATOR',
                                     'registered_tournaments':(tourney1.pk)},
                                    follow=True)
        # No errors and redirection is okay
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse('player_detail', kwargs={'slug': 'dictator-yuvega'})
        )
        # Player has been updated
        self.assertIsInstance(
            Player.objects.get(pk=player.pk, name='YuVega', team='DICTATOR'),
            Player
        )
        # Old player does not exist anymore
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          name='Taira',
                          team='')


class PlayerDeleteTestCase(TestCase):
    def test_delete_unexisting_player(self):
        response = self.client.post(reverse('delete_player',
                                           kwargs={'slug':'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_delete_existing_player(self):
        player = Player.utilities.create_player(name='MAO')
        tourney = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('delete_player',
                                           kwargs={'slug':player.slug}))
        # Checking the data is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['player'],
            player
        )
        # Deleting the player
        response = self.client.post(reverse('delete_player',
                                            kwargs={'slug':player.slug}))
        # No errors and redirection ok
        self.assertRedirects(
            response,
            reverse('player_list')
        )
        # Old player doesn't exist
        self.assertRaises(ObjectDoesNotExist,
                          Player.objects.get,
                          name='MAO')


class TournamentCreateTestCase(TestCase):
    def test_create_tournament_valid_form(self):
        response = self.client.get(reverse('create_tournament'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create_tournament'),
                                    {'title':'Tournoi Des Sacs',
                                     'game':'2X',
                                     'date':date.today(),
                                     'support':'Arcade',
                                     'nb_max':32,
                                     'price':10,
                                     'nb_per_team':1},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        slug = slugify(unicode(date.today().isoformat() + '-' + 'Tournoi des Sacs'))
        self.assertRedirects(
            response,
            reverse('tournament_detail', kwargs={'slug': slug})
        )
        self.assertIsInstance(
            Tournament.objects.get(title='Tournoi Des Sacs'),
            Tournament
        )


class TournamentUpdateTestCase(TestCase):
    def test_update_tournament_valid_form(self):
        tourney = Tournament.utilities.create_tournament(
            title='NantesGeki',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('update_tournament',
                                           kwargs={'slug': tourney.slug}))
        # Checking the data is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournament'],
            tourney
        )
        # Updating the data
        response = self.client.post(reverse('update_tournament',
                                            kwargs={'slug': tourney.slug}),
                                    {'title':'Tournoi Des Sacs',
                                     'game':'2X',
                                     'date':date.today(),
                                     'support':'Arcade',
                                     'nb_max':32,
                                     'price':10,
                                     'nb_per_team':1},
                                    follow=True)
        # No errors and redirection ok
        self.assertEqual(response.status_code, 200)
        slug = slugify(unicode(
            date.today().isoformat() + '-' + 'Tournoi des Sacs'
        ))
        self.assertRedirects(
            response,
            reverse('tournament_detail', kwargs={'slug': slug})
        )
        # Tournament has been updated
        self.assertIsInstance(
            Tournament.objects.get(title='Tournoi Des Sacs'),
            Tournament
        )
        # Old tournament doesn't exist
        self.assertRaises(ObjectDoesNotExist,
                          Tournament.objects.get,
                          title='NantesGeki')


class TournamentDeleteTestCase(TestCase):
    def test_delete_unexisting_tournament(self):
        response = self.client.post(reverse('delete_tournament',
                                           kwargs={'slug':'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_delete_existing_tournament(self):
        tourney = Tournament.utilities.create_tournament(
            title='NantesGeki',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('delete_tournament',
                                           kwargs={'slug': tourney.slug}))
        # Checking the data is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournament'],
            tourney
        )
        # Deleting the tournament
        response = self.client.post(reverse('delete_tournament',
                                            kwargs={'slug': tourney.slug}))
        # No errors and redirection ok
        self.assertRedirects(
            response,
            reverse('tournament_list')
        )
        # Old tournament doesn't exist
        self.assertRaises(ObjectDoesNotExist,
                          Tournament.objects.get,
                          title='NantesGeki')
