from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
import matplotlib as plt
from sklearn.neighbors import KNeighborsClassifier

types = {
    0: 'PayControl', 1: 'КЭП на токене', 2: 'КЭП в приложении'
}

data = pd.read_csv("output.csv")
target = data['currentMethod']
data.drop("currentMethod", axis=1, inplace=True)
data.drop(['clientId', 'organizationId'], axis=1, inplace=True)
X_train, x, y_train, y = train_test_split(data, target, test_size=0.2, shuffle=True, random_state=42)
model = KNeighborsClassifier(n_neighbors=150, metric='cosine')
model.fit(X_train, y_train)
preds = model.predict(x)
print(list(map(int, preds)), list(y), sep='\n')
print(model.score(x, y))
neighbors = model.kneighbors(x, n_neighbors=10, return_distance=False)[0]
for usr in range(len(x)):
    role = [0, 0]
    segment = [0, 0, 0]
    mobile = 0
    web = 0
    special = 0
    for i in range(len(neighbors)):
        elem = data.iloc[int(neighbors[i])]
        segment[elem['segment']] += 1
        role[elem['role']] += 1
        mobile += elem['sig/com/mob'] + elem['sig/spec/mob']
        web += elem['sig/com/web'] + elem['sig/spec/web']
        special += elem['sig/spec/mob'] + elem['sig/spec/web']
    cur = x.iloc[usr]
    if segment[2] >= 0.5 * sum(segment) :
        print(f"Для большого бизнеса обычно используют {types[preds[usr]]}.")
    elif role[1] > 0.6 * sum(role):
        print(f"Руководители большого бизнеса обычно используют {types[preds[usr]]}.")
    elif special > len(neighbors) * 0.6:
        print(f"Вам рекомендуется {types[preds[usr]]}, так как вы часто подписываете важные документы", end=' ')
        if mobile > (web + mobile) * 0.6:
            print("с мобильного приложения.")
        elif web > (web + mobile) * 0.6:
            print("с персонального компьютера.")
        else:
            print()
    elif cur['claims'] > 1:
        print(f"Вам рекомендуется {types[preds[usr]]}, так как вы жалуетесь, что СМС не приходят.")
    else:
        print("Подписывайте документы через приложение, не нужно больше ждать СМС!")

