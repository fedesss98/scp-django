"""
Created by Federico Amato
Save athletes codes and names in /codes folder
codes = np.load('/codes/codici_canottaggioservice.npy')
names = np.load('/codes/nomi_canottaggioservice.npy')
"""
import numpy as np
import requests
from bs4 import BeautifulSoup


def get_names(headers):
    names_urls = [
        'https://canottaggioservice.canottaggio.net/cerca22.php',
        # 'https://canottaggioservice.canottaggio.net/cerca23.php',
        # 'https://canottaggioservice.canottaggio.net/cerca24.php',
        # 'https://canottaggioservice.canottaggio.net/cerca25.php',
    ]
    codes = []
    names = []
    for names_url in names_urls:
        r_names = requests.get(names_url, headers=headers)

        soup = BeautifulSoup(r_names.text, 'html.parser')

        codes.extend([li.text for li in soup.find_all('li')])
        names.extend([name[1].strip() for name in np.char.split(codes, sep='-')])

    codes = np.array(codes)
    names = np.array(names)
    np.save('codes/codici_canottaggioservice', codes)
    np.save('codes/nomi_canottaggioservice', names)

    return codes


if __name__ == '__main__':
    headers = {
        'User-Agent': 'fantapoma',
    }
    get_names(headers)
