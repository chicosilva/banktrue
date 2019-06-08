from customers.views import *
from django.conf.urls import url, include
app_name = 'customers'

urlpatterns = [
    
    url(r'^create/$', create, name='create'),

]