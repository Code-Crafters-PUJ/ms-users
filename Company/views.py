from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import jwt
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db import IntegrityError

import datetime
import json


from .models import company
from Users.models import Account
# Create your views here.
class createCompany(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_name(self, businessName):
        if company.objects.filter(businessName=businessName).exists():
            return True
        return False
    def post(self, request):
        try:
            jd = json.loads(request.body)
            businessName = jd.get('businessName')
            if not jd['NIT'] or not jd['businessArea'] or not jd['employeeNumber'] or not jd['businessName']:
                return JsonResponse({'message': 'Campos faltantes'})
            if self.verify_name(businessName):
                return JsonResponse({'message': 'La empresa ya esta registrada'}, status=201)
            else:
                NIT = jd.get('NIT')
                businessArea = jd.get('businessArea')
                employeeNumber = jd.get('employeeNumber')
                company.objects.create(businessName=businessName,
                                                 employeeNumber=employeeNumber, NIT=NIT, businessArea=businessArea)
                return JsonResponse({'message': 'Empresa creada correctamente'})

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
