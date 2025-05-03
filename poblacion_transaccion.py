from faker import Faker
import random
import csv
from datetime import datetime, timedelta

fake = Faker('es_CL')

#Suposiciones relacionadas a transaccion

#Para las transacciones de consultas particulares y pabellón se
#emite una boleta, por lo que se debe dejar registro de su
#numeración

#En el caso de las consultas de pacientes que tienen previsión Fonasa
#y se atienden con un profesional con convenio Fonasa se les 
#debe vender un bono de consulta, dejando registro de su numeración.

#El atributo “váucher” tendrá la numeración del ticket emitido al
#pagar con “débito” o “crédito”

#Si un paciente tiene previsión Fonasa, el valor de la consulta médica 
#con médico con convenio es de $25.300, 
#para un médico sin convenio es de $35.000

#Si un paciente no tiene previsión deberá pagar el valor de la 
#atención particular $50.500

#Para generar transacciones necesito:
#id: int secuencial
#rut_personal: char asociado al rut de alguien del personal (solo medicos)
#id_hora: int asociado a id_hora de consulta, el cual esta asociado al id de hora
#rut_paciente: char asociado al rut_paciente de consulta
#fecha_hora: una fecha que servira como emision de la transaccion, este pagada o no
#monto: un int que tendra un valor dependiente de ciertas condiciones
#estado: un int que dependiendo de su valor, se sabra si la transaccion esta pagada o no

#AVISO en cuanto a estado: los valores que tendra estado son
#0 = no pagada
#1 = pagada
#el valor de estado depende del estado de la consulta asociada, los cuales son
#0 = reservada
#1 = confirmada
#3 = pagada
#4 = finalizada
#luego de una conversacion, tomamos la decision de que el estado de transaccion SOLO cambiaria
#de valor a 1 (pagada) si la consulta asociada tuviera como estado 3 (pagada), puesto que a pesar de que existe
#el estado 4 (finalizada) no se especifica si esta finalizada y pagada, o finalizada pero no pagada

#mediopago: int que tendra un valor dependiente de que medio de pago se haya utilizado para pagar la transaccion
#bono: un int que tendra un valor secuencial dependiendo de si se registra un bono o no
#boleta: un int que tendra un valor secuencial dependiendo de si se registra una boleta o no
#vaucher: un int que tendra un valor secuencial dependiendo de si se registra un vaucher o no

