from satchless.item import InsufficientStock, StockedItem

from django.db import models
from django_prices.models import PriceField

from registration.models import Tournament

class Product(models.Model, StockedItem):
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


class TournamentProduct(Product):
    tournament = models.OneToOneField(Tournament)
