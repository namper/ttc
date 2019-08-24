import requests
import subprocess
import re

DIRECTION = {
    0: 'არა მთავარი',
    1: 'მთავარი'
}


def formatter(sp: str, extend: int) -> int:
    sp = len(sp)
    if sp == 1:
        sp = 3
    elif sp == 3:
        sp = 1
    return sp + extend


def show_times(stop_id: int) -> None:
    r = requests.get(f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={stop_id}')
    r = r.json()['ArrivalTime']
    print('-' * 15 + 'ტაბლო' + '-' * 25)
    for bus in r:
        route_n, time = str(bus['RouteNumber']), str(bus['ArrivalTime'])
        print(f"{route_n}" + " " * formatter(route_n, 2) + f"{bus['ArrivalTime']} წუთი" + ' ' * formatter(
            time, 5) + f"{bus['DestinationStopName']}")


def live_bus(bus_id: int) -> None:
    _LIVE_URLS = [
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={bus_id}&forward=0',
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={bus_id}&forward=1'
    ]
    _STOP_URLS = [
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={bus_id}&forward=0',
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={bus_id}&forward=1'
    ]
    stop_data = requests.get(_STOP_URLS[0]).json().get('Stops', '') + requests.get(_STOP_URLS[1]).json().get('Stops',
                                                                                                             '')
    for url in _LIVE_URLS:
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


def generate_distance_url(current, destination, travel_by: str = 'walking',
                          token: str = 'sk.eyJ1IjoibmFtcGVyIiwiYSI6ImNqemxsMDR4djAzZDkzanBiMGNheGs4dHMifQ.VNRhf1JGDRPL-x0rry3Ngg') -> str:
    current = f'{current[0]},{current[1]}'
    destination = f'{destination[0]},{destination[1]}'
    return \
        f'https://api.mapbox.com/directions-matrix/v1/mapbox/{travel_by}/{current};{destination}?access_token={token}'


def closest_stop(location: tuple, stop_data: list, moving_type: str = 'walking') -> list:
    stop_data = [{'name': i['Name'], 'location': (i['Lon'], i['Lat']), 'id': i['StopId']} for i in stop_data]
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


def closest_stop_runner(bus_id: int) -> None:
    _LIVE_URLS = [
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={bus_id}&forward=0',
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={bus_id}&forward=1'
    ]
    _STOP_URLS = [
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={bus_id}&forward=0',
        f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={bus_id}&forward=1'
    ]
    stop_data = requests.get(_STOP_URLS[0]).json().get('Stops', '') + requests.get(_STOP_URLS[1]).json().get('Stops',
                                                                                                             '')
    result = subprocess.run(['../whereami'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    lat = re.search(r'(?<=Latitude: )([\d+\.]+)', result).group(0)
    lon = re.search(r'(?<=Longitude: )([\d+\.]+)', result).group(0)
    location = float(lon), float(lat)
    stop, dur = closest_stop(location, stop_data)
    print(f'უახლოესი გაჩერება {stop["name"]} საჭიროა დაახლოებით: {round(dur / 60, 2)} წუთი')
    print('')
    show_times(stop['id'])
