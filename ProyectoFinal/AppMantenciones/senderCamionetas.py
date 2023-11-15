import pika

def mandarMensajeCamionetas(mensaje:str):
    #crea los parametros de coneccion
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # crea un canal con los parametros de la coneccion
    channel = connection.channel()

    # crea una cola con el nombre hello rabbit
    channel.queue_declare(queue='colaCamionetas')


    # envia el mensaje 
    channel.basic_publish(exchange='',
                        routing_key='colaCamionetas', #mismo nombre que el nombre de la cola
                        body=mensaje)

    connection.close()

    print(" [x] Sent to Camionetas")