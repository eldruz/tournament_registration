from django.db import models

class Tournament(models.Model):
    GAME_LIST = (
        (u'2X', u'Super Street Fighter 2X'),
        (u'USF4', u'Ultra Street Fighter 4'),
        (u'3.3', u'Street Fighter III Third Strike'),
    )
    title = models.CharField('Tournament title.',
                             max_length=256,
                             unique=True)
    game = models.CharField('Game played for this tournament.\n\
                            The games are chosen from a hardcoded list.',
                            max_length=256,
                            choices=GAME_LIST)
    date = models.DateTimeField('Date of the tournament')
    support = models.CharField('Support on which the tournament will be played.',
                               max_length=256)
    nb_max = models.PositiveSmallIntegerField('Maximum number of participants.')
    price = models.PositiveSmallIntegerField('Entry fee for the tournament')
    nb_per_team = models.PositiveSmallIntegerField('Number of players per team.',
                                                   default=1)

    class Meta:
        " A tournament title can only be associated with a single date "
        unique_together = (('title', 'date'))

    def __unicode__(self):
        return self.title

class Entry(models.Model):
    tournament_title = models.ForeignKey(Tournament, to_field='title')
    player = models.CharField(max_length=256)

    def __unicode__(self):
        return self.player + ' in ' + self.tournament_title.__unicode__()
