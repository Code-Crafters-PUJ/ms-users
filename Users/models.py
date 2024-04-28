from django.db import models

# Create your models here.





class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    permise_view = models.BooleanField(default=False)
    permise_modify = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)

class company(models.Model):
    id = models.AutoField(primary_key=True)
    NIT = models.CharField(max_length=45)
    businessArea = models.CharField(max_length=45)
    employeeNumber = models.IntegerField()


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey(company, on_delete=models.CASCADE)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, default='E')