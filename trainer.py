import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Simulación de datos
data = {
    'distancia': [5, 10, 15, 20, 25],
    'tipo_actividad': [0, 1, 1, 0, 1],  # 0 = caminadora, 1 = correr
    'tiempo': [30, 60, 90, 120, 150]  # Tiempo en minutos
}

df = pd.DataFrame(data)

X = df[['distancia', 'tipo_actividad']]
y = df['tiempo']

# Entrenamiento del modelo
model = LinearRegression()
model.fit(X, y)

# Guardar el modelo
joblib.dump(model, 'model.joblib')
