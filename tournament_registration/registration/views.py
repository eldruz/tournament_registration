from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Tournament
from .models import Entry
from .models import Player

# Display Views

class TournamentList(ListView):
    model = Tournament


class TournamentDetail(DetailView):
    model = Tournament


class PlayerList(ListView):
    model = Player


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


# Edit views

class TournamentCreate(CreateView):
    model = Tournament
    fields = ['title', 'game', 'date', 'support', 'nb_max', 'price', 'nb_per_team']
    template_name = 'registration/create_tournament.html'


class TournamentUpdate(UpdateView):
    model = Tournament
    fields = ['title', 'game', 'date', 'support', 'nb_max', 'price', 'nb_per_team']
    template_name = 'registration/create_tournament.html'


class TournamentDelete(DeleteView):
    model = Tournament
    success_url = reverse_lazy('tournament_list')
    template_name = 'registration/delete_tournament.html'


class EntryCreateView(CreateView):
    model = Entry
    fields = ['tournament_id', 'player']
    template_name = 'registration/create_tournament.html'


class PlayerCreate(CreateView):
    model = Player
    fields = ['name', 'team', 'registered_tournaments']
    template_name = 'registration/create_tournament.html'

    def form_valid(self, form):
        player = form.save(commit=False)
        player.save()
        for tournament in form.cleaned_data.get('registered_tournaments'):
            entry = Entry(player=player, tournament_id=tournament)
            entry.save()
        return HttpResponseRedirect(self.get_success_url())
