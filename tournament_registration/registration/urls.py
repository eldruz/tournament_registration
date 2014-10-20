from django.conf.urls import patterns, url

from .views import TournamentDetail, TournamentCreate, TournamentDelete, \
    TournamentUpdate, TournamentList
from .views import EntryCreateView
from .views import PlayerCreate, PlayerUpdate, PlayerDetail, PlayerList, \
    PlayerDelete
from .views import PlayersPerTournamentList


urlpatterns = patterns('',
    url(r'^tournaments/update/(?P<slug>[-_\w]+)/$',
        TournamentUpdate.as_view(), name='update_tournament'),
    url(r'^tournaments/delete/(?P<slug>[-_\w]+)/$',
        TournamentDelete.as_view(), name='delete_tournament'),
    url(r'^tournaments/create/$',
        TournamentCreate.as_view(), name='create_tournament'),
    url(r'^tournaments/(?P<tournament_id>[-_\w]+)/players$',
        PlayersPerTournamentList.as_view(), name='players_per_tournament'),
    url(r'^tournaments/(?P<slug>[-_\w]+)/$',
        TournamentDetail.as_view(), name='tournament_detail'),
    url(r'^tournaments/$',
        TournamentList.as_view(), name='tournament_list'),
    url(r'^entries/create/$',
        EntryCreateView.as_view(), name='create_entry'),
    url(r'^players/update/(?P<slug>[-_\w]+)/$',
        PlayerUpdate.as_view(), name='update_player'),
    url(r'^players/delete/(?P<slug>[-_\w]+)/$',
        PlayerDelete.as_view(), name='delete_player'),
    url(r'^players/create/$',
        PlayerCreate.as_view(), name='create_player'),
    url(r'^players/(?P<slug>[-_\w]+)/$',
        PlayerDetail.as_view(), name='player_detail'),
    url(r'^players/$',
        PlayerList.as_view(), name='player_list')
)
