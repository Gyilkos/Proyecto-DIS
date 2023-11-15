# las app no se comunican entre si solo usan sus sender para pedir informacion y la procesan con el receiver
import sqlite3
import time
import senderMantenciones

with open('archivo.txt', 'w') as archivo:
    archivo.write("True"+"\n")
    archivo.write("segunda linea con info")

archivo.close()

#seguirEsperando = [True]  # las listas pueden ser modificadas por funciones sin perder el valor fuera de estas
#informacionPedida = [""]

def pedirKilometrajesCamionetas(patentes):
    # mandar mensaje con peticion a receiverMantenciones mediante senderMantenciones
    senderMantenciones.mandarMensajeMantenciones("10 "+ patentes) #el primer digito representa que peticion es, por ejemplo el 1 es pedir listado camionetas, el segundo digito denota si es una peticion (0) o una respuesta a esta peticion(1)

    # Luego su reciever va a responder, pero por mientras tenemos que esperar hasta que nos respondan
def inicializarEspera():
    with open('archivo.txt', 'w') as archivo:
        # El archivo se abre en modo escritura ('w'), lo que elimina el contenido existente
        
        # Escribir una nueva línea en el archivo
        archivo.write("True\n")
        archivo.close()

def esperar():
    seguirEsperando = True
    with open('archivo.txt', 'r') as archivo:
        linea = archivo.readline()
        linea = linea.strip("\n") 
        #print(linea)  #print(linea, end='')  # 'end='' evita la impresión de líneas en blanco adicionales
        seguirEsperando = linea
        archivo.close()
    if seguirEsperando == "True":
        print("Esperando...")
        time.sleep(1)
        return esperar()
    else:
        print("fin espera")
        return




def main():
    # menu simple
    salirMenu = False
    while salirMenu != True:
        print("="*30)
        print("App Camionetas")
        print("Acciones:")
        print("1: Mostrar Listado Camionetas")
        print("2: Arrendar Auto")
        print("3: Entregar Auto")

        print("="*30)
        

        respuesta = input(": ")


        # Acciones
        if respuesta == "1":
            #mostrar listado Camionetas
            #buscar patentes de autos disponibles (estado: 1) y pedir el kilometraje a 
            # esas patentes por el pedirKilometrajesCamionetas()
            stringPatentes = ""
            con = sqlite3.connect("DBcamioneta.db")
            cur = con.cursor()
            cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 1;")
            for row in cur.fetchall():
              #print(row[0])
              stringPatentes += " "+str(row[0])
            con.commit()
            con.close()

            
            
            

            informacionPedida = ""
            pedirKilometrajesCamionetas(stringPatentes)
            inicializarEspera() #setea True en la primera linea archivo.txt
            esperar()    #espera hasta que cambie la variable de espera (primera linea archivo.txt)
            # llega la info a nuestro archivo.txt cambiando la primera linea a False , para salir de esperar y pone la info en la segunda linea
            # ahora deberiamos de contar con la informacion en la segunda linea del archivo

            with open('archivo.txt', 'r') as archivo:
                linea = archivo.readline()
                #print(linea)
                linea = archivo.readline()
                linea = linea.strip("\n") 
                #print(linea)
                informacionPedida = linea
            archivo.close()


            print("+"*10)
            print("estos son los autos disponibles y su kilometraje")
            lista_autos = informacionPedida[2:].split(" ")
            for datosAuto in lista_autos:
                datos = datosAuto.split(",")
                print(f"Patente: {datos[0]}, Kilometraje: {datos[1]}")
            
            #print(informacionPedida)
            print("+"*10)

        elif respuesta == "2":
            #Arrendar Auto
            patenteArrendar = input("Ingrese la patente del auto para arrendar: ").upper()
            autoDisponible = False
            try:
                #query para verificar que este la patente y el auto disponibles
                con = sqlite3.connect("DBcamioneta.db")
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
                    con = sqlite3.connect("DBcamioneta.db")

                    cur = con.cursor()
                    cur.execute("UPDATE Camioneta SET Estado = 2 WHERE Patente = '"+patenteArrendar+"';")
                    con.commit()
                    con.close()

                    print("+"*10)
                    print("Arriendo de "+patenteArrendar+" realizado con exito")
                    print("+"*10)
                except:
                    print("ERROR: hubo problemas con su arriendo intente denuevo")
                    
                    


        elif respuesta == "3":
            #Entregar auto
            patenteEntregado = input("Ingrese la patente del auto para entregar: ").upper()
            autoDisponible = False
            try:
                #query para verificar que este la patente y el auto arrendado 
                con = sqlite3.connect("DBcamioneta.db")
                cur = con.cursor()
                cur.execute("SELECT Patente FROM Camioneta WHERE Estado = 2 AND Patente = '"+ patenteEntregado+ "';")
                if len(cur.fetchall()) == 0:
                    print("ERROR:Ingrese bien la patente(len=0)")

                else:
                    autoDisponible = True
                
                con.commit()
                con.close()
            except:
                print("ERROR:Ingrese bien la patente(except)")
        
            if autoDisponible == True: #todo correcto, se procede a la entrega
                #Hacer query para cambiar estado a disponible (1)
                try:
                    con = sqlite3.connect("DBcamioneta.db")

                    cur = con.cursor()
                    cur.execute("UPDATE Camioneta SET Estado = 1 WHERE Patente = '"+patenteEntregado+"';")
                    con.commit()
                    con.close()

                    print("+"*10)
                    print("Entrega de "+patenteEntregado+" realizado con exito")
                    print("+"*10)
                except:
                    print("ERROR: hubo problemas con su entrega intente denuevo")
            
            

if __name__ == '__main__':
    main()