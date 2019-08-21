import requests
from settings import *
from pprint import pprint


def live_bus() -> None:
    stop_data = [requests.get(i).json().get('Stops', '') for i in STOP_URLS]

    for url in LIVE_URLS:
        live_xml = requests.get(url)
        route_data = live_xml.json().get('bus', '')
        for route in route_data:
            live_stop_id = route['nextStopId']
            forwarding_integer = int(route['forward'])
            direction = DIRECTION[forwarding_integer]
            current_stops = stop_data[forwarding_integer]
            stop_name = ''
            for stop_item in current_stops:
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


# @TODO(need fix)
def closest_stop():
    loc = requests.get('https://api.ipdata.co?api-key=test').json()
    location = (loc['latitude'], loc['longitude'])
    stop_data = requests.get(STOP_URLS[0]).json().get('Stops', '') + requests.get(STOP_URLS[1]).json().get('Stops', '')

    base = stop_data[0]
    to = generate_distance_url(location, (base['Lat'], base['Lon']))
    minimal = [base, max(requests.get(to).json()['durations'][0])]
    for stop in stop_data:
        destination = (stop['Lat'], stop['Lon'])
        to = generate_distance_url(location, destination)
        duration = max(requests.get(to).json()['durations'][0])
        if minimal[1] > duration:
            minimal = [stop, duration]
    pprint(minimal[0])


if __name__ == '__main__':
    closest_stop()
