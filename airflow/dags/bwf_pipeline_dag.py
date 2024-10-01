from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess
import os

# Define the path to your project root
PROJECT_ROOT = os.getenv('BWF_PROJECT_ROOT', '/opt/airflow/BWF-PredictionSystem')
print(f"Using PROJECT_ROOT: {PROJECT_ROOT}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'bwf_pipeline_dev',
    default_args=default_args,
    description='BWF data pipeline for development',
    schedule_interval='@monthly',  # Run monthly
    catchup=False
)

def run_python_script(script_path):
    def run_script(**kwargs):
        full_path = os.path.join(PROJECT_ROOT, script_path)
        print(f"Attempting to run script at: {full_path}")
        result = subprocess.run(['python', full_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Script failed with error: {result.stderr}")
        print(result.stdout)
    return run_script

# Create tasks for each scraper
scraper_tasks = []
scraper_scripts = [
    'src/scraper/ranking_week.py'
]

for script in scraper_scripts:
    task = PythonOperator(
        task_id=f"run_{os.path.basename(script).replace('.py', '')}",
        python_callable=run_python_script(script),
        dag=dag
    )
    scraper_tasks.append(task)

# Create task for S3 uploader
s3_upload_task = PythonOperator(
    task_id='upload_to_s3',
    python_callable=run_python_script('aws/s3_uploader.py'),
    dag=dag
)

# Set up task dependencies
for task in scraper_tasks:
    task >> s3_upload_task