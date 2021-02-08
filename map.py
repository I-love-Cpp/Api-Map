import os

import pygame
import requests
from find_spn import find_s

x, y = map(float, input().split())

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "ll": f"{x},{y}",
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('Тут что то неправильно:(')
    exit(0)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

ll, spn = find_s(json_response)

point = ll.split(',')


def load_map(spn):
    org_point = "{0},{1}".format(point[0], point[1])
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "pt": "{0},pm2dgl".format(org_point)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


map_file = load_map(spn)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_PAGEUP]:
            spn = f"{int(spn.split(',')[0]) - 0.1},{int(spn.split(',')[1]) - 0.1}"
            load_map(spn)
        elif pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
            spn = f"{int(spn.split(',')[0]) + 0.1},{int(spn.split(',')[1]) + 0.1}"
            load_map(spn)
pygame.quit()
os.remove(map_file)
