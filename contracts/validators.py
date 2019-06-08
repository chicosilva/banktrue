from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def min_amount(value):

    if value < settings.MIN_AMOUNT:
        raise ValidationError("Min amount is 5000")