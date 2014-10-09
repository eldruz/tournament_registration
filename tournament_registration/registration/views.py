from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Tournament
from .models import Entry


class TournamentList(ListView):
    model = Tournament


class TournamentDetail(DetailView):
    model = Tournament
