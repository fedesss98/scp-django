from django.core.management.base import BaseCommand, CommandError
from fantapoma.models import Event, Race, Crew
import csv


class Command(BaseCommand):
    help = 'Import crews data from csv file'

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
                race_number = row[0]
                bow_number = row[1]
                club_name = row[2]
                athletes_names = row[3:]

                try:
                    race = Race.objects.get(number=race_number,event=event)
                except Race.DoesNotExist:
                    raise CommandError(f'Race {race_number} does not exist')

                try:
                    club = Club.objects.get(name=club_name)
                except Club.DoesNotExist:
                    raise CommandError(f'Club {club_name} does not exist')

                crew = Crew(
                    bow_number=bow_number,
                    event=event,
                    club=club,
                    race=race
                )
                crew.save()

                for name in athletes_names:
                    try:
                        athlete = Athlete.objects.get(name=name)
                        crew.athletes.add(athlete)
                    except Athlete.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Athlete {name} does not exist'))

                self.stdout.write(self.style.SUCCESS(f'Imported crew {crew}'))

        self.stdout.write(self.style.SUCCESS('Done importing crews'))