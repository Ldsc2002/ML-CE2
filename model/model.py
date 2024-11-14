from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd

app = Flask(__name__)
model = xgb.Booster()
model.load_model('model.json')
actividadesValidas = ['caminadora', 'correr']

@app.route('/predictTime', methods=['POST'])
def predict_time():
    distancia = request.args.get('distancia')
    rank = request.args.get('ranking')
    edad = request.args.get('edad')
    sexo = request.args.get('sexo')
    sexo = 1 if sexo == 'M' else 0

    distancia = int(distancia)
    rank = int(rank)
    edad = int(edad)
    sexo = int(sexo)

    df = pd.DataFrame([[sexo, rank, distancia, edad]], columns=['sex', 'place_in_class', 'distance', 'age'])
    data = xgb.DMatrix(df)

    prediction = model.predict(data)
    
    return jsonify({"predictedTime": str(prediction[0])}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
