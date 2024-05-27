import jwt
from .models import Account, profile, Role, Permission, Module, plan_has_services, contactUs, services, clients, trials, coupons, billings, plan, payment
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AccountSerializer, TrialsSerializer, PlanSerializer, PermissionSerializer, BillingSerializer
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction

import datetime
import json

import random

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
            with transaction.atomic():
                jd = json.loads(request.body)
                jdAccount = jd.get('Account', {})
                jdCompany = jd.get('Company', {})
                jdBill = jd.get('Bill', {})
                email = jdAccount['email']

                # Check for missing or invalid data before proceeding
                required_fields_account = [
                    'name', 'lastname', 'phone', 'email', 'password', 'type_id_card', 'id_card']
                required_fields_company = [
                    'NIT', 'businessArea', 'employeeNumber', 'name']
                required_fields_bill = ['initial_date', 'final_date', 'amount',
                                        'active', 'payment_date', 'payment_id', 'plan', 'coupon']
                for field in required_fields_account:
                    if field not in jdAccount:
                        raise ValueError(
                            f"Missing required field 'Account.{field}'")
                for field in required_fields_company:
                    if field not in jdCompany:
                        raise ValueError(
                            f"Missing required field 'Company.{field}'")
                for field in required_fields_bill:
                    if field not in jdBill:
                        raise ValueError(
                            f"Missing required field 'Bill.{field}'")

                if self.verify_email(email):
                    raise ValueError("Email is already registered")
                try:
                    plan.objects.get(plan_id=jdBill['plan'])
                    payment_data = payment.objects.get(payment_id=jdBill['payment_id'])
                except plan.DoesNotExist:
                    raise ValueError("Invalid plan ID")
                except payment.DoesNotExist:
                    raise ValueError("Invalid payment method")
                prof = profile.objects.create(
                    name=jdAccount['name'], lastname=jdAccount['lastname'], phone=jdAccount['phone'])
                company.objects.create(NIT=jdCompany['NIT'], businessArea=jdCompany['businessArea'],
                                       employeeNumber=jdCompany['employeeNumber'], businessName=jdCompany['name'])
                
                Account.objects.create(
                    email=jdAccount['email'],
                    password=make_password(jdAccount['password']),
                    role_id=1,
                    profile_id=prof.id,
                    company=company.objects.get(
                        NIT=jdCompany['NIT']),
                    type='R',
                    type_id_card=jdAccount['type_id_card'],
                    id_card=jdAccount['id_card']
                )
                jdBill = jd.get('Bill', {})
                billings.objects.create(initial_date=jdBill['initial_date'], final_date=jdBill['final_date'], amount=jdBill['amount'],
                                        active=jdBill['active'], payment_date=jdBill['payment_date'], payment_method=payment_data.method, plan=plan.objects.get(plan_id=jdBill['plan']), coupon=jdBill['coupon'], payment=payment_data)
                module= Module.objects.all()
                for mod in module:
                    Permission.objects.create(
                        module=mod,
                        account_id=Account.objects.get(
                            id_card=jdAccount['id_card']),
                        modify=True,
                        view=True
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
                    type='E',
                    company=company.objects.get(
                        NIT=jd['businessNit']),
                    type_id_card=jd['type_id_card'],
                    id_card=jd['id_card']
                )
                permissions_data = jd.get('permissions', {})
                for key, permission_data in permissions_data.items():
                    module_name = permission_data.get('module', '')
                    view = permission_data.get('view', False)
                    Modify = permission_data.get('modify', False)
                    Permission.objects.create(
                        module=Module.objects.get(name=module_name),
                        account_id=Account.objects.get(
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
            permissions = Permission.objects.filter(
                account_id=account.id).all()
            permissions_data = PermissionSerializer(permissions, many=True).data
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = JsonResponse(
                {'jwt': token, 'role': account.role.name, 'Permissions': permissions_data, })
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

    def validate_email(self, email):
        if Account.objects.filter(email=email).exists():
            return True
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
                    if not self.validate_email(request.body['email']):
                        jd = json.loads(request.body)
                        user = Account.objects.get(id=pk)
                        user.email = jd['email']
                        user.password = make_password(jd['password'])
                        user.save()
                        return JsonResponse({'message': 'Usuario actualizado correctamente'})
                    else:
                        return JsonResponse({'message': 'El email ya existe'})
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


class getRootAccount(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id(self, id):
        if company.objects.filter(id=id).exists():
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
                if not self.verify_Id(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    company_data = get_object_or_404(company, id=pk)
                    Account_data = Account.objects.filter(
                        company_id=company_data.id, role_id=1).all()
                    company_serializer = AccountSerializer(
                        Account_data, many=True)
                    return JsonResponse({'Accounts': company_serializer.data})
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})


class logoutAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        response = JsonResponse({'message': 'Sesión cerrada correctamente'})
        response.delete_cookie('jwt')

        return response


class deleteAccountView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Company(self, id):
        if company.objects.filter(id=id).exists():
            return True
        return False

    def verify_Id_User(self, id):
        if Account.objects.filter(id=id).exists():
            return True
        return False

    def delete(self, request, idUser, idCompany):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_Id_Company(idCompany):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                if not self.verify_Id_User(idUser):
                    return JsonResponse({'message': 'Usuario no encontrado'})
                else:
                    user = Account.objects.get(id=idUser)
                    user.delete()
                    return JsonResponse({'message': 'Usuario eliminado correctamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class UpdatePlanView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Plan(self, id):
        if billings.objects.filter(id=id).exists():
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

    def put(self, request, pk):
        try:
            if not self.verify_Id_Plan(pk):
                return JsonResponse({'message': 'Plan no encontrado'})
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                jd = json.loads(request.body)
                billings.objects.filter(id=pk).update(
                    initial_date=jd['initial_date'],
                    final_date=jd['final_date'],
                    amount=jd['amount'],
                    active=jd['active'],
                    payment_date=jd['payment_date'],
                    payment_method=jd['payment_method'],
                    plan=plan.objects.get(plan_id=jd['plan']),
                    coupon=jd['coupon'],
                    payment=payment.objects.get(method=jd['payment_method'])
                )
            return JsonResponse({'message': 'Plan actualizado correctamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class getPlans(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Plan(self, id):
        if billings.objects.filter(id=id).exists():
            return True
        return False

 

    def get(self, request):
        try:
            list_plans = plan.objects.all()

            plan_data = PlanSerializer(list_plans, many=True)
            return JsonResponse({'Plan': plan_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class BillsView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Plan(self, id):
        if billings.objects.filter(id=id).exists():
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
            if not pk:
                if not self.validate_token(request.headers['Authorization']):
                    return JsonResponse({'message': 'Token invalido o expirado'})
                else:
                    plans = billings.objects.all()
                    plans_data = BillingSerializer(plans, many=True)
                    return JsonResponse({'Plans': plans_data.data})
            else:
                if not self.validate_token(request.headers['Authorization']):
                    return JsonResponse({'message': 'Token invalido o expirado'})
                else:
                    if not self.verify_Id_Plan(pk):
                        return JsonResponse({'message': 'Plan no encontrado'})
                    else:
                        plan = billings.objects.get(id=pk)
                        plan_data = BillingSerializer(plan)
                        return JsonResponse({'Plan': plan_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class TrialsView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Plan(self, id):
        if billings.objects.filter(id=id).exists():
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

    def get(self, request):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                trialList = trials.objects.all()
                trial_data = TrialsSerializer(trialList, many=True)
                return JsonResponse({'Trials': trial_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class TrialsCompanyView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def verify_Id_Company(self, id):
        if company.objects.filter(id=id).exists():
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
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_Id_Company(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    client = clients.objects.get(
                        company_id=pk)

                    trialList = trials.objects.filter(
                        client_id=client, active=0).all()
                    trial_data = TrialsSerializer(trialList, many=True)
                    return JsonResponse({'Trials': trial_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class CouponView(APIView):
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

    def get(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                coupon = coupons.objects.get(code=pk)
                if not coupon:
                    return JsonResponse({'message': 'Cupón no encontrado'})
                if coupon.active == 0:
                    return JsonResponse({'isAvailable': False})
                else:
                    return JsonResponse({'isAvailable': True})

        except Exception as e:
            return JsonResponse({'message': str(e)})


class ServicesView(APIView):
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

    def validate_company(self, id):
        if company.objects.filter(id=id).exists():
            return True
        return False

    def get(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.validate_company(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    plan = plan.objects.get(company_id=pk)
                    if not plan:
                        return JsonResponse({'message': 'No hay plan para esta empresa'})
                    else:
                        services = plan_has_services.objects.filter(
                            plan_id=plan).all()
                        if not services:
                            return JsonResponse({'message': 'No hay servicios en este plan'})
                        service_data = PlanSerializer(services, many=True)
                        return JsonResponse({'Services': service_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class PlansView(APIView):
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

    def validate_company(self, id):
        if company.objects.filter(id=id).exists():
            return True
        return False

    def validate_plan(self, id):
        if plan.objects.filter(id=id).exists():
            return True
        return False

    def get(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.validate_company(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    if pk == '':
                        plans = plan.objects.all()
                        if not plans:
                            return JsonResponse({'message': 'No hay planes'})
                        plan_data = PlanSerializer(plans, many=True)
                        return JsonResponse({'Plans': plan_data.data})
                    else:
                        plans = plan.objects.filter(company_id=pk).all()
                        if not plans:
                            return JsonResponse({'message': 'No hay planes para esta empresa'})
                        plan_data = PlanSerializer(plans, many=True)
                        return JsonResponse({'Plans': plan_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class ServicesTypeView(APIView):
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

    def validate_company(self, id):
        if company.objects.filter(id=id).exists():
            return True
        return False

    def validate_type(self, id):
        if plan.objects.filter(type=id).exists():
            return True
        return False

    def get(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.validate_company(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    if not self.validate_type(pk):
                        return JsonResponse({'message': 'Tipo de servicio no encontrado'})
                    else:
                        services = plan_has_services.objects.filter(
                            plan_id=plan.objects.get(type=pk)).all()
                        if not services:
                            return JsonResponse({'message': 'No hay servicios en este plan'})
                        service_data = PlanSerializer(services, many=True)
                        return JsonResponse({'Services': service_data.data})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class contactUsView(APIView):
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

    def post(self, request):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                jd = json.loads(request.body)
                contactUs.objects.create(
                    fullname=jd['fullname'],
                    email=jd['email'],
                    city=jd['city'],
                    company=jd['company'],
                    telephone=jd['telephone'],
                    howYoufindUs=jd['howYoufindUs']
                )
                return JsonResponse({'message': 'Empresa creada correctamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class changePasswordAccountView(APIView):
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

    def put(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                jd = json.loads(request.body)
                user = Account.objects.get(id=pk)
                if not user:
                    return JsonResponse({'message': 'Usuario no encontrado'})
                else:
                    if not check_password(jd['actualPassword'], user.password):
                        return JsonResponse({'message': 'Contraseña actual incorrecta'})
                    else:
                        user.password = make_password(jd['newPassword'])
                        user.save()
                        return JsonResponse({'message': 'Contraseña actualizada correctamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class temporalpasswordView(APIView):
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

    def get(self, request, pk):
        try:
            if not self.validate_token(request.headers['Authorization']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                user = Account.objects.get(id=pk)
                if not user:
                    return JsonResponse({'message': 'Usuario no encontrado'})
                else:

                    new_password = 'thisisatemporalpassword' + \
                        str(random.randint(100000, 999999))

                    return JsonResponse({'message': '"Temporary password retrieved successfully', 'password': new_password})
        except Exception as e:
            return JsonResponse({'message': str(e)})


class updateRootAccountView(APIView):
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

    def put(self, request, pk):
        try:
            jd = json.loads(request.body)
            if not self.validate_token(jd['jwt']):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:

                payload = jwt.decode(
                    jd['jwt'], SECRET_KEY, algorithms=['HS256'])

                user = Account.objects.get(id=payload['id_account'])
                if not user:
                    return JsonResponse({'message': 'Usuario no encontrado'})
                else:
                    profile.objects.filter(id=user.profile_id).update(
                        name=jd['name'],
                        lastname=jd['lastname'],
                        phone=jd['phone']
                    )
                    Account.objects.filter(id=pk).update(
                        email=jd['email'],
                        password=make_password(jd['password']),
                        type_id_card=jd['type_id_card'],
                        id_card=jd['id_card'],
                        company=company.objects.get(id=jd['company_NIT'])
                    )

                    return JsonResponse({'message': 'Usuario actualizado correctamente'})
        except Exception as e:
            return JsonResponse({'message': str(e)})
