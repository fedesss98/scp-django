from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from fantapoma.models import Player

class PlayerCreationForm(UserCreationForm):
    team_name = forms.CharField(
        max_length=200, 
        required=True,
        label='Il tuo 8+',)

    def __init__(self, *args, **kwargs):
        super(PlayerCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'aria-describedby': 'emailHelp'
        }
        self.fields['team_name'].widget.attrs = {
            'class': 'form-control',
            'aria-describedby': 'teamNameHelp'
        }
        self.fields['password1'].widget.attrs = {
            'class': 'form-control',
            'aria-describedby': 'passwordHelp'
        }
        self.fields['password2'].widget.attrs = {
            'class': 'form-control',
            'aria-describedby': 'repeatPasswordHelp'
        }

    class Meta:
        model = User
        fields = ('username', 'email', 'team_name', 'password1', 'password2')

        labels = {
            'username': 'Username',
            'email': 'Indirizzo Email',
            'password1': 'Password',
            'password2': 'Ripeti Password'
        }

    def save(self, commit=True):
        user = super(PlayerCreationForm, self).save()
        team_name = self.cleaned_data['team_name']
        player = Player.objects.create(user=user, team_name=team_name)


