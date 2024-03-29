"""
Scrape national events from canottaggioservice.net
and creates instances of the Event model
"""
from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError
from events.models import Event

from datetime import datetime
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Scrape Canottaggioservice.net to get urls of all national events'

    def handle(self, *args, **options):
        base_events_url = 'https://canottaggioservice.canottaggio.net/'
        soup = self.request_page()
        table = soup.find('div', class_='box').find()
        for row in table.find_all('tr')[2:]:
            info = row.find_all('td')
            url = base_events_url + info[0].find('a').get('href')
            date = self.format_date(info[1].string.strip())
            location = info[2].string.strip().title()
            name = info[3].string.strip().title()
            self.stdout.write(f'{"-"*10}\nURL: {url}\nDate: {date}\nLocation: {location}\nName: {name}')
            # Create the Event object
            event = Event(
                url=url,
                date=date,
                location=location,
                name=name,
                type='NAT',
            )
            try:
                event.save()
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f'Event {name} already exists'))
        self.stdout.write(self.style.SUCCESS('Scraping completed'))

    @staticmethod
    def format_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        formatted_date_string = date_object.strftime('%Y-%m-%d')
        return formatted_date_string

    @staticmethod
    def request_page():
        url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=menu_nazionali.php'
        headers = {
            "User-Agent": "fantapoma"
        }
        page = requests.get(url, headers=headers)
        return BeautifulSoup(page.text, 'html.parser')


# DEBUGGING FEATURES
def format_date(date_string):
    date_object = datetime.strptime(date_string, '%d/%m/%Y')
    formatted_date_string = date_object.strftime('%Y-%m-%d')
    return formatted_date_string


def main():
    url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=menu_nazionali.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    base_events_url = 'https://canottaggioservice.canottaggio.net/'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('div', class_='box').find()
    for row in table.find_all('tr')[2:]:
        info = row.find_all('td')
        url = base_events_url + info[0].find('a').get('href')
        date = format_date(info[1].string.strip())
        location = info[2].string.strip().title()
        name = info[3].string.strip().title()
        print(url, date, location, name, sep='\n')
    print('Done!')


if __name__ == '__main__':
    main()
