from customers.views import *
from django.conf.urls import url, include
app_name = 'customers'

urlpatterns = [
    
    url(r'^create/$', create, name='create'),
    #url(r'^reset-senha/(?P<id>[0-9a-z-]+)$', nova_senha, name='nova_senha'),

]