from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from scripts.theme_park_helpers import run_get_data, calculate_schedule_from_datetime, run_backup_dataset

config = Variable.get('extract_config', deserialize_json=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 25, 21, 0),
    'tags':['CORE', 'USER'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="extract_theme_park_api_dag",
         default_args=default_args,
         schedule=calculate_schedule_from_datetime(datetime.now())) as dag:

    extract_park = PythonOperator(
        task_id='get_data_task',
        python_callable=run_get_data,
        op_kwargs={'config_track':config.get('tracking_parks'),
                    'datetime': datetime.now()
                    },
        provide_context=True,
        dag=dag
    )

    compress_and_backup_dataset = PythonOperator(
        task_id='compress_and_backup_dataset',
        python_callable=run_backup_dataset,
        provide_context=True,
        dag=dag
    )
    # Set dependencies between tasks
    extract_park >> compress_and_backup_dataset