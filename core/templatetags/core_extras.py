from django import template
import uuid
from django.conf import settings

register = template.Library()

@register.simple_tag
def token_scripts():
    
    if not settings.DEBUG:
        return "?token=2001"
    
    return "?token={0}".format(uuid.uuid4())