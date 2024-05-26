from rest_framework import serializers
from .models import company, branch, support

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'

class branchSerializer(serializers.ModelSerializer):
    class Meta:
        model = branch
        fields = '__all__'

class supportSerializer(serializers.ModelSerializer):
    class Meta:
        model = support
        fields = '__all__'
        