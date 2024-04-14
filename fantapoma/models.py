from django.db import models
from django.contrib.auth.models import User

from django.db.models import Sum

import math
import datetime


from events.models import Athlete, Crew, Event  # Import the Athlete model

# Create your models here.


class FantaAthlete(models.Model):
    name = models.CharField(max_length=200)
    born = models.DateField('Date of Birth', default=datetime.date(2000,1,1))
    #total = models.IntegerField('Total Races', default=0)
    #first = models.IntegerField(default=0)
    #second = models.IntegerField(default=0)
    #third = models.IntegerField(default=0)
    first_time = models.DateField('First Race Date')
    last_time = models.DateField('Last Race Date')
    release_date = models.DateField('Release Date', default=datetime.date(2024,1,1))
    price = models.IntegerField(default=0)
    race_points = models.IntegerField(default=0)
    actions_points = models.IntegerField(default=0)

    # Corresponding real Athlete
    athlete = models.OneToOneField(Athlete, blank=True, null=True, on_delete=models.CASCADE)
    # Players who have booked this athlete
    players = models.ManyToManyField(User, blank=True, related_name='athletes_set')
    # Corresponding real User
    is_user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='true_athlete')

    def __str__(self):
        return self.name

    @property
    def category(self):
        categories = {9: 'Allievi A', 10: 'Allievi A',
                      11: 'Allievi B', 12: 'Allievi B',
                      13: 'Allievi C',
                      14: 'Cadetti',
                      15: 'Ragazzi', 16: 'Ragazzi',
                      17: 'Junior', 18: 'Junior',
                      19: 'Under23', 20: 'Under23', 21: 'Under23', 22: 'Under23',
                      23: 'Senior', 24: 'Senior', 25: 'Senior', 26: 'Senior', 27: 'Senior',
        }
        today = datetime.date.today()
        age = today.year - self.born.year
        return categories.get(age, 'Master')

    @property
    def bookings(self):
        return self.players.all().count()

    @property
    def adjusted_price(self):
        booking_term = self.price*(math.tanh(self.bookings/4))
        base_price = 5
        if self.athlete is not None:
            crews = self.athlete.crew_set.filter(race__event__date__year=2024)
            for crew in crews:
                if crew.result == 1:
                    base_price += 25
                elif crew.result == 2:
                    base_price += 15
                elif crew.result == 3:
                    base_price += 10
                else:
                    base_price += 3
        booking_term = base_price*math.tanh(self.bookings/4)
        return int(base_price + booking_term)
    
    def get_crew_set(self, date=None):
        if date is None:
            date = datetime.datetime.now().year
        return self.athlete.crew_set.filter(race__event__date__year__gte=date)
    
    @property
    def total(self):
        """Total of medals won by the Athlete"""
        try:
            crew_set = self.get_crew_set()
            return crew_set.count()
        except AttributeError:
            return 0

    @property
    def first(self):
        """Total of gold medals won by the Athlete"""
        try:
            crew_set = self.get_crew_set()
            return sum(crew.result == 1 for crew in crew_set)
        except AttributeError:
            return 0
    
    @property
    def second(self):
        """Total of silver medals won by the Athlete"""
        try:
            crew_set = self.get_crew_set()
            return sum(crew.result == 2 for crew in crew_set)
        except AttributeError:
            return 0
    
    @property
    def third(self):
        """Total of bronze medals won by the Athlete"""
        try:
            crew_set = self.get_crew_set()
            return sum(crew.result == 3 for crew in crew_set)
        except AttributeError:
            return 0
    
    @property
    def total_points(self):
        return self.race_points + self.actions_points


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField('nome', max_length=100, blank=True, null=True)
    last_name = models.TextField('cognome', max_length=100, blank=True, null=True)
    franchs = models.IntegerField(blank=True, default=400)
    team_name = models.CharField(max_length=200, default='8+')
    cox = models.ForeignKey(FantaAthlete, blank=True, null=True, on_delete=models.SET_NULL, related_name='cox')

    def get_athletes(self):
        print(self.user)
        return self.user.athletes_set.all()

    @property
    def score(self):
        athletes = self.get_athletes()
        score = sum(athlete.adjusted_price for athlete in athletes)
        # Add two times the scores of the Player's Athlete
        # if hasattr(self.user, 'true_athlete'):
        #     score += 2*self.user.true_athlete.actions_points
        score = score if score is not None else 0
        return score

    def __str__(self):
        return self.user.username

class Special(models.Model):
    COACH = 'CCH'
    OBJECT = 'OBJ'
    STAFF = 'STFF'
    SPECIAL_CLASSES = (
        (COACH, 'allenatore'), 
        (OBJECT, 'oggetto'), 
        (STAFF, 'staff'),
    )

    name = models.CharField(max_length=200)
    special_class = models.CharField(max_length=50, choices=SPECIAL_CLASSES, default='oggetto')
    special = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)

    # Players who have booked this athlete
    players = models.ManyToManyField(User, blank=True, related_name='specials_set')

    @property
    def tipo(self):
        return str(dict(self.SPECIAL_CLASSES)[self.special_class]).capitalize()

    def __str__(self):
        return f'{self.special_class}: {self.name}'
    

