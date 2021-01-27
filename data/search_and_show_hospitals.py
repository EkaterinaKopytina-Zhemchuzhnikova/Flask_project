import requests


def search(adresses):
    pt_list = []
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    for adress in adresses:
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": adress,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        pt_list.append("{},{},pm2rdm".format(toponym_longitude, toponym_lattitude))
    return pt_list


def show(pt_list, scale='0.002,0.002'):
    map_params = {
        "spn": scale,
        "l": "map",
        "pt": "~".join(pt_list)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response
