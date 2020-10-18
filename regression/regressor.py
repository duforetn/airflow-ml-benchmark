import pandas as pd 
import numpy as np
import sklearn
import click
import os
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

class Regressor():

    def __init__(self, model_name: str, n_batch: int = 5):
        self.model_name = model_name
        self.n_batch = int(n_batch)
        self.data_dir = '/data'
        self.result_dir = '/results'
        self.data_files = sorted([f for f in os.listdir(self.data_dir) if ".csv" in f])
        if len(self.data_files) > self.n_batch:
            self.data_files = self.data_files[:-self.n_batch]
        self.result_file = os.path.join(self.result_dir, self.model_name + '.csv')
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.init_model()

    def init_model(self):
        if self.model_name == "LM":
            self.model = linear_model.Ridge(alpha = 0)
        if self.model_name == "RF":
            self.model = RandomForestRegressor(1000)
        if self.model_name == "GB":
            self.model = GradientBoostingRegressor(1000)

    def load_data(self):
        full_df = pd.DataFrame()
        for file in self.data_files:
            full_df = full_df.append(pd.read_csv(os.path.join(self.data_dir, file), engine='python'))

        y = full_df['y']
        X = full_df.drop(columns='y')

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate_results(self):
        self.load_data()
        self.train_model()
        y_tilde = self.model.predict(self.X_test)
        result_df = pd.DataFrame(np.array(y_tilde), columns = ["y_predict"])
        result_df['y'] = np.array(self.y_test)
        os.makedirs(self.result_dir, exist_ok=True)
        result_df.to_csv(self.result_file)

@click.command()
@click.argument("model_name")
@click.argument("n_batch")
def regress(model_name: str, n_batch: int):
    reg = Regressor(model_name, n_batch)
    reg.evaluate_results()

if __name__ == '__main__':
    regress()
