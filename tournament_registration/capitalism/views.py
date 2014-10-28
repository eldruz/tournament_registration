from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from django.http import HttpResponseRedirect

from .models import TournamentProduct

# Display views
class TournamentProductDetailView(DetailView):
    model = TournamentProduct


class TournamentProductListView(ListView):
    model = TournamentProduct
    context_object_name = 'tournament_list'


# Edit views
class TournamentProductCreateView(CreateView):
    model = TournamentProduct
    fields = ['tournament', 'price', 'stock']
    template_name = 'capitalism/create_tournamentproduct.html'

    def form_valid(self, form):
        tournament_product = form.save(commit=False)
        tournament_product = \
            TournamentProduct.utilities.create_tournament_product(
                tournament=tournament_product.tournament,
                price=tournament_product.price,
                stock=tournament_product.stock
            )
        return HttpResponseRedirect(tournament_product.get_absolute_url())
