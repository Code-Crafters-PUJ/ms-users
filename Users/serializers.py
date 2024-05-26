from rest_framework import serializers
from .models import Account, trials, billings, clients, plan
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ['password']
class BillingSerializer(serializers.ModelSerializer):

    class Meta:
        model = billings
        fields = '__all__'

class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = clients
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = plan
            fields = '__all__'

class TrialsSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = trials
                fields = '__all__'