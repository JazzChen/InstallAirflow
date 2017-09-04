# -*- coding: utf-8 -*-

# execute below command first:
# sudo systemctl stop airflow-scheduler
# sudo systemctl stop airflow-flower
# sudo systemctl stop airflow-worker
# sudo systemctl stop airflow-webserver

from celery import Celery
app = Celery('tasks', backend='redis', broker='redis://localhost:6379/0')
app.control.purge()
