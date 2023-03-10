import qrcode
import os

from settings import BASE_DIR

url = "https://goscp.it/fantapoma/statistics/"
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

directory = BASE_DIR / 'goscp/static/img/qr/'
if not os.path.exists(directory):
    os.makedirs(directory)

filename = 'best_athlete_20230304.png'
filepath = os.path.join(directory, filename)
img.save(filepath)