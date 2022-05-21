from operator import mod
from pyexpat import model
from time import time
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

import math
import datetime

# Create your models here.

class Athlete(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField('Total Races', default=0)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    first_time = models.DateField('First Race Date')
    last_time = models.DateField('Last Race Date')
    points = models.IntegerField(default=0)

    players = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    @property
    def bookings(self):
        n = self.players.all().count()
        return n

    @property
    def adjusted_points(self):
        booking_term = self.points*(math.tanh(self.bookings/4))
        adjusted_points = self.points + booking_term
        return int(adjusted_points)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.name

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
    special_class = models.CharField(max_length=50, default='oggetto')
    special = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)

    player = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.special_class}: {self.name}'