import pandas as pd 
import numpy as np
import sklearn
import click
import os
from sklearn.metrics import mean_absolute_error
from influxdb import InfluxDBClient
from datetime import datetime

class Evaluator():

    def __init__(self, db: str):
        self.result_dir = 'results/'
        self.result_files = os.listdir(self.result_dir)
        self.db = db
        self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.db)
        
    @staticmethod
    def evaluate_metric(df):
        return mean_absolute_error(df['y'], df['y_predict'])

    def write_db_results(self, model: str, value: float):
        self.client.create_database(self.db)
        body = [{
                "measurement": model,
                "time": int(datetime.timestamp(datetime.now())),
                "fields": {
                    "value": value
                }
            }]
        print(body)
        self.client.write_points(body)

    def evaluate_results(self):
        for file in self.result_files:
            df = pd.read_csv(os.path.join(self.result_dir, file))
            res = self.evaluate_metric(df)
            self.write_db_results(file.replace('.csv', ''), res)    

@click.command()
@click.argument("db")
def evaluate(db: str):
    eval = Evaluator(db)
    eval.evaluate_results()

if __name__ == '__main__':
    evaluate()