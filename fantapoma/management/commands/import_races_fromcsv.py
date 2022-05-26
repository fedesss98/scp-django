"""
Importa tutte le gare SCP disputate a Poma nel database.
Usa il modello Race.
Ogni Race è collegata a un Athlete (Many to One).

=========
TERMINALE
=========
python manage.py import_races_fromcsv --path ../gare_scp_poma.csv
"""

from lib2to3.pytree import Base
from django.core.management.base import BaseCommand, CommandError
from numpy import float64
from fantapoma.models import Race, Athlete

import csv, datetime

class Command(BaseCommand):
    help = 'Import Races from .csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(path)
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            next(reader)
            i = 0
            for row in reader:
                self.stdout.write(f'- {i}\n')
                try:
                    athlete = Athlete.objects.get(name=row[9].title())
                except Athlete.DoesNotExist:
                    self.stdout.write(f'No athlete {row[9]} in database!')
                else:
                    time_units = row[5].split(':')
                    time = datetime.timedelta(
                        minutes=int(time_units[0]),
                        seconds=int(time_units[1]),
                        milliseconds=10*int(time_units[2]),
                    )
                    race = {
                        'athlete': athlete,
                        'date':  datetime.datetime.strptime(row[1], '%Y-%m-%d'),
                        'location':  row[2].lower(),
                        'event': row[3].lower(),
                        'result':  row[4].lower(),
                        'time':  time,
                        'boat':  row[6].lower(),
                        'cat':  row[7],
                        'soc':  row[8].upper(),
                    }
                    Race.objects.get_or_create(**race)
                    # self.stdout.write(f'{race}')
                    i += 1
                
