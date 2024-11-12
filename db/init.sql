-- init.sql

DROP TABLE IF EXISTS actividades;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE IF NOT EXISTS usuarios (
    nombre VARCHAR(100) PRIMARY KEY,
    carga_entrenamiento FLOAT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS actividades (
    id SERIAL PRIMARY KEY,
    usuario_nombre VARCHAR(100) REFERENCES usuarios(nombre),
    distancia FLOAT NOT NULL,
    tiempo FLOAT NOT NULL,
    tipo_actividad VARCHAR(50) NOT NULL
);

-- INSERT INTO usuarios (nombre, carga_entrenamiento) VALUES ('admin', 0);