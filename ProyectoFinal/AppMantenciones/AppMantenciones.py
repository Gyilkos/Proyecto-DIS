# las app no se comunican entre si solo usan sus sender para pedir informacion y la procesan con el receiver
import sqlite3
import time
import senderCamionetas

with open('archivo.txt', 'w') as archivo:
    archivo.write("True"+"\n")
    archivo.write("segunda linea con info")

archivo.close()

#seguirEsperando = [True]  # las listas pueden ser modificadas por funciones sin perder el valor fuera de estas
#informacionPedida = [""]

def pedirPatentesCamionetasMantenimiento():
    # mandar mensaje con peticion a receiverCamionetas mediante senderCamionetas
    senderCamionetas.mandarMensajeCamionetas("20 ") #el primer digito representa que peticion es, por ejemplo el 1 es pedir kilometraje camionetas, el segundo digito denota si es una peticion (0) o una respuesta a esta peticion(1)

def cambiarEstadoCamioneta(camioneta:str,estado:str):
    senderCamionetas.mandarMensajeCamionetas("30 "+camioneta+" "+estado)

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
        print("2: Iniciar Mantencion y actualizar kilometraje")
        print("3: Terminar Mantencion y actualizar ProximoMantenimiento")

        print("="*30)
        

        respuesta = input(": ")


        # Acciones
        if respuesta == "1":
            # Mostrar lista con info de las patentes que no esten en arriendo (disponibles y en mantenimiento)
            informacionPedida = ""
            pedirPatentesCamionetasMantenimiento()
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
            
            # formato:Codigo patente,estado patente,estado
            
            lista_autos = informacionPedida[2:].split(" ")
            lista_autos_formateada = []
            
            for datosAuto in lista_autos:
                datos = datosAuto.split(",")
                lista_autos_formateada.append(datos)
                #print(f"Patente: {datos[0]}, Kilometraje: {datos[1]}")
            #print(lista_autos_formateada)
            
            
            #formateo correcto para la query
            query = "("
            for datosAuto in lista_autos_formateada:
                query += "'"+ datosAuto[0]+"',"
            query = query.strip(",")
            query += ");"
            query = "SELECT Patente, Kilometraje ,ProximaMantencion FROM Mantencion WHERE Patente IN " + query

            #print(query)
            #print(query)

            con = sqlite3.connect("DBmantencion.db")

            cur = con.cursor()
            cur.execute(query)
            respuestaQuery = cur.fetchall()
            print("+"*10)
            print("estos son los autos en mantenimiento")
            for fila in respuestaQuery:
                # fila es una tupla que contiene los valores de las columnas
                patente, kilometraje ,proximaMantencion = fila
                estado = 0
                
                #buscar estado en lista_autos_formateada
                for datosAuto in lista_autos_formateada:
                    if datosAuto[0] == patente:
                        estado = datosAuto[1]
                    


                print(f"Patente: {patente}, Estado: {estado}, Kilometraje: {kilometraje}, ProximaMantencion: {proximaMantencion}")
            print("+"*10)
            con.commit()
            con.close()


            
            
            #print(informacionPedida)
            

        elif respuesta == "2":
            # Iniciar Mantencion
            patenteIniciarMantencion = input("Ingrese la patente del auto para hacerle mantencion: ").upper()
            nuevoKilometraje = input("ingrese el nuevo kilometraje: ")
            
            cambiarEstadoCamioneta(patenteIniciarMantencion,"0")   #0 por que inicia mantencion
        

            # actualizar kilometraje
            autoDisponible = False
            try:
                con = sqlite3.connect("DBmantencion.db")

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

            

                  


        elif respuesta == "3":
            # terminar mantencion 
            patenteTerminarMantencion = input("Ingrese la patente del auto para hacerle mantencion: ").upper()
            nuevaProximaMantencion = input("ingrese la nueva ProximaMantencion: ")
            
            cambiarEstadoCamioneta(patenteTerminarMantencion,"1")   #1 por que  termina mantencion y queda disponible
            
        
            # actualizar porxima mantencion
            autoDisponible = False
            try:
                con = sqlite3.connect("DBmantencion.db")

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
           
            

if __name__ == '__main__':
    main()