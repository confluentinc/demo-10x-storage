import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio
from config import COLUMNS

print("tensorflow-io version: {}".format(tfio.__version__))
print("tensorflow version: {}".format(tf.__version__))

print(COLUMNS)

susy_iterator = pd.read_csv('./data/SUSY.csv', header=None, names=COLUMNS, chunksize=100000)
susy_df = next(susy_iterator)
print(susy_df.head())