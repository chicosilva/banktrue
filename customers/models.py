from django.db import models
from core.models import ModelDefault
from model_utils.managers import QueryManager


class Customer(ModelDefault):

    class Meta:
        ordering = ['name']

    
    name = models.CharField(max_length=150)
    taxid = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    cellphone = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    token = models.CharField(max_length=255)

    objects = QueryManager(canceled_at__isnull=True)

    def __str__(self):
        return self.name
    