from django.db import models
from Company.models import company
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
    permise_view_or_modify = models.CharField(max_length=2)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


class profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=150)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey(company, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, default='E')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = True
