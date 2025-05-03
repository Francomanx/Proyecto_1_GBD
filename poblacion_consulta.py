from faker import Faker
import random
import csv
from datetime import datetime, timedelta

fake = Faker('es_CL')

#Suposiciones relacionadas a consulta
#La Consulta tiene un estado que es independiente de la “hora”, esto permite dejar registros 
#si es que un paciente anula su consulta, lo que podría volver a dejar la hora como disponible. 
#El estado de la consulta podrá tomar valores 0 = “Reserva”, 1 = “Confirmada”, 3 = “Pagada” y 4 = “Finalizada”.

#Las Consultas que son de tipo “pabellón” podrán tener el apoyo de un segundo médico, en cuyo caso el ingreso
#percibido por ese procedimiento será distribuido en un 70% para el primer médico y un 30% para el médico de apoyo.

#Para generar consultas necesito
#id_hora: es un int unico para cada consulta proveniente de la id de horas
#rut_paciente: es un char proveniente del rut de un paciente (azar)
#estado: int que puede tener 4 valores (especifico arriba)
#id_contacto: es un int unico para cada consulta proveniente de la id de contactos
#id_procedimiento: es un int proveniente del id de los procedimientos (azar)
#apoyo: char proveniente del personal que tiene condiciones

#el apoyo es opcional solo para consultas de pabellon, en ese caso
#si fuera pabellon y hubiera apoyo, hay que asegurarse de
#que no exista el mismo medico dos veces
#y para hacer eso debemos
#conseguir id_hora de contactos
#verificar qué medico existe en esa hora

#proceso para generar consultas
def generar_consultas(num_consultas, id_horas, id_contactos, rut_pacientes, id_procedimientos, ruts_medicos, id_hora_de_contactos, rut_medico_de_horas):
    consultas = []
    lista_id_de_horas = list(id_horas)
    for _ in range (num_consultas):
        id_hora = random.choice(lista_id_de_horas)
        #ahora hay que coincidirlo con el de contacto
        #hagamos un bucle
        for i in range(len(id_hora_de_contactos)):
            #las listas estan ordenadas, entonces si encontramos la misma id en i posicion, significa que ahi
            #se encuentra el id del contacto que estamos buscando
            if id_hora_de_contactos[i] == id_hora:
                id_contacto = id_contactos[i]
        rut_paciente = random.choice(rut_pacientes)
        estado = random.choice([0,1,3,4]) #0.Reserva 1.Confirmada 3.Pagada 4.Finalizada
        id_procedimiento = random.choice(id_procedimientos)
        #en cuanto al apoyo
        #primero debemos verificar si la consulta es de tipo pabellon o consulta medica
        if id_procedimiento!='1': #si no es uno, significa que es de tipo pabellon, asi que puede haber apoyo
            #Hagamos un coso de probabilidad para ver si hay apoyo en la consulta o no
            decision = random.choice([1,2])
            if decision==1:#si hay apoyo
                apoyo = random.choice(ruts_medicos)
                rut_medico_de_hora = rut_medico_de_horas[int(id_hora) - 1]
                while apoyo==rut_medico_de_hora:#si ambos son lo mismo estaria mal porque un doctor no se apoya a el mismo
                    apoyo = random.choice(ruts_medicos)
            elif decision==2:#no hay apoyo
                apoyo = 'No'
        else:#si es una consulta medica, no puede haber apoyo
            apoyo = 'No'
        lista_id_de_horas.remove(id_hora)#se remueve para asegurarse que no vuelva a ser elegido
        consultas.append([id_hora,rut_paciente,estado,id_contacto,id_procedimiento,apoyo])
    return consultas

#aqui genero listas con datos necesarios para hacer las conexiones entre los diferentes atributos que me piden..
#de la forma correcta
id_horas = []
rut_medico_de_horas = []
with open('horas_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_horas.append(row['id'])
        rut_medico_de_horas.append(row['medico'])

id_contactos = []
id_hora_de_contactos = []
with open('contactos_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_contactos.append(row['id'])
        id_hora_de_contactos.append(row['id_hora'])

rut_pacientes = []
with open('paciente_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rut_pacientes.append(row['rut'])

id_procedimientos = []
with open('procedimiento_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_procedimientos.append(row['id'])

rut_medicos = []
with open('personal_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['tipo'] == 'Médico':
            rut_medicos.append(row['rut'])

#genero consultas
consultas_data = generar_consultas(3675, id_horas, id_contactos, rut_pacientes, id_procedimientos, rut_medicos, id_hora_de_contactos, rut_medico_de_horas)

#y las guardo en un archivo.csv
with open('consulta_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id_hora", "rut_paciente", "estado", "id_contacto", "id_procedimiento", "apoyo"])
    writer.writerows(consultas_data)

print("Datos de consultas generados correctamente.")
