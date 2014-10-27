from satchless.item import InsufficientStock, StockedItem
from datetime import date
from django.utils import timezone

from django.db import models
from django_prices.models import PriceField

from registration.models import Tournament

class Product(models.Model, StockedItem):
    """An abstract class that embodies everything that can be sold."""
    price = PriceField('Price',
                       currency='EUR',
                       max_digits=5,
                       decimal_places=2,
                       blank=False,
                       default=0.0)
    date_added = models.DateField('Date added')
    last_modified = models.DateTimeField('Last modified')

    class Meta:
        abstract = True


class TournamentProductUtilitiesManager(models.Manager):
    def createTournamentProduct(self, tournament, price=0.0):
        tourney_product = TournamentProduct(tournament=tournament,
                                            price=price,
                                            date_added=date.today(),
                                            last_modified=timezone.now())
        tourney_product.save()
        return tourney_product

    def updateTournamentProduct(self, product_id, **kwargs):
        additional_attributes = {'price'}
        tourney_product = TournamentProduct.objects.get(pk=product_id)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(tourney_product, attribute, value)
        tourney_product.save()
        return tourney_product

    def deleteTournamentProduct(self, product_id):
        tourney_product = TournamentProduct.objects.get(pk=product_id)
        tourney_product.delete()


class TournamentProduct(Product):
    tournament = models.OneToOneField(Tournament)
    objects = models.Manager()
    utilities = TournamentProductUtilitiesManager()
