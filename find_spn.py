import json


def find_s(json_response):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = [toponym_longitude, toponym_lattitude]
    envelope = toponym['boundedBY']['Envelope']
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope['upperCorner'].split(" ")

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    span = f"{dx}, {dy}"
    return ll, span
