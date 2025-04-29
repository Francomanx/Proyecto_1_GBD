# Proyecto_1_GBD
alo como se usa esta wea? xdddd
ya aqui estan las tablas para cargarlas en el sql porque la forma en las que tenia el profe no me funcaban mucho

CREATE TABLE paciente (
  rut VARCHAR(12) PRIMARY KEY,
  nombres VARCHAR(50) NOT NULL,
  apellido_p VARCHAR(20) NOT NULL,
  apellido_m VARCHAR(20),
  telefono VARCHAR(12) NOT NULL,
  correo VARCHAR(50) NOT NULL,
  direccion VARCHAR(50) NOT NULL,
  prevision VARCHAR(15) NOT NULL,
  fecha_nac DATE NOT NULL,
  fecha_reg DATE NOT NULL
);

CREATE TABLE personal (
  rut VARCHAR(12) PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(20) NOT NULL,
  telefono VARCHAR(12) NOT NULL,
  correo VARCHAR(50) NOT NULL,
  nombre_corto VARCHAR(21) NOT NULL,
  tipo VARCHAR(10) NOT NULL,
  fecha_ing DATE NOT NULL,
  estado INTEGER NOT NULL DEFAULT 1,
  porcentaje INTEGER NOT NULL DEFAULT 0,
  fonasa VARCHAR(2) NOT NULL DEFAULT 'si'
);

CREATE TABLE procedimiento (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  area VARCHAR(20) NOT NULL,
  valor INTEGER NOT NULL
);

CREATE TABLE horas (
  id SERIAL PRIMARY KEY,
  fecha_hora TIMESTAMP NOT NULL,
  medico VARCHAR(12) NOT NULL REFERENCES personal(rut),
  personal VARCHAR(12) NOT NULL REFERENCES personal(rut),
  tipo INTEGER NOT NULL,
  web VARCHAR(2) NOT NULL DEFAULT 'no',
  sobrecupo VARCHAR(2) NOT NULL DEFAULT 'no',
  estado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE contacto (
  id SERIAL PRIMARY KEY,
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  fecha_hora TIMESTAMP NOT NULL,
  via_conformado VARCHAR(20) NOT NULL,
  rut_personal VARCHAR(12) NOT NULL REFERENCES personal(rut)
);

CREATE TABLE consulta (
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  rut_paciente VARCHAR(12) NOT NULL REFERENCES paciente(rut),
  estado INTEGER NOT NULL DEFAULT 0,
  id_contacto INTEGER NOT NULL REFERENCES contacto(id),
  id_procedimiento INTEGER NOT NULL REFERENCES procedimiento(id),
  apoyo VARCHAR(12),
  PRIMARY KEY (id_hora, rut_paciente)
);

CREATE TABLE transaccion (
  id SERIAL PRIMARY KEY,
  rut_personal VARCHAR(12) NOT NULL REFERENCES personal(rut),
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  rut_paciente VARCHAR(12) NOT NULL REFERENCES paciente(rut),
  fecha_hora TIMESTAMP NOT NULL,
  monto INTEGER NOT NULL,
  estado INTEGER NOT NULL DEFAULT 0,
  mediopago INTEGER NOT NULL,
  bono INTEGER,
  boleta INTEGER,
  vaucher INTEGER
);

CREATE TABLE ficha (
  numero SERIAL PRIMARY KEY,
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  rut_paciente VARCHAR(12) NOT NULL REFERENCES paciente(rut),
  fecha_hora TIMESTAMP NOT NULL,
  comentario TEXT NOT NULL
);
