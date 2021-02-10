import os

import pygame
import requests
from find_spn import find_s

x, y = map(float, input().split())

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": f"{x},{y}",
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('Тут что то неправильно:(')
    exit(0)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

ll, spn = find_s(json_response)

print(spn)
map_file = "map.png"

org_point = "{0},{1}".format(ll[0], ll[1])


def load_map(spn):
    print(spn)
    map_params = {
        "ll": f"{ll[0]},{ll[1]}",
        "spn": f"{spn[0]},{spn[1]}",
        "l": "map",
        "pt": "{0},pm2dgl".format(org_point)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    with open(map_file, "wb") as file:
        file.write(response.content)
    file.close()
    return


load_map(spn)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if pygame.key.get_pressed()[pygame.K_q]:
            if spn[0] - 1 >= 0:
                spn[0] = spn[0] - 1
            if spn[1] - 1 >= 0:
                spn[1] = spn[1] - 1
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        elif pygame.key.get_pressed()[pygame.K_z]:
            spn = [spn[0] + 1, spn[1] + 1]
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_d]:
            delta = spn[0] / 2
            print(ll)
            ll = [float(ll[0]) + delta, ll[1]]
            print(ll)
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        # # elif pygame.key.get_pressed()[pygame.K_LEFT]:
        #     delta = spn[0] / 2
        #     ll = [float(ll[0]) - delta, ll[1]]
        #     load_map(spn)
        #     screen.blit(pygame.image.load(map_file), (0, 0))
        #     pygame.display.flip()
pygame.quit()
os.remove(map_file)
