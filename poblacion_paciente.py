from faker import Faker
import random
import csv
import unicodedata
fake = Faker('es_CL')  #con esto practicamente los valores van a ser en su mayoria chilenos (nombres, direcciones, etc)

#metodo para generar un rut
def generar_rut():
    rut = random.randint(10000000, 99999999)
    dv = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    return f"{rut}-{dv}"

# Método para limpar texto.
def limpiar_texto(texto):
    if isinstance(texto, str):
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

#con este metodo crearemos los datos de los pacientes
def generar_paciente(num_pacientes):
    pacientes = []
    previsiones = ["Fonasa", "Isapre"]

    #generar pacientes
    for _ in range(num_pacientes):
        nombres = limpiar_texto(fake.first_name() + " " + fake.first_name())
        apellido_p = limpiar_texto(fake.last_name_male())
        apellido_m = limpiar_texto(fake.last_name_female())
        rut = generar_rut()
        telefono = "+569" + str(random.randint(10000000, 99999999))
        correo = limpiar_texto(fake.email())
<<<<<<< HEAD
        direccion = limpiar_texto(fake.street_name()[:50])
=======
        direccion = limpiar_texto(fake.street_name()[:50]) #solo se usan direcciones que no superen los 50 caracteres
>>>>>>> 3a26ad0f46a1c7f6778e2b2069fbb49de1653b6b
        prevision = random.choice(previsiones)
        fecha_nac = fake.date_of_birth(minimum_age=0, maximum_age=90)
        fecha_reg = fake.date_this_decade()
        
        pacientes.append([rut, nombres, apellido_p, apellido_m, 
                          telefono, correo, direccion, prevision, fecha_nac, fecha_reg])

    return pacientes

#generaremos 250 pacientes
paciente_data = generar_paciente(250)

#y los guardamos en un archivo.csv
with open('paciente_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["rut", "nombres", "apellido_p", "apellido_m", "telefono", "correo", "direccion", "prevision", "fecha_nac", "fecha_reg"])
    writer.writerows(paciente_data)          
print("Datos de personal generados correctamente.")
