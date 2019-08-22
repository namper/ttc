import requests
from settings import *
import geocoder


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


def closest_stop(stop_data: list):
    # error is too high for this task
    me = geocoder.ip('me')
    location = (me.lon, me.lat)

    stop_data = [{'name': i['Name'], 'location': (i['Lon'], i['Lat'])} for i in stop_data]
    base = stop_data[0]
    to = generate_distance_url(location, base['location'])
    minimal = [base, max(requests.get(to).json()['durations'][0])]
    for _stop in stop_data:
        destination = _stop['location']
        to = generate_distance_url(location, destination, 'driving')
        duration = max(requests.get(to).json()['durations'][0])
        if minimal[1] > duration:
            minimal = [_stop, duration]
    return minimal


if __name__ == '__main__':
    stops = requests.get(STOP_URLS[0]).json().get('Stops', '') + requests.get(STOP_URLS[1]).json().get('Stops', '')
    # stop, dur = closest_stop(stops)
    # print(f'უახლოესი გაჩერება {stop["name"]} საჭიროა დაახლოებით: {round(dur / 60, 2)} წუთი')
    live_bus(stops)
