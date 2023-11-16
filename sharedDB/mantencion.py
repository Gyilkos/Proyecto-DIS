# Imports
import sqlite3



# *Mostrar lista
# Patente, Estado, Kilometraje,ProximaMantencion
def showList():
    print("Show List")
    #buscar patentes de autos disponibles y mantenimiento (estado: 0 y 1) y devolver las patentes
    #print("peticion patentes y estados de no arrendadas")
    con = sqlite3.connect("Shared.db")
    cur = con.cursor()
    cur.execute("SELECT Patente, Estado FROM Camioneta WHERE Estado = 0 OR Estado = 1;")
    respuestaQuery = cur.fetchall()
    respuesta = ""
    for fila in respuestaQuery:
        # fila es una tupla que contiene los valores de las columnas
        columna1, columna2 = fila
        respuesta += " "+str(columna1) + ","+ str(columna2) 
        #print(f"Columna1: {columna1}, Columna2: {columna2}")
    
    respuesta = respuesta[1:]
    respuesta = respuesta.split(" ")
    matrizPatenteEstado = []
    listaPatentes = []
    for x in respuesta:
        parDatos = x.split(",")
        matrizPatenteEstado.append(parDatos)
        listaPatentes.append(parDatos[0])
    print(matrizPatenteEstado)
    print(listaPatentes)


    string = "("
    for patente in listaPatentes:
        
        string += "'"+patente + "',"
    string = str(string).strip(',')
    string += ')'
    print(string)
    cur.execute("SELECT Patente, Kilometraje FROM Mantencion WHERE Patente IN" + string + ';')

    con.commit()
    con.close()

# *Actualizar kilometros
# Patente, Kilometraje
def setKilometer(patente, newKilometer):
    print("Set Kilometer")
    # Realizar función SELECT para buscar auto
    # Actualizar dato de la base de datos (Kilometraje = newKilometer)
    # Cerrar la conección

# *Actualizar proxima mantencion
# Patente
def setNextMaintence(patente, newNextMaintence):
    print("Set Next Maintence")
    # Realizar función SELECT para buscar auto
    # Actualizar dato de la base de datos (nextMaintence = newNextMaintence)
    # Cerrar la conección

# *Iniciar mantencion
# Patente, Estado
def startMaintence(patente):
    print("Start Maintence")
    # Realizar función SELECT para buscar auto
    # Actualizar dato de la base de datos (Estado => 1)
    # Cerrar la conección

# *Terminar mantencion
# Patente, Estado
def finishMaintence(patente):
    print("Finish Maintence")
    # Realizar función SELECT para buscar auto
    # Actualizar dato de la base de datos (Estado => 0)
    # Cerrar la conección

# *Main
# Menu
def showMenu():
    print("="*30)
    print("App Camionetas")
    print("Acciones:")
    print("1: Mostrar Listado Camionetas")
    print("2: ")
    print("3: ")
    print("4: ")
    print("="*30)

salirMenu = False
while salirMenu != True:
    showMenu()
    respuesta = input(": ")
    match respuesta:
        case "1":
            showList()
        case "2":
            print()
        case "3":
            print()
        #case "4":
            #print("")
        case _:
        #    salirMenu = True
            print("")

#showList()