import math
import requests
from settings import STOP_URLS


# DOESN'T ACCOMMODATE ROUTES
def polar_distance(coord1: tuple, coord2: tuple) -> float:
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def shortest_stop() -> dict:
    loc = requests.get('https://api.ipdata.co?api-key=test').json()
    location = (loc['latitude'], loc['longitude'])
    stop_data = requests.get(STOP_URLS[0]).json().get('Stops', '')

    minimum = [stop_data, polar_distance(location, (stop_data['Lat'], stop_data['Lon']))]
    for stop in stop_data:
        distance = polar_distance(location, (stop['Lat'], stop['Lon']))
        if minimum[1] > distance:
            minimum = [stop, distance]
    return minimum[0]
