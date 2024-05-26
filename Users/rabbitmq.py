import pika
import json
import uuid


def send_request_to_rabbitmq(queue_name, request_data):
    # Configura la conexión con RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Asegúrate de que la cola existe
    channel.queue_declare(queue=queue_name)

    # Genera un ID de correlación único
    correlation_id = str(uuid.uuid4())

    # Define la cola de respuesta
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    # Publica el mensaje
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=correlation_id,
        ),
        body=json.dumps(request_data)
    )

    # Escucha la respuesta
    response = None

    def on_response(ch, method, properties, body):
        nonlocal response
        if properties.correlation_id == correlation_id:
            response = json.loads(body)

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    while response is None:
        connection.process_data_events()

    connection.close()
    return response
