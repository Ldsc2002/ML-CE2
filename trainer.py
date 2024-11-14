
# Importar librerías para red neuronal que prediga un tiempo continuo 

# Pandas
import pandas as pd

# Numpy
import numpy as np

# xgboost
import xgboost as xgb

# Sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# -------------- COLUMNAS ----------------

# place,age_class,place_in_class,bib,name,sex,nation,team,official_time,
# net_time,birth_date,event,event_year,distance

# ----------------------------------------



# ----------------------------------------

# Importar datos
data = pd.read_csv('all_races.csv', low_memory=False)


# Seleccionar las columnas 'birth_date', 'event_year', 'sex', 'place_in_class', 'distance', 'net_time'
data = data[['birth_date', 'event_year', 'sex', 'place_in_class', 'distance', 'net_time']]

# ----------------------------------------



# ----------------------------------------

# Eliminar filas con valores nulos
data = data.dropna()

# Obtener la edad
data['birth_date'] = pd.to_datetime(data['birth_date'], format='%d/%m/%Y', errors='coerce', dayfirst=True)
data['birth_year'] = data['birth_date'].dt.year
data['event_year'] = pd.to_numeric(data['event_year'], errors='coerce')
data['event_year'] = data['event_year'].fillna(0).astype(int)
data['age'] = data['event_year'] - data['birth_year']
data = data.drop(columns=['event_year', 'birth_date', 'birth_year'])


# Cambiar time para que sea en minutos. 00:29:56.000000000 -> 29.933333333333334
data['net_time'] = pd.to_timedelta(data['net_time'], errors='coerce')
data['net_time'] = data['net_time'].apply(lambda x: ((x.total_seconds() / 60)) if pd.notna(x) else None)

# Aproximar el net_time a el 5 más cercano. Por ejemplo, 49 es 50, 47 es 45.
data['net_time'] = data['net_time'].apply(lambda x: round(x / 5) * 5 if pd.notna(x) else None)


# Eliminar filas con valores nulos
data = data.dropna()

# ----------------------------------------



# ----------------------------------------

# Cambiar tipos de datos
data['age'] = data['age'].astype(int)
data['place_in_class'] = data['place_in_class'].astype(int)
data['distance'] = data['distance'].astype(int)
data['net_time'] = data['net_time'].astype(int)
data['sex'] = data['sex'].apply(lambda x: 1 if x == 'M' else 0)

print(data.head())

# ----------------------------------------



# ----------------------------------------

# Separar en variables dependientes e independientes    
Y = data['net_time']
X = data.drop(columns=['net_time'])

# Crear conjunto de entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Imprimir size de los conjuntos
print('X_train:', X_train.shape)
print('X_test:', X_test.shape)

# ----------------------------------------



# ----------------------------------------

# Convertir los datos a formato DMatrix, que es utilizado por XGBoost
dtrain = xgb.DMatrix(X_train, label=Y_train)
dtest = xgb.DMatrix(X_test, label=Y_test)

# Parámetros para el modelo XGBoost
params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'max_depth': 6,
    'learning_rate': 0.01,          # Reducir la tasa de aprendizaje
    'num_boost_round': 2000,        # Más iteraciones
    'lambda': 1,                    # Regularización L2
    'alpha': 0.5,                   # Regularización L1
    'colsample_bytree': 0.8,        # Submuestreo de columnas
    'subsample': 0.8,               # Submuestreo de datos
}

# Entrenar el modelo XGBoost
model = xgb.train(params, dtrain, num_boost_round=1000, evals=[(dtest, 'test')], early_stopping_rounds=10)

# Realizar predicciones
predictions = model.predict(dtest)

# Evaluar el modelo RMSE
rmse = np.sqrt(mean_squared_error(Y_test, predictions))
print('RMSE:', rmse)

# Guardar el modelo
model.save_model('model.json')

# Comparar predicciones con valores reales
comparison_df = pd.DataFrame({
    'Real': Y_test,
    'Predicted': predictions
})
print(comparison_df.head())

# ----------------------------------------


