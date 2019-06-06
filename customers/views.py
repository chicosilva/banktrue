from rest_framework import viewsets
from customers.models import Customer
from customers.serializers import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from django.conf import settings
import copy


@api_view(http_method_names=['POST'])
def create(request):

    data = copy.copy(request.POST)
    
    token = jwt.encode({'taxid': data.get('taxid')}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    data['token'] = token
    
    serializer = CustomerSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    print(serializer.validated_data)
    serializer.create(serializer.validated_data)
    
    return Response(serializer.data)