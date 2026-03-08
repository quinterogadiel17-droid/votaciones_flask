CREATE DATABASE IF NOT EXISTS votaciones_db;
USE votaciones_db;

CREATE TABLE IF NOT EXISTS puestos_votacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lugar VARCHAR(120) NOT NULL,
    direccion VARCHAR(180) NOT NULL,
    mesa VARCHAR(30) NOT NULL,
    zona VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS ciudadanos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_identificacion VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(120) NOT NULL,
    puesto_id INT NOT NULL,
    CONSTRAINT fk_ciudadanos_puesto
        FOREIGN KEY (puesto_id) REFERENCES puestos_votacion(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

INSERT IGNORE INTO puestos_votacion (id, lugar, direccion, mesa, zona)
VALUES
    (1, 'Colegio Central', 'Calle 10 # 20-30', 'Mesa 1', 'Urbana'),
    (2, 'Escuela San Juan', 'Carrera 12 # 40-20', 'Mesa 2', 'Urbana'),
    (3, 'Instituto Nacional', 'Avenida 5 # 15-80', 'Mesa 3', 'Rural');
