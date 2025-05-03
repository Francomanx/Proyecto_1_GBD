from faker import Faker
import random
import csv
from datetime import datetime, timedelta

fake = Faker('es_CL')

#Para generar fichas necesito
#numero: voy a suponer que esto es como id unico para cada ficha
#id_hora: int unico para cada ficha proveniente de la id_hora de consulta
#rut_paciente: char proveniente de rut_paciente de consulta 
#fecha_hora: Datetime que sera igual a la fecha y hora proveniente de horas
#comentario: un string que dependiendo del tipo de procedimiento, tendra relacion con una cirugia o con una consulta medica

#proceso para generar fichas
def generar_fichas(num_fichas, id_horas_de_consultas, fecha_horas_de_horas, id_procedimientos_de_consultas, rut_pacientes_de_consultas):
    fichas = []
    comentarios_consulta = [
        "Consulta general",
        "Dolor abdominal y nauseas",
        "Problemas respiratorios",
        "Revision de cicatriz postoperatoria",
        "Solicitud de examen de sangre",
        "Solicitud de radiografia",
    ]
    comentarios_cirugia = [
        "Realizacion de cirugia abdominal",
        "Realizacion de cirugia en torax",
        "Realizacion de cirugia renal",
        "Realizacion de cirugia ortopedica",
        "Realizacion de cirugia cardiovascular",
        "Realizacion de cirugia plastica",
        "Realizacion de cirugia neurologica",
        "Realizacion de cirugia otorrinolaringologica"
    ]
    lista_id_horas_de_consultas = list(id_horas_de_consultas)
    num_counter = 1

    for _ in range(num_fichas):
        id_hora = random.choice(lista_id_horas_de_consultas)
        #para tener el rut del paciente:
        #podria hacer un bucle en el que busque el indice en donde
        #id_hora sea igual a i, significando que en ese mismo indice
        #existe el rut del paciente a asociar
        for i in range(len(id_horas_de_consultas)):
            if id_horas_de_consultas[i] == id_hora:
                rut_paciente = rut_pacientes_de_consultas[i]
                #para el comentario, deberiamos verificar si el procedimiento
                #a realizar fue una consulta o cirugia
                if id_procedimientos_de_consultas[i]!='1':#si no es una consulta
                    comentario = random.choice(comentarios_cirugia)
                else:#si es una consulta
                    comentario = random.choice(comentarios_consulta)
        #conseguimos la fecha_hora en base a la id de la hora asociada a la ficha
        fecha_hora = fecha_horas_de_horas[int(id_hora) - 1]
        lista_id_horas_de_consultas.remove(id_hora)
        fichas.append([num_counter,id_hora,rut_paciente,fecha_hora,comentario])
        num_counter+=1
    return fichas

#aqui genero listas con datos necesarios para hacer las conexiones entre los diferentes atributos que me piden..
#de la forma correcta
id_horas_de_consultas = []
id_procedimientos_de_consultas = []
rut_pacientes_de_consultas = []
with open('consulta_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_horas_de_consultas.append(row['id_hora'])
        id_procedimientos_de_consultas.append(row['id_procedimiento'])
        rut_pacientes_de_consultas.append(row['rut_paciente'])

fecha_horas_de_horas = []
with open('horas_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        fecha_horas_de_horas.append(row['fecha_hora'])

#generamos las fichas
fichas_data = generar_fichas(3675, id_horas_de_consultas, fecha_horas_de_horas, id_procedimientos_de_consultas, rut_pacientes_de_consultas)

#y los guardamos en un archivo.csv
with open('fichas_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["numero", "id_hora", "rut_paciente", "fecha_hora", "comentario"])
    writer.writerows(fichas_data)

print("Datos de fichas generados correctamente.")