import requests
import subprocess
import re
from ttc_live import closest_stop, live_bus, show_times
from settings import STOP_URLS


def closest_stop_runner(stop_data: list) -> None:
    result = subprocess.run(['./whereami'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    lat = re.search(r'(?<=Latitude: )([\d+\.]+)', result).group(0)
    lon = re.search(r'(?<=Longitude: )([\d+\.]+)', result).group(0)
    location = float(lon), float(lat)
    stop, dur = closest_stop(location, stop_data)
    print(f'უახლოესი გაჩერება {stop["name"]} საჭიროა დაახლოებით: {round(dur / 60, 2)} წუთი')
    print('')
    show_times(stop['id'])


if __name__ == '__main__':
    stops = requests.get(STOP_URLS[0]).json().get('Stops', '') + requests.get(STOP_URLS[1]).json().get('Stops', '')
    live_bus(stops)
    closest_stop_runner(stops)