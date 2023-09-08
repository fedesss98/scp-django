"""
Created by Federico Amato
Get race program,
then get Athletes names from race program and save it in a json file
"""
import logging
from datetime import datetime

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import lxml
import json
import unicodedata

from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

URL = 'https://canottaggioservice.canottaggio.net/dati/prx231301.html'
BASE_URL = 'https://canottaggioservice.canottaggio.net/'


class Event:
    def __init__(self, url):
        self.url = url
        self.soup = self.request_page()

        self._program_url = None
        self._results_url = None
        self._event_name = None
        self._event_date = None

    def request_page(self):
        headers = {
            'User-Agent': 'fantapoma',
        }
        # Take the webpage
        page = requests.get(self.url, headers=headers)
        return BeautifulSoup(page.text, 'html.parser')

    @staticmethod
    def find_event_info(soup):
        # Top section with Event info
        section = soup.find('td', class_='centercoltext')
        return section.find_all('tr')[3].string

    @property
    def event_name(self):
        name_and_date = self.find_event_info(self.soup)
        self._event_name = name_and_date.split(' - ')[0].strip()
        return self._event_name

    @property
    def event_date(self):
        name_and_date = self.find_event_info(self.soup)
        self._event_date = name_and_date.split(' - ')[1].strip().replace('/', '-')
        return self._event_date

    @staticmethod
    def find_event_links(soup):
        # The section "Documenti della regata" is a div class 'box'
        section_links = soup.find('div', class_='box')
        return section_links.find_all('tr')

    @property
    def program_url(self):
        rows = self.find_event_links(self.soup)
        for row in rows:
            if link := row.find('a'):
                if row.find_all('td')[1].text == "PROGRAMMA GARE":
                    self._program_url = link.get('href')
        return BASE_URL + self._program_url

    @property
    def results_url(self):
        rows = self.find_event_links(self.soup)
        for row in rows:
            if link := row.find('a'):
                text = row.find_all('td')[1].text
                if text in ["RISULTATI FINALI", "RISULTATI GARE"]:
                    self._results_url = link.get('href')
        return BASE_URL + self._results_url


class ProgramExtractor:
    def __init__(self, event: Event):
        self.event_name = event.event_name
        self.event_date = event.event_date
        self.url = event.program_url
        self.soup = self.request_race()

        self.race_plan = pd.DataFrame()
        self.race_infos_index = {}
        self.registered_athletes = None

        # Extract program
        self.make_race_plan()

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
            'Numero Gara': race_number,
            'Orario': race_time,
            'Specialità': race_boat,
            'Categoria': category,
            'Sesso': sex,
            'Tipo Gara': info[8].split('\xa0')[-1].strip(),
        }

    def get_all_clubs(self):
        # Clubs names are the only with css class "font-weight: bolder"
        html_socs = self.soup.find_all("font", attrs={'style': 'font-weight:bolder;'})
        return np.unique(np.array([soc.string.split('(')[0] for soc in html_socs]))

    def make_race_infos(self, table):
        # Take the header of the race (in parent table)
        race_info_table = table.parent.previous_sibling.previous_sibling.find('td', class_='t3')
        race_infos = list(race_info_table.strings)
        # Make a dictionary from the race header with info of the race
        race_infos = self.format_race_info(race_infos)
        return race_infos["Numero Gara"], race_infos

    @staticmethod
    def normalize_athletes_names(athlete):
        athlete = unicodedata.normalize('NFKC', athlete)
        athlete = athlete.replace("-Tim.", "").strip()
        return athlete.title()

    def make_race_crew(self, soc):
        bow_number = int(soc.parent.b.string.strip())
        soc_name = soc.string.split('(')[0]
        # Same crew number
        crew_number = soc.string.split('(')[1].strip(' )')
        athletes = [self.normalize_athletes_names(at) for at in soc.next_sibling.stripped_strings
                    if at.strip(' .') != ''
                    and '(' not in at]
        return bow_number, soc_name, athletes

    def make_race(self, table_socs):
        # Initialize dictionary of the race crews
        race = {}
        bow_numbers = []
        for soc in table_socs:
            bow_number, soc_name, athletes = self.make_race_crew(soc)
            bow_numbers.append(bow_number)
            # Dictionary entries are labeled with club name and crew number
            race[(bow_number, soc_name)] = athletes
        # Add empty lanes
        for i in range(1, 9):
            if i not in bow_numbers:
                race[(i, None)] = [np.nan for _ in athletes]
        return pd.DataFrame(race)

    def make_race_plan(self):
        # The race plan will be a dictionary with race DataFrames labeled by race number
        race_plan = {}
        # This dictionary will label race infos by race number
        race_infos_index = pd.DataFrame()

        for table in self.soup.find_all('tr'):
            # We are only interested in tables where there are club's names
            table_socs = table.find_all("font", attrs={'style': 'font-weight:bolder;'})
            if len(table_socs) > 0:
                # That's a race table and there are entries
                race_number, race_infos = self.make_race_infos(table)
                race = self.make_race(table_socs)
                # Use the race number to label each race
                race_plan[race_number] = race
                race_infos_index = pd.concat([race_infos_index, pd.DataFrame(race_infos, index=[race_number])])
        self.race_plan = pd.concat(race_plan.values(), axis=0, keys=race_plan.keys())
        self.race_infos_index = race_infos_index
        return self.race_plan, self.race_infos_index

    def request_race(self):
        headers = {
            'User-Agent': 'fantapoma',
        }
        # Take the webpage
        program = requests.get(self.url, headers=headers)
        return BeautifulSoup(program.text, 'html.parser')

    def get_clubs_athletes(self):
        clubs_groups = self.race_plan.groupby(axis=1, level=1)
        self.registered_athletes = {club: list(crews.melt().dropna().value.unique()) for club, crews in clubs_groups}
        return self.registered_athletes

    def save_race_plan(self):
        filepath = ROOT_DIR / f'data/program_{"_".join(self.event_date.split("-"))}.csv'
        self.race_plan.to_csv(filepath, sep=';')

    def save_registered_athletes(self):
        if self.registered_athletes is None:
            self.registered_athletes = self.get_clubs_athletes()
        filepath = ROOT_DIR / f'data/names/registered_athletes_{"_".join(self.event_date.split("-"))}.json'
        # Create file if it does not exist
        filepath.touch()
        with filepath.open(mode="w") as f:
            json.dump(self.registered_athletes, f)


if __name__ == '__main__':
    event_date = '2023-03-04'
    url = 'https://canottaggioservice.canottaggio.net/menu_reg.php?reg=231301&&k1=R'

    event = Event(url=url)
    print(event.event_name)
    print(event.event_date)
    event_program = ProgramExtractor(event)
    # Save race plan
    event_program.save_race_plan()
    # Save registered athletes
    event_program.save_registered_athletes()


