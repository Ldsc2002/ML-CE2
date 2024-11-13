from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('model.joblib')
actividadesValidas = ['caminadora', 'correr']

@app.route('/predictTime', methods=['POST'])
def predict_time():
    distancia = request.args.get('distancia')
    tipoActividad = request.args.get('tipo_actividad')

    if tipoActividad not in actividadesValidas:
        return jsonify({"error": "Tipo de actividad no válido" , "actividades": actividadesValidas}), 400

    prediction = model.predict([[distancia, actividadesValidas.index(tipoActividad)]])
    
    return jsonify({"predictedTime": prediction[0]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
