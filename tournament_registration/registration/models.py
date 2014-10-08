from django.db import models
from django.core.exceptions import ValidationError


class ValidateOnSaveMixin(object):
    """Force model validation on save()

    Everytime a model is saved, the mixin calls the validation
    function of the model.
    Useful for now as there is yet to be a form associated with
    the model. It might trigger a double validation with the
    associated ModelForm later on."""
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update,
                                              **kwargs)


class TournamentManager(models.Manager):
    def create_tournament(self, title, game, date, nb_max, **kwargs):
        additional_attributes = {'support', 'price', 'nb_per_team'}
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
    # For now the game list is hardcoded in the model
    GAME_LIST = (
        (u'2X', u'Super Street Fighter 2X'),
        (u'USF4', u'Ultra Street Fighter 4'),
        (u'3.3', u'Street Fighter III Third Strike'),
    )

    # Fields
    title   = models.CharField('Tournament title.',
                               max_length=256,
                               unique=True,
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
    nb_max      = models.PositiveSmallIntegerField('Maximum number of participants.', blank=False)
    price       = models.PositiveSmallIntegerField('Entry fee for the tournament', default=0)
    nb_per_team = models.PositiveSmallIntegerField('Number of players per team.',  default=1)
    objects   = models.Manager()
    utilities = TournamentManager()

    class Meta:
        " A tournament title can only be associated with a single date "
        unique_together = (('title', 'date'))

    def clean(self):
        # A game has to be on the game list
        if self.game not in [x[0] for x in self.GAME_LIST]:
            msg = u'Game is not in the games list'
            raise ValidationError(msg)

    def __unicode__(self):
        return self.title


class Entry(models.Model):
    tournament_title = models.ForeignKey(Tournament, to_field='title')
    player           = models.CharField(max_length=256)

    def __unicode__(self):
        return self.player + ' in ' + self.tournament_title.__unicode__()
