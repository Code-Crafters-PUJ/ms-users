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
