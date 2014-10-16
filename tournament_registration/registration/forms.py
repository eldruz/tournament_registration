from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Player


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = {'name', 'team', 'registered_tournaments'}
        widgets = {
            'registered_tournaments': CheckboxSelectMultiple
        }
