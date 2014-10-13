from django.conf.urls import patterns, url

from .views import TournamentList
from .views import TournamentDetail
from .views import PlayerList

urlpatterns = patterns('',
    url(r'^tournaments/(?P<tournament_id>[-_\w]+)/players$', PlayerList.as_view()),
    url(r'^tournaments/(?P<pk>[-_\w]+)/$', TournamentDetail.as_view()),
    url(r'^tournaments/$', TournamentList.as_view())
)
