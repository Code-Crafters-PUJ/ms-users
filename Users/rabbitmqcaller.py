import pika
import django
import os

from Users.models import plan, services, plan_has_services
import json


def create_plan(ch, method, properties, body):
    # Aquí escribe la lógica para actualizar tu base de datos
    message = body.decode('utf-8')
    data = json.loads(message)

    plan_data = plan.objects.create(
        typePlan=data['type'],
        mensual_price=data['mensualPrice'],
        semestral_price=data['semestralPrice'],
        anual_price=data['anualPrice'],
        state=data['state'],
        num_accounts=data['numAccounts'],
    )

    plan_has_services.objects.filter(plan_id=plan_data.plan_id).delete()
    for service in data['services']:
        # Suponiendo que tienes un modelo Service y puedes obtener los servicios por algún identificador
        service_obj = services.objects.get(id=service['id'])
        plan_has_services.objects.create(
            plan_id=plan_data.plan_id, service_id=service_obj, active=1)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_plan(ch, method, properties, body):
    # Aquí escribe la lógica para actualizar tu base de datos
    message = body.decode('utf-8')
    print(message)
    # Supongamos que `message` es el nuevo valor que deseas establecer
    data = json.loads(message)

    dto = data.get('dto', {})
    if plan.objects.filter(typePlan=data['type']).exists():
        plan.objects.filter(typePlan=data['type']).update(
            typePlan=data['type'],
            mensual_price=dto['mensualPrice'],
            semestral_price=dto['semestralPrice'],
            anual_price=dto['anualPrice'],
            state=dto['state'],
            num_accounts=dto['numAccounts'],
        )
        plan_data = plan.objects.get(typePlan=data['type'])

        plan_has_services.objects.filter(plan_id=plan_data.plan_id).delete()
        for service in data['services']:
            # Suponiendo que tienes un modelo Service y puedes obtener los servicios por algún identificador
            service_obj = services.objects.get(id=service['id'])
            plan_has_services.objects.create(
                plan_id=plan_data.plan_id, service_id=service_obj, active=1)
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def delete_plan(ch, method, properties, body):
    # Aquí escribe la lógica para actualizar tu base de datos
    message = body.decode('utf-8')
    # Supongamos que `message` es el nuevo valor que deseas establecer
    data = json.loads(message)

    plan.objects.filter(typePlan=data['type']).delete()

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    credentials = pika.PlainCredentials('prueba', '123')
    parameters = pika.ConnectionParameters(
        '10.147.17.214',
        5672,
        '/',
        credentials,
        socket_timeout=2,
        heartbeat=6
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # Declarar colas

    # Consumir mensajes de las colas
    channel.basic_consume(queue='create_plan',
                          on_message_callback=create_plan)
    channel.basic_consume(queue='update_plan',
                          on_message_callback=update_plan)
    channel.basic_consume(queue='delete_plan',
                          on_message_callback=delete_plan)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def process_message(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Aquí puedes llamar a las funciones específicas para procesar el mensaje
    # Por ejemplo:
    # if method.routing_key == 'create_plan':
    #     create_plan(body)
    # elif method.routing_key == 'update_plan':
    #     update_plan(body)
    # elif method.routing_key == 'delete_plan':
    #     delete_plan(body)
