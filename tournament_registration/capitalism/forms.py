from django.forms import Form
from django.forms import ModelChoiceField, IntegerField

from .models import TournamentProduct

class CartAddItemForm(Form):
    tournament = ModelChoiceField(queryset=TournamentProduct.objects.all())
    quantity = IntegerField()
