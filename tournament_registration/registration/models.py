from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
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
        """Utily function to create a tournament.

        It might not be that useful... Keeping it for the time being.

        :param title: Title of the tournament
        :param game: Game played during the tournament
        :param date: Date of the tournament
        :param nb_max: Maximum number of entries
        :param **kwargs: Optional arguments id, support and nb_per_team
        """
        additional_attributes = {'id', 'support', 'nb_per_team'}
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

    :param title: Title of the tournament
    :param game: The game the tournament willl be played on. For now, we assume \
    that a tournament can only run one game
    :param date: The day of the tournament
    :param support: Usually either the name of the console, PC or arcade
    :param nb_max: The maximum amount of players that can register
    :param nb_per_team: The number of players per team
    :param objects: The default Manager for django to use
    :param utilities: The manager used to create or update tournaments

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
    nb_per_team = models.PositiveSmallIntegerField('Number of players per team.',
                                                   default=1)
    slug = models.SlugField('Tournament slug', max_length=256)
    objects   = models.Manager()
    utilities = TournamentUtilitiesManager()

    class Meta:
        " A tournament title can only be associated with a single date "
        unique_together = (('title', 'date'))

    def save(self, *args, **kwargs):
        " Override the save method to set the slug and validate the game "
        if self.game not in [x[0] for x in self.GAME_LIST]:
            msg = u'Game is not in the games list'
            raise ValidationError(msg)
        self.slug = slugify(unicode(self.date.isoformat() + '-' + self.title))
        super(Tournament, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tournament_detail', kwargs={'slug': self.slug})

    def get_available_spots(self):
        """Returns the number of spots available for new entries."""
        # Checking the number of entries for this tournament
        nb_registered = Entry.objects.\
            filter(tournament_id = self).\
            count()
        return self.nb_max - nb_registered


class PlayerUtilitiesManager(models.Manager):
    """Manager for creating and updating players in tournaments.

    Everytime a view needs to create a player, this is the function they
    have to use.

    """
    def create_player(self, name, **kwargs):
        """Creates a new player and adds it to the database

        :param name: Name of the player, the only required parameter
        :param **kwargs: A dict containing additional parameters, which are
            listed below.
        """
        additional_attributes = {'id', 'team', 'registered_tournaments'}
        player = Player(name=name)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(player, attribute, value)
        player.save()
        return player

    def update_player(self, player_id, **kwargs):
        """Updates an existing player in the database.

        :param player_id: ID of the existing player.
        :param **kwargs: A dict containing additional parameters, which are
            listed below.
        """
        additional_attributes = {'name', 'team'}
        player = Player.objects.get(pk=player_id)
        for attribute, value in kwargs.items():
            assert attribute in additional_attributes
            setattr(player, attribute, value)
        player.save()
        return player

    def delete_player(self, name='', team='', player_id=None):
        """Deletes a player from the database.

        There is two options to access a player's data:
            *an id given in the kwargs parameter
            *a name and a team, as players are designed with a unicity
            constrint on the (name, team) couple of arguments

        :param name: Name of the player
        :param team: Name of the team
        :param player_id: Optional id of the player
        """
        if player_id:
            player = Player.objects.get(pk=player_id)
        else:
            player = Player.objects.get(name=name,
                                        team=team)
        player.delete()


class Player(models.Model):
    """The Player model.

    Represents the players that will register at tournaments. We only need
    the minimal information about them, usually only their nicknames.

    :param name: The nickname of the player
    :param team: Optional name of the team that the player is part of
    :param registered_tournaments: A many to many field that represents all \
    the tournaments the player is registered in

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nickname of the player',
                            max_length=256,
                            blank=False)
    team = models.CharField('Name of her team',
                            max_length=128,
                            blank=True)
    registered_tournaments = models.ManyToManyField('Tournament',
                                                    through='Entry')
    slug = models.SlugField('Player slug', max_length=256)
    objects = models.Manager()
    utilities = PlayerUtilitiesManager()

    class Meta:
        unique_together = (('name', 'team'))

    def save(self, *args, **kwargs):
        " Override the save method to automatically set the slug "
        self.slug = slugify(unicode(self.team + '-' + self.name))
        super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return '[' + self.team + '] ' + self.name

    def get_absolute_url(self):
        return reverse('player_detail', kwargs={'slug': self.slug})


class EntryUtilitiesManager(models.Manager):
    """Manager for creating and updating entries in tournaments.

    Everytime a view needs to create an entry, this is the function they
    have to use.

    """
    def create_entry(self, tournament, player):
        """Adds an entry according to a set of constraints.

        For now the only constraint is that a player cannot be registered into \
        a tournament that is already full.
        If the function is called to create an already existing entry, it \
        merely returns the entry withou doing anything database wise.

        :param tournament: The tournament that is being registered to
        :param player: The player that is regitering
        """
        try:
            already_registered = Entry.objects.get(tournament_id=tournament,
                                                   player=player)
            return already_registered
        except ObjectDoesNotExist:
            if tournament.get_available_spots() > 0:
                entry = Entry(tournament_id=tournament,
                            player=player)
                entry.save()
                return entry
            else:
                msg = 'The tournament is full.'
                raise ValidationError(msg)

    def register_tournaments(self, player, registered, unregister=False):
        """Registers a given player to a number of tournaments.

        If the unregister parameter is set to True, the function will also \
        unregister the player from all the existing tournaments that are not \
        listed in the registered parameter.

        :param player: The player to register
        :param registered: The tournaments that are being registered to
        :param unregister: A boolean that triggers the unregistration process
        """
        if unregister:
            unregistered_tournaments = \
                Entry.objects.\
                exclude(tournament_id__in=registered).\
                filter(player=player)
            unregistered_tournaments.delete()
        for tournament in registered:
            Entry.utilities.create_entry(tournament, player)


class Entry(models.Model):
    """Entry model, which is the 'trough' table between Tournament & Player.

    param: tournament_id: The foreign key to the Tournament model
    param: player: The foreign key to the Player model
    param: objects: The default Manager for django to use
    param: utilities: The utility manager used to create or update entries

    """
    tournament_id = models.ForeignKey('Tournament')
    player        = models.ForeignKey('Player')
    objects       = models.Manager()
    utilities     = EntryUtilitiesManager()

    class Meta:
        unique_together = (('tournament_id', 'player'))

    def __unicode__(self):
        return self.player.__unicode__()\
            + ' in '\
            + self.tournament_id.__unicode__()

    def get_absolute_url(self):
        return reverse('tournament_detail', kwargs={'pk': self.tournament_id})
