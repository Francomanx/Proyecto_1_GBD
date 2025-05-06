# Proyecto_1_GBD

Este proyecto permite reflejar un escenario realista de gestión de servicios médicos privados, destacando la importancia de una base de datos bien estructurada para la trazabilidad de información clínica y financiera, y la toma de decisiones estratégicas a partir de datos confiables y eficientes.


## Tablas

```sql
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
```
```sql
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
```
```sql
CREATE TABLE procedimiento (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  area VARCHAR(20) NOT NULL,
  valor INTEGER NOT NULL
);
```
```sql
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
```
```sql
CREATE TABLE contacto (
  id SERIAL PRIMARY KEY,
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  fecha_hora TIMESTAMP NOT NULL,
  via_conformado VARCHAR(20) NOT NULL,
  rut_personal VARCHAR(12) NOT NULL REFERENCES personal(rut)
);
```
```sql
CREATE TABLE consulta (
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  rut_paciente VARCHAR(12) NOT NULL REFERENCES paciente(rut),
  estado INTEGER NOT NULL DEFAULT 0,
  id_contacto INTEGER NOT NULL REFERENCES contacto(id),
  id_procedimiento INTEGER NOT NULL REFERENCES procedimiento(id),
  apoyo VARCHAR(12),
  PRIMARY KEY (id_hora, rut_paciente)
);
```
```sql
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
```
```sql
CREATE TABLE ficha (
  numero SERIAL PRIMARY KEY,
  id_hora INTEGER NOT NULL REFERENCES horas(id),
  rut_paciente VARCHAR(12) NOT NULL REFERENCES paciente(rut),
  fecha_hora TIMESTAMP NOT NULL,
  comentario TEXT NOT NULL
);
```

- A la hora de importar los csv en las tablas asegurese de que antes de importarlo, en las opciones de import habilite los headers.

**Orden recomendado de los imports:**
1. personal
2. paciente
3. procedimiento
4. horas
5. contacto
6. consulta
7. ficha
8. transaccion

## Indices agregados
- **Contexto de la Query:** Ingreso de cada profesional y monto que cobra el centro de salud a cada profesional en arriendos de instalaciones.
El cobro par consultas medicas corresponde a un porcentaje definido por medico.
Cada procedimiento que se realiza en pabellon tiene 5% de para la empresa.  

Query para generar reportes de contabilidad:

```sql
select
  personal.rut AS "RUT del Profesional",
  personal.nombre || ' ' || personal.apellido AS "Nombre Completo",
  SUM(
    CASE
      -- Consulta médica.
      WHEN horas.tipo = 1 THEN transaccion.monto * (1-personal.porcentaje*0.01)
      -- Pabellón.
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.05                     
      ELSE 0
    END
  ) AS "Pago a la Empresa",
  SUM(
    CASE
      -- Consulta médica.
      WHEN horas.tipo = 1 THEN transaccion.monto * personal.porcentaje*0.01
      -- Pabellón.
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.95                     
      ELSE 0
    END
  ) AS "Ingreso del Profesional"
FROM
  transaccion
  JOIN horas ON transaccion.id_hora = horas.id
  JOIN personal ON transaccion.rut_personal = personal.rut
GROUP BY
  personal.rut, personal.nombre, personal.apellido
```

### Indices posibles:
- personal.rut (M, poca cantidad de datos).
- horas.id (B, arta cantidad de datos).
- transaccion.id_hora (B, deberia tener la misma cantidad de elementos que horas).
- transaccion.rut_personal (B, deberia tener la misma cantidad de elementos que horas).

```sql
CREATE INDEX idx_horas_id ON horas USING BTREE (id);
```
```sql
CREATE INDEX idx_transaccion_id_hora ON transaccion USING BTREE (id_hora);
```
```sql
CREATE INDEX idx_transaccion_rut_personal ON transaccion USING BTREE (rut_personal);
```

## Querys solicitadas

- ***a.*** Montos por pagar a cada médico por concepto de Consultas y/o Pabellones, separar ambos registros.
```sql 
SELECT 
personal.rut AS "RUT del Profesional",
personal.nombre || ' ' || personal.apellido AS "Nombre Completo",
SUM(
    CASE
      -- Consulta médica.
      WHEN horas.tipo = 1 THEN transaccion.monto * personal.porcentaje*0.01
      ELSE 0
    END
) AS "Ingreso por Consultas",
SUM(
    CASE
         -- Pabellón.
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.95
      ELSE 0
    END
) AS "Ingreso por Pabellones"
FROM transaccion
JOIN horas ON transaccion.id_hora = horas.id 
JOIN personal ON transaccion.rut_personal = personal.rut
GROUP BY
  personal.rut, personal.nombre, personal.apellido
```

- ***b.*** Montos por cobrar a cada médico por concepto de arriendo de las instalaciones.
```sql
SELECT 
personal.rut AS "RUT del Profesional",
personal.nombre || ' ' || personal.apellido AS "Nombre Completo",
SUM(
    CASE
      -- Consulta médica.
      WHEN horas.tipo = 1 THEN transaccion.monto * (1-personal.porcentaje*0.01)
      -- Pabellón.
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.05                     
      ELSE 0
    END
) AS "Cobros por Arriendo"
FROM transaccion
JOIN horas ON transaccion.id_hora = horas.id 
JOIN personal ON transaccion.rut_personal = personal.rut
GROUP BY
  personal.rut, personal.nombre, personal.apellido
```

