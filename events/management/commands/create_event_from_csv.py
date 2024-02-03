"""
Create an Event instance from a URL
"""

from django.core.management.base import BaseCommand, CommandError
from events.models import Event

from datetime import datetime
import csv



class Command(BaseCommand):
    help = 'Create an Event instance from data in a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the CVS file')

    def handle(self, *args, **options):
        filename = options['path']

        # Open the CSV file and create a reader object
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                # Loop through the rows of the CSV file and create Event objects
                for row in reader:
                    # Get the values from the row dictionary
                    url = row["url"]
                    date = row["date"]  # Check if those are well formatted
                    location = row["location"]
                    name = row["name"]

                    # Create the Event object
                    event = Event(
                        url=url,
                        date=date,
                        location=location,
                        name=name,
                        type='Regionale'
                    )
                    event.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully created event "{event}"'))

        except FileNotFoundError as e:
            raise CommandError(f'File "{filename}" not found') from e

        
    @staticmethod
    def format_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        return date_object.strftime('%Y-%m-%d')
