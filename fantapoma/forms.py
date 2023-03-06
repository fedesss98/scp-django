from django import forms
from .models import Athlete

class UpdatePointsForm(forms.ModelForm):
    SPECIAL_ACTIONS = (
        ('cannone', 'Video "A CANNONE" con Ficarra'),
        ('cibo', 'Offrire cibo'),
        ('salto', 'Foto con salto in premiazione'),
        ('selfie', 'Selfie con un Allenatore di Secondo Livello o superiore'),
        ('bevanda', 'Bevanda offerta a un Allenatore di Primo Livello o superiore'),
        ('franchina', 'Selfie con Bruno Franchina'),
        ('batticinque', 'Batticinque a Ficarra'),
        ('vittoria', 'Video "VITTORIA PER LA CANOTTIERI PALERMO" con Vito Scarpello'),
        ('stretta', 'Foto stringendo la mano a un avversario di un altro club'),
        ('calzini', 'Indossare calzini variopinti/spaiati'),
        ('maglietta', 'Indossare una maglietta variopinta'),
        ('occhiali', 'Indossare occhiali da sole'),
        ('cappellino', 'Indossare un cappellino'),
        ('miele', 'Selfie con Miele'),
    )
    ACTION_POINTS_DICT = {
        'golds': 50,
        'silvers': 30,
        'bronzes': 20,
        'lasts': -10,
        'cannone': 5,
        'cibo': 5,
        'salto': 5,
        'selfie': 5,
        'bevanda': 5,
        'franchina': 5,
        'batticinque': 3,
        'vittoria': 3,
        'stretta': 3,
        'calzini': 3,
        'maglietta': 1,
        'occhiali': 1,
        'cappellino': 1,
        'miele': 1,
        }
    golds = forms.IntegerField(label="Medaglie d'Oro", initial=0, required=False)
    silvers = forms.IntegerField(label="Medaglie di Argento", initial=0, required=False)
    bronzes = forms.IntegerField(label="Medaglie di Bronzo", initial=0, required=False)
    lasts = forms.IntegerField(label="Ultimi Posti", initial=0, required=False)
    actions = forms.MultipleChoiceField(
        label='Seleziona le Azioni Speciali che hai compiuto:',
        required=False,
        choices=SPECIAL_ACTIONS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Athlete
        fields = []

    def save(self, commit=True):
        print(self.instance.points)
        ACTION_POINTS_DICT = {
            'golds': 50,
            'silvers': 30,
            'bronzes': 20,
            'lasts': -10,
            'cannone': 5,
            'cibo': 5,
            'salto': 5,
            'selfie': 5,
            'bevanda': 5,
            'franchina': 5,
            'batticinque': 3,
            'vittoria': 3,
            'stretta': 3,
            'calzini': 3,
            'maglietta': 1,
            'occhiali': 1,
            'cappellino': 1,
            'miele': 1,
        }
        points = 0
        for position in ['golds', 'silvers', 'bronzes', 'lasts']:
            # Number of first, second, third or last positions
            n = self.cleaned_data[position] if self.cleaned_data[position] else 0
            points += ACTION_POINTS_DICT[position] * n
        for action in self.cleaned_data['actions']:
            points += ACTION_POINTS_DICT[action]
        self.instance.points = points
        print(self.instance.points)
        return super().save(commit)
