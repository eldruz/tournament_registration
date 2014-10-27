from datetime import date

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
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
        TournamentProduct.utilities.createTournamentProduct(
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
                          TournamentProduct.utilities.createTournamentProduct,
                          tournament=tourney,
                          price=5.25)

    def test_update_tournament_product(self):
        tourney_product = \
            TournamentProduct.objects.get(price=10.50)
        TournamentProduct.utilities.updateTournamentProduct(
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
        TournamentProduct.utilities.deleteTournamentProduct(tourney_product.pk)
        self.assertRaises(ObjectDoesNotExist,
                          TournamentProduct.objects.get,
                          price=10.50)