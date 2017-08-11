# -*- coding: utf-8 -*-

import airflow
from airflow import DAG
from airflow.operators import BashOperator
from airflow.operators import EmailOperator
from airflow.operators import DummyOperator, BranchPythonOperator
from datetime import timedelta, datetime
from airflow.models import Variable

email_addr = Variable.get("email_recipients")

default_args = {
    'owner': 'etl',
    'depends_on_past': False,
    'email': email_addr.split(','),
    'email_on_failure': True,
    'email_on_retry': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'concurrency': 1,
    'max_active_run': 4
}

'''
基本格式 :
*　　*　　*　　*　　*　　command
分　时　日　月　周　命令

第1列表示分钟1～59 每分钟用*或者 */1表示
第2列表示小时1～23（0表示0点）
第3列表示日期1～31
第4列表示月份1～12
第5列标识号星期0～6（0表示星期天）
第6列要运行的命令
'''

dag = DAG('source_data_count', default_args=default_args, schedule_interval="0 12 * * *")

run_this_first = DummyOperator(task_id='run_this_first', dag=dag)

branching = BranchPythonOperator(task_id='branching', python_callable=lambda: 'source_count' if datetime.now().day <= 7 and datetime.today().weekday() == 6 else 'ignore_not_sunday', dag=dag) 
branching.set_upstream(run_this_first)

esucc = EmailOperator(
    task_id='email_success_' + dag.dag_id,
    to=email_addr,
    subject= dag.dag_id + ' [success] on ' + datetime.now().strftime('%Y-%m-%d'),
    html_content='Congratulation!',
    trigger_rule='all_success',
    dag=dag)

source_count = BashOperator(
    task_id='source_count',
    bash_command='/disk1/source_data_count; ./daily_table_count.sh > out.log ',
    dag=dag)

source_count.set_upstream(branching)
esucc.set_upstream(source_count)

ignore_not_sunday = DummyOperator(task_id='ignore_not_sunday', dag=dag)
ignore_not_sunday.set_upstream(branching)

join = DummyOperator(task_id='join', trigger_rule='all_success', dag=dag)
join << ignore_not_sunday
join << esucc
