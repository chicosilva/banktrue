
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path(r'', include('core.urls', 'core')),
    path(r'customers/', include('customers.urls', 'customers')),
    path(r'contracts/', include('contracts.urls', 'contracts')),
  

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
