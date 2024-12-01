# generate dataset
import pandas as pd
import random

ex = {
    "clientId":"client", # ИД пользователя
    "organizationId":"organization", # ИД организациии
    "segment":"value", # Сегмент организации: "Малый бизнес", "Средний бизнес", "Крупный бизнес"
    "role":"value", # Роль уполномоченного лица: "ЕИО", "Сотрудник"
    "organizations": 3, # Общее количество организаций у уполномоченного лица: 1..300
    "currentMethod": "method", # Действующий способ подписания."SMS", "PayControl", "КЭП на токене", "КЭП в приложении"
    "mobileApp": True, # Наличие мобильного приложения
    "signatures": { # Подписанные ранее типы документов
        "common": {
            "mobile":3, # Количество подписанных базовых документов в мобайле
            "web":10, # Количество подписанных базовых документов в вебе
        },
        "special": {
            "mobile":5, # Количество подписанных документов особой важности в мобайле
            "web":6, # Количество подписанных документов особой важности в вебе
        }
    },
    "availableMethods":["method1", "method2"], # Уже подключенные способы подписания."SMS", "PayControl", "КЭП на токене", "КЭП в приложении"
    "claims": 0 # Наличие обращений в банк по причине проблем с использованием СМС
}

columns = ["clientId", "organizationId", "segment", "role", "organizations", "mobileApp", "sig/com/mob", "sig/com/web", "sig/spec/mob", "sig/spec/web", "availableMethods", "claims", "currentMethod"]
dataset = []
# random.seed(42)
for i in range(1000):
    weights = [0, 0, 0] # [mob, kep pc, kep mob]
    cur = \
        [
            random.randint(0, 2001), # 0 clientID
            random.randint(0, 2001), # 1 orgID
            random.randint(0, 2), # 2 Segment
            random.randint(0, 1), # 3 role
            random.randint(0, 10), # 4 organizations
            random.randint(0, 1), # 5 mobile app
        # common
            random.randint(0, 5), # 6 signed mobile
            random.randint(0, 5), # 7 signed web
        # special
            random.randint(0, 5),  # 8 signed mobile
            random.randint(0, 5),  # 9 signed web

            random.randint(0, 15) | 1, # 10 bitset of available methods
            random.randint(0, 10), # 11 claims
        ]
    if cur[2] in [0, 1]:
        weights[0] += random.randint(0, 5)
    if cur[2] in [1, 2]:
        weights[1] += random.randint(0, 5)
        weights[2] += random.randint(0, 5)
    if cur[3] == 0:
        weights[0] += random.randint(3, 5)
        weights[1] += random.randint(0, 5)
        weights[2] += random.randint(0, 5)
    else:
        weights[0] += random.randint(0, 4)
        weights[1] += random.randint(3, 5)
        weights[2] += random.randint(3, 5)
    if cur[5] == 1:
        weights[0] += random.randint(0, 5)
        weights[2] += random.randint(0, 5)
    else:
        weights[0] -= random.randint(0, 3)
        weights[2] -= random.randint(0, 3)
    weights[0] += cur[6] * random.uniform(0, 1)
    weights[2] += cur[6] * random.uniform(0, 1)
    weights[1] += cur[7] * random.uniform(0, 1)
    weights[2] += cur[7] * random.uniform(0, 1)
    weights[1] += cur[8] * random.uniform(0, 1)
    p = 2
    for j in range(3):
        if p & cur[10]:
            weights[j] += random.randint(0, 5)
        p <<= 1
    m = max(weights)
    for j in range(3):
        if weights[j] == m:
            cur.append(j)
            break

    dataset.append(cur)
data_frame = pd.DataFrame(dataset, columns=columns)
data_frame.to_csv('output.csv', index=False, encoding='utf-8')