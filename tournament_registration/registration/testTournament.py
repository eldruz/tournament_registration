from datetime import date

from django.test import TestCase
from django.db import IntegrityError

from .models import Tournament
from .models import TournamentManager

class TournamentTestCase(TestCase):
    def setUp(self):
        Tournament.utilities.create_tournament(title='Tournoi test',
                                               game='2X',
                                               date=date.today(),
                                               nb_max=64)

    def test_utilities_creation(self):
        """Asserts that a tournament created with the utility creation funtion
            is created correctly"""
        tourney = Tournament.utilities.get(title='Tournoi test')
        self.assertEqual(tourney.title, 'Tournoi test')
        self.assertEqual(tourney.game, '2X')
        self.assertEqual(tourney.date, date.today())
        self.assertEqual(tourney.nb_max, 64)
        self.assertEqual(tourney.support, u'Unknown')
        self.assertEqual(tourney.nb_per_team, 1)
        self.assertEqual(tourney.price, 0)

    def test_cannot_create_duplicate(self):
        """Asserts that only one (title, date) couple can exist
            in the database"""
        self.assertRaises(IntegrityError,
                          Tournament.utilities.create_tournament,
                          title='Tournoi test',
                          game='USF4',
                          date=date.today(),
                          nb_max=32)


