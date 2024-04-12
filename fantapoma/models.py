from django.db import models
from django.contrib.auth.models import User

from django.db.models import Sum

import math
import datetime


from events.models import Athlete, Crew  # Import the Athlete model

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
            athlete_instance = self.athlete
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
        adjusted_points = base_price + booking_term
        return int(adjusted_points)
    
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
        score = sum(athlete.total_points for athlete in athletes)
        # Add two times the scores of the Player's Athlete
        if hasattr(self.user, 'true_athlete'):
            score += 2*self.user.true_athlete.actions_points
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