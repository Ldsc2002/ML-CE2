from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Cargar el modelo preentrenado
model = joblib.load('model.joblib')

@app.route('/predict_time', methods=['POST'])
def predict_time():
    data = request.json
    # Aquí se procesarían los datos de entrada para hacer la predicción
    # Se espera que el payload contenga 'distancia' y 'tipo_actividad'
    distancia = data.get('distancia')
    tipo_actividad = data.get('tipo_actividad')

    # Simulación: supongamos que el modelo devuelve un tiempo fijo por simplicidad
    prediction = model.predict([[distancia, 1 if tipo_actividad == "correr" else 0]])
    
    return jsonify({"predicted_time": prediction[0]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
