from lib2to3.pytree import Base
from django.core.management.base import BaseCommand, CommandError
from fantapoma.models import Athlete

import csv, datetime

class Command(BaseCommand):
    help = 'Import Athletes from .csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(path)
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                athlete = {
                    'name': str(row[1]).title(),
                    'total': row[2],
                    'first': row[3],
                    'second': row[4],
                    'third': row[5],
                    'first_time': datetime.datetime.strptime(row[6], '%Y-%m-%d').date(),
                    'last_time': datetime.datetime.strptime(row[7], '%Y-%m-%d').date(),
                    'points': int(row[8]),
                }
                Athlete.objects.get_or_create(**athlete)
                
                self.stdout.write(f'{athlete}')
