import requests
import os
import json
from pathlib import Path
from datetime import datetime

DISNEY_PARK_LIVE_API = 'https://api.themeparks.wiki/v1/entity/{park_id}/live'
JSON_FILE_PATH = str(Path(__file__).absolute()).rpartition('/')[0].rpartition('/')[0] + '/dataset/park_{name}.json'

def get_disney_park_data(park_id, park_name):
    req = requests.get(DISNEY_PARK_LIVE_API.format(park_id=park_id))

    json_filename = JSON_FILE_PATH.format(name=park_name)

    print(json_filename)

    if not req.status_code == 200:
        raise Exception(f"There's was a problem when calling API! HTTP status code = {req.status_code}")
    else:
        data = req.json()
        data['extracted_at'] = int(datetime.now().timestamp())
        print(data)

    with open(json_filename, 'a') as f:
        json.dump(data, f)
        f.write('\n')

def run_get_data(config_track, datetime):
    print("Initializing Job!")
    print(datetime)
    calculate_schedule_from_datetime(datetime)
    for park, id_park in config_track.items():
        get_disney_park_data(park_id=id_park, park_name=park.lower().replace(' ', '_'))

def calculate_schedule_from_datetime(current_datetime: datetime):
    ho, mi = current_datetime.hour, current_datetime.minute
    print(f'Current time [UTC]: {ho:02}h{mi:02}')
    if not 1 < ho < 12:
        return "*/5 * * * *"
    else:
        return "0 */2 * * *"