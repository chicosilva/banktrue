from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import copy
from customers.models import Customer
from core import get_client_ip
from .service import create_installment, calc_interest
from contracts.models import Contract, Installment
from django.db.models import Sum
from customers.service import check_token
import datetime
from decimal import Decimal


@api_view(http_method_names=['POST'])
def payment(request):

    tax_id = check_token(request)

    if not tax_id:
        return Response({'message': 'invalid token'}, status=400)
    
    data = copy.copy(request.POST)

    installment = Installment.objects.get(pk=data.get('id'), \
        contract=data.get('contract_id'))

    installment.payment_date = datetime.datetime.now()
    installment.amount_due = Decimal(data.get('amount_due'))
    installment.late_fee = Decimal(data.get('late_fee'))
    installment.save()
    
    installment_serializer = InstallmentSerializer(installment)

    return Response(installment_serializer.data)


@api_view(http_method_names=['GET'])
def detail(request, id):

    taxid = check_token(request)

    if not taxid:
        return Response({'message': 'invalid token'}, status=400)
    
    contract = Contract.objects.get(pk=id, customer__taxid=taxid)
    installments = Installment.objects.filter(contract=id)
    
    contract_serializer = ConstractDetailsSerializer(contract)
    installments = InstallmentSerializer(installments, many=True)
    
    debits = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=True).\
                aggregate(Sum('amount'))
    
    amout_pay = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=False).\
                aggregate(Sum('amount'))
    
    installmets_pay = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=False).\
                count()
    
    summary = {
        'amount_due': debits['amount__sum'],
        'amount_pay': amout_pay['amount__sum'],
        'installmets_pay': installmets_pay,
    }
    
    data = {
        'contract': contract_serializer.data,
        'summary': summary,
        'installments': installments.data,
    }

    return Response(data)


@api_view(http_method_names=['POST'])
def create(request):
    
    data = copy.copy(request.POST)
    
    taxid = check_token(request)

    if not taxid:
        return Response({'message': 'invalid token'}, status=400)

    customer = Customer.objects.get(taxid=taxid)
    data['customer'] = customer.pk
    data['ip_address'] = get_client_ip(request)
    data['amount_due'] = calc_interest(data.get('amount'), data.get('interest_rate'))

    serializer = ConstractSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    contract = serializer.create(serializer.validated_data)
    
    create_installment(contract)

    return Response(serializer.data)