from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Tournament
from .models import Entry


class TournamentList(ListView):
    model = Tournament


class TournamentDetail(DetailView):
    model = Tournament


class PlayerList(ListView):
    model = Entry
    template_name = 'registration/player_list.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        """Returns only the names of the player for the tournament"""
        tourney = Tournament.objects.get(id=self.kwargs['tournament_id'])
        self.tournament_name = tourney.title
        self.tournament_date = tourney.date
        return Entry.utilities.get_player_list(self.kwargs['tournament_id'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlayerList, self).get_context_data(**kwargs)
        # Add in the tournament name and date
        context['tournament_name'] = self.tournament_name
        context['tournament_date'] = self.tournament_date
        return context
