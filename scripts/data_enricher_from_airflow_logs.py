from glob import glob
import json
from datetime import datetime
import re
import ast
import gzip
import shutil

def get_diff(timestamp):
    pass

def extract_dt_metadata(metadata):
    match = re.search(r'\[.*\]', metadata)
    return datetime.fromisoformat(match.group()[1:-1])

def get_int_timestamp(dt: datetime):
    return int(dt.timestamp())

def get_datetime(timestamp):
    print(timestamp)
    return datetime.fromtimestamp(timestamp)


def data_enricher_recovery():
    # MAIN_PATH = '../../cluster_airflow/logs/dag_id=extract_theme_park_api_data/*/*/*.log'
    MAIN_PATH = '../../cluster_airflow/logs/dag_id=extract_theme_park_api_dag/*/*/*.log'

    print(MAIN_PATH)
    for file in glob(MAIN_PATH):
        print(f'Processing file: {file}')
        with open(file, 'r') as f:
            for idx, line in enumerate(f.readlines()):
                metadata, _, json_str = line.partition('INFO - ')
                print(idx, metadata, json_str[:100])
                if json_str[:2] == "{'":
                    # payload = json.loads(json_str)
                    payload = ast.literal_eval(json_str)
                    extracted_at_generated = get_int_timestamp(extract_dt_metadata(metadata))
                    if not payload.get('extracted_at'):
                        payload['extracted_at'] = extracted_at_generated
                        file_name_gen = last_line.rpartition('/')[-1].strip()
                        with open('./recovered/'+file_name_gen, 'a') as g:
                            json.dump(payload, g)
                            g.write('\n')
                else:
                    last_line = json_str

def data_concat():
    MAIN_PATH = '../../cluster_airflow/dags/dataset/*.json'

    print(MAIN_PATH)
    for file in glob(MAIN_PATH):
        print(f'Processing file: {file}')
        with open(file, 'r') as f:
            for line in f.readlines():
                payload = json.loads(line)
                file_name_gen = file.rpartition('/')[-1].strip()
                with open('./recovered/'+file_name_gen, 'a') as g:
                    json.dump(payload, g)
                    g.write('\n')

def move_gzip():
    MAIN_PATH = '../../cluster_airflow/dags/dataset/*.json'

    print(MAIN_PATH)
    for file in glob(MAIN_PATH):
        print(f'Processing file: {file}')
        with open(file, 'rb') as f_in:
            file_name_gen = file.rpartition('/')[-1].strip()
            with gzip.open('./recovered/'+file_name_gen+'.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


if __name__ == '__main__':

    # data_enricher_recovery()
    move_gzip()