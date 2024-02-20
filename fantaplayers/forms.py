from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from fantapoma.models import Player, FantaAthlete

class PlayerCreationForm(UserCreationForm):
    team_name = forms.CharField(
        max_length=200, 
        required=True,
        label='Il tuo 8+',)
    fanta_athlete = forms.ModelChoiceField(
        queryset=FantaAthlete.objects.filter(player__isnull=True),
        label="Seleziona l'Atleta che ti rappresenta",
        required=False,)

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
        fields = ('username', 'email', 'team_name', 'fanta_athlete', 'password1', 'password2')

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
        fanta_athlete = self.cleaned_data['fanta_athlete']
        if fanta_athlete is not None:
            fanta_athlete.is_user = player
            fanta_athlete.save()
        else:
            print("No Fanta Athlete selected. Contact the webmaster.")
        return user


