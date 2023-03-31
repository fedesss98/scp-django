"""
Create an Event instance from a URL
"""

from django.core.management.base import BaseCommand
from events.models import Event

from datetime import datetime
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Create an Event instance from data obtained via a GET request to a specified URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the event to be created')

    def handle(self, *args, **options):
        requested_url = options['url']
        found = False
        base_events_url = 'https://canottaggioservice.canottaggio.net/'
        soup = self.request_page()
        table = soup.find('div', class_='box').find()
        for row in table.find_all('tr'):
            info = row.find_all('td')
            url = base_events_url + info[0].find('a').get('href')
            if url == requested_url:
                found = True
                date = self.format_date(info[1].string.strip())
                location = info[2].string.strip().title()
                name = info[3].string.strip().title()
                self.stdout.write(f'{"-" * 10}\nURL: {url}\nDate: {date}\nLocation: {location}\nName: {name}')
                # Create the Event object
                event = Event(
                    url=url,
                    date=date,
                    location=location,
                    name=name
                )
                event.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created event "{event}" from data obtained via GET request to {url}'))
        if not found:
            self.stdout.write(self.style.WARNING(f'Requested URL not found'))

    @staticmethod
    def format_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        formatted_date_string = date_object.strftime('%Y-%m-%d')
        return formatted_date_string

    @staticmethod
    def request_page():
        url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=menu_regionali.php?reg=13&amp;&amp;sta_ag=2023'
        headers = {
            "User-Agent": "fantapoma"
        }
        # Define url parameters for GET request
        params = {
            'reg': 13,
        }
        page = requests.get(url, headers=headers, params=params)
        return BeautifulSoup(page.text, 'html.parser')