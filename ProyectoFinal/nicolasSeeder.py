import sqlite3
import random

#generar datos falsos
listaCamionetas = []
listaMantenciones = []
listaLetrasNumeros = "ABCDEFGHIJKLMNOPQRSTVWXYZ123456789"

NumeroDatos = 10


for i in range(NumeroDatos):
    camioneta = []

    patente = ""
    for i in range(6):
        index = random.randint(0,len(listaLetrasNumeros)-1)
        patente += listaLetrasNumeros[index]
    camioneta.append(patente)
    estado = str(random.randint(0,2))
    camioneta.append(estado)

    listaCamionetas.append(camioneta)

print(listaCamionetas)

for i in range(NumeroDatos):
    mantencion = []
    patente = listaCamionetas[i][0]
    kilometraje = str(random.randint(0,10000))
    proximaMantencion = str(int(kilometraje) + 1000) 
    mantencion.append(patente)
    mantencion.append(kilometraje)
    mantencion.append(proximaMantencion)
    listaMantenciones.append(mantencion)
print(listaMantenciones)



#Crear y poblar Database Camioneta

con = sqlite3.connect("DBcamioneta.db")

cur = con.cursor()
cur.execute("CREATE TABLE Camioneta (Patente varchar(6) PRIMARY KEY,Estado INTEGER);")
for i in range(NumeroDatos):
    cur.execute("INSERT INTO Camioneta (Patente, Estado) VALUES ('"+listaCamionetas[i][0] +"', '"+listaCamionetas[i][1] +"');")
    

con.commit()
con.close()



#Crear y poblar Database Mantencion

con = sqlite3.connect("DBmantencion.db")

cur = con.cursor()
cur.execute("CREATE TABLE Mantencion (Patente varchar(6) PRIMARY KEY,Kilometraje INTEGER ,ProximaMantencion INTEGER);")
for i in range(NumeroDatos):
    cur.execute("INSERT INTO Mantencion (Patente, kilometraje, ProximaMantencion) VALUES ('"+listaMantenciones[i][0] +"', '"+listaMantenciones[i][1] +"', '"+listaMantenciones[i][2] +"');")


con.commit()
con.close()