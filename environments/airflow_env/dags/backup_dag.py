from glob import glob
from datetime import datetime, timedelta

from pathlib import Path
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

config = Variable.get('extract_config', deserialize_json=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 27, 1, 0),
    'tags':['CORE', 'USER'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

BKP_PATH = str(Path(__file__).absolute()).rpartition('/')[0] + '/dataset_backup/'

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="backup_data_dag",
         default_args=default_args,
         schedule='3 2 * * *') as dag:
    
    start = DummyOperator(task_id='start_workflow')
    end = DummyOperator(task_id='end_workflow')

    create_new_dir = BashOperator(
            task_id=f'create_new_dir',
            bash_command=f'ls /opt/***/; mkdir -p -v "{BKP_PATH}date=$date_template"',
            env={'date_template': '{{ yesterday_ds }}'},
            dag=dag
        )


    for file in glob(BKP_PATH+'*.json.gz'):

        filename_w_ext = file.rpartition('/')[-1]
        filename_wo_ext = filename_w_ext.partition('.')[0]

        move_backup_to_partition = BashOperator(
            task_id=f'move_backup_{filename_wo_ext}',
            bash_command=f'mv {file} "{BKP_PATH}date=$date_template/{filename_w_ext}"',
            env={'date_template': '{{ yesterday_ds }}'},
            dag=dag
        )

        # Set dependencies between tasks
        start >> create_new_dir >> move_backup_to_partition >> end