#función para generar transacciones
def generar_transacciones(id_horas_de_consulta, id_procedimientos_de_consulta, estados_de_consulta, fonasa_de_medicos, rut_pacientes_de_consultas, rut_de_pacientes, prevision_de_pacientes, id_de_horas, rut_medico_de_horas, id_de_procedimientos, monto_de_procedimientos, fecha_horas_de_hora, rut_de_medicos):
    transacciones = []
    id_counter = 1
    bono_counter = 1
    boleta_counter = 1
    vaucher_counter = 1

    for i in range(len(id_horas_de_consulta)):
        id_hora = id_horas_de_consulta[i]
        id_procedimiento = id_procedimientos_de_consulta[i]
        rut_paciente = rut_pacientes_de_consultas[i]
        #el rut_personal debe ser el mismo rut del medico de la hora
        for j in range(len(id_de_horas)):
            if id_de_horas[j]==id_hora:
                rut_personal = rut_medico_de_horas[j]
        try:
            fecha_base = datetime.strptime(fecha_horas_de_hora[int(id_hora)-1], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            #en caso de que los segundos no funcionen
            fecha_base = datetime.strptime(fecha_horas_de_hora[int(id_hora)-1], "%Y-%m-%d %H:%M")

        fecha_hora = fecha_base + timedelta(days=random.randint(-2, 2)) #la transaccion se emite en un lapso de 4 dias (2 antes y 2 despues)

        #AVISO: la seccion que esta por venir esta pesimamente optimizada (o eso creo yo). si logro
        #encontrar una forma de simplificarlo u optimizarlo modificare el codigo, pero sino lo dejare asi
        #puesto que luego de unas pruebas pude verificar que los calculos que se relizan en esta
        #seccion igual estan buenos

        #en cuanto al estado de la transaccion
        #podria tener dos valores
        #1 si esta pagada y 0 si no esta pagada
        #y para adquirir este valor, hay que buscar el estado de la consulta y ver que dice
        if estados_de_consulta[i]=='3':
            #esta pagada
            estado = 1
            mediopago = random.choice([1,2,3,4])#1.credito 2.debito 3.transferencia 4.efectivo
            if mediopago==1 or mediopago==2:#si fue pagada con credito o debito, se enumera el vaucher
                vaucher = vaucher_counter
                vaucher_counter +=1
            else:
                vaucher = 0
            #aqui verificamos si se entrega boleta o bono junto con el calculo del monto
            for j in range(len(rut_de_pacientes)):
                if rut_de_pacientes[j]==rut_paciente:
                    prevision = prevision_de_pacientes[j] 
            if id_procedimiento == '1':#si es una consulta medica
                #hay que ver si el medico asociado a la hora tiene convenio fonasa y el paciente tambien
                for j in range(len(rut_de_medicos)):
                    if rut_de_medicos[j]==rut_personal:                   
                        if fonasa_de_medicos[j]=='si' and prevision=='Fonasa':
                            monto = 25300
                            bono = bono_counter
                            bono_counter+=1
                            boleta = 0
                        elif fonasa_de_medicos[j]=='no'and prevision=='Fonasa':
                            monto = 35000
                            bono = 0
                            boleta = 0
                        elif prevision!='Fonasa':
                            monto = 50500
                            bono = 0
                            boleta = boleta_counter
                            boleta_counter+=1  
            else:
                #hay que buscar el monto del procedimiento hecho
                for j in range(len(id_de_procedimientos)):
                    if id_de_procedimientos[j] == id_procedimiento:
                        monto = monto_de_procedimientos[j]
                        bono = 0
                        boleta = boleta_counter
                        boleta_counter+=1
        else:
            #no esta pagada
            estado = 0
            mediopago = 0
            vaucher = 0
            #para esto debemos buscar que prevision tiene el paciente
            for j in range(len(rut_de_pacientes)):
                if rut_de_pacientes[j]==rut_paciente:
                    prevision = prevision_de_pacientes[j] 
            if id_procedimiento == '1':#si es una consulta medica
                #hay que ver si el medico asociado a la hora tiene convenio fonasa y el paciente tambien
                for j in range(len(rut_de_medicos)):
                    if rut_de_medicos[j]==rut_personal:                   
                        if fonasa_de_medicos[j]=='si' and prevision=='Fonasa':
                            monto = 25300
                            bono = 0
                            boleta = 0
                        elif fonasa_de_medicos[j]=='no'and prevision=='Fonasa':
                            monto = 35000
                            bono = 0
                            boleta = 0
                        elif prevision != 'Fonasa':
                            monto = 50500
                            bono = 0
                            boleta = 0  
            else:
                #hay que buscar el monto del procedimiento hecho
                for j in range(len(id_de_procedimientos)):
                    if id_de_procedimientos[j] == id_procedimiento:
                        monto = monto_de_procedimientos[j]
                        bono = 0
                        boleta = 0
        transacciones.append([id_counter,rut_personal,id_hora,rut_paciente,fecha_hora.strftime('%Y-%m-%d %H:%M:%S'), monto, estado, mediopago, bono, boleta, vaucher])
        id_counter += 1

    return transacciones

#aqui genero listas con datos necesarios para hacer las conexiones entre los diferentes atributos que me piden..
#de la forma correcta
id_horas_de_consulta = []
id_procedimientos_de_consulta = []
estados_de_consulta = []
rut_pacientes_de_consulta = []
with open('consulta_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_horas_de_consulta.append(row['id_hora'])
        id_procedimientos_de_consulta.append(row['id_procedimiento'])
        estados_de_consulta.append(row['estado'])
        rut_pacientes_de_consulta.append(row['rut_paciente'])

fonasa_de_medicos = []
rut_de_medicos = []
with open('personal_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['tipo']=='Médico':
            fonasa_de_medicos.append(row['fonasa'])
            rut_de_medicos.append(row['rut'])

rut_de_pacientes = []
prevision_de_pacientes = []
with open('paciente_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rut_de_pacientes.append(row['rut'])
        prevision_de_pacientes.append(row['prevision'])

id_de_horas = []
rut_medico_de_horas = []
fecha_horas_de_hora = []
with open('horas_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_de_horas.append(row['id'])
        rut_medico_de_horas.append(row['medico'])
        fecha_horas_de_hora.append(row['fecha_hora'])

id_de_procedimientos = []
monto_de_procedimientos = []
with open('procedimiento_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        id_de_procedimientos.append(row['id'])
        monto_de_procedimientos.append(row['valor'])



#genero los datos de transacciones
transacciones_data = generar_transacciones(id_horas_de_consulta, id_procedimientos_de_consulta, estados_de_consulta, fonasa_de_medicos, rut_pacientes_de_consulta, rut_de_pacientes, prevision_de_pacientes, id_de_horas, rut_medico_de_horas, id_de_procedimientos, monto_de_procedimientos, fecha_horas_de_hora, rut_de_medicos)

#y los guardo en un archivo.csv
with open('transaccion_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["id","rut_personal","id_hora","rut_paciente","fecha_hora","monto","estado","mediopago","bono","boleta","vaucher"])
    writer.writerows(transacciones_data)

print("Datos de transacciones generados correctamente.")