from io import BytesIO
import requests
from PIL import Image
import os
hospitals = ["Лиски, ул. Сеченова, 24", "Воронеж, ул. Красноармейская, 19", "Воронеж, ул. Героев Сибиряков, 37"]
coord_list, pt_list = [], []


def search(adress):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": adress,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    coord_list.append(response)


for hospital in hospitals:
    search(hospital)


def show(response):
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    pt_list.append("{},{},pm2rdm".format(toponym_longitude, toponym_lattitude))


for response in coord_list:
    show(response)

map_params = {
    "l": "map",
    "pt": "~".join(pt_list)
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

os.chdir('..')
os.chdir('static\img')
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
