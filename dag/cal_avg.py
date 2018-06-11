from airflow.hooks.mysql_hook import MySqlHook
# from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import airflow
from airflow.models import DAG
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator

# CREATE TABLE user (
  # `id` int(11) NOT NULL AUTO_INCREMENT,
  # `name` varchar(32) NOT NULL,
  # `age` int(11) NOT NULL,
  # `creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  # PRIMARY KEY (`id`),
  # UNIQUE KEY `name` (`name`)
# );

# CREATE TABLE tongji (
  # `id` int(11) NOT NULL AUTO_INCREMENT,
  # `average_age` int(11) NOT NULL,
  # `creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  # PRIMARY KEY (`id`)
# );

args = {
    'owner': 'roc',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    dag_id='cal_average_age',
    schedule_interval=timedelta(days=1),
    start_date=airflow.utils.dates.days_ago(2),
    default_args=args)

def cal_avg(**kwargs):
    # pushes an XCom without a specific target
    hook = MySqlHook(mysql_conn_id='mysql_default', schema='test')

    age = hook.get_first('select round(avg(age),0) from user')

    kwargs['ti'].xcom_push(key='age', value=age)

def save_avg(**kwargs):

    hook = MySqlHook(mysql_conn_id='mysql_default', schema='test')

    ti = kwargs['ti']
    age = ti.xcom_pull(key='age', task_ids='cal_avg')

    hook.run(
        'insert into tongji(average_age) values(%s)' % (age),
        autocommit=True)

cal = PythonOperator(
    task_id='cal_avg', dag=dag, python_callable=cal_avg)

save = PythonOperator(
    task_id='save_avg', dag=dag, python_callable=save_avg)

save.set_upstream(cal)

