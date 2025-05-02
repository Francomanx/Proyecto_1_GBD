from faker import Faker
import random
import csv
fake = Faker('es_CL')  #con esto practicamente los valores van a ser en su mayoria chilenos (nombres, direcciones, etc)


#con este metodo crearemos los datos de los procedimientos
def generar_procedimiento(num_procedimientos):
    procedimientos = []

    for i in range(1,num_procedimientos + 1):
        id = i
        if i==1:#El primer procedimiento sera una consulta medica
            nombre = "Consulta Médica"
            area = "Consulta"
            valor = 50500
        else:#El resto seran cirugias
            nombre = f"Cirugia {id - 1}"
            area = "Pabellon"
            valor = random.randint(1500000, 3500000)
        procedimientos.append([id, nombre, area, valor])

    return procedimientos

#Generaremos 16 procedimientos
procedimiento_data = generar_procedimiento(16)

#Y lo guardamos en un archivo.csv
with open('procedimiento_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "nombre", "area", "valor"])
    writer.writerows(procedimiento_data)          
print("Datos de procedimientos generados correctamente.")
