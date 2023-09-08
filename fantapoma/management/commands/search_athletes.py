"""
Created by Federico Amato
Get Athletes data from canottaggioservice.canottaggio.net
using their names
"""
import json
import logging
from datetime import datetime

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import lxml

logging.basicConfig(filename='search_athletes.log',
                    level=logging.INFO)

SICILIAN_SOCIETIES = [
    'PALERMO SC', 'S.C. PALERMO', 'S.CAN.PALERMO',
    'LAURIA CCR', 'CLUB CANOTTIERI "ROGGERO DI LAURIA"',
    'CUS PALERMO',
    'TELIMAR',
    'PELORO CC', 'PELORO CIR.CAN.', 'PELOROROW'
]


def request_curriculum(code):
    # Richiede un curriculum
    curriculum_url = 'https://canottaggioservice.canottaggio.net/print_cur_atl.php'
    data = {
        'squadra': code,
    }
    headers = {
        'User-Agent': 'fantapoma',
    }
    r_curric = requests.post(curriculum_url, data=data, headers=headers)
    return r_curric.text


def make_curriculum_dataframe(curriculum, name, dob):
    df = pd.read_html(
        curriculum,
        attrs={'class': 'rightcoltext'},
        skiprows=1,
        flavor='lxml',
    )
    if len(df) == 0:
        raise Exception("No entry in canottaggioservice.net")
    df = df[0]
    df = df.iloc[:, [1, 2, 3, 5, 6, 7, 8, 9]].dropna(how='all')
    df.columns = ['Data', 'Località', 'Manifestazione', 'Posizione', 'Tempo', 'Barca', 'Categoria', 'Società']
    df[['Data', 'Località', 'Manifestazione']] = df[['Data', 'Località', 'Manifestazione']].fillna(
        method='ffill',
    )
    df['Posizione'] = df['Posizione'].fillna('Non Pervenuto')
    df['Atleta'] = name
    df['Data di Nascita'] = dob
    return df


def save_curriculum(df, name):
    filename = '_'.join(name.replace("'", "-").split()).lower()
    df.to_csv(f'curricula/{filename}.csv', sep=";")
    return None


if __name__ == '__main__':
    logging.info(f"\n[{datetime.now()}] "
                 f"Starting search for athletes in canottaggioservice.canottaggio.net\n")

    fic_names = np.load('codes/nomi_canottaggioservice.npy')
    fic_codes = np.load('codes/codici_canottaggioservice.npy')

    NAME_DATABASE = 'data/names/registered_athletes.json'

    with open('data/names/registered_athletes.json', 'r') as fp:
        soc_athletes = json.load(fp)
    for society in soc_athletes.keys():
        # Remove numbers from society name
        soc = society.strip('0123456789')
        for name in soc_athletes[society]:
            print(name)
            # Find the FIC code for the name.
            # Function find returns -1 for indices where the string 'name' is not found
            name_filter = np.char.find(fic_codes, name.upper())
            code = fic_codes[name_filter != -1]
            # The name could be linked to more than one code,
            # so iterate over them
            for c in code:
                # Take the date of birth from the FIC code
                dob = c.split(' - ')[-1]
                athlete = name + ' ' + dob
                logging.info(athlete)
                curriculum = request_curriculum(c)
                try:
                    curriculum = make_curriculum_dataframe(curriculum, name, dob)
                except Exception as e:
                    logging.warning(f"{c}: {e}")
                else:
                    if any(curriculum['Società'].isin(SICILIAN_SOCIETIES)):
                        logging.info('-- Save')
                        print(' --Save')
                        save_curriculum(curriculum, athlete)
                    else:
                        logging.warning(f"{c} did not row for sicilian societies")
