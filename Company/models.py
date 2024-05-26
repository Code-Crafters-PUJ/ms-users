from django.db import models

# Create your models here.


class company(models.Model):
    id = models.AutoField(primary_key=True)
    NIT = models.CharField(max_length=45,unique=True)
    businessArea = models.CharField(max_length=45)
    employeeNumber = models.IntegerField()
    businessName = models.CharField(max_length=45)
    electronicBilling = models.CharField(max_length=45)
    electronicPayroll = models.CharField(max_length=45)

class branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    company = models.ForeignKey(company, on_delete=models.CASCADE)

class support(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    company = models.ForeignKey(company, on_delete=models.CASCADE)