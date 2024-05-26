"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import threading
from django.core.wsgi import get_wsgi_application
from Users.rabbitmqcaller import start_consumer

# Configurar las variables de entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Función para iniciar el consumidor en un hilo separado
def start_consumer_thread():
    start_consumer()

# Crear y arrancar el hilo para el consumidor
consumer_thread = threading.Thread(target=start_consumer_thread)
consumer_thread.start()

# Obtener la aplicación WSGI
application = get_wsgi_application()
