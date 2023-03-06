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
from tqdm import tqdm
import lxml
import json

URL = 'https://canottaggioservice.canottaggio.net/dati/prx231301.html'


def request_race(url):
    headers = {
        'User-Agent': 'fantapoma',
    }
    program = requests.get(url, headers=headers)
    soup = BeautifulSoup(program.text, 'html.parser')
    race_plan = pd.DataFrame()

    html_socs = soup.find_all("font", attrs={'style': 'font-weight:bolder;'})
    societies = np.unique(np.array([soc.string.split('(')[0] for soc in html_socs]))

    for table in soup.find_all('tr'):
        table_socs = table.find_all("font", attrs={'style': 'font-weight:bolder;'})
        if len(table_socs) > 0:
            # That's a race table
            race_info_table = table.parent.previous_sibling.previous_sibling.find('td', class_='t3')
            race_info = [s for s in race_info_table.strings]
            race_info = {
                'Numero Gara': race_info[2].strip(),
                'Orario': race_info[7].strip().replace('\xa0', ''),
                'Specialità': race_info[8].split('\xa0')[0].strip(),
                'Tipo Gara': race_info[8].split('\xa0')[-1].strip()
            }
            race = dict()
            for soc in table_socs:
                soc_name = soc.string.split('(')[0]
                athletes = [at.strip() for at in soc.next_sibling.stripped_strings
                            if at.strip(' .') != ''
                            and '(' not in at]
                if race.get(soc_name) is not None:
                    # There are already boats for this society
                    soc_name = soc_name + str(len(race.get(soc_name)))
                race[soc_name] = athletes
            race.update(race_info)
            race = pd.DataFrame(race)
            race_plan = pd.concat([race_plan, race])
    return race_plan


if __name__ == '__main__':
    plan = request_race(URL)
    columns = ['Numero Gara', 'Orario', 'Specialità', 'Tipo Gara']
    societies = [col for col in plan.columns if col not in columns]
    columns.extend(societies)
    plan = plan[columns]
    plan.to_csv('data/program.csv', sep=';')

    registered_athletes = {soc: [ath for ath in plan[soc].dropna()] for soc in societies}
    json.dump(registered_athletes, 'data/names/registered_athletes.json')
