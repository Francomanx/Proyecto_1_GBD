from faker import Faker
import random
import csv
fake = Faker('es_CL')  # Usamos el proveedor de Chile en Faker

# Función para generar el RUT chileno
def generar_rut():
    rut = random.randint(10000000, 99999999)
    dv = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    return f"{rut}-{dv}"

# Crear datos de Personal
def generar_personal(num_medicos, num_administrativos, num_jefaturas):
    personal = []
    
    # Generar Médicos
    for _ in range(num_medicos):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"  # Nombre corto
        tipo = "Médico"
        fecha_ing = fake.date_this_decade()
        estado = 1  # Médico siempre habilitado
        porcentaje = random.randint(10, 30)  # Porcentaje aleatorio para médicos
        fonasa = random.choice(["si", "no"])  # Médico con o sin Fonasa
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])
    
    # Generar Administrativos
    for _ in range(num_administrativos):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"  # Nombre corto
        tipo = "Administra"
        fecha_ing = fake.date_this_decade()
        estado = 1  # Administrativo habilitado
        porcentaje = 0
        fonasa = "no"
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])
    
    # Generar Jefaturas
    for _ in range(num_jefaturas):
        nombre = fake.first_name()
        apellido = fake.last_name()
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = fake.email()
        nombre_corto = f"{nombre[0]}.{apellido}"  # Nombre corto
        tipo = "Jefatura"
        fecha_ing = fake.date_this_decade()
        estado = 0  # Jefaturas inicialmente deshabilitadas
        porcentaje = 0
        fonasa = "no"
        
        personal.append([rut, nombre, apellido, telefono, correo, nombre_corto, tipo, fecha_ing, estado, porcentaje, fonasa])

    return personal

# Generar 6 médicos, 8 administrativos, 3 jefaturas
personal_data = generar_personal(6, 8, 3)

# Guardar en un archivo CSV (o puedes insertar directamente en la base de datos)
with open('personal_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["rut", "nombre", "apellido", "telefono", "correo", "nombre_corto", "tipo", "fecha_ing", "estado", "porcentaje", "fonasa"])
    writer.writerows(personal_data)

print("Datos de personal generados correctamente.")
