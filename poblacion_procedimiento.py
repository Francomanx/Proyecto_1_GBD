from faker import Faker
import random
import csv
fake = Faker('es_CL')  #con esto practicamente los valores van a ser en su mayoria chilenos (nombres, direcciones, etc)


#con este metodo crearemos los datos de los procedimientos
def generar_procedimiento(num_procedimientos):
    procedimientos = []
    nombre_procedimientos = ["Consulta Medica", "Cirugia"]
    numero_cirugia = 1
    # Generar pacientes
    for i in range(1,num_procedimientos):
        id = i
        nombre = random.choice(nombre_procedimientos)
        if nombre=="Consulta Medica":
            area = "Consulta"
            valor = 50500
        elif nombre=="Cirugia":
            nombre = f"Cirugia {numero_cirugia}"
            area = "Pabellon"
            valor = random.randint(1500000, 3500000)
            numero_cirugia=+1
        procedimientos.append([id, nombre, area, valor])

    return procedimientos

#Generaremos 16 procedimientos
procedimiento_data = generar_procedimiento(16)

# Guardar en un archivo CSV para importarlo a la base de datos
with open('procedimiento_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "nombre", "area", "valor"])
    writer.writerows(procedimiento_data)          
print("Datos de personal generados correctamente.")
