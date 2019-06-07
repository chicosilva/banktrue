from django.db import models
from core.models import ModelDefault
from model_utils.managers import QueryManager
from uuid import uuid4


class Contract(ModelDefault):

    class Meta:
        ordering = ['-pk']


    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    number = models.CharField(max_length=100, editable=False, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_due = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate  = models.DecimalField(max_digits=15, decimal_places=2)
    installment_number = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    bank = models.CharField(max_length=70)
    objects = QueryManager(canceled_at__isnull=True)

    def save(self, *args, **kwargs):
        
        if self._state.adding:
            self.number = uuid4().int & (1<<64)-1
        
        super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer.name


class Installment(ModelDefault):
    
    class Meta:
        ordering = ['pk']

    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField()
    number = models.IntegerField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_due = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    objects = QueryManager(canceled_at__isnull=True)

    def __str__(self):
        return self.customer.name
    
    