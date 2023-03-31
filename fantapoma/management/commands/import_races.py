from django.core.management.base import BaseCommand, CommandError
from fantapoma.models import Event, Race
import csv

class Command(BaseCommand):
    help = 'Import races data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        event_id = options['event_id']
        csv_file = options['csv_file']

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise CommandError(f'Event {event_id} does not exist')

        with open(csv_file) as f:
            reader = csv.reader(f)
            next(reader) # skip header row
            for row in reader:
                number = row[0]
                time = row[1]
                boat_type = row[2]
                category = row[3]
                gender = row[4]
                type = row[5]

                race = Race(
                    number=number,
                    time=time,
                    boat_type=boat_type,
                    category=category,
                    gender=gender,
                    type=type,
                    event=event
                )
                race.save()
                self.stdout.write(self.style.SUCCESS(f'Imported race {race}'))

        self.stdout.write(self.style.SUCCESS('Done importing races'))