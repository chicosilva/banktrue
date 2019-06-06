from django.http import HttpResponseRedirect
from functools import wraps
from django.shortcuts import reverse


def access_required(sessao=None, redirect_to=None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):

            result = request.session.get(sessao, False)

            if not result:
                return HttpResponseRedirect(reverse(redirect_to))
            else:
                return func(request, *args, **kwargs)

        return wraps(func)(inner_decorator)

    return decorator