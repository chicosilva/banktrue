from .views import *
from django.conf.urls import url, include
app_name = 'contracts'

urlpatterns = [
    
    url(r'^create/$', create, name='create'),

]