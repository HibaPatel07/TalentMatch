from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'talentmatch',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'talentmatch_core_pipeline',
    default_args=default_args,
    description='Automated ML pipeline for Resume-Job matching',
    schedule_interval=None, 
    catchup=False,
) as dag:

    preprocess_data = BashOperator(
        task_id='preprocess_data',
        bash_command='python /app/src/preprocessing/preprocess.py' 
    )

    generate_embeddings = BashOperator(
        task_id='generate_embeddings',
        bash_command='python /app/scripts/generate_embeddings.py'
    )

    generate_match_features = BashOperator(
        task_id='generate_match_features',
        bash_command='python /app/scripts/generate_match_scores.py'
    )

    evaluate_model = BashOperator(
        task_id='evaluate_model',
        bash_command='python /app/src/evaluation/evaluate_model.py'
    )

    register_model = BashOperator(
        task_id='register_model',
        bash_command='python /app/scripts/register_model.py'
    )

    # The pipeline order
    preprocess_data >> generate_embeddings >> generate_match_features >> evaluate_model >> register_model