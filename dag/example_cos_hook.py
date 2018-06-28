from airflow.contrib.hooks.cos_hook import CloudObjectStorageHook
from airflow.utils.decorators import apply_defaults
import airflow
from airflow.models import DAG
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'roc',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    dag_id='example_cos_hook',
    schedule_interval=timedelta(days=1),
    start_date=airflow.utils.dates.days_ago(2),
    default_args=args)

def put(**kwargs):
    hook = CloudObjectStorageHook(cos_conn_id='cos_default')
    hook.put("what the hell???", "test-cos", "airflow")
    print("data put")

def get(**kwargs):
    hook = CloudObjectStorageHook(cos_conn_id='cos_default')
    print(hook.get("test-cos", "airflow"))

put_cos = PythonOperator(
    task_id='put_cos', dag=dag, python_callable=put)

get_cos = PythonOperator(
    task_id='get_cos', dag=dag, python_callable=get)

get_cos.set_upstream(put_cos)