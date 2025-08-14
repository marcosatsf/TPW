import time
import json
import sys
import os
from glob import glob
from datetime import datetime, timezone,timedelta
from scripts.theme_park_helpers import calculate_schedule_from_datetime, run_get_data
import threading

def execute_log_command(command):
    print(f'Executing command: {command}')
    os.system(command)

def compress_bkp_data(date):
    print(f'Compressing date={date} data')

    for file in glob('dataset/*.json'):
        filename_gz = file.rpartition('/')[-1] + '.gz'
        park_name = filename_gz.partition('.')[0]
        bkp_path = f'TPW_bkp/{park_name}/date={date}'
        print(f'Backing up on {bkp_path} path...')
        if not os.path.exists(f'../{bkp_path}/{filename_gz}'):
            execute_log_command(f'mkdir -p ../{bkp_path}')
            execute_log_command(f'gzip {file}')
            execute_log_command('mv "./dataset/{filename_gz}" "../{bkp_path}/{filename_gz}"'.format(bkp_path=bkp_path, filename_gz=filename_gz))
        else:
            print('Already compressed, skipping!')

if __name__ == "__main__":
    try:
        time_set = 60
        last_schedule = ''
        
        with open('extract_config.json','r') as f:
            config = json.load(f)
        while True:
            trigger_bkp = False
            datenow = datetime.now(timezone.utc)
            schedule_value = calculate_schedule_from_datetime(datenow)
            t_get_data = threading.Thread(target=run_get_data, args=(config.get('tracking_parks'),datenow,))
            if schedule_value != last_schedule:
                schedule_list = schedule_value.split(' ')
                for idx, value in enumerate(schedule_list[:2]):
                    multiplier = value.rpartition('/')[-1]
                    if multiplier != '*':
                        time_set = int(multiplier) * (60**(idx+1))
                    # If changing to next day, compress and save!
                    if time_set > 300:
                        trigger_bkp = True
                print(f"Schedule went from:{last_schedule}, to:{schedule_value}!")
                last_schedule = schedule_value
            original_stdout = sys.stdout
            t_waiting = threading.Thread(target=time.sleep, args=(time_set,))
            print(f'Spawning thread_task and waiting for {time_set} seconds...')
            sys.stdout = open('/dev/null', 'w')
            t_get_data.start()
            t_waiting.start()
            t_get_data.join()
            if trigger_bkp:
                sys.stdout = original_stdout
                compress_bkp_data((datetime.now(timezone.utc)-timedelta(days=1)).strftime('%Y-%m-%d'))
            t_waiting.join()
            if not trigger_bkp:
                sys.stdout = original_stdout
    except KeyboardInterrupt:
        sys.stdout = original_stdout
        print('Finishing...')
        #with CronTab(user=True) as cron:
        #    cron.remove_all()