- ***c.*** Utilidades percibidas por el centro de salud por Consultas, Pabellones y Arriendos.
```sql
SELECT
SUM(
    CASE
      -- Consulta médica.
      WHEN horas.tipo = 1 THEN transaccion.monto * (1-personal.porcentaje*0.01)
      ELSE 0
    END
) AS "Utilidades por Consultas",
SUM(
    CASE
      -- Pabellón.
        WHEN horas.tipo = 2 THEN transaccion.monto * 0.05                     
        ELSE 0
    END
) AS "Utilidades por Pabellones",
SUM(
    CASE
      -- Arriendos.
      WHEN horas.tipo = 1 THEN transaccion.monto * (1-personal.porcentaje*0.01)
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.05                     
      ELSE 0
    END
) AS "Utilidades Total por Arriendos"
FROM transaccion
JOIN horas ON transaccion.id_hora = horas.id 
JOIN personal ON transaccion.rut_personal = personal.rut;
```

## Tablas desnormalizadas

```sql
CREATE TABLE reporte_contable AS
SELECT
  transaccion.id AS id_transaccion,
  transaccion.fecha_hora,
  transaccion.rut_paciente,
  transaccion.rut_personal AS rut_medico,
  personal.nombre AS nombre_medico,
  personal.apellido AS apellido_medico,
  personal.porcentaje,
  horas.tipo AS tipo_atencion,
  transaccion.monto,
  CASE
      WHEN horas.tipo = 1 THEN transaccion.monto * (1-personal.porcentaje*0.01)
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.05     
    ELSE 0
  END AS utilidad_empresa,
  CASE
      WHEN horas.tipo = 1 THEN transaccion.monto * personal.porcentaje*0.01
      WHEN horas.tipo = 2 THEN transaccion.monto * 0.95
    ELSE 0
  END AS ingreso_profesional
FROM
  transaccion
  JOIN horas ON transaccion.id_hora = horas.id
  JOIN personal ON transaccion.rut_personal = personal.rut;
```

## Experimentos

Las siguientes querys son las antes vistas, pero ahora utilizando la tabla generada luego de la
desnormalización pertinente. Los experimentos con el uso del índice auxiliar no conlleva generar
querys distintas a las iniciales, por lo cual en esta sección solo se muestran las consultas modificadas.




- ***Query reportes de utilidad:*** Ingreso de cada profesional y monto que cobra el centro de salud a cada profesional en arriendos de instalaciones.

Query para generar reportes de contabilidad:

```sql
SELECT
  rut_medico AS "RUT del Profesional",
  nombre_medico || ' ' || apellido_medico AS "Nombre del Profesional",
  SUM(ingreso_profesional) AS "Ingreso del Profesional",
  SUM(utilidad_empresa) AS "Pago a la empresa"
FROM
  reporte_contable
GROUP BY
  rut_medico, nombre_medico, apellido_medico
ORDER BY
  "Ingreso del Profesional" DESC;
```
- ***Query a:*** Ingreso de cada profesional y monto que cobra el centro de salud a cada profesional en arriendos de instalaciones.

Query para generar reportes de contabilidad:

```sql
SELECT 
  rut_medico AS "RUT del Profesional",
  nombre_medico || ' ' || apellido_medico AS "Nombre Completo",
  SUM(CASE WHEN tipo_atencion = 1 THEN ingreso_profesional ELSE 0 END) AS "Ingreso por Consultas",
  SUM(CASE WHEN tipo_atencion = 2 THEN ingreso_profesional ELSE 0 END) AS "Ingreso por Pabellones"
FROM reporte_contable
GROUP BY rut_medico, nombre_medico, apellido_medico;
```
- ***Query b:*** Ingreso de cada profesional y monto que cobra el centro de salud a cada profesional en arriendos de instalaciones.

Query para generar reportes de contabilidad:

```sql
SELECT
  rut_medico AS "RUT del Profesional",
  nombre_medico || ' ' || apellido_medico AS "Nombre del Profesional",
  SUM(utilidad_empresa) AS "Cobros por Arriendo"
FROM
  reporte_contable
GROUP BY
  rut_medico, nombre_medico, apellido_medico
ORDER BY
  "Cobros por Arriendo" DESC;
```
- ***Query c:*** Ingreso de cada profesional y monto que cobra el centro de salud a cada profesional en arriendos de instalaciones.

Query para generar reportes de contabilidad:

```sql
SELECT
  SUM(CASE WHEN tipo_atencion = 1 THEN utilidad_empresa ELSE 0 END) AS "Utilidades por Consultas",
  SUM(CASE WHEN tipo_atencion = 2 THEN utilidad_empresa ELSE 0 END) AS "Utilidades por Pabellones",
  SUM(utilidad_empresa) AS "Utilidades Totales"
FROM reporte_contable;
```

## Librerias necesarias
- Faker
```bash
pip install faker
```

## Consideraciones
- Implementar la codificación UTF-8 a los datos mediante la libreria unicodedata.