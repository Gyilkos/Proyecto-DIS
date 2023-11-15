import sys, os
import sqlite3
import pika
import senderCamionetas
def main():
    #crea los parametros de coneccion
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # crea un canal con los parametros de la coneccion
    channel = connection.channel()

    # crea una cola con el nombre colaMantenciones
    channel.queue_declare(queue='colaMantenciones')

    #cada vez que llega un mensaje a la cola se llama esta funcion callback
    #primero definimos la funcion
    def callback(ch, method, properties, body):
        # logica de respuesta en base a codigo al inicio del mensaje
        #el primer digito representa que peticion es, por ejemplo el 1 es pedir listado camionetas, el segundo digito denota si es una peticion (0) o una respuesta a esta peticion(1)
        respuesta = ""
        body = str(body)[2:].strip("'") #codigo DATOSdatosDatos
        print("body:")
        print(body)
        
        if body[0] == "1" and body[1] == "0": #1 es pedir kilometraje segun patentes dadas
            lista_patentes = body[4:].split(" ")
            #print(lista_patentes)
            query = "("
            for patente in lista_patentes:
                query += "'"+ patente+"',"
            query = query.strip(",")
            query += ");"
            query = "SELECT Patente, Kilometraje FROM Mantencion WHERE Patente IN" + query
            #print(query)
            #########hacer query base de datos local
            con = sqlite3.connect("DBmantencion.db")

            cur = con.cursor()
            cur.execute(query)
            respuestaQuery = cur.fetchall()
            for fila in respuestaQuery:
                # fila es una tupla que contiene los valores de las columnas
                columna1, columna2 = fila
                respuesta += " "+str(columna1) + ","+ str(columna2) 
                #print(f"Columna1: {columna1}, Columna2: {columna2}")
            
            con.commit()
            con.close()
            senderCamionetas.mandarMensajeCamionetas("11 "+respuesta)  


            #respuesta = "datos falsos datos falsos"
            #pass
        elif body[0] == "2" and body[1] == "1": #2 es la respuesta de camionetas en mantenimiento
            respuesta = body[2:]  #devuelve todo el texto exepto los primeros 2 caracteres
            #print(respuesta)
            with open('archivo.txt', 'w') as archivo:
                # El archivo se abre en modo escritura ('w'), lo que elimina el contenido existente
                
                # Escribir una nueva línea en el archivo
                archivo.write("False\n")
                archivo.write(respuesta)
                archivo.close()


        
        ########## mandar respuesta 
        #print("mandando:")
        #print("11 "+respuesta)
        


        print(f" [x] ReceivedMantenciones {body}")

    #ahora subscribimos esta funcio a la cola "colaMantenciones"

    channel.basic_consume(queue='colaMantenciones',   #cola a la que se subscribe la funion
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


