import jwt
from .models import Account, profile
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# from .serializers import AccountSerializer, CredentialsSerializer, ReportSerializer, PermissionsSerializer, CredentialsSerializer, PermissionsSerializerLogIn
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db import IntegrityError


import datetime
import json

from Company.models import company


class RegisterRootAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_email(self, email):
        if Account.objects.filter(email=email).exists():
            return True
        return False

    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd['email']
            errors = {}
            if self.verify_email(email):
                return JsonResponse({'message': 'El email ya esta registrado'}, status=201)
            else:
                prof = profile.objects.create(
                    name=jd['name'], lastname=jd['lastname'], phone=jd['phone'])
                Account.objects.create(
                    email=jd['email'],
                    password=make_password(jd['password']),
                    role_id=1,
                    profile_id=prof.id,
                    company_id=company.objects.get(
                        NIT=jd['businessNit']).id,
                )

                return JsonResponse({'message': 'Cuenta creada exitosamente'}, status=201)
        except IntegrityError as e:
            error_message = 'El ID ya existe en la base de datos'
            return JsonResponse({'message': error_message}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)


class RegisterAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_email(self, email):
        if Account.objects.filter(email=email).exists():
            return True
        return False

    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd['email']
            errors = {}
            if self.verify_email(email):
                return JsonResponse({'message': 'El email ya esta registrado'}, status=201)
            else:
                prof = profile.objects.create(
                    name=jd['name'], lastname=jd['lastname'], phone=jd['phone'])
                Account.objects.create(
                    email=jd['email'],
                    password=make_password(jd['password']),
                    role_id=jd['role'],
                    profile_id=prof.id,
                    company_id=company.objects.get(
                        NIT=jd['businessNit']).id,
                )

                return JsonResponse({'message': 'Cuenta creada exitosamente'}, status=201)
        except IntegrityError as e:
            error_message = 'El ID ya existe en la base de datos'
            return JsonResponse({'message': error_message}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=400)



class LoginUserView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            jd = json.loads(request.body)
            email = jd['email']
            password = jd.get('password')
            if not email or not password:
                return JsonResponse({'jwt': 'Campos faltantes'})
            user = get_object_or_404(Account, email=email)
            if not check_password(password, user.password):
                return JsonResponse({'jwt': 'ups! credenciales incorrectas'})
            account = Account.objects.get(id=user.id)
            payload = {
                'id_account': account.id,
                'id_company': account.company_id,
                'role': account.role.name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = JsonResponse(
                {'jwt': token, 'role': account.role.name})
            response.set_cookie(key='jwt', value=token, httponly=True)
            return response

        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            print("Cuerpo de la solicitud:", request.body)
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'jwt': 'Error en el formato de datos'})
        except ObjectDoesNotExist:
            print("Usuario no encontrado")
            # Manejar el error adecuadamente, por ejemplo, devolver una respuesta de error
            return JsonResponse({'jwt': 'Usuario no encontrado'})
        except Exception as e:
            print("Error durante el procesamiento de la solicitud:", e)
            # Devolver una respuesta de error adecuada
            return JsonResponse({'jwt': str(e)})


class getAccountInfoview(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
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
    def validate_id(self, token, pk):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload['id_account'] == pk:
                return True
            if payload['role'] == 'Raiz' and payload['id_account'] != pk:
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
                if self.validate_id(token,pk):
                    account = Account.objects.get(id=pk)
                    return JsonResponse({'email': account.email, 'role': account.role.name, 'company': company.objects.get(id=account.company.id).businessName})
                account = Account.objects.get(id=pk)
                return JsonResponse({'email': account.email, 'role': account.role.name, 'company': company.objects.get(id=account.company.id).businessName})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'message': str(e)})