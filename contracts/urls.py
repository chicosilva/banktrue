from .views import *
from django.conf.urls import url, include
app_name = 'contracts'

urlpatterns = [
    
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>[0-9a-z-]+)$', detail, name='detail'),
]