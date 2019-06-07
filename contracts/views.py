from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from django.conf import settings
import copy
from customers.models import Customer
from core import get_client_ip
from .service import create_installment, calc_interest
from decimal import Decimal
from contracts.models import Contract, Installment
from django.db.models import Sum


@api_view(http_method_names=['GET'])
def detail(request, id):

    token = request.GET.get('token')
    tax_id = None

    try:

        payload = result = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        tax_id = payload.get('taxid')

    except jwt.DecodeError:
        return Response({'message': 'invalid token'}, status=400)

    contract = Contract.objects.get(pk=id, customer__taxid=tax_id)
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
    
    token = data.get('token')
    tax_id = None

    try:

        payload = result = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        tax_id = payload.get('taxid')

    except jwt.DecodeError:
        return Response({'message': 'invalid token'}, status=400)

    customer = Customer.objects.get(taxid=tax_id)
    data['customer'] = customer.pk
    data['ip_address'] = get_client_ip(request)

    amount = Decimal(data.get('amount'))
    interest_rate = Decimal(data.get('interest_rate'))

    data['amount_due'] = calc_interest(amount, interest_rate)

    serializer = ConstractSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    contract = serializer.create(serializer.validated_data)
    
    create_installment(contract)

    return Response(serializer.data)