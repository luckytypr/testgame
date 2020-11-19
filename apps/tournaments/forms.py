from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .models import Tournament


class TournamentCreateForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = ('name', )
