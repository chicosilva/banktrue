from rest_framework import serializers
from customers.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'taxid', 'cellphone', 'city', 'token']
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)
