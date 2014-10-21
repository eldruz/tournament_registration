from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

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
    model = Tournament
    template_name = 'registration/player_tournament_list.html'
    context_object_name = 'tournament'

    def get_queryset(self):
        """Returns only the names of the player for the tournament"""
        try:
            tourney = Tournament.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        self.players = tourney.player_set.all()
        return tourney

    def get_context_data(self, **kwargs):
        context = super(PlayersPerTournamentList, self).\
            get_context_data(**kwargs)
        # Add in the tournament name and date
        context['players'] = self.players
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
        # Player information given to the form
        player = form.save(commit=False)
        # The player is updated with additional id attribute given by the
        # creation function and needed for the entry model
        player = Player.utilities.create_player(name=player.name,
                                                team=player.team)
        registered = form.cleaned_data.get('registered_tournaments')
        Entry.utilities.register_tournaments(player, registered)
        return HttpResponseRedirect(player.get_absolute_url())


class PlayerUpdate(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'registration/create_tournament.html'

    def form_valid(self, form):
        player = form.save(commit=False)
        registered = form.cleaned_data.get('registered_tournaments')
        player = Player.utilities.update_player(player_id=player.pk,
                                                name=player.name,
                                                team=player.team)
        Entry.utilities.register_tournaments(player, registered, unregister=True)
        return HttpResponseRedirect(player.get_absolute_url())


class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('player_list')
    template_name = 'registration/delete_tournament.html'
