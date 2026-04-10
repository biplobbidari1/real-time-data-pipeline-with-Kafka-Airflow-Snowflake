from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from consumer import run_kafka_batch

default_args = {
    'owner': 'elite',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': False,
    'email_on_retry': False
}

with DAG(
    dag_id="elite_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",  # every 5 min
    catchup=False,
    default_args=default_args,
    tags=["kafka", "snowflake", "etl"]   # to display in  UI
) as dag:

    start = PythonOperator(
        task_id="start",
        python_callable=lambda: print("🚀 Pipeline started")
    )

    consumer_etl = PythonOperator(
        task_id="consume_kafka_and_load_snowflake",
        python_callable=run_kafka_batch,
        execution_timeout=timedelta(minutes=2)  # to prevent long runs
    )

    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("Pipeline completed")
    )

    start >> consumer_etl >> end