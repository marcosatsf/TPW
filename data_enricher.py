from glob import glob
import json
from datetime import datetime

def get_deff(timestamp):
    pass

def get_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

if __name__ == '__main__':
    for file in glob('./dataset/*.json'):
        print(f'Processing file: {file}')
        with open(file, 'r') as f:
            for idx, line in enumerate(f.readlines()):
                payload = json.loads(line)
                extracted_value = payload.get('extracted_at')
                print(f'Payload {idx}, ', end='')
                if extracted_value:
                    print(f'extracted_at value -> {get_datetime(extracted_value)}')
                else:
                    print('without extracted_at value...')
                