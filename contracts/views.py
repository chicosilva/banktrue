from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import copy
from customers.models import Customer
from core import get_client_ip
from .service import *
from contracts.models import Contract, Installment
from customers.service import check_token
import datetime
from decimal import Decimal


@api_view(http_method_names=['GET'])
def user(request):

    taxid = check_token(request)

    if not taxid:
        return Response({'message': 'invalid token'}, status=400)
    
    customer = Customer.objects.get(taxid=taxid)
    contracts = Contract.objects.filter(customer=customer)
    serializer = ConstractDetailsSerializer(contracts, many=True)

    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def installments(request, contract_id):

    taxid = check_token(request)

    if not taxid:
        return Response({'message': 'invalid token'}, status=400)
    
    customer = Customer.objects.get(taxid=taxid)
    contract = Contract.objects.get(pk=contract_id, customer=customer)

    installments = Installment.objects.filter(contract=contract_id)
    serializer = InstallmentSerializer(installments, many=True)

    return Response(serializer.data)


@api_view(http_method_names=['POST'])
def payment(request):

    taxid = check_token(request)

    if not taxid:
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
    
    summary = {
        'amount_due': debits(contract),
        'amount_pay': amount_pay(contract),
        'installmets_pay': installmets_pay(contract),
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
    
    serializer = ConstractSerializer(data=data)
    data['amount_due'] = 0
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data['amount_due'] = calc_interest(data.get('amount'), data.get('interest_rate'))

    contract = serializer.create(serializer.validated_data)
    
    create_installment(contract)

    return Response(serializer.data)