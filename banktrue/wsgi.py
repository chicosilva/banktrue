import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banktrue.settings")
_application = get_wsgi_application()
from django.conf import settings

def application(environ, start_response):
    
    return _application(environ, start_response)