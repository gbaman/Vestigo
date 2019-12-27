from CO2Meter import *
import time
import requests

base_url = "http://10.0.12.70:5000"

sensor = CO2Meter("/dev/hidraw0")
while True:
    time.sleep(10)
    data = sensor.get_data()
    if 'co2' in data:
        requests.get(f"{base_url}/upload_data_live/ac9d8f74-d8b0-40a1-a1a1-0587d7aac624/co2/{data['co2']}")
    if 'temperature' in data:
        requests.get(f"{base_url}:5000/upload_data_live/ac9d8f74-d8b0-40a1-a1a1-0587d7aac624/temperature/{data['temperature']}")