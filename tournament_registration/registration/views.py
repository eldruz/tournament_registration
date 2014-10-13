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
    queryset = Entry.players.get_player_list()
    template_name = 'registration/player_list.html'
    context_object_name = 'player_list'


class PlayersPerTournamentList(ListView):
    model = Entry
    template_name = 'registration/player_tournament_list.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        """Returns only the names of the player for the tournament"""
        entry = Entry.players.get_players_per_tournament(self.kwargs['tournament_id'])
        tourney = Tournament.objects.get(id=self.kwargs['tournament_id'])
        self.tournament_name = tourney.title
        self.tournament_date = tourney.date
        return entry

    def get_context_data(self, **kwargs):
        context = super(PlayersPerTournamentList, self).get_context_data(**kwargs)
        # Add in the tournament name and date
        context['tournament_name'] = self.tournament_name
        context['tournament_date'] = self.tournament_date
        return context


class TournamentsPerPlayerList(ListView):
    model = Entry
    template_name = 'registration/player_detail.html'
    context_object_name = 'player'

    def get_queryset(self):
        """Returns the tournament the specified player is registered in."""
        entry = Entry.players.get_tournaments_per_player(self.kwargs['player_name'])
        self.player_name = self.kwargs['player_name']
        return entry

    def get_context_data(self, **kwargs):
        context = super(TournamentsPerPlayerList, self).get_context_data(**kwargs)
        context['player_name'] = self.player_name
        return context
