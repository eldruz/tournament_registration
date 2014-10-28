from django.conf.urls import patterns, url

from .views import TournamentProductListView, TournamentProductCreateView, \
    TournamentProductDetailView

urlpatterns = patterns('',
    url(r'^tproduct/list/$',
        TournamentProductListView.as_view(), name='tournament_product_list'),
    url(r'^tproduct/create/$',
        TournamentProductCreateView.as_view(), name='tournament_product_create'),
    url(r'^tproduct/(?P<slug>[-_\w]+)/$',
        TournamentProductDetailView.as_view(), name='tournament_product_detail'),
)
