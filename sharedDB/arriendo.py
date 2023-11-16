# Imports
import sqlite3

# Datos Generales


# *Mostrar lista (Disponibles)
# Estado, Kilometraje
def showList():
    print("Show List")
    # Realizar una función SELECT
    con = sqlite3.connect("Shared.db")

    cur = con.cursor()
    cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 1;")

    respuestaQuery = cur.fetchall()

    string = "("
    for fila in respuestaQuery:
        fila = str(fila).strip('(),')
        string += fila + ","
    string = str(string).strip(',')
    string += ')'
    #print(string)

    cur.execute("SELECT Patente, Kilometraje FROM Mantencion WHERE Patente IN" + string + ';')
    
    respuestaQuery = cur.fetchall()
    for fila in respuestaQuery:
        columna1, columna2 = fila
        print("Patente: " + str(columna1) + " | Kilometraje: " + str(columna2))



    # Imprimir cada componente en bucle
    
    # Cerrar la conección
    con.commit()
    con.close()

# *Arriendo Auto
# Patente, Estado
def rentCar():
    print("Rent Car")
    patenteArrendar = input("Ingrese la patente del auto para arrendar: ").upper()
    autoDisponible = False
    try:
        #query para verificar que este la patente y el auto disponibles
        con = sqlite3.connect("Shared.db")
        cur = con.cursor()
        cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 1 AND Patente = '"+ patenteArrendar+ "';")
        if len(cur.fetchall()) == 0:
            print("ERROR:Revise que el vehiculo esta disponible(len=0)")
        else:
            autoDisponible = True
        
        con.commit()
        con.close()
    except:
        print("ERROR:Revise que el vehiculo esta disponible(except)")
    if autoDisponible == True:
        #Hacer query para cambiar estado a Arrendado (2)
        try:
            con = sqlite3.connect("Shared.db")
            cur = con.cursor()
            cur.execute("UPDATE Camioneta SET Estado = 2 WHERE Patente = '"+patenteArrendar+"';")
            con.commit()
            con.close()
            print("+"*10)
            print("Arriendo de "+patenteArrendar+" realizado con exito")
            print("+"*10)
        except:
            print("ERROR: hubo problemas con su arriendo intente denuevo")

# *Devolver auto
# Patente, Estado, Kilometraje (actualizado)
def releaseCar():
    print("Rent Car")
    patenteArrendar = input("Ingrese la patente del auto para arrendar: ").upper()
    autoDisponible = False
    try:
        #query para verificar que este la patente y el auto Arrendado
        con = sqlite3.connect("Shared.db")
        cur = con.cursor()
        cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 2 AND Patente = '"+ patenteArrendar+ "';")
        if len(cur.fetchall()) == 0:
            print("ERROR:Revise que el vehiculo esta disponible(len=0)")
        else:
            autoDisponible = True
        
        con.commit()
        con.close()
    except:
        print("ERROR:Revise que el vehiculo esta disponible(except)")
    if autoDisponible == True:
        #Hacer query para cambiar estado a Disponible (1)
        try:
            con = sqlite3.connect("Shared.db")
            cur = con.cursor()
            cur.execute("UPDATE Camioneta SET Estado = 1 WHERE Patente = '"+patenteArrendar+"';")
            con.commit()
            con.close()
            print("+"*10)
            print("Entrega de "+patenteArrendar+" realizado con exito")
            print("+"*10)
        except:
            print("ERROR: hubo problemas con su arriendo intente denuevo")

# *Main
# Menu
def showMenu():
    print("="*30)
    print("App Camionetas")
    print("Acciones:")
    print("1: Mostrar Listado Camionetas")
    print("2: Arrendar Auto")
    print("3: Entregar Auto")
    #print("4: Salir")
    print("="*30)

#Testing
salirMenu = False
while salirMenu != True:
    showMenu()
    respuesta = input(": ")
    match respuesta:
        case "1":
            showList()
        case "2":
            rentCar()
        case "3":
            releaseCar()
        #case "4":
        #    salirMenu = True
        case _:
            print("")
#showList()

'''
print("="*30)
        print("App Camionetas")
        print("Acciones:")
        print("1: Mostrar Listado Camionetas")
        print("2: Arrendar Auto")
        print("3: Entregar Auto")

        print("="*30)
        respuesta = input(": ")
'''