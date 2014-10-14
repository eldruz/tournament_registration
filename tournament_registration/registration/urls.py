from django.conf.urls import patterns, url

from .views import TournamentList
from .views import TournamentDetail
from .views import PlayerList
from .views import PlayersPerTournamentList
from .views import TournamentsPerPlayerList

urlpatterns = patterns('',
    url(r'^tournaments/(?P<tournament_id>[-_\w]+)/players$', PlayersPerTournamentList.as_view(), name='players_per_tournament'),
    url(r'^tournaments/(?P<pk>[-_\w]+)/$', TournamentDetail.as_view(), name='tournament_detail'),
    url(r'^tournaments/$', TournamentList.as_view(), name='tournament_list'),
    url(r'^players/(?P<player_name>[-_\w]+)/$', TournamentsPerPlayerList.as_view(), name='tournaments_per_player'),
    url(r'^players/$', PlayerList.as_view(), name='player_list')
)
