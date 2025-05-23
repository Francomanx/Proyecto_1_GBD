from faker import Faker
import random
import csv
from datetime import datetime, timedelta

fake = Faker('es_CL')

#proceso para generar horas
def generar_horas(num_horas, medicos, administrativos):
    horas = []
    id_counter = 1

    #calculo para conseguir la cantidad de horas que estaran activas (95%)
    total_horas = int(num_horas * 1.05)  

    for _ in range(total_horas):
        #generacion de fecha y hora en base a un solo mes juasjuas
        fecha_base = datetime(2025, 4, 1, 0, 0)  #1 de abril de 2025 a las 12 am
        dias_offset = random.randint(1, 30)  #1 a 30 días
        horas_offset = random.randint(8, 18)  #desde las 8 de la mñana hasta las 18 de la tarde
        minutos_offset = random.choice([0, 15, 30, 45])  #intervalos de 15 minutos
        fecha_hora = fecha_base + timedelta(days=dias_offset, hours=horas_offset, minutes=minutos_offset)

        #asignamos a un medico y un personal al azar
        medico = random.choice(medicos)
        personal = random.choice(administrativos)

        #definimos el tipo de procedimiento (70% consulta médica, 30% cirugía/pabellón)
        if random.random() < 0.7:
            tipo = 1 #consulta medica
            web = random.choice(['si','no'])
        else:
            tipo = 2 #pabellon
            web = 'no'
        
        #sobrecupo.
        if any(h[2] == medico and h[1] == fecha_hora for h in horas):
            sobrecupo = 'si'
        else:
            sobrecupo = 'no'

        #definicion de estado (5% anuladas)
        if random.random() < 0.05:
            estado = 2 # cancelada
        else:
            estado = random.choice([0,1]) #disponible o reservada

        horas.append([id_counter,fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),medico,personal,tipo,web,sobrecupo,estado])

        id_counter += 1

    return horas


medicos = []
administrativos = []
#se pueden cargar archivos csv, lo que me ahorra la lata de andar haciendo arraylist con mil ruts :O
with open('personal_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['tipo'] == 'Médico':
            medicos.append(row['rut'])
        elif row['tipo'] == 'Administra':
            administrativos.append(row['rut'])

#generamos horas
horas_data = generar_horas(3500, medicos, administrativos)

#y guardamps en archivo.csv
with open('horas_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "fecha_hora", "medico", "personal", "tipo", "web", "sobrecupo", "estado"])
    writer.writerows(horas_data)

print("Datos de horas generados correctamente.")
