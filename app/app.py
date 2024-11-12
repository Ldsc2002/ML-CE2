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
    usuario_nombre = data['usuario_nombre']
    distancia = data['distancia']
    tiempo = data['tiempo']
    tipo_actividad = data['tipo_actividad']

    # Conectar a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el usuario ya existe, si no, crearlo
    cursor.execute('SELECT * FROM usuarios WHERE nombre = %s', (usuario_nombre,))
    usuario = cursor.fetchone()

    if not usuario:
        # Crear un nuevo usuario si no existe
        cursor.execute('INSERT INTO usuarios (nombre, carga_entrenamiento) VALUES (%s, %s)',
                       (usuario_nombre, 0))

    # Registrar la actividad
    cursor.execute('INSERT INTO actividades (usuario_nombre, distancia, tiempo, tipo_actividad) VALUES (%s, %s, %s, %s)',
                   (usuario_nombre, distancia, tiempo, tipo_actividad))
    
    # Actualizar la carga de entrenamiento
    carga_adicional = calculate_training_load(distancia, tiempo)  # Lógica para calcular la carga
    cursor.execute('UPDATE usuarios SET carga_entrenamiento = carga_entrenamiento + %s WHERE nombre = %s',
                   (carga_adicional, usuario_nombre))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Actividad registrada y carga de entrenamiento actualizada", "data": data}), 201

def calculate_training_load(distancia, tiempo):
    # Implementar la lógica para calcular la carga de entrenamiento
    # Por simplicidad, supongamos que la carga es proporcional a la distancia y tiempo
    carga = (distancia / tiempo) * 10  # Ajustar el factor según sea necesario
    return carga

@app.route('/get_activities', methods=['GET'])
def get_activities():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM actividades')
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({"actividades": actividades}), 200

@app.route('/get_user_training_load/<string:usuario_nombre>', methods=['GET'])
def get_user_training_load(usuario_nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT carga_entrenamiento FROM usuarios WHERE nombre = %s', (usuario_nombre,))
    carga_entrenamiento = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if carga_entrenamiento:
        return jsonify({"usuario_nombre": usuario_nombre, "carga_entrenamiento": carga_entrenamiento[0]}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
