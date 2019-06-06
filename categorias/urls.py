from .views import *
from django.conf.urls import url, include
app_name = 'categorias'

urlpatterns = [
    url(r'^$', lista, name='lista'),
    url(r'^novo/$', novo, name='novo'),
    url(r'^remover/(?P<id>[0-9a-z-]+)$', remover, name='remover'),
    url(r'^editar/(?P<id>[0-9a-z-]+)$', editar, name='editar'),
]