from datetime import date

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from registration.models import Tournament
from capitalism.models import TournamentProduct

class TournamentProductTestCase(TestCase):
    def setUp(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64,
        )
        TournamentProduct.utilities.create_tournament_product(
            tournament=tourney,
            price=10.50
        )

    def test_creation_tournament_product(self):
        tourney_product = \
            TournamentProduct.objects.get(price=10.50)
        self.assertIsInstance(tourney_product, TournamentProduct)

    def test_create_tournament_product_only_existing_tournament(self):
        tourney = Tournament(title='LoL',
                             game='2X',
                             date=date.today(),
                             nb_max=16)
        self.assertRaises(IntegrityError,
                          TournamentProduct.utilities.create_tournament_product,
                          tournament=tourney,
                          price=5.25)

    def test_tournament_product_too_much_stock(self):
        """A tournament product cannot have more stock than available spots"""
        tourney = Tournament.objects.get(title='Tournoi test')
        # Test on creation of a new tournament product
        self.assertRaises(ValidationError,
                          TournamentProduct.utilities.create_tournament_product,
                          tournament=tourney,
                          price=15,
                          stock=65
                          )
        tourney_product = \
            TournamentProduct.objects.get(price=10.50)
        # Test on updating an existing tournament product
        self.assertRaises(ValidationError,
                          TournamentProduct.utilities.update_tournament_product,
                          product_id=tourney_product.pk,
                          stock=65
                          )

    def test_update_tournament_product(self):
        tourney_product = \
            TournamentProduct.objects.get(price=10.50)
        TournamentProduct.utilities.update_tournament_product(
            product_id=tourney_product.pk,
            price=12
            )
        # Updated product exists in the database
        tourney_product = \
            TournamentProduct.objects.get(price=12)
        self.assertIsInstance(tourney_product, TournamentProduct)
        # Old one does not
        self.assertRaises(ObjectDoesNotExist,
                          TournamentProduct.objects.get,
                          price=10.50)

    def test_delete_tournament_product(self):
        tourney_product = \
            TournamentProduct.objects.get(price=10.50)
        self.assertIsInstance(tourney_product, TournamentProduct)
        TournamentProduct.utilities.delete_tournament_product(tourney_product.pk)
        self.assertRaises(ObjectDoesNotExist,
                          TournamentProduct.objects.get,
                          price=10.50)
