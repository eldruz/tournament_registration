from django.conf.urls import patterns, url

from .views import TournamentList
from .views import TournamentDetail

urlpatterns = patterns('',
    url(r'^tournaments/(?P<pk>[-_\w]+)/$', TournamentDetail.as_view()),
    url(r'^tournaments/$', TournamentList.as_view())
)
