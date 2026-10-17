from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

def run_pipeline():
    import subprocess
    subprocess.run(['python', 'main.py'], check=True, cwd=os.environ.get('AIRFLOW_HOME', os.getcwd()))

default_args = {
    'owner': 'dataquality',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='data_quality_pipeline',
    default_args=default_args,
    description='AI Data Quality & Anomaly Detection Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['dataquality'],
) as dag:
    pipeline_task = PythonOperator(
        task_id='run_full_pipeline',
        python_callable=run_pipeline,
    )
    pipeline_task
