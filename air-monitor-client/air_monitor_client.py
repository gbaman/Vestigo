from CO2Meter import *
import time
import requests

from config import node_key, base_url

DELAY_TIME = 120

sensor = CO2Meter("/dev/hidraw0")
time.sleep(1)

while True:
    data = sensor.get_data()
    try:
        if 'co2' in data:
            requests.get(f"{base_url}/upload_data_live/{node_key}/co2/{data['co2']}")
            print(f"Data sent to server for co2 of {data['co2']}")
            time.sleep(0.2)
        if 'temperature' in data:
            requests.get(f"{base_url}/upload_data_live/{node_key}/temperature/{data['temperature']}")
            print(f"Data sent to server for temperature of {data['temperature']}")
    except requests.RequestException as e:
        print(f"Unable to connect, waiting for {DELAY_TIME} seconds...")
        print(e)

    time.sleep(DELAY_TIME)