from faker import Faker
import random
import csv
fake = Faker('es_CL')

#metodo para generar rut chileno
def generar_rut():
    rut = random.randint(10000000, 99999999)
    dv = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    return f"{rut}-{dv}"

#metodo para crear datos de personal
def generar_personal(num_medicos, num_administrativos, num_jefaturas):
    personal = []
    
    #generamos medicos
    for _ in range(num_medicos):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"
        tipo = "Médico"
        fecha_ing = fake.date_this_decade()
        estado = 1
        porcentaje = random.randint(10, 30)
        fonasa = random.choice(["si", "no"])
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])
    
    #generamos administrativos
    for _ in range(num_administrativos):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"
        tipo = "Administra"
        fecha_ing = fake.date_this_decade()
        estado = 1
        porcentaje = 0
        fonasa = "no"
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])
    
    #generamos jefaturas
    for _ in range(num_jefaturas):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"
        tipo = "Jefatura"
        fecha_ing = fake.date_this_decade()
        estado = 0
        porcentaje = 0
        fonasa = "no"
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])

    return personal

#generamos 6 médicos, 8 administrativos, 3 jefaturas
personal_data = generar_personal(6, 8, 3)

#y lo guardamos en un archivo.csv
with open('personal_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["rut", "nombre", "apellido", "telefono", "correo", "nombre_corto", "tipo", "fecha_ing", "estado", "porcentaje", "fonasa"])
    writer.writerows(personal_data)

print("Datos de personal generados correctamente.")
