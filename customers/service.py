import jwt
from django.conf import settings


def check_token(request):
    
    token = request.GET.get('token')

    if request.method == "POST":
        token = request.POST.get('token')
    
    tax_id = None

    try:

        payload = result = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload.get('taxid')

    except jwt.DecodeError:
        return False