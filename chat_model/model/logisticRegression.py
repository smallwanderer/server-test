import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras import optimizers

file_path = "dataset/dataset.csv"
dataset = pd.read_csv(file_path)

X = dataset[['x1', 'x2', 'x3']].values
y = dataset['y'].values

model = Sequential()
model.add(Dense(1, input_dim=3, activation='linear'))

sgd = optimizers.SGD(learning_rate=0.0001)
model.compile(optimizer=sgd, loss='mse', metrics=['mse'])
model.fit(X, y, epochs=2000)

model.save('my_model.h5')