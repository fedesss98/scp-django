import uuid

from django.db import models

from fantapoma.models import Athlete

# Create your models here.


class Club(models.Model):
    SCP = 'PALERMO SC'
    TLMR = 'TELIMAR'
    CCRL = 'LAURIA CCR'
    AUGST = 'AUGUSTA'
    ORTG = 'ORTIGIA'
    CUS = 'CUS PALERMO'
    PLR = 'PELOROROW'
    UNS = 'UNIONE SICILIANA'
    PRD = 'PARADISO'
    CLUB_CHOICES = [
        (SCP, 'PALERMO SC'),
        (TLMR, 'TELIMAR'),
        (CUS, 'CUS PALERMO'),
        (PLR, 'PELOROROW'),
        (CCRL, 'LAURIA CCR'),
        (AUGST, 'AUGUSTA'),
        (ORTG, 'ORTIGIA'),
        (UNS, 'UNIONE SICILIANA'),
        (PRD, 'PARADISO')
    ]
    name = models.CharField(max_length=50, choices=CLUB_CHOICES)
    athletes = models.ManyToManyField(Athlete)

    def __str__(self):
        return self.name


class Event(models.Model):
    url = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    date = models.DateField()
    location = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    EVENT_TYPES = [
        ('REG', 'Regionale'),
        ('NAT', 'Nazionale'),
    ]
    type = models.CharField(max_length=80, choices=EVENT_TYPES, default='REG')

    def __str__(self):
        return self.name


class Race(models.Model):
    number = models.IntegerField(default=0)
    time = models.TimeField(null=True)
    # BOAT_TYPE_CHOICES = [
    #     ('1x', 'Single scull'),
    #     ('2x', 'Double scull'),
    #     ('4x', 'Quadruple scull'),
    #     ('8+', 'Eight'),
    # ]
    boat_type = models.CharField(max_length=20, default='SINGOLO')
    # CATEGORY_CHOICES = [
    #     ('ALLIEVIA1', '7,20 Allievi B1'),
    #     ('JUNIOR', 'Junior'),
    #     ('SENIOR', 'Senior'),
    #     ('MASTERA', 'Master'),
    # ]
    category = models.CharField(max_length=20, default='SENIOR')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Mix'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    TYPE_CHOICES = [
        ('HEAT', 'Qualificazione'),
        ('FINAL', 'Finale'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='FINAL')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} - {self.number}"


class Crew(models.Model):
    bow_number = models.IntegerField(choices=[(i, i) for i in range(1, 9)])
    athletes = models.ManyToManyField(Athlete)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} - {self.bow_number}"


class Athlete(models.Model):
    name = models.CharField(max_length=80)

