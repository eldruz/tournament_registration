from satchless.cart import Cart

from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, DeleteView, \
    UpdateView, View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import TournamentProduct
from .forms import CartAddItemForm

# Display views
class TournamentProductDetailView(DetailView):
    model = TournamentProduct


class TournamentProductListView(ListView):
    model = TournamentProduct
    context_object_name = 'tournament_list'


class CartContentsView(View):
    template_name = 'capitalism/cart_contents.html'

    def get(self, request, *args, **kwargs):
        # if (request.session['cart']):
        #     cart = Cart(items=session['cart'])
        # else:
        #     cart = Cart()

        return render(request, self.template_name)


class CartAddItemView(FormView):
    form_class = CartAddItemForm
    template_name = 'capitalism/cart_add_product.html'
    success_url = reverse_lazy('cart_contents')

    def form_valid(self, form):
        tournament = form.cleaned_data['tournament']
        quantity = form.cleaned_data['quantity']
        cart = Cart()
        cart.add(tournament, quantity=quantity)
        # self.request.session['cart'] = list(cart)
        return HttpResponseRedirect(self.get_success_url())


# Edit views
class TournamentProductCreateView(CreateView):
    model = TournamentProduct
    fields = ['tournament', 'price', 'stock']
    template_name = 'capitalism/create_tournament_product.html'

    def form_valid(self, form):
        tournament_product = form.save(commit=False)
        tournament_product = \
            TournamentProduct.utilities.create_tournament_product(
                tournament=tournament_product.tournament,
                price=tournament_product.price,
                stock=tournament_product.stock
            )
        return HttpResponseRedirect(tournament_product.get_absolute_url())


class TournamentProductUpdateView(UpdateView):
    model = TournamentProduct
    fields = ['tournament', 'price', 'stock']
    template_name = 'capitalism/create_tournament_product.html'

    def form_valid(self, form):
        tournament_product = form.save(commit=False)
        tournament_product = \
            TournamentProduct.utilities.update_tournament_product(
                product_id=tournament_product.pk,
                price=tournament_product.price,
                stock=tournament_product.stock,
                tournament=tournament_product.tournament
            )
        return HttpResponseRedirect(tournament_product.get_absolute_url())


class TournamentProductDeleteView(DeleteView):
    model = TournamentProduct
    success_url = reverse_lazy('tournament_product_list')
    template_name = 'capitalism/delete_tournament_product.html'
