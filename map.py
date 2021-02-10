import os

import requests
from find_spn import find_s

import os

import pygame
import pygame_gui
import pyglet

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

type = "map"

def load_map(spn):
    print(spn)
    map_params = {
        "ll": f"{ll[0]},{ll[1]}",
        "spn": f"{spn[0]},{spn[1]}",
        "l": type,
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
screen = pygame.display.set_mode((800, 450))
screen.fill((245, 245, 220))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

manager = pygame_gui.UIManager((800, 450))

clock = pygame.time.Clock()

sat = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (650, 30), (100, 50)),
    text='Set sat',
    manager=manager
)

mapp = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (650, 100), (100, 50)),
    text='Set map',
    manager=manager
)

gbr = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (650, 170), (100, 50)
    ),
    text="hybrid",
    manager=manager
)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == sat:
                    type = "sat"
                    load_map(spn)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                if event.ui_element == mapp:
                    type = "map"
                    load_map(spn)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.ui_element == gbr:
                    type = "sat,skl"
                    load_map(spn)
                    screen.blit(pygame.image.load(map_file), (0, 0))
        if pygame.key.get_pressed()[pygame.K_q]:
            if spn[0] - 1 >= 0:
                spn[0] = spn[0] - 1
            if spn[1] - 1 >= 0:
                spn[1] = spn[1] - 1
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        elif pygame.key.get_pressed()[pygame.K_z]:
            spn = [spn[0] + 1, spn[1] + 1]
            if spn[0] > 180:
                spn[0] = 179
            if spn[1] > 90:
                spn[1] = 89
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        if pygame.key.get_pressed()[pygame.K_d]:
            delta = spn[0] / 2
            ll = [float(ll[0]) + delta, ll[1]]
            if ll[0] > 180:
                ll[0] = -(ll[0] % 180)
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        elif pygame.key.get_pressed()[pygame.K_a]:
            delta = spn[0] / 2
            ll = [float(ll[0]) - delta, ll[1]]
            if ll[0] < -180:
                ll[0] = ll[0] % 180
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        elif pygame.key.get_pressed()[pygame.K_w]:
            delta = spn[1] / 2
            ll[1] = float(ll[1]) + delta
            if ll[1] > 90:
                ll[1] = -(ll[1] % 90)
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        elif pygame.key.get_pressed()[pygame.K_s]:
            delta = spn[1] / 2
            ll[1] = float(ll[1]) - delta
            if ll[1] < -90:
                ll[1] = -85
            load_map(spn)
            screen.blit(pygame.image.load(map_file), (0, 0))
        manager.process_events(event)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()
os.remove(map_file)
