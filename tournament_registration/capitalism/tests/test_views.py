from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from registration.models import Tournament
from capitalism.models import TournamentProduct
from capitalism.views import TournamentProductCreateView, \
    TournamentProductUpdateView, TournamentProductListView, \
    TournamentProductDeleteView, TournamentProductDetailView

class TournamentProductListTestCase(TestCase):
    def test_list_with_no_products(self):
        response = self.client.get(reverse('tournament_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No products are available')
        self.assertQuerysetEqual(response.context['tournament_list'], [])

    def test_list_with_products(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64,
        )
        product = TournamentProduct.utilities.create_tournament_product(
            tournament=tourney,
            price=10
        )
        response = self.client.get(reverse('tournament_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['tournament_list'],
            ['<TournamentProduct: Tournoi test>']
        )


class TournamentProductDetailTestCase(TestCase):
    def test_detail_with_no_product(self):
        response = self.client.get(reverse('tournament_product_detail',
                                           kwargs={'slug': 'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_detail_with_existing_product(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64,
        )
        product = TournamentProduct.utilities.create_tournament_product(
            tournament=tourney,
            price=10
        )
        response = self.client.get(
            reverse('tournament_product_detail', kwargs={'slug': product.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournamentproduct'],
            product
        )


class TournamentProductCreateTestCase(TestCase):
    def test_product_creation_valid_form(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        response = self.client.get(reverse('tournament_product_create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('tournament_product_create'),
                                    {'price':20.50,
                                     'stock':64,
                                     'tournament':(tourney.pk)},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        slug = slugify(unicode(date.today().isoformat() + '-tougekiche'))
        self.assertRedirects(
            response,
            reverse('tournament_product_detail', kwargs={'slug': slug})
        )
        self.assertIsInstance(
            TournamentProduct.objects.get(price=20.50, stock=64),
            TournamentProduct
        )


class TournamentProductUpdateTestCase(TestCase):
    def test_product_update_valid_form(self):
        # We create 2 tournaments, and one tournament product
        tourney1 = Tournament.utilities.create_tournament(
            title='Tournoi test',
            game='2X',
            date=date.today(),
            nb_max=64,
        )
        tourney2 = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        product = TournamentProduct.utilities.create_tournament_product(
            tournament=tourney1,
            price=10,
            stock=64
        )
        # Checking the data is correct
        response = self.client.get(reverse('tournament_product_update',
                                           kwargs={'slug':product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournamentproduct'],
            product
        )
        # Changing the form to change the product
        response = self.client.post(reverse('tournament_product_update',
                                            kwargs={'slug':product.slug}),
                                    {'price':20,
                                     'stock':16,
                                     'tournament':tourney2.pk},
                                    follow=True)
        # No errors and redirection is okay
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse('tournament_product_detail', kwargs={'slug': tourney2.slug})
        )
        # Product has been updated
        self.assertIsInstance(
            TournamentProduct.objects.get(pk=product.pk, price=20, stock=16),
            TournamentProduct
        )
        # Old product does not exist anymore
        self.assertRaises(ObjectDoesNotExist,
                          TournamentProduct.objects.get,
                          price=10,
                          stock=64)


class TournamentProductDeleteTestCase(TestCase):
    def test_unexisting_product_delete(self):
        response = self.client.post(reverse('tournament_product_delete',
                                           kwargs={'slug':'neant'}))
        self.assertEqual(response.status_code, 404)

    def test_existing_product_delete(self):
        tourney = Tournament.utilities.create_tournament(
            title='Tougekiche',
            game='2X',
            date=date.today(),
            nb_max=64
        )
        product = TournamentProduct.utilities.create_tournament_product(
            tournament=tourney,
            price=10,
            stock=63
        )
        response = self.client.get(reverse('tournament_product_delete',
                                           kwargs={'slug':product.slug}))
        # Checking the data is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['tournamentproduct'],
            product
        )
        # Deleting the product
        response = self.client.post(reverse('tournament_product_delete',
                                            kwargs={'slug':product.slug}))
        # No errors and redirection ok
        self.assertRedirects(
            response,
            reverse('tournament_product_list')
        )
        # Old player doesn't exist
        self.assertRaises(ObjectDoesNotExist,
                          TournamentProduct.objects.get,
                          price=10,
                          stock=63)
