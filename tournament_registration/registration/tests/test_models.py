from datetime import date

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from registration.models import Tournament
from registration.models import TournamentManager
from registration.models import Entry

class TournamentTestCase(TestCase):
    def setUp(self):
        Tournament.utilities.create_tournament(title='Tournoi test',
                                               game='2X',
                                               date=date.today(),
                                               nb_max=64)

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

    def test_cannot_create_duplicate(self):
        """Only one (title, date) couple can exist in the database"""
        self.assertRaises(ValidationError,
                          Tournament.utilities.create_tournament,
                          title='Tournoi test',
                          game='USF4',
                          date=date.today(),
                          nb_max=32)

    def test_game_not_in_list(self):
        """Game field of the tournament is in the authorized games list"""
        self.assertRaises(ValidationError,
                          Tournament.utilities.create_tournament,
                          title='Invalid Game Tournament',
                          game='PACMAN',
                          date=date.today(),
                          nb_max=32)


class EntryTestCase(TestCase):
    def setUp(self):
        Tournament.utilities.create_tournament(title='X-MANIA',
                                               game='2X',
                                               date=date.today(),
                                               nb_max=64)
        Entry.utilities.create_entry(tournament_title='X-MANIA',
                                     tournament_date=date.today(),
                                     player='Komoda')

    def test_valid_entry_creation(self):
        """Entry created with the utility function is correct"""
        entry = Entry.utilities.get(player='Komoda')
        self.assertEqual(entry.tournament_title, 'X-MANIA')
        self.assertEqual(entry.tournament_date, date.today())

    def test_foreign_key_constraint(self):
        """An entry has to reference an existing tournament"""
        self.assertRaises(ObjectDoesNotExist,
                          Entry.utilities.create_entry,
                          tournament_title='STUNFEST',
                          tournament_date=date.today(),
                          player='Zoulolz')
        self.assertRaises(ObjectDoesNotExist,
                          Entry.utilities.create_entry,
                          tournament_title='X-MANIA',
                          tournament_date=date(2012, 12, 12),
                          player='Waldoze')
