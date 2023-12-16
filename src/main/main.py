import numpy as np
from sklearn.model_selection import train_test_split

from dataset_handler import get_training_set
from models.layers.dense import Dense
from models.model import Model
from initializer import Random
from activation import ReLu, Identity, Sigmoid
from optimizer import SGD
from loss import MSE
from metric import RootMeanSquaredError
import sys

print(sys.path)

x_train, y_train = get_training_set("../../data/ML-CUP23-TR.csv")

x_train, x_test = train_test_split(x_train, test_size=0.2, random_state=42)
y_train, y_test = train_test_split(y_train, test_size=0.2, random_state=42)

"""
data = np.load("../../data/y=2x/training.npy")
labels = np.load("../../data/y=2x/labels.npy")

x_train = data[:80, :]
x_test = data[80:, :]

y_train = labels[:80, :]
y_test = labels[80:, :]"""

print(x_train.shape)
print(y_train.shape)

intializer = Random()
relu = ReLu()
identity = Identity()
sigmoid = Sigmoid()
sgd = SGD(learning_rate=0.01, momentum=0)
loss = MSE()
metrics = [RootMeanSquaredError()]


model = Model()
model.add(Dense(10, 32, intializer, -0.1, 0.1, relu))
model.add(Dense(32, 16, intializer, -0.1, 0.1, relu))
model.add(Dense(16, 3, intializer, -0.1, 0.1, identity))

model.compile(sgd, loss, metrics)

# model.summary()

model.fit(x_train, y_train, 1001, 20, True)

errors = model.evaluate(x_test, y_test)

print(errors)


