from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import jwt
from .serializers import companySerializer

import datetime
import json
import pika


from .models import company
from Users.models import Account
# Create your views here.


class createCompany(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_NIT(self, nit):
        if company.objects.filter(NIT=nit).exists():
            return True
        return False

    def post(self, request):
        try:
            jd = json.loads(request.body)
            NIT = jd.get('NIT')

            if not jd['NIT'] or not jd['businessArea'] or not jd['employeeNumber'] or not jd['businessName']:
                return JsonResponse({'message': 'Campos faltantes'})
            if self.verify_NIT(NIT):
                return JsonResponse({'message': 'La empresa ya esta registrada'}, status=201)
            else:
                businessName = jd.get('businessName')
                businessArea = jd.get('businessArea')
                employeeNumber = jd.get('employeeNumber')
                electronicBilling = jd.get('electronicBilling')
                electronicPayroll = jd.get('electronicPayroll')
                company.objects.create(businessName=businessName,
                                       employeeNumber=employeeNumber, NIT=NIT, businessArea=businessArea, electronicBilling=electronicBilling, electronicPayroll=electronicPayroll)
                mensaje = "businessName:"+businessName+",employeeNumber:" + \
                    employeeNumber+",NIT:"+NIT+",businessArea:"+businessArea
                print(mensaje)
                self.publish_to_rabbitmq(mensaje, "company_queue")
                return JsonResponse({'message': 'Empresa creada correctamente'})

            """
            Ejemplo de JSON
            {
            "NIT": "123456789",
            "businessArea": "Tecnología",
            "employeeNumber": "100",
            "businessName": "Mi Empresa"
            }
            """

        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            print("Cuerpo de la solicitud:", request.body)
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'message': 'Error en el formato de datos'})
        except ObjectDoesNotExist:
            print("Usuario no encontrado")
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            print("Error durante el procesamiento de la solicitud:", e)
            # Devolver una respuesta de error adecuada
            return JsonResponse({'message': str(e)})

    def publish_to_rabbitmq(self, message, queuename):

        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', port=5672))
            channel = connection.channel()
            channel.queue_declare(queue=queuename)
            channel.basic_publish(
                exchange='', routing_key=queuename, body=json.dumps(message))
            connection.close()
            print("Mensaje publicado en RabbitMQ correctamente.")
        except Exception as e:
            print("Error al publicar en RabbitMQ:", e)


class getInfoCompany(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_NIT(self, nit):
        if company.objects.filter(NIT=nit).exists():
            return True
        return False

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if datetime.datetime.utcnow() + datetime.timedelta(minutes=360) > datetime.datetime.fromtimestamp(payload['exp']):
                return True
            else:
                return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def get(self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_NIT(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    company_data = get_object_or_404(company, NIT=pk)

                    company_serializer = companySerializer(company_data)

                    return JsonResponse(company_serializer.data)
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})
