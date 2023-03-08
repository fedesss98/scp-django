from django.db import models
from django.contrib.auth.models import User

from django.db.models import Sum

import math
import datetime

# Create your models here.

class Athlete(models.Model):
    name = models.CharField(max_length=200)
    born = models.DateField('Date of Birth', default=datetime.date(2000,1,1))
    club = models.CharField(max_length=200, default='Società Canottieri Palermo')
    total = models.IntegerField('Total Races', default=0)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    first_time = models.DateField('First Race Date')
    last_time = models.DateField('Last Race Date')
    price = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    race_points = models.IntegerField(default=0)
    actions_points = models.IntegerField(default=0)

    players = models.ManyToManyField(User, blank=True)
    is_user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='true_athlete')

    def __str__(self):
        return self.name

    @property
    def category(self):
        CATEGORIES = {
            9: 'Allievi A',
            10: 'Allievi A',
            11: 'Allievi B',
            12: 'Allievi B',
            13: 'Allievi C',
            14: 'Cadetti',
            15: 'Ragazzi',
            16: 'Ragazzi',
            17: 'Junior',
            18: 'Junior',
            19: 'Under23',
            20: 'Under23',
            21: 'Under23',
            22: 'Under23',
            23: 'Senior',
            24: 'Senior',
            25: 'Senior',
            26: 'Senior',
            27: 'Senior',
        }
        today = datetime.date.today()
        age = today.year - self.born.year
        return CATEGORIES[age]

    @property
    def bookings(self):
        n = self.players.all().count()
        return n

    @property
    def adjusted_price(self):
        booking_term = self.price*(math.tanh(self.bookings/4))
        adjusted_points = self.price + booking_term
        return int(adjusted_points)

    @property
    def total_points(self):
        return self.race_points + self.actions_points


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField('nome', max_length=100, blank=True, null=True)
    last_name = models.TextField('cognome', max_length=100, blank=True, null=True)
    franchs = models.IntegerField(blank=True, default=450)
    team_name = models.CharField(max_length=200, default='8+')

    def get_athletes(self):
        return self.user.athlete_set.all()

    @property
    def score(self):
        athletes = self.get_athletes()
        score = sum(athlete.total_points for athlete in athletes)
        # Add two times the scores of the Player's Athlete
        if hasattr(self.user, 'true_athlete'):
            score += 2*self.user.true_athlete.actions_points
        score = score if score is not None else 0
        return score

    def __str__(self):
        return self.user.username


class Race(models.Model):
    DEFAULT_RACE_TIME = datetime.timedelta(minutes=0, seconds=0, milliseconds=0)

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=200)
    event = models.CharField(max_length=200)
    result = models.CharField(max_length=20)
    time = models.DurationField(null=True, blank=True, default=DEFAULT_RACE_TIME)
    boat = models.CharField(max_length=100)
    cat = models.CharField(max_length=50)
    soc = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.athlete} - {self.location}, {self.date}'


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
    points = models.IntegerField(default=0)

    player = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.special_class}: {self.name}'