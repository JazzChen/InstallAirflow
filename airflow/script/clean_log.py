import sys
import MySQLdb

if len(sys.argv) < 3:
        print("usage: "+sys.argv[0]+ " 2017-07-15 import_mongodb_jeffery")
        exit(1)

exec_date = sys.argv[1]
dag_id = sys.argv[2]

query = {'delete from task_instance where execution_date > "' + exec_date + '" and dag_id = "' + dag_id + '"',
        'delete from log where execution_date > "' + exec_date + '" and dag_id = "' + dag_id + '"',
        'delete from dag_run where execution_date > "' + exec_date + '" and dag_id = "' + dag_id + '"',
        "delete from dag_stats where state = 'running'  and dag_id = '" + dag_id + "'"}

def connect(query):
        db = MySQLdb.connect(host="localhost", user="airflow", passwd="airflow", db="airflow")
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        db.close()
        return

for value in query:
        print value
        connect(value)
