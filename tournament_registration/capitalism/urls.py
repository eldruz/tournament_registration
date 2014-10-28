from django.conf.urls import patterns, url

from .views import TournamentProductListView, TournamentProductCreateView, \
    TournamentProductDetailView, TournamentProductDeleteView, \
    TournamentProductUpdateView

urlpatterns = patterns('',
    url(r'^tproduct/list/$',
        TournamentProductListView.as_view(), name='tournament_product_list'),
    url(r'^tproduct/create/$',
        TournamentProductCreateView.as_view(), name='tournament_product_create'),
    url(r'^tproduct/delete/(?P<slug>[-_\w]+)/$',
        TournamentProductDeleteView.as_view(), name='tournament_product_delete'),
    url(r'^tproduct/update/(?P<slug>[-_\w]+)/$',
        TournamentProductUpdateView.as_view(), name='tournament_product_update'),
    url(r'^tproduct/(?P<slug>[-_\w]+)/$',
        TournamentProductDetailView.as_view(), name='tournament_product_detail'),
)
