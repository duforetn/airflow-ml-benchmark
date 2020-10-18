import pandas as pd 
import numpy as np
import random
import click
import os

class Generator():

    def __init__(self, batch_id):
        self.n_vars = 10
        self.batch_len = 100
        self.batch_id = batch_id
        self.data_dir = "/data"
        self.result_file = os.path.join(self.data_dir, str(self.batch_id).zfill(3) + '.csv')
        self.noise_var = .2
        self.betas = np.array([3, 4, 0, 0, 1, 0, 2, 0, 10, 5])
        self.second_order = [[0, 2],[2, 6], [5, 7], [8, 9]]

    def target_generator(self, x):
        y = self.betas.dot(x) + random.normalvariate(0, self.noise_var)
        for interaction in self.second_order:
            y = y + 2*x[interaction[0]]*x[interaction[1]]
        return y

    def write_df(self):
        os.makedirs(self.data_dir, exist_ok=True)
        df_x, df_y = [], []
        for row in range(self.batch_len):
            x = np.random.rand(self.n_vars)
            y = self.target_generator(x)
            df_x.append(x)
            df_y.append(y)

        df = pd.DataFrame(np.array(df_x))
        df.insert(0, 'y', np.array(df_y))
        df.to_csv(self.result_file, index = False)

@click.command()
@click.argument("batch_id")
def generate(batch_id: int):
    gen = Generator(batch_id)
    gen.write_df()

if __name__ == '__main__':
    generate()
