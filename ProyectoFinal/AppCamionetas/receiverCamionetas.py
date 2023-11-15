import sys, os
import sqlite3
import pika
import senderMantenciones

import time

def main():
    #crea los parametros de coneccion
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # crea un canal con los parametros de la coneccion
    channel = connection.channel()

    # crea una cola con el nombre colaCamionetas
    channel.queue_declare(queue='colaCamionetas')

    #cada vez que llega un mensaje a la cola se llama esta funcion callback (esta es nuestra respuesta al mensaje)
    #primero definimos la funcion
    
    def callback(ch, method, properties, body):
        respuesta = ""
        body = str(body)[2:].strip("'")
        #print(body)
        if body[0] == "1" and body[1] == "1": #1 es la respuesta de pedir listado camionetas
            #print("Testetest")
            respuesta = body[2:]  #devuelve todo el texto exepto los primeros 2 caracteres (codigo de identificacion)
            # mandar info ordenada a AppCamionetas
            
            #print(respuesta)
            with open('archivo.txt', 'w') as archivo:
                # El archivo se abre en modo escritura ('w'), lo que elimina el contenido existente
                
                # Escribir una nueva línea en el archivo
                archivo.write("False\n")
                archivo.write(respuesta)
                archivo.close()
            
        elif body[0] == "2" and body[1] == "0": #2 es la peticion de camionetas no arrendadas
            #buscar patentes de autos disponibles y mantenimiento (estado: 0 y 1) y devolver las patentes
            #print("peticion patentes y estados de no arrendadas")
            con = sqlite3.connect("DBcamioneta.db")
            cur = con.cursor()
            cur.execute("SELECT Patente, Estado FROM Camioneta WHERE Estado = 0 OR Estado = 1;")
            respuestaQuery = cur.fetchall()
            for fila in respuestaQuery:
                # fila es una tupla que contiene los valores de las columnas
                columna1, columna2 = fila
                respuesta += " "+str(columna1) + ","+ str(columna2) 
                #print(f"Columna1: {columna1}, Columna2: {columna2}")
            
            con.commit()
            con.close()
            senderMantenciones.mandarMensajeMantenciones("21 "+respuesta)

        elif body[0] == "3" and body[1] == "0": #3 es la peticion de cambiar el estado de una camioneta 
            #A mantenimiento o disponible (0 o 1)
            print("peticion cambiar estado a mantencion o disponible")
            #print(body)
            respuesta = body[3:]
            respuesta = respuesta.split(" ")
            if respuesta[1] != "2":
                #hacer query local para cambiar el estado
                con = sqlite3.connect("DBcamioneta.db")
                cur = con.cursor()
                cur.execute("UPDATE Camioneta SET Estado = "+respuesta[1]+" WHERE Patente = '"+respuesta[0]+"';")
                
                
                con.commit()
                con.close()
            
            #print(respuesta)

            
        
        print(f" [x] ReceivedCamionetas {body}")

    #ahora subscribimos esta funcio a la cola "colaCamionetas

    channel.basic_consume(queue='colaCamionetas',   #cola a la que se subscribe la funion
                        auto_ack=True,
                        on_message_callback=callback)  # funcion subscrita a la cola


    # loop infinito para recivir mensajes (queda escuchado)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
#esto no es necesario es mas que nada para tener redundancia con el try y asi manejar errores

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


