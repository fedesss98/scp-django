from django import forms
from .models import FantaAthlete, Special, FantaAthleteEventScore

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
        ('cazziata', 'Cazziatone da Beni'),
        ('fermars', "Fermarsi prima dell'arrivo"),
        ('ritardo', "Arrivare in ritardo"),
        ('cadere', "Cadere in acqua"),
        ('litigare', "Litigare con un avversario"),
        ('rifiutare', "Rifiutarsi di buttare i rifiuti"),
        ('boe', "Tagliare il traguardo fuori dalle boe"),
        ('sbagliato', "Il giudice in partenza sbaglia il tuo nome"),
        ('ultimo', "Ultimo a gareggiare"),
    )
    golds = forms.IntegerField(label="Medaglie d'Oro", initial=0, required=False)
    silvers = forms.IntegerField(label="Medaglie di Argento", initial=0, required=False)
    bronzes = forms.IntegerField(label="Medaglie di Bronzo", initial=0, required=False)
    lasts = forms.IntegerField(label="Ultimi Posti", initial=0, required=False)
    actions = forms.MultipleChoiceField(
        label='Seleziona le Azioni Speciali che hai compiuto:',
        required=False,
        choices=SPECIAL_ACTIONS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = FantaAthlete
        fields = []

    def save(self, commit=True):
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
            'cazziata': -10,
            'fermarsi': -5,
            'ritardo': -5,
            'cadere': -5,
            'litigare': -5,
            'rifiutare': -2,
            'boe': -2,
            'sbagliato': -1,
            'ultimo': -1,
        }
        race_points = 0
        # Race points
        for position in ['golds', 'silvers', 'bronzes', 'lasts']:
            # Number of first, second, third or last positions
            n = self.cleaned_data[position] or 0
            race_points += ACTION_POINTS_DICT[position] * n
        self.instance.race_points = race_points
        actions_points = sum(
            ACTION_POINTS_DICT[action] for action in self.cleaned_data['actions']
        )
        self.instance.actions_points = actions_points
        return super().save(commit)
    
    
class SpecialForm(forms.ModelForm):
    class Meta:
        model = Special
        fields = ['name', 'special_class', 'special', 'price']


class FantaAthleteEventScoreForm(forms.ModelForm):
    class Meta:
        model = FantaAthleteEventScore
        fields = '__all__'