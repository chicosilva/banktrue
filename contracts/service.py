from .models import Installment
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

def calc_interest(amount, interest_rate):

        amount = Decimal(amount)
        interest_rate = Decimal(interest_rate)

        amount_due = (amount + (amount * interest_rate/ 100))
        return amount_due


def create_installment(contract):

    amount = contract.amount_due / contract.installment_number

    for i in range(0, contract.installment_number):

        due_date = data_vencimento = datetime.date.today() + relativedelta(months=i+1)

        installment = Installment()
        installment.contract = contract
        installment.due_date = due_date
        installment.amount = amount
        installment.number = i+1
        installment.save()