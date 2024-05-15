import jwt
from .models import Account, profile, Role, Permission, Module
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AccountSerializer
from django.contrib.auth.hashers import make_password
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
                account = Account.objects.create(
                    email=jd['email'],
                    password=make_password(jd['password']),
                    role_id=1,
                    profile_id=prof.id,
                    company=company.objects.get(
                        NIT=jd['company_NIT']),
                    type_id_card=jd['type_id_card'],
                    id_card=jd['id_card']
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
                    role=Role.objects.get(name=jd['role']),
                    profile_id=prof.id,
                    company=company.objects.get(
                        NIT=jd['businessNit']),
                    type_id_card=jd['type_id_card'],
                    id_card=jd['id_card']
                )
                permissions_data = jd.get('permissions', {})
                for key, permission_data in permissions_data.items():
                    module_name = permission_data.get('module', '')
                    view = permission_data.get('view', False)
                    Modify = permission_data.get('Modify', False)
                    Permission.objects.create(
                        module=Module.objects.get(name=module_name),
                        idAccount=Account.objects.get(
                            id_card=jd['id_card']),
                        modify=Modify,
                        view=view
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
                if self.validate_id(token, pk):
                    user = get_object_or_404(Account, id=pk)
                    user_data = AccountSerializer(user).data
                    return JsonResponse({'Account': user_data, 'role': user.role.name, 'company': company.objects.get(id=user.company.id).businessName})
                else:
                    return JsonResponse({'message': 'No tienes permisos para ver esta información'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    def put(self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if self.validate_id(token, pk):
                    jd = json.loads(request.body)
                    user = Account.objects.get(id=pk)
                    user.email = jd['email']
                    user.password = make_password(jd['password'])
                    user.save()
                    return JsonResponse({'message': 'Usuario actualizado correctamente'})
                else:
                    return JsonResponse({'message': 'No tienes permisos para realizar esta acción'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'message': str(e)})
    def delete(self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if self.validate_id(token, pk):
                    user = Account.objects.get(id=pk)
                    user.delete()
                    return JsonResponse({'message': 'Usuario eliminado correctamente'})
                else:
                    return JsonResponse({'message': 'No tienes permisos para realizar esta acción'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class allUsersInfobyCompany(APIView):
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

    def validate_role(self, token, pk):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload['role'] == 'Raiz':
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
                if self.validate_role(token, pk):
                    accounts = Account.objects.filter(company_id=pk).all()
                    if not accounts:
                        return JsonResponse({'message': 'No hay usuarios en esta empresa'})
                    user_data = AccountSerializer(accounts, many=True)
                    return JsonResponse({'Account': user_data.data,  'company': company.objects.get(id=pk).businessName})
                else:
                    return JsonResponse({'message': 'No tienes permisos para ver esta información'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class logoutAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        response = JsonResponse({'message': 'Sesión cerrada correctamente'})
        response.delete_cookie('jwt')
        
        return response