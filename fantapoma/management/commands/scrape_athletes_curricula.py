"""
Take athletes name and confront them with canottaggioservice.net database entries.
Retrieve race curricula of every athlete.
"""
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


class AthleteCurriculum:
    def __init__(self, code, name, dob):
        self.code = code
        self.name = name
        self.dob = dob
        self.soup = self.request_curriculum()

        self.curriculum = self.make_curriculum

    def request_curriculum(self):
        # Richiede un curriculum
        curriculum_url = 'https://canottaggioservice.canottaggio.net/print_cur_atl.php'
        data = {
            'squadra': self.code,
        }
        headers = {
            'User-Agent': 'fantapoma',
        }
        r_curric = requests.post(curriculum_url, data=data, headers=headers)
        return r_curric.text

    def make_curriculum(self):
        df = pd.read_html(
            self.soup,
            attrs={'class': 'rightcoltext'},
            skiprows=1,
            flavor='lxml',
        )
        if len(df) == 0:
            raise Exception("No entry in canottaggioservice.net")
        else:
            df = df[0]
            df = df.iloc[:, [1, 2, 3, 5, 6, 7, 8, 9]].dropna(how='all')
            df.columns = ['Data', 'Località', 'Manifestazione', 'Posizione', 'Tempo', 'Barca', 'Categoria', 'Società']
            df[['Data', 'Località', 'Manifestazione']] = df[['Data', 'Località', 'Manifestazione']].fillna(
                method='ffill',
            )
            df['Posizione'] = df['Posizione'].fillna('Non Pervenuto')
            df['Atleta'] = self.name
            df['Data di Nascita'] = self.dob
        self.curriculum = df
        return self.curriculum


def retrieve_code_from_name(name):
    pass
