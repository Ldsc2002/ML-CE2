-- init.sql

CREATE TABLE IF NOT EXISTS actividades (
    id SERIAL PRIMARY KEY,
    distancia FLOAT NOT NULL,
    tiempo FLOAT NOT NULL,
    tipo_actividad VARCHAR(50) NOT NULL
);
