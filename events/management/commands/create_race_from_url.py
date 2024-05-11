"""
Create all Race instances from an Event URL
"""
import unicodedata
from django.core.management.base import BaseCommand
from events.models import Event, Race, Crew, Club, Athlete
# from fantapoma.models import Athlete

from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

from urllib.parse import unquote


BASE_URL = 'https://canottaggioservice.canottaggio.net/'

PROGRAMMA_EXPRESSIONS = [
    "PROGRAMMA GARE",
    "PROGRAMMA Sabato",
    "PROGRAMMA Domenica",
    "PROGRAMMA COMPLETO MANIFESTAZIONE",
]


class Command(BaseCommand):
    help = 'Create all the Race instances from data obtained via a GET request to an Event URL'
    event = None

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the race to be created')

    def handle(self, *args, **options):
        requested_url = unquote(options['url'])
        try:
            self.event = Event.objects.get(url=requested_url)
        except Event.DoesNotExist:
            self.stdout.write(self.style.WARNING("Event not found"))
            return None
        soup = self.request_page(requested_url)
        table = self.find_race_table(soup)
        if table is None:
            raise ValueError("No table found")
        else:
            program_links = self.search_race_program(table)
        if program_links is None:
            raise ValueError("No program link found")
        for program_link in program_links:
            soup = self.request_page(BASE_URL + program_link)
            self.scrape_race_plan(soup)
        return None

    @staticmethod
    def find_race_table(soup):
        outer_table = soup.find('div', class_='box').find()
        if len(outer_table.find_all('table')) == 0:
            return outer_table
        else:
            return outer_table.find_all('table')[1]

    @staticmethod
    def format_date(date_string):
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        return date_object.strftime('%Y-%m-%d')

    @staticmethod
    def request_page(url):
        # url = 'https://canottaggioservice.canottaggio.net/scrivi_cook.php?ritorno=' + url
        headers = {
            "User-Agent": "fantapoma"
        }
        # Request the page
        page = requests.get(url, headers=headers)
        return BeautifulSoup(page.text, 'html.parser')

    def search_race_program(self, table):
        links = []
        for row in table.find_all('tr'):
            if len(row.contents) < 4:
                continue
            if row.find_all('td')[1].string.strip() in PROGRAMMA_EXPRESSIONS:
                link = row.find('a').get('href')
                self.stdout.write(f"Found the RACE PROGRAM link: {link}")
                links.append(link)
        # If pass through the loop without finding the link
        if not links:
            self.stdout.write(self.style.WARNING("Race program not found."))
        return links or None

    @staticmethod
    def take_boat_info(info):
        print(info)
        categories = [
            'master',
            'senior',
            'under',
            'junior',
            'ragazzi',
            'cadetti',
            'allievi',
            'esordienti',
            'pr3'
        ]
        words = info.split(' ')
        # Take last part of the sting and removes it
        sex = words[-1]
        words = words[:-1]
        i = 0
        while words[i].isupper() and words[i].lower() not in categories:
            i += 1
        boat = ' '.join(words[:i])
        category = ' '.join(words[i:])
        return boat, category, sex

    def format_race_info(self, info, n_crews):
        race_number = info[2].strip()
        race_time = info[7].strip().replace('\xa0', '')
        race_boat, category, sex = self.take_boat_info(info[8].split('\xa0')[0].strip())
        return {'number': race_number,
                'time': race_time,
                'boat_type': race_boat,
                'category': category,
                'gender': sex,
                'type': info[8].split('\xa0')[-1].strip(),
                'event': self.event,
                'enrolled': n_crews,}

    def create_race(self, table):
        # Number of crews in race
        n_crews = len(table.find_all('td'))
        # Take the header of the race (in parent table)
        race_info_table = table.parent.previous_sibling.previous_sibling.find('td', class_='t3')
        race_infos = self.format_race_info(list(race_info_table.strings), n_crews)
        return Race.objects.create(**race_infos)

    @staticmethod
    def normalize_athletes_names(athlete):
        athlete = unicodedata.normalize('NFKC', athlete)
        athlete = athlete.replace("-Tim.", "").strip()
        return athlete.title()

    def add_athletes_to_crew(self, crew, soc):
        for at in soc.next_sibling.stripped_strings:
            if at.strip(' .') != '' and '(' not in at:
                athlete = self.normalize_athletes_names(at)
                athlete_object, created = Athlete.objects.get_or_create(name=athlete)
                # print(athlete)
                crew.athletes.add(athlete_object)
        return None

    def create_crew(self, soc, race):
        bow_number = int(soc.parent.b.string.strip())
        soc_name = soc.string.split('(')[0]
        print(soc_name)
        club, created = Club.objects.get_or_create(name=soc_name)
        # Create the Crew model instance
        crew = Crew(
            bow_number=bow_number,
            club=club,
            race=race,
        )
        crew.save()
        self.add_athletes_to_crew(crew, soc)
        return None

    def make_race_crews(self, table_socs, race):
        for soc in table_socs:
            self.create_crew(soc, race)
        return None

    def scrape_race_plan(self, soup):
        for table in soup.find_all('tr'):
            # We are only interested in tables where there are club's names
            table_socs = table.find_all("font", attrs={'style': 'font-weight:bolder;'})
            if len(table_socs) > 0:
                # That's a race table and there are entries
                race = self.create_race(table)
                self.make_race_crews(table_socs, race)
        return None
