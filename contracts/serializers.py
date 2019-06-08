from rest_framework import serializers
from .models import Contract, Installment


class InstallmentPaySerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField()

    class Meta:

        model = Installment

        fields = [
            'id',
            'contract_id',
            'amount_due',
            'late_fee',
        ]


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
    
    def validate_amount(self, data):
        
        """
        Check that the start is before the stop.
        """
        #if not data.is_integer():
        #    raise serializers.ValidationError("finish must occur after start")
        
        return data

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
    
