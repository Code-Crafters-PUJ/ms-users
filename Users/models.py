from django.db import models
from Company.models import company
# Create your models here.


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=150)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey(company, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, default='E')
    type_id_card = models.CharField(max_length=45, null=True)
    id_card = models.CharField(max_length=45, null=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = True


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    view = models.BooleanField(default=False)
    modify = models.BooleanField(default=False)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


class payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    method = models.CharField(max_length=45)


class plan (models.Model):
    plan_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    mensual_price = models.FloatField()
    semestral_price = models.FloatField()
    anual_price = models.FloatField()
    users = models.IntegerField()
    state = models.CharField(max_length=45)
    num_accounts = models.IntegerField()
    num_services = models.IntegerField()
    active = models.IntegerField(default=1)


class services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    active = models.IntegerField( default=1)
    users = models.IntegerField()


class plan_has_services(models.Model):
    plan_id = models.ForeignKey(plan, on_delete=models.CASCADE)
    service_id = models.ForeignKey(services, on_delete=models.CASCADE)
    active = models.IntegerField(default=1)


class clients (models.Model):
    client_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    phone = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    company_id = models.ForeignKey(company, on_delete=models.CASCADE)


class coupons(models.Model):
    code = models.CharField(max_length=45, primary_key=True)
    duration = models.IntegerField()
    discount = models.FloatField()
    expiration_date = models.DateField()
    active = models.IntegerField(default=1)
    client = models.ForeignKey(clients, on_delete=models.CASCADE)
class trials(models.Model):
    trial_id = models.IntegerField(primary_key=True)
    duration = models.IntegerField()
    state = models.CharField(max_length=45)
    active = models.IntegerField(default=1)
    plan_id = models.ForeignKey(plan, on_delete=models.CASCADE)
    client_id = models.ForeignKey(clients, on_delete=models.CASCADE)


class billings(models.Model):
    id = models.AutoField(primary_key=True)
    suscription_id = models.IntegerField(null=True,blank=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    amount = models.FloatField()
    coupon = models.CharField(max_length=45, null=True, blank=True)
    active = models.IntegerField(default=1)
    
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=45)
    payment = models.ForeignKey(payment, on_delete=models.CASCADE)


class contactUs(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    city = models.CharField(max_length=45)
    company = models.CharField(max_length=45)
    telephone = models.CharField(max_length=45)
    howYoufindUs = models.CharField(max_length=45)
