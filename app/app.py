from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )

@app.route('/register_activity', methods=['POST'])
def register_activity():
    data = request.json
    # Conectar a la base de datos y registrar la actividad
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO actividades (distancia, tiempo, tipo_actividad) VALUES (%s, %s, %s)',
                   (data['distancia'], data['tiempo'], data['tipo_actividad']))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Actividad registrada", "data": data}), 201

@app.route('/get_activities', methods=['GET'])
def get_activities():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM actividades')
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({"actividades": actividades}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
