from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)
actividadesValidas = ['caminadora', 'correr']

def getConnection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )

@app.route('/registerActivity', methods=['POST'])
def registerActivity():
    usuarioNombre = request.args.get('usuario_nombre')
    distancia = request.args.get('distancia')
    tiempo = request.args.get('tiempo')
    tipoActividad = request.args.get('tipo_actividad')

    if tipoActividad not in actividadesValidas:
        return jsonify({"error": "Tipo de actividad no válido" , "actividades": actividadesValidas}), 400

    try:
        distancia = int(distancia)
        tiempo = int(tiempo)
    except ValueError:
        return jsonify({"error": "Distancia y tiempo deben ser números enteros"}), 400

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE nombre = %s', (usuarioNombre,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.execute('INSERT INTO usuarios (nombre, carga_entrenamiento) VALUES (%s, %s)',
                       (usuarioNombre, 0))

    cursor.execute('INSERT INTO actividades (usuario_nombre, distancia, tiempo, tipo_actividad) VALUES (%s, %s, %s, %s)',
                   (usuarioNombre, distancia, tiempo, tipoActividad))
    
    cargaEntrenamiento = calculateTrainingLoad(usuarioNombre, distancia, tiempo, tipoActividad)
    cursor.execute('UPDATE usuarios SET carga_entrenamiento = %s WHERE nombre = %s',
                   (cargaEntrenamiento, usuarioNombre))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Actividad registrada y carga de entrenamiento actualizada", "carga_entrenamiento": cargaEntrenamiento}), 201

def calculateTrainingLoad(usuarioNombre, distancia, tiempo, tipoActividad):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM actividades WHERE usuario_nombre = %s', (usuarioNombre,))
    actividades = cursor.fetchall()

    if not actividades:
        return 0
    else:
        actividades = actividades[-2:]

    cargaEntrenamiento = 0
    for actividad in actividades:
        carga = actividad[2] * actividad[3]

        if actividad[4] == 'correr':
            carga = carga * 2
        elif actividad[4] == 'caminadora':
            carga = carga * 1.5

        cargaEntrenamiento = cargaEntrenamiento + carga

    carga = distancia * tiempo
    if tipoActividad == 'correr':
        carga = carga * 2
    elif tipoActividad == 'caminadora':
        carga = carga * 1.5

    cargaEntrenamiento = cargaEntrenamiento + carga

    conn.commit()
    cursor.close()
    conn.close()

    return cargaEntrenamiento

@app.route('/getActivities', methods=['GET'])
def getActivities():
    usuarioNombre = request.args.get('usuario_nombre')

    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM actividades WHERE usuario_nombre = %s', (usuarioNombre,))
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()

    if actividades:
        return jsonify({"usuario_nombre": usuarioNombre, "actividades": actividades}), 200
    else:   
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/getUserTrainingLoad', methods=['GET'])
def getUserTrainingLoad():
    usuarioNombre = request.args.get('usuario_nombre')

    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT carga_entrenamiento FROM usuarios WHERE nombre = %s', (usuarioNombre,))
    cargaEntrenamiento = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if cargaEntrenamiento:
        return jsonify({"usuario_nombre": usuarioNombre, "carga_entrenamiento": cargaEntrenamiento[0]}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
@app.route('/getUsers', methods=['GET'])
def getUsers():
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({"usuarios": usuarios}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
