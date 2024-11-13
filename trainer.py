import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

data = {
    'distancia': [5, 10, 15, 20, 25],
    'tipoActividad': [0, 1, 1, 0, 1], # 0 = caminadora, 1 = correr
    'tiempo': [30, 60, 90, 120, 150]
}

df = pd.DataFrame(data)

X = df[['distancia', 'tipoActividad']]
y = df['tiempo']

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, 'model.joblib')