class FantaAthleteEventScore(models.Model):
    athlete = models.ForeignKey(FantaAthlete, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ficarra_video = models.BooleanField(default=False, verbose_name='Video "A CANNONE" con Ficarra')
    offered_food = models.BooleanField(default=False, verbose_name='Offrire cibo')
    photo_jumping = models.BooleanField(default=False, verbose_name='Foto con salto in premiazione')
    selfie_coach = models.BooleanField(default=False, verbose_name='Selfie con un allenatore di Secondo Livello o superiore')
    drink_to_coach = models.BooleanField(default=False, verbose_name='Offrire da bere ad un allenatore di Primo Livello o superiore')
    selfie_franchina = models.BooleanField(default=False, verbose_name='Selfie con Bruno Franchina')
    highfive_ficarra = models.BooleanField(default=False, verbose_name='Batticinque a Ficarra')
    vittoria_video = models.BooleanField(default=False, verbose_name='Video "VITTORIA PER LA CANOTTIERI PALERMO" con Vito Scarpello')
    shaking_hands = models.BooleanField(default=False, verbose_name='Foto con stretta di mano a un avversario di un altro club')
    selfie_miele = models.BooleanField(default=False, verbose_name='Selfie con Miele')
    anger_beni = models.BooleanField(default=False, verbose_name='Far arrabbiare Beni')
    stop_before_end = models.BooleanField(default=False, verbose_name='Fermarsi prima del traguardo')
    coming_late = models.BooleanField(default=False, verbose_name='Arrivare in ritardo')
    fall_in_water = models.BooleanField(default=False, verbose_name='Cadere in acqua')
    fight_adversary = models.BooleanField(default=False, verbose_name='Litigare con un avversario')
    not_throwing_garbage = models.BooleanField(default=False, verbose_name='Non gettare la spazzatura')
    out_of_buoys = models.BooleanField(default=False, verbose_name='Tagliare il traguardo fuori dalle boe')
    bad_name_pronunciation = models.BooleanField(default=False, verbose_name='Nome pronunciato male dal giudice di partenza')
    last_to_go = models.BooleanField(default=False, verbose_name='Ultimo a gareggiare')
    has_hat = models.BooleanField(default=False, verbose_name='Indossare un cappellino')
    has_sunglasses = models.BooleanField(default=False, verbose_name='Indossare occhiali da sole')
    has_red_tshirt = models.BooleanField(default=False, verbose_name='Indossare una maglietta rossa')
    has_supporter = models.BooleanField(default=False, verbose_name='Portare un #scpsupporter')

    class Meta:
        unique_together = ('athlete', 'event')

    @property
    def action_points(self):
        ACTION_POINTS_MAP = {
            'ficarra_video': 10,
            'offered_food': 5,
            'photo_jumping': 5,
            'selfie_coach': 5,
            'drink_to_coach': 5,
            'selfie_franchina': 5,
            'highfive_ficarra': 3,
            'vittoria_video': 3,
            'shaking_hands': 3,
            'selfie_miele': 1,
            'anger_beni': -10,
            'stop_before_end': -5,
            'coming_late': -5,
            'fall_in_water': -5,
            'fight_adversary': -5,
            'not_throwing_garbage': -2,
            'out_of_buoys': -2,
            'bad_name_pronunciation': -2,
            'last_to_go': -1,
        }

        return sum(
            ACTION_POINTS_MAP[action]
            for action in ACTION_POINTS_MAP
            if getattr(self, action)
        )


class PlayerEventScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def calculate_score(self):
        KALOS_ATHLETES = [
            'Coppola Gabriele',
            'Castiglione Andrea',
            'Marino Alberto',
            'Romano Gabriele',
            'Palumbo Lorenzo',
        ]
        KIDS_ATHLETES = [
            'Oliva Salvatore',
            'Panzica Lorenzo',
            'Coppola Eleonora',
            'Mascari Giuseppe',
            'Sciabarrà Flavio',
            'Li Greci Riccardo',
            'Martucci Francesco Jan',
        ]

        fanta_athletes = self.player.athletes.all()
        crew_has_hat = False
        crew_has_red_shirt = False
        crew_has_sunglasses = False
        crew_has_supporter = False
        kalos_club = 0
        kids_club = 0
        for fanta_athlete in fanta_athletes:
            if fanta_athlete in KALOS_ATHLETES:
                kalos_club += 1
            if fanta_athlete in KIDS_ATHLETES:
                kids_club += 1
            try:
                fanta_athlete_event_score = FantaAthleteEventScore.objects.get(athlete=fanta_athlete, event=self.event)
            except FantaAthleteEventScore.DoesNotExist:
                continue
            else:
                if fanta_athlete == self.player.cox:
                    self.score += fanta_athlete_event_score.action_points * 2
                else:
                    self.score += fanta_athlete_event_score.action_points
                if fanta_athlete_event_score.has_hat:
                    crew_has_hat = True
                if fanta_athlete_event_score.has_red_tshirt:
                    crew_has_red_shirt = True
                if fanta_athlete_event_score.has_sunglasses:
                    crew_has_sunglasses = True
                if fanta_athlete_event_score.has_supporter:
                    crew_has_supporter = True

            OBJECTS_SCORE_MAP = {
                'Cappellino FantaPoma': (crew_has_hat, 20, -20),
                'Maglietta Rossa': (crew_has_red_shirt, 10, -10),
                'Occhiali da Sole': (crew_has_sunglasses, 10, -10),
                'Supporter': (crew_has_supporter, 15, 0),
            }

            COACHES_SCORE_MAP = {
                'Calogero Galletto': kalos_club*20,
                'Naselli Marta': kids_club*20,
            }

            for special, (condition, positive_points, negative_points) in OBJECTS_SCORE_MAP.items():
                if Special.objects.filter(name=special, players=self.player.user).exists():
                    self.score += positive_points if condition else negative_points

            for coach, points in COACHES_SCORE_MAP.items():
                if Special.objects.filter(name=coach, players=self.player.user).exists():
                    self.score += points

        self.save()