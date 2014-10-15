from django.db import models
from django.core.urlresolvers import reverse

from django.core.exceptions import ValidationError
from django.http import Http404


class ValidateOnSaveMixin(object):
    """Force model validation on save() mixin.

    Everytime a model is saved, the mixin calls the validation
    function of the model.
    Useful for now as there is yet to be a form associated with
    the model. It might trigger a double validation with the
    associated ModelForm later on.

    """
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update,
                                              **kwargs)


class TournamentUtilitiesManager(models.Manager):
    """Manager for creating and updating tournaments.

    Everytime a view needs to create a tournament, this is the
    function they have to use.

    """
    def create_tournament(self, title, game, date, nb_max, **kwargs):
        additional_attributes = {'id', 'support', 'price', 'nb_per_team'}
        tourney = Tournament(title=title,
                             game=game,
                             date=date,
                             nb_max=nb_max)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(tourney, attribute, value)
        tourney.save()
        return tourney


class Tournament(ValidateOnSaveMixin, models.Model):
    """Tournament Model.

    Attributes:
        title: Title of the tournament
        game: The game the tournament willl be played on. For now, we assume
        that a tournament can only run one game
        date: The day of the tournament
        support: Usually either the name of the console, PC or arcade
        nb_max: The maximum amount of players that can register
        nb_per_team: The number of players per team
        objects: The default Manager for django to use
        utilities: The manager used to create or update tournaments

    """
    # For now the game list is hardcoded in the model
    # It will be in its own model later on, probably inside its own app
    GAME_LIST = (
        (u'2X', u'Super Street Fighter 2X'),
        (u'USF4', u'Ultra Street Fighter 4'),
        (u'3.3', u'Street Fighter III Third Strike'),
    )

    title   = models.CharField('Tournament title.',
                               max_length=256,
                               blank=False)
    game    = models.CharField('Game played for this tournament.\n\
                               The games are chosen from a hardcoded list.',
                               max_length=256,
                               choices=GAME_LIST,
                               blank=False)
    date    = models.DateField('Date of the tournament', blank=False)
    support = models.CharField('Support on which the tournament will be played.',
                               max_length=256,
                               default=u'Unknown')
    nb_max      = models.PositiveSmallIntegerField('Max number of participants.',
                                                   blank=False,
                                                   default=32)
    price       = models.PositiveSmallIntegerField('Entry fee',
                                                   default=0)
    nb_per_team = models.PositiveSmallIntegerField('Number of players per team.',
                                                   default=1)
    objects   = models.Manager()
    utilities = TournamentUtilitiesManager()

    class Meta:
        " A tournament title can only be associated with a single date "
        unique_together = (('title', 'date'))

    def clean(self):
        " A game has to be on the game list "
        if self.game not in [x[0] for x in self.GAME_LIST]:
            msg = u'Game is not in the games list'
            raise ValidationError(msg)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tournament_detail', kwargs={'pk': self.pk})


class PlayerUtilitiesManager(models.Manager):
    """Manager for creating and updating players in tournaments.

    Everytime a view needs to create a player, this is the function they
    have to use.

    """
    def create_player(self, name, **kwargs):
        additional_attributes = {'team', 'registered_tournaments'}
        player = Player(name=name)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(player, attribute, value)
        player.save()
        return player


class Player(models.Model):
    """The Player model.

    Represents the players that will register at tournaments. We only need
    the minimal information about them, usually only their nicknames.

    Attributes:
        name: The nickname of the player, which acts as a primary key to the
        model. Sorry for those of you who share nicknames
        team: Optional name of the team that the player is part of
        registered_tournaments: A many to many field that represents all
        the tournaments the player is registered in

    """
    name = models.CharField('Nickname of the player',
                            max_length=256,
                            primary_key=True)
    team = models.CharField('Name of her team',
                            max_length=128,
                            blank=True)
    registered_tournaments = models.ManyToManyField('Tournament',
                                                    through='Entry')
    objects = models.Manager()
    utilities = PlayerUtilitiesManager()

    class Meta:
        unique_together = (('name', 'team'))

    def __unicode__(self):
        return '[' + self.team + '] ' + self.name


class EntryUtilitiesManager(models.Manager):
    """Manager for creating and updating entries in tournaments.

    Everytime a view needs to create an entry, this is the function they
    have to use.

    """
    def create_entry(self, tournament, player):
        """A function that adds an entry according to a set of constraints.

        First of all, we cannot add an entry to a full tournament, that is
        we cannot have more entries than the maximum number of attendees
        specified in the tournament specs.

        """
        if self.is_tournament_full(tournament):
            msg = 'The tournament is full.'
            raise ValidationError(msg)
        else:
            entry = Entry(tournament_id=tournament,
                          player=player)
            entry.save()
            return entry

    def is_tournament_full(self, tournament):
        # We get the number of registered players in the tournaments
        nb_registered = Entry.players.get_players_per_tournament(tournament.id).count()
        # Maximum number of attendees
        nb_max = tournament.nb_max

        if nb_registered < nb_max:
            return False
        else:
            return True


class EntryPlayersManager(models.Manager):
    """Manager with helper functions to get specific subsets of entries

    """
    def get_players_per_tournament(self, tournament_id):
        tourney = Tournament.objects.get(pk=tournament_id)
        player_list = Entry.objects.\
            filter(tournament_id=tournament_id).\
            only('player')
        return player_list

    def get_tournaments_per_player(self, player_name):
        player = Player.objects.get(pk=player_name)
        tournaments_list = Entry.objects.\
            select_related('tournament_id').\
            filter(player=player_name)
        if not tournaments_list:
            raise Http404
        return tournaments_list


class Entry(models.Model):
    """Entry model, which is the 'trough' table between Tournament & Player.

    Attributes:
        tournament_id: The foreign key to the Tournament model
        player: The foreign key to the Player model
        objects: The default Manager for django to use
        utilities: The utility manager used to create or update entries
        players: The helper manager used to query specific sets in the model

    """
    tournament_id = models.ForeignKey('Tournament')
    player        = models.ForeignKey('Player')
    objects       = models.Manager()
    utilities     = EntryUtilitiesManager()
    players       = EntryPlayersManager()

    def __unicode__(self):
        return self.player.__unicode__()\
            + ' in '\
            + self.tournament_id.__unicode__()
