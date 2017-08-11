# -*- coding: utf-8 -*-

import airflow
from airflow import DAG
from airflow.operators import BashOperator
from airflow.operators import EmailOperator
from datetime import timedelta, datetime
from airflow.models import Variable

email_addr = Variable.get("email_recipients")


default_args = {
    'owner': 'etl',
    'depends_on_past': False,
    'email': email_addr.split(','),
    'email_on_failure': True,
    'email_on_retry': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'concurrency': 1,
    'max_active_run': 4
}

dag = DAG('import_applog_mongodb', default_args=default_args, schedule_interval="10 5 * * *")

esucc = EmailOperator(
    task_id='email_success_' + dag.dag_id,
    to=email_addr,
    subject= dag.dag_id + ' [success] on ' + datetime.now().strftime('%Y-%m-%d'),
    html_content='Congratulation!',
    trigger_rule='all_success',
    dag=dag)

# add table here:
tables = ['browser_history', 'account_list', 'event_ios', 'event_app', 'ios_deviceinfo', 'frequentlocation', 'coordinates', 'hardware', 'location', 'network', 'telephone', 'hardwareios']
# copy table to bi
bitables = ['hardware', 'hardwareios']

for table in tables:
    imp = BashOperator(
        task_id='import_' + table,
        bash_command='/disk1/etl/imp_mongo_doc_by_day.sh {table} > /disk1/etl/log/{table}.log '.format(table=table),
        dag=dag)
    if table in bitables:
        bimp = BashOperator(
            task_id = 'send_2_bi_' + table,
            bash_command = '/disk1/etl/send_bi_impala_by_day.sh {table} > /disk1/etl/log/BI/{table}.log '.format(table=table),
            dag=dag)
        bimp.set_upstream(imp)
        esucc.set_upstream(bimp)
    else: 
        esucc.set_upstream(imp)

imp_software = BashOperator(
    task_id = 'import_software',
    bash_command = '/disk1/etl/imp_software_doc_by_day.sh > /disk1/etl/log/software.log ',
    dag=dag)
esucc.set_upstream(imp_software)
