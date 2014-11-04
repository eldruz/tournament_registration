from datetime import date

from django.test import TestCase

from registration.models import Tournament, Player, Entry
from export import TournamentExport, TournamentJsonExport


class TournamentExportTestCase(TestCase):
    def setUp(self):
        self.tourney = \
            Tournament.utilities.create_tournament(
                title='X-MANIA',
                game='2X',
                date=date.today(),
                nb_max=64,
            )
        player = Player.utilities.create_player(name='Komoda')
        Entry.utilities.create_entry(
            tournament=self.tourney,
            player=player
        )
        player = Player.utilities.create_player(name='Eldruz')
        Entry.utilities.create_entry(
            tournament=self.tourney,
            player=player
        )

    def test_tournament_is_retrieved(self):
        t_export = TournamentExport(self.tourney.pk)
        self.assertEqual(self.tourney, t_export.tournament.first())

    def test_players_are_retrieved(self):
        t_export = TournamentExport(self.tourney.pk)
        self.assertItemsEqual(self.tourney.player_set.all(),
                              t_export.players)

    def test_cannot_export(self):
        t_export = TournamentExport(self.tourney.pk)
        self.assertRaises(NotImplementedError, t_export.export)

    def test_export_to_json(self):
        json_export = TournamentJsonExport(self.tourney.pk)
        print(' >>> ' + str(type(json_export.tournament)))
        print(json_export.export())
