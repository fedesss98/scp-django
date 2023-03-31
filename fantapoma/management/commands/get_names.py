"""
Created by Federico Amato
Save athletes codes and names in /codes folder
codes = np.load('/codes/codici_canottaggioservice.npy')
names = np.load('/codes/nomi_canottaggioservice.npy')
"""
import numpy as np
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent


class Command(BaseCommand):
    help = 'Scrape athletes registered in Canottaggioservice.net'
    headers = {
        'User-Agent': 'fantapoma',
    }

    def handle(self, *args, **options):
        names_url = 'https://canottaggioservice.canottaggio.net/cerca22.php'
        request_names = requests.get(names_url, headers=self.headers)

        soup = BeautifulSoup(request_names.text, 'html.parser')

        codes = [li.text for li in soup.find_all('li')]
        names = [name[1].strip() for name in np.char.split(codes, sep='-')]

        codes = np.array(codes)
        names = np.array(names)
        np.save(ROOT_DIR / 'data/codes/codici_canottaggioservice', codes)
        np.save(ROOT_DIR / 'data/codes/nomi_canottaggioservice', names)


# if __name__ == '__main__':
#     Command.handle()
