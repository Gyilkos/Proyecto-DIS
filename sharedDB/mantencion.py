# Imports
import sqlite3



# *Mostrar lista
# Patente, Estado, Kilometraje,ProximaMantencion
def showList():
    #buscar patentes de autos disponibles y mantenimiento (estado: 0 y 1) y devolver las patentes
    #print("peticion patentes y estados de no arrendadas")

    #Abrir conección
    con = sqlite3.connect("Shared.db")
    cur = con.cursor()

    #Realizar query de vehículos disponibles y en mantenimiento
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
    #print(matrizPatenteEstado)
    #print(listaPatentes)


    string = "("
    for patente in listaPatentes:
        
        string += "'"+patente + "',"
    string = str(string).strip(',')
    string += ')'
    #print(string)

    #Realizar query de vehículos y su kilometraje
    cur.execute("SELECT Patente, Kilometraje,ProximaMantencion FROM Mantencion WHERE Patente IN" + string + ';')
    respuestaQuery = cur.fetchall()
    respuesta = ""
    for fila in respuestaQuery:
        # fila es una tupla que contiene los valores de las columnas
        columna1, columna2, columna3 = fila
        for datos in matrizPatenteEstado:
            if columna1 == datos[0]:
                datos.append(columna2)
                datos.append(columna3)

    
    #print(matrizPatenteEstado)
    for i in matrizPatenteEstado:
        print(i)

    #Cerrar la conección
    con.commit()
    con.close()

# *Actualizar kilometros
# Patente, Kilometraje
def IniciarMantencion():
    # Iniciar Mantencion
    patenteIniciarMantencion = input("Ingrese la patente del auto para hacerle mantencion: ").upper()
    nuevoKilometraje = input("ingrese el nuevo kilometraje: ")
    
    
    #hacer query local para cambiar el estado
    con = sqlite3.connect("Shared.db")
    cur = con.cursor()
    cur.execute("UPDATE Camioneta SET Estado = 0 WHERE Patente = '"+patenteIniciarMantencion+"';")
    
    
    con.commit()
    con.close()
    

    # actualizar kilometraje
    autoDisponible = False
    try:
        con = sqlite3.connect("Shared.db")

        cur = con.cursor()
        cur.execute("UPDATE Mantencion SET Kilometraje = "+nuevoKilometraje+" WHERE Patente = '"+patenteIniciarMantencion+"';")
        
    
        autoDisponible = True
        
        con.commit()
        con.close()

        
    except:
        print("ERROR: hubo problemas con actualizar kilometraje intente denuevo(except)")
    
    if autoDisponible == True:
        print("+"*10)
        print("Vehiculo "+patenteIniciarMantencion+" en mantenimiento, kilometraje actualizado con exito")
        print("+"*10)
    else:
        print("ERROR: hubo problemas con actualizar kilometraje intente denuevo(autoDIsponible)")

# *Actualizar proxima mantencion
# Patente
'''
def setNextMaintence():
    patente = input("Ingrese la patente del auto para fijar proxima mantencion: ").upper()
    nuevaProximaMantencion = input("ingrese la nueva ProximaMantencion: ")
    
    
    

    # actualizar porxima mantencion
    autoDisponible = False
    try:
        con = sqlite3.connect("DBmantencion.db")

        cur = con.cursor()
        cur.execute("UPDATE Mantencion SET ProximaMantencion = "+nuevaProximaMantencion+" WHERE Patente = '"+patente+"';")
        
    
        autoDisponible = True
        
        con.commit()
        con.close()

        
    except:
        print("ERROR: hubo problemas con actualizar nuevaProximaMantencion intente denuevo(except)")
    
    if autoDisponible == True:
        print("+"*10)
        print("Vehiculo "+patente+" , ProximaMantencion actualizado con exito")
        print("+"*10)
    else:
        print("ERROR: hubo problemas con actualizar nuevaProximaMantencion intente denuevo(autoDIsponible)")
'''

# *Iniciar mantencion
# Patente, Estado
'''
def startMaintence():
    # Realizar función SELECT para buscar auto
    # Actualizar dato de la base de datos (Estado => 1)
    # Cerrar la conección
    # TODO: Testear
    patenteMantencion = input("Ingrese la patente del auto para iniciar mantención: ").upper()
    autoDisponible = False
    try:
        #query para verificar que este la patente y el auto disponible
        con = sqlite3.connect("Shared.db")
        cur = con.cursor()
        cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 1 AND Patente = '"+ patenteMantencion+ "';")
        print(cur)
        if len(cur.fetchall()) == 0:
            print("ERROR:Revise que el vehiculo esta disponible(len=0)")
        else:
            autoDisponible = True
        
        con.commit()
        con.close()
    except:
        print("ERROR:Revise que el vehiculo esta disponible(except)")
    if autoDisponible == True:
        #Hacer query para cambiar estado a Mantencion (0)
        try:
            con = sqlite3.connect("Shared.db")
            cur = con.cursor()
            cur.execute("UPDATE Camioneta SET Estado = 0 WHERE Patente = '"+patenteMantencion+"';")
            con.commit()
            con.close()
            print("+"*10)
            print("Inicio de mantención de "+patenteMantencion+" realizado con exito")
            print("+"*10)
        except:
            print("ERROR: hubo problemas con su arriendo intente denuevo")
'''

# *Terminar mantencion
# Patente, Estado
def FinalizarMantencion():
    # terminar mantencion 
    patenteTerminarMantencion = input("Ingrese la patente del auto para hacerle mantencion: ").upper()
    nuevaProximaMantencion = input("ingrese la nueva ProximaMantencion: ")
      
    #hacer query local para cambiar el estado
    con = sqlite3.connect("Shared.db")
    cur = con.cursor()
    cur.execute("UPDATE Camioneta SET Estado = 1 WHERE Patente = '"+patenteTerminarMantencion+"';")
    
    
    con.commit()
    con.close()
    #1 por que  termina mantencion y queda disponible
    

    # actualizar porxima mantencion
    autoDisponible = False
    try:
        con = sqlite3.connect("Shared.db")

        cur = con.cursor()
        cur.execute("UPDATE Mantencion SET ProximaMantencion = "+nuevaProximaMantencion+" WHERE Patente = '"+patenteTerminarMantencion+"';")
        
    
        autoDisponible = True
        
        con.commit()
        con.close()

        
    except:
        print("ERROR: hubo problemas con actualizar nuevaProximaMantencion intente denuevo(except)")
    
    if autoDisponible == True:
        print("+"*10)
        print("Vehiculo "+patenteTerminarMantencion+" ahora esta disponible, ProximaMantencion actualizado con exito")
        print("+"*10)
    else:
        print("ERROR: hubo problemas con actualizar nuevaProximaMantencion intente denuevo(autoDIsponible)")
    
# *Main
# Menu
def showMenu():
    print("="*30)
    print("App Camionetas")
    print("Acciones:")
    print("1: Mostrar Listado Camionetas")
    print("2: Iniciar Mantencion y Actualizar kilometros")
    print("3: Finalizar mantencion y Actualizar próxima mantención")
    print("4: Salir")
    print("="*30)

salirMenu = False
while salirMenu != True:
    showMenu()
    respuesta = input(": ")
    match respuesta:
        case "1":
            showList()
        case "2":
            IniciarMantencion()
        case "3":
            FinalizarMantencion()
        case "4":
            salirMenu = True
        case _:
            print("")
