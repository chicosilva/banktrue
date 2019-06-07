from rest_framework import serializers
from .models import Contract


class ConstractSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Contract

        fields = [
            'customer',
            'amount',
            'amount_due',
            'interest_rate',
            'installment_number',
            'ip_address',
            'bank',
        ]
    
    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
