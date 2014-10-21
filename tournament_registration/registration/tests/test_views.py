from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify

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

