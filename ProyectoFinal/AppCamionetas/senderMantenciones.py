import pika

def mandarMensajeMantenciones(mensaje:str):
    #crea los parametros de coneccion
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # crea un canal con los parametros de la coneccion
    channel = connection.channel()

    # crea una cola con el nombre hello rabbit
    channel.queue_declare(queue='colaMantenciones')


    # envia el mensaje 
    channel.basic_publish(exchange='',
                        routing_key='colaMantenciones', #mismo nombre que el nombre de la cola
                        body=mensaje)

    connection.close()

    print(" [x] Sent to Mantenciones")