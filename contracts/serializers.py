from rest_framework import serializers
from .models import Contract, Installment


class InstallmentSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Installment

        fields = [
            'payment_date',
            'due_date',
            'number',
            'amount',
            'amount_due',
            'late_fee',
        ]


class ConstractDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Contract

        fields = [
            'customer',
            'amount',
            'amount_due',
            'interest_rate',
            'installment_number',
            'bank',
        ]
    

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
    
