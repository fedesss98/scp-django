from operator import mod
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

import math

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

    player = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    @property
    def bookings(self):
        n = self.player.all().count()
        return n

    @property
    def adjusted_points(self):
        adjusted_points = self.points*(1 + math.log(self.bookings+1))
        return int(adjusted_points)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.name
