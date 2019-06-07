from .serializers import ConstractSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from django.conf import settings
import copy
from customers.models import Customer
from core import get_client_ip


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
    data['amount_due'] = 100

    serializer = ConstractSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.create(serializer.validated_data)
    
    return Response(serializer.data)