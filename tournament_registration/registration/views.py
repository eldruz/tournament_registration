from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Tournament
from .models import Entry
from .models import Player
from .forms import PlayerForm

# Display Views

class TournamentList(ListView):
    model = Tournament


class TournamentDetail(DetailView):
    model = Tournament


class PlayerList(ListView):
    model = Player

class PlayerDetail(DetailView):
    model = Player


class PlayersPerTournamentList(ListView):
    model = Entry
    template_name = 'registration/player_tournament_list.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        """Returns only the names of the player for the tournament"""
        entry = Entry.utilities.\
            get_players_per_tournament(self.kwargs['tournament_id'])
        tourney = Tournament.objects.get(id=self.kwargs['tournament_id'])
        self.tournament_name = tourney.title
        self.tournament_date = tourney.date
        return entry

    def get_context_data(self, **kwargs):
        context = super(PlayersPerTournamentList, self).\
            get_context_data(**kwargs)
        # Add in the tournament name and date
        context['tournament_name'] = self.tournament_name
        context['tournament_date'] = self.tournament_date
        return context


# Edit views

class TournamentCreate(CreateView):
    model = Tournament
    fields = ['title', 'game', 'date', 'support',\
              'nb_max', 'price', 'nb_per_team']
    template_name = 'registration/create_tournament.html'


class TournamentUpdate(UpdateView):
    model = Tournament
    fields = ['title', 'game', 'date', 'support',\
              'nb_max', 'price', 'nb_per_team']
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
    form_class = PlayerForm
    template_name = 'registration/create_tournament.html'

    def form_valid(self, form):
        player = form.save(commit=False)
        player.save()
        for tournament in form.cleaned_data.get('registered_tournaments'):
            Entry.utilities.create_entry(tournament, player)
        return HttpResponseRedirect(player.get_absolute_url())


class PlayerUpdate(UpdateView):
    model = Player
    fields = ['name', 'team', 'registered_tournaments']
    template_name = 'registration/create_tournament.html'

    # def form_valid(self, form):
    #     return HttpResponseRedirect(self.get_success_url())


class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('player_list')
    template_name = 'registration/delete_tournament.html'
