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
    """Lists the available tournaments"""
    model = Tournament


class TournamentDetail(DetailView):
    """Details of a specific tournament"""
    model = Tournament


class PlayerList(ListView):
    """Lists the available players"""
    model = Player


class PlayerDetail(DetailView):
    """Details of a specific player"""
    model = Player


class PlayersPerTournamentList(ListView):
    """Lists all the players registered to a particular tournament"""
    model = Tournament
    template_name = 'registration/player_tournament_list.html'
    context_object_name = 'tournament'

    def get_queryset(self):
        """Returns only the tournament given in the uri"""
        try:
            tourney = Tournament.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        self.players = tourney.player_set.all()
        return tourney

    def get_context_data(self, **kwargs):
        """Adds the list of players to the context object."""
        context = super(PlayersPerTournamentList, self).\
            get_context_data(**kwargs)
        # Add in the tournament name and date
        context['players'] = self.players
        return context


# Edit views

class TournamentCreate(CreateView):
    """Creates a tournament."""
    model = Tournament
    fields = ['title', 'game', 'date', 'support',\
              'nb_max', 'nb_per_team']
    template_name = 'registration/create_tournament.html'


class TournamentUpdate(UpdateView):
    """Updates a tournament."""
    model = Tournament
    fields = ['title', 'game', 'date', 'support',\
              'nb_max', 'nb_per_team']
    template_name = 'registration/create_tournament.html'


class TournamentDelete(DeleteView):
    """Deletes a tournament."""
    model = Tournament
    success_url = reverse_lazy('tournament_list')
    template_name = 'registration/delete_tournament.html'


class PlayerCreate(CreateView):
    """Creates a player.

    As the Player and Tournament models are linked by a ManyToMany relationship \
    this view uses a custom form_valid function to correctly register the \
    corresponding entries.

    """
    model = Player
    form_class = PlayerForm
    template_name = 'registration/create_tournament.html'

    def form_valid(self, form):
        """Registers a new Player given a valid form.

        The function first registers the player into the database before adding \
        the entries, otherwise the ForeignKey constraint on the Entry model \
        would not be satisfied.

        :param form: The valid form
        """
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
    """Updates a player.

    As the Player and Tournament models are linked by a ManyToMany relationship \
    this view uses a custom form_valid function to correctly register the \
    corresponding entries.

    """
    model = Player
    form_class = PlayerForm
    template_name = 'registration/create_tournament.html'

    def form_valid(self, form):
        """Updates an existing Player given a valid form.

        The function first registers the player into the database before adding \
        the entries, otherwise the ForeignKey constraint on the Entry model \
        would not be satisfied.

        :param form: The valid form
        """
        player = form.save(commit=False)
        registered = form.cleaned_data.get('registered_tournaments')
        player = Player.utilities.update_player(player_id=player.pk,
                                                name=player.name,
                                                team=player.team)
        Entry.utilities.register_tournaments(player, registered, unregister=True)
        return HttpResponseRedirect(player.get_absolute_url())


class PlayerDelete(DeleteView):
    """Deletes a player"""
    model = Player
    success_url = reverse_lazy('player_list')
    template_name = 'registration/delete_tournament.html'
