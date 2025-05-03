from faker import Faker
import random
import csv
from datetime import datetime, timedelta

fake = Faker('es_CL')

#Para generar contactos necesito
#id: es un int unico para cada contacto
#id_hora: es un int vinculado a una id de hora (no se repiten id_horas)
#fecha_hora: como no se especifica nada de esto en el documento, tendra el mismo valor de la fecha_hora de la hora a la que..
#..esta vinculada a traves de id_hora
#via_conformado: indica si la forma en que se registro el contacto(?) es remoto o presencial
#rut_personal: va a estar asociado a alguien del personal, pero solo a medicos o a administrativos

#proceso para generar contactos
def generar_contactos(num_contactos, id_horas, fecha_horas, ruts_personal):
    contactos = []
    id_counter = 1
    lista_id_horas = list(id_horas)
    lista_fecha_horas = list(fecha_horas)
    lista_via_conformado = ['Remoto','Presencial']
    for _ in range (num_contactos):
        #asociacion de id_hora
        id_hora = random.choice(lista_id_horas)
        #como las ids de horas estan ordenadas [1,2,3,4....], significa que si quiero la fecha_hora de...
        #... la hora que tiene el id = 45, el valor de fecha_hora de esa hora estara en la posicion 44
        fecha_hora = lista_fecha_horas[int(id_hora) - 1]
        #una vez que haya sacado tanto la id_hora como la fecha_hora de la hora, elimino la id de la lista de...
        #...id de horas para evitar que vuelvan a ser elejidas mediante el random.choice()
        lista_id_horas.remove(id_hora)
        via_conformado = random.choice(lista_via_conformado)
        rut_personal = random.choice(ruts_personal)
        
        contactos.append([id_counter,id_hora,fecha_hora,via_conformado,rut_personal])
        id_counter+=1

    return contactos

#aqui genero listas con datos necesarios para hacer las conexiones entre los diferentes atributos que me piden..
#de la forma correcta
id_horas = []
fecha_horas = []

with open('horas_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_horas.append(row['id'])
        fecha_horas.append(row['fecha_hora'])

ruts_personal = []

with open('personal_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['tipo'] == 'Médico':
            ruts_personal.append(row['rut'])
        elif row['tipo'] == 'Administra':
            ruts_personal.append(row['rut'])

#genero los contactos
contactos_data = generar_contactos(3675, id_horas, fecha_horas, ruts_personal)

#para guardarlos en un archivo.csv
with open('contactos_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "id_hora", "fecha_hora", "via_conformado", "rut_personal"])
    writer.writerows(contactos_data)

print("Datos de contactos generados correctamente.")