from django.core import serializers

from registration.models import Tournament


class TournamentExport(object):
    def __init__(self, tournament_id):
        self._get_tournament(tournament_id)

    def _get_tournament(self, tournament_id):
        tourney = Tournament.objects.filter(pk=tournament_id)
        self.tournament = tourney
        self.players = tourney.first().player_set.all()

    def export(self):
        raise NotImplementedError


class ExportJsonMixin(object):
    def export(self):
        player_fields = ('team', 'name')
        tournament_fields = ('title', 'game', 'support', 'date', 'nb_max')
        data_tournament = serializers.serialize(
            'json',
            self.tournament,
            fields=tournament_fields
        )
        data_players = serializers.serialize(
            'json',
            self.players,
            fields=player_fields
        )
        return data_tournament + data_players


class TournamentJsonExport(ExportJsonMixin, TournamentExport):
    pass
