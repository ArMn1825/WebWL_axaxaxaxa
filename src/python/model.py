from pandas.core.common import random_state
from scipy.linalg import solve
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
import matplotlib as plt

data = pd.read_csv("output.csv")
target = data['currentMethod']
data.drop("currentMethod", axis=1, inplace=True)
data.drop(['clientId', 'organizationId'], axis=1, inplace=True)
print(data)
print(target)
X_train, x, y_train, y = train_test_split(data, target, test_size=0.2, shuffle=True)

model = MLPClassifier([1000], max_iter=400, verbose=True)
model.fit(X_train, y_train)
preds = model.predict(x)
print(preds)
print(list(y))
score = model.score(x, y)
print(score)
# print(model.coefs_)

