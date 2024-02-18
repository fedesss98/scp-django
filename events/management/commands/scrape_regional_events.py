"""
Scrape regional events from canottaggioservice.net
and creates instances of the Event model
"""
from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError
from events.models import Event

from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://canottaggioservice.canottaggio.net/'


class Command(BaseCommand):
    help = 'Scrape Canottaggioservice.net to get urls of all regional events'

    def add_arguments(self, parser):
        # Optional URL argument
        parser.add_argument(
            '--url',
            type=str,
            help='The URL of the event to be created'
        )

    def handle(self, *args, **options):
        soup = self.request_page()
        table = soup.find('div', class_='box').find()
        #print(table)
        print(len(table.find_all('tr')))
        for row in table.find_all('tr'):
            print(row)
            if options['url'] is not None:
                links = [BASE_URL + link.get('href') for link in row.find_all('a')]
                if options['url'] in links:
                    self.stdout.write('Found the requested event')
                    self.create_event(row)
                    break
            else:
                self.create_event(row)
        self.stdout.write(self.style.SUCCESS('Scraping completed'))

    @staticmethod
    def format_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        return date_object.strftime('%Y-%m-%d')

    @staticmethod
    def request_page():
        url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=menu_regionali.php?reg=13&&;sta_ag=2023'
        headers = {
            "User-Agent": "fantapoma"
        }
        # Define url parameters for GET request
        params = {
            'reg': 13,
        }
        page = requests.get(url, headers=headers, params=params)
        return BeautifulSoup(page.text, 'html.parser')

    def create_event(self, row):
        info = row.find_all('td')
        url = BASE_URL + info[0].find('a').get('href')
        date = self.format_date(info[1].string.strip())
        location = info[2].string.strip().title()
        name = info[3].string.strip().title()
        self.stdout.write(f'{"-" * 10}\nURL: {url}\nDate: {date}\nLocation: {location}\nName: {name}')
        # Create the Event object
        event = Event(
            url=url,
            date=date,
            location=location,
            name=name,
            type='Regionale',
        )
        try:
            event.save()
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Event {name} already exists'))
        return None


# DEBUGGING FEATURES
def format_date(date_string):
    date_object = datetime.strptime(date_string, '%d/%m/%Y')
    return date_object.strftime('%Y-%m-%d')


def main():
    url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=menu_regionali.php?reg=13&amp;&amp;sta_ag=2023'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    # Define url parameters for GET request
    params = {
        'reg': 13,
    }
    base_events_url = 'https://canottaggioservice.canottaggio.net/'
    page = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('div', class_='box').find()
    for row in table.find_all('tr'):
        info = row.find_all('td')
        url = base_events_url + info[0].find('a').get('href')
        date = format_date(info[1].string.strip())
        location = info[2].string.strip().title()
        name = info[3].string.strip().title()
        print(url, date, location, name, sep='\n')


if __name__ == '__main__':
    main()
