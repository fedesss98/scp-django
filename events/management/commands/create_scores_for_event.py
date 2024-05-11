from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from fantapoma.models import FantaAthlete, FantaAthleteEventScore
from events.models import Event

class Command(BaseCommand):
    help = 'Create a FantaAthleteEventScore instance for every FantaAthlete'

    def add_arguments(self, parser):
        parser.add_argument('event_url', type=str, help='The URL of the Event')

    def handle(self, *args, **options):
        event_url = options['event_url']

        try:
            # Get the Event with the given URL
            event = Event.objects.get(url=event_url)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'No Event found with URL {event_url}'))
            return

        # Get all FantaAthlete instances
        fanta_athletes = FantaAthlete.objects.all()

        for fanta_athlete in fanta_athletes:
            # Create a FantaAthleteEventScore instance for the FantaAthlete and Event
            FantaAthleteEventScore.objects.create(athlete=fanta_athlete, event=event)

        self.stdout.write(self.style.SUCCESS(f'Successfully created FantaAthleteEventScore instances for all FantaAthletes for Event with URL {event_url}'))