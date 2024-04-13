"""
Update a Race instance with Crews Results from an Event URL
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

RISULTATI_EXPRESSIONS = [
    "RISULTATI FINALI",
    "RISULTATI GARE",
    "RISULTATI Domenica",
]

class Command(BaseCommand):
    help = 'Update a Race instance with results from data obtained via a GET request to an Event URL'
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
            raise Exception("No table found")
        else:
            program_link = self.search_race_program(table)
        if program_link is None:
            raise Exception("No program link found")
        print(BASE_URL + program_link)
        soup = self.request_page(BASE_URL + program_link)
        self.scrape_race_results(soup)
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
        for row in table.find_all('tr'):
            if len(row.contents) < 4:
                continue
            if row.find_all('td')[1].string.strip() in RISULTATI_EXPRESSIONS:
                link = row.find('a').get('href')
                self.stdout.write(f"Found the RACE PROGRAM link: {link}")
                return link
        # If pass through the loop without finding the link
        self.stdout.write(self.style.WARNING("Race program not found."))
        return None

    @staticmethod
    def take_boat_info(info):
        categories = [
            'master',
            'senior',
            'under',
            'junior',
            'ragazzi',
            'cadetti',
            'allievi',
            'esordienti',
            'pr3',
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

    def format_race_info(self, info):
        race_number = info[2].strip()
        race_time = info[7].strip().replace('\xa0', '')
        race_boat, category, sex = self.take_boat_info(info[8].split('\xa0')[0].strip())
        return {
            'number': race_number,
            'time': race_time,
            'boat_type': race_boat,
            'category': category,
            'gender': sex,
            'type': info[8].split('\xa0')[-1].strip(),
            'event': self.event,
        }

    def find_race(self, race_infos):
        """Connect to the instance of the race in the database"""
        # Take the header of the race (in parent table)
        infos = list(race_infos.stripped_strings)
        race_number = infos[1]
        print(race_number)
        # Get the Race object with this number
        try:
            race_instance = Race.objects.get(event=self.event, number=race_number)
        except Race.DoesNotExist:
            race_instance = None
            print("Given Race not found")
        return race_instance

    @staticmethod
    def normalize_athletes_names(athlete):
        athlete = unicodedata.normalize('NFKC', athlete)
        athlete = athlete.replace("-Tim.", "").strip()
        return athlete.title()

    def get_athletes(self, crew):
        athletes = []
        for at in crew.stripped_strings:
            if at.strip(' .') != '' and '(' not in at and '**' not in at:
                athlete = self.normalize_athletes_names(at)
                try:
                    athlete_object = Athlete.objects.get(name=athlete)
                except Athlete.DoesNotExist:
                    self.stderr.write(f"Athlete {athlete} not found in the database")
                    return []
                print(athlete)
                athletes.append(athlete_object)
        print(athletes)
        return athletes

    def update_crew(self, result, race):
        if len(result.find_all('font')) == 0:
            # This is a void table element without crews
            return None
        # Extract infos from the table data
        position, time, _, crew = result.find_all('font', recursive=False)
        athletes = self.get_athletes(crew)
        # Filter out the Crew model instance
        crew_instance = Crew.objects.filter(race=race, athletes__in=athletes).distinct()
        if not crew_instance.exists():
            self.stderr.write(self.style.ERROR(f"Crew with athletes {athletes} not found in the database"))
            return None
        elif crew_instance.count() > 1:
            self.stderr.write(self.style.ERROR(f"Multiple Crews found with athletes {athletes}"))
            return None
        else:
            crew_instance = crew_instance.first()
        crew_instance.result = position.text.strip().split(' ')[0]
        crew_instance.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated crew "{crew_instance}" with result {position.text.strip()}'))
        return None

    def make_crews_results(self, results, race):
        for result in results.find_all('td'):
            self.update_crew(result, race)
        return None

    def scrape_race_results(self, soup):
        divs = [div for div in soup.find_all('div') if div.find_all('table')]
        for div in divs:
            race_infos, results = div.find_all('table')[-2:]
            race = self.find_race(race_infos)
            if race is not None:
                self.make_crews_results(results, race)
        return None
