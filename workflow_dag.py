
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
 
wf_dag = DAG('workflow', description='DAG', 
    schedule_interval=timedelta(seconds=60), 
    start_date=datetime.now())
 
data_batch_generation = BashOperator(task_id='data_batch_generation', 
    bash_command = "python3 generation/generator.py 8", dag=wf_dag)
train_LM = BashOperator(task_id='train_LM', 
    bash_command = "python3 regression/regressor.py LM 5", dag=wf_dag)
train_GB = BashOperator(task_id='train_GB', 
    bash_command = "python3 regression/regressor.py GB 5", dag=wf_dag)
train_RF = BashOperator(task_id='train_RF', 
    bash_command = "python3 regression/regressor.py RF 5", dag=wf_dag)
evaluation = BashOperator(task_id='evaluation', 
    bash_command = "python3 evaluation/evaluator.py workflow", dag=wf_dag)

data_batch_generation >> [train_GB, train_LM, train_RF] >> evaluation
