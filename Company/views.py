from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import companySerializer, branchSerializer, supportSerializer

import datetime
import json
import pika
import jwt
import random

from .models import company, branch,support
from Users.models import Account,plan
from Users.serializers import PlanSerializer

from Users.rabbitmqcaller import publish_to_rabbitmq
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
                compa = company.objects.create(businessName=businessName,
                                       employeeNumber=employeeNumber, NIT=NIT, businessArea=businessArea, electronicBilling=electronicBilling, electronicPayroll=electronicPayroll)
                mensaje = "businessName:"+businessName+",employeeNumber:" + \
                    employeeNumber+",NIT:"+NIT+",businessArea:"+businessArea+",IDCompany:"+str(compa.id)
                print(mensaje)
                publish_to_rabbitmq(mensaje, "company_queue")
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
    def put(self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_NIT(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    payload = jwt.decode(
                        token, SECRET_KEY, algorithms=['HS256'])
                    
                    company_data = get_object_or_404(
                        company, id=payload['id_company'])
                    jd = json.loads(request.body)
                    company_data.businessName = jd.get('businessName')
                    company_data.businessArea = jd.get('businessArea')
                    company_data.employeeNumber = jd.get('employeeNumber')
                    company_data.electronicBilling = jd.get('electronicBilling')
                    company_data.electronicPayroll = jd.get('electronicPayroll')
                    company_data.NIT = jd.get('NIT')
                    company_data.save()
                    return JsonResponse({'message': 'Company updated successfully'})
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})


class getInfoPlanCompany(APIView):
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
                    plan_data = plan.objects.filter(company=company_data)
                    plan_serializer = PlanSerializer(plan_data, many=True)
                    return JsonResponse(plan_serializer.data)
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})


class validBranchView(APIView):
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
                    company_data = company.objects.get(id=pk)
                    branch_data = branch.objects.filter(company=company_data)
                    id_branch = random.randint(1, 100)
                    if branch_data.id != id_branch:
                        return JsonResponse({'message': 'branch id', 'id': id_branch})
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})


class branchInfoview(APIView):
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
                    print(company_data)
                    branch_data = branch.objects.filter(company=company_data.id)
                    branch_serializer = branchSerializer(
                        branch_data, many=True).data
                    return JsonResponse(branch_serializer)
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})
    def post(self, request):
        try:
            jd = json.loads(request.body)
            NIT = jd.get('NIT')
            if not jd['name'] or not jd['address']:
                return JsonResponse({'message': 'Campos faltantes'})
            if not self.verify_NIT(NIT):
                return JsonResponse({'message': 'Empresa no encontrada'})
            else:
                company_data = get_object_or_404(company, NIT=NIT)
                name = jd.get('name')
                address = jd.get('address')
                branch.objects.create(name=name, address=address, company=company_data)
                mensaje = "name:"+str(name)+",address:"+str(address)+",NIT:"+str(NIT)+",CompanyId:"+str(company_data.id)
                print(mensaje)
                publish_to_rabbitmq(mensaje, "branch_queue")
                return JsonResponse({'message': 'Sucursal creada correctamente'})
        except json.JSONDecodeError as e:

            return JsonResponse({'message': 'Data format error'})
    def put (self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_NIT(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    payload = jwt.decode(
                        token, SECRET_KEY, algorithms=['HS256'])
                    
                    company_data = get_object_or_404(
                        company, id=payload['id_company'])
                    jd = json.loads(request.body)
                    branch_data = get_object_or_404(branch, id=jd['id'])
                    branch_data.name = jd.get('name')
                    branch_data.address = jd.get('address')
                    branch_data.save()
                    return JsonResponse({'message': 'Branch updated successfully'})
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})
    def delete(self, request, pk):
        try:
            token = request.headers['Authorization']
            if not self.validate_token(token):
                return JsonResponse({'message': 'Token invalido o expirado'})
            else:
                if not self.verify_NIT(pk):
                    return JsonResponse({'message': 'Empresa no encontrada'})
                else:
                    jd = json.loads(request.body)
                    branch_data = get_object_or_404(branch, id=jd['id'])
                    branch_data.delete()
                    return JsonResponse({'message': 'Branch deleted successfully'})
        except KeyError:
            return JsonResponse({'message': 'Token no encontrado'})