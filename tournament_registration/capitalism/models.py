from satchless.item import InsufficientStock, StockedItem
from datetime import date

from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models
from django_prices.models import PriceField
from django.core.exceptions import ValidationError

from registration.models import Tournament

class Product(models.Model, StockedItem):
    """An abstract class that embodies everything that can be sold."""
    price = PriceField('Price',
                       currency='EUR',
                       max_digits=5,
                       decimal_places=2,
                       blank=False,
                       default=0.0)
    stock = models.PositiveSmallIntegerField('Product Stock',
                                             blank=False,
                                             default=0)
    date_added = models.DateField('Date added')
    last_modified = models.DateTimeField('Last modified')
    slug = models.SlugField('Product slug', max_length=256)

    def get_price_per_item(self):
        return price

    class Meta:
        abstract = True


class TournamentProductUtilitiesManager(models.Manager):
    def create_tournament_product(self, tournament, price=0.0, stock=0):
        tourney_product = TournamentProduct(tournament=tournament,
                                            price=price,
                                            stock=stock,
                                            date_added=date.today(),
                                            last_modified=timezone.now())
        tourney_product.save()
        return tourney_product

    def update_tournament_product(self, product_id, **kwargs):
        additional_attributes = {'price', 'stock'}
        tourney_product = TournamentProduct.objects.get(pk=product_id)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(tourney_product, attribute, value)
        tourney_product.save()
        return tourney_product

    def delete_tournament_product(self, product_id):
        tourney_product = TournamentProduct.objects.get(pk=product_id)
        tourney_product.delete()


class TournamentProduct(Product):
    tournament = models.OneToOneField(Tournament)
    objects = models.Manager()
    utilities = TournamentProductUtilitiesManager()

    def get_stock(self):
        return self.stock

    def save(self, *args, **kwargs):
        " Override the save method to check the stock and set the slug "
        if self.stock > self.tournament.get_available_spots():
            msg = 'Stock of a TournamentProduct cannot be greater than the \
                tournament available spots'
            raise ValidationError(msg)
        self.slug = slugify(
            unicode(self.tournament.date.isoformat() + '-' + self.tournament.title))
        super(TournamentProduct, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tournamentproduct_detail', kwargs={'slug': self.slug})
