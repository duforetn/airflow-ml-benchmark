
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

 
args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

wf_dag = DAG(
    dag_id='workflow',
    default_args=args,
    schedule_interval='*/5 * * * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=['example']
)

data_batch_generation = BashOperator(task_id='data_batch_generation', 
    bash_command = "venv/bin/python3.7 generation/generator.py $DATADIR", dag=wf_dag)
train_LM = BashOperator(task_id='train_LM', 
    bash_command = "venv/bin/python3.7 regression/regressor.py LM 5 $DATADIR $RESULTDIR", dag=wf_dag)
train_RF = BashOperator(task_id='train_RF', 
    bash_command = "venv/bin/python3.7 regression/regressor.py RF 5 $DATADIR $RESULTDIR", dag=wf_dag)
evaluation = BashOperator(task_id='evaluation', 
    bash_command = "venv/bin/python3.7 evaluation/evaluator.py workflow $RESULTDIR", dag=wf_dag)

data_batch_generation >> [train_LM, train_RF] >> evaluation
