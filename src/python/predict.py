from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import sys
import json

input_data = sys.stdin.read()
data = json.loads(input_data)

encoder = LabelEncoder()
X = []

encoder.fit(['small business', 'medium business', 'large business'])
X.append(encoder.transform([data['segment']])[0])

encoder.fit(['eio', 'employee'])
X.append(encoder.transform([data['role']])[0])

X.append(data['organizations'])
X.append(data['mobileApp'])
X.append(data['signatures']['common']['mobile'])
X.append(data['signatures']['common']['web'])
X.append(data['signatures']['special']['mobile'])
X.append(data['signatures']['special']['web'])
X.append(0)
encoder.fit(['SMS', 'PayControl', 'ES on token', 'ES in app'])
for el in data['availableMethods']:
    X[-1] += encoder.transform([el])[0]
X.append(data['claims'])

columns = ["segment", "role", "organizations", "mobileApp", "sig/com/mob",
           "sig/com/web", "sig/spec/mob", "sig/spec/web", "availableMethods", "claims"]

types = {
    0: 'PayControl', 1: 'КЭП на токене', 2: 'КЭП в приложении'
}

data = pd.read_csv("output.csv")
target = data['currentMethod']
data.drop("currentMethod", axis=1, inplace=True)
data.drop(['clientId', 'organizationId'], axis=1, inplace=True)
model = KNeighborsClassifier(n_neighbors=150, metric='cosine')
model.fit(data, target)
pred = model.predict([X])
neighbors = model.kneighbors([X], n_neighbors=10, return_distance=False)
role = [0, 0]
segment = [0, 0, 0]
mobile = 0
web = 0
special = 0
for i in range(len(neighbors)):
    elem = data.iloc[int(neighbors[0][i])]
    segment[elem['segment']] += 1
    role[elem['role']] += 1
    mobile += elem['sig/com/mob'] + elem['sig/spec/mob']
    web += elem['sig/com/web'] + elem['sig/spec/web']
    special += elem['sig/spec/mob'] + elem['sig/spec/web']
if segment[2] >= 0.5 * sum(segment) :
    print(f"Для большого бизнеса обычно используют {types[pred[0]]}.")
elif role[1] > 0.6 * sum(role):
    print(f"Руководители большого бизнеса обычно используют {types[pred[0]]}.")
elif special > len(neighbors) * 0.6:
    print(f"Вам рекомендуется {types[pred[0]]}, так как вы часто подписываете важные документы", end=' ')
    if mobile > (web + mobile) * 0.6:
        print("с мобильного приложения.")
    elif web > (web + mobile) * 0.6:
        print("с персонального компьютера.")
    else:
        print()
elif X[-1] > 1:
    print(f"Вам рекомендуется {types[pred[0]]}, так как вы жалуетесь, что СМС не приходят.")
else:
    print("Подписывайте документы через приложение, не нужно больше ждать СМС!")