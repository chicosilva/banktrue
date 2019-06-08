from .models import Installment
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db.models import Sum


def amount_pay(contract):

        amout_pay = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=False).\
                aggregate(Sum('amount'))

        if not amout_pay['amount__sum']:
                return 0

        return amout_pay['amount__sum']


def installmets_pay(contract):

        installmets_pay = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=False).\
                count()

        return installmets_pay

def debits(contract):

        debits = Installment.objects.\
                filter(contract=contract).\
                filter(payment_date__isnull=True).\
                aggregate(Sum('amount'))

        return debits['amount__sum']

def calc_interest(amount, interest_rate):

        amount = Decimal(amount)
        interest_rate = Decimal(interest_rate)

        amount_due = (amount + (amount * interest_rate/ 100))
        return amount_due


def create_installment(contract):

    amount = contract.amount_due / contract.installment_number

    for i in range(0, contract.installment_number):

        due_date = datetime.date.today() + relativedelta(months=i+1)

        installment = Installment()
        installment.contract = contract
        installment.due_date = due_date
        installment.amount = amount
        installment.number = i + 1
        installment.save()