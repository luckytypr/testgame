from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .models import Tournament


class TournamentCreateForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = ('name', )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper
    #     self.helper.form_method = 'post'
    #
    #     self.helper.layout = Layout(
    #         'name',
    #         Submit('submit', 'Create', css_class='btn-primary mr-1')
    #     )