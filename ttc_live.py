import requests
import geocoder
from settings import *


def live_bus(stop_data: list) -> None:
    for url in LIVE_URLS:
        live_xml = requests.get(url)
        route_data = live_xml.json().get('bus', '')
        for route in route_data:
            live_stop_id = route['nextStopId']
            forwarding_integer = int(route['forward'])
            direction = DIRECTION[forwarding_integer]
            stop_name = ''
            for stop_item in stop_data:
                if live_stop_id == stop_item['StopId']:
                    stop_name = stop_item['Name']
                    break
            print(f'ადგილმდებარეობა: {stop_name}  მიმართულება: {direction}')
        print('')


def generate_distance_url(current, destination, travel_by: str = 'walking', token: str = secret_token) -> str:
    current = f'{current[0]},{current[1]}'
    destination = f'{destination[0]},{destination[1]}'
    return \
        f'https://api.mapbox.com/directions-matrix/v1/mapbox/{travel_by}/{current};{destination}?access_token={token}'


def closest_stop(location: tuple, stop_data: list, moving_type: str = 'walking') -> list:
    stop_data = [{'name': i['Name'], 'location': (i['Lon'], i['Lat'])} for i in stop_data]
    base = stop_data[0]
    to = generate_distance_url(location, base['location'])
    minimal = [base, requests.get(to).json()['durations'][0][1]]
    for _stop in stop_data:
        destination = _stop['location']
        to = generate_distance_url(location, destination, moving_type)
        duration = requests.get(to).json()['durations'][0][1]
        if minimal[1] > duration:
            minimal = [_stop, duration]
    return minimal
