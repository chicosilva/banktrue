import re
import decimal
import locale
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import hashlib
import string
import random
import datetime
import uuid
from django.template.defaultfilters import slugify
from datetime import date
from django.shortcuts import HttpResponse
from bs4 import BeautifulSoup


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def clean_valor_moeda(valor):
    if not valor or valor == "":
        return 0

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return decimal.Decimal(valor)

def dict_errors_form_api(errors):
    errors_dict = {}
    if errors:
        for error in errors:
            e = errors[error]
            soup = BeautifulSoup(u"{0}".format(e))
            errors_dict[error] = soup.get_text()

    return errors_dict



def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def date_to_python(date):
    
    if not date:
        return None

    return datetime.datetime.strptime(date, "%d/%m/%Y").date()


def list_filter(kwargs, request, data_inicio, data_fim):

    dados = {}

    for v in kwargs:

        if request.GET.get('{0}'.format(v)):
            
            if '__in' in v:
                dados[v] = request.GET.getlist('{0}'.format(v))
            else:
                dados[v] = request.GET.get('{0}'.format(v))

    data_inicio_get = request.GET.get('data_inicio', None)
    data_fim_get = request.GET.get('data_fim', None)

    if data_inicio_get and not data_fim_get:
        dados['{0}'.format(data_inicio)] = date_to_python(data_inicio_get)

    if data_inicio_get and data_fim_get:
        dados['{0}'.format(data_inicio)] = date_to_python(data_inicio_get)
        dados['{0}'.format(data_fim)] = date_to_python(data_fim_get)
    
    return dados


def search_filter(termo, request):
    if request.GET.get('%s' % termo):
        return {'%s__icontains' % termo: request.GET.get('%s' % termo)}

    return {}


# traduz 123.456.789-10 para 12345678910
_translate = lambda cpf: ''.join(re.findall("\d", cpf))


def _exceptions(cpf):
    """Se o número de CPF estiver dentro das exceções é inválido

    """
    if len(cpf) != 11:
        return True
    else:
        s = ''.join(str(x) for x in cpf)
        if s == '00000000000' or s == '11111111111' or s == '22222222222' or s == '33333333333' or s == '44444444444' or s == '55555555555' or s == '66666666666' or s == '77777777777' or s == '88888888888' or s == '99999999999':
            return True
    return False


def _gen(cpf):
    """Gera o próximo dígito do número de CPF

    """
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0

class CPF(object):
    _gen = staticmethod(_gen)
    _translate = staticmethod(_translate)

    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:

        12345678910
        123.456.789-10

        ou uma lista ou tuple
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0)

        """
        from six import string_types
        if isinstance(cpf, string_types):
            if not cpf.isdigit():
                cpf = self._translate(cpf)

        self.cpf = [int(x) for x in cpf]

    def __getitem__(self, index):
        """Retorna o dígito em index como string

        """

        return self.cpf[index]

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cpf)) == cpf

        """

        return "CPF('%s')" % ''.join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF

        """

        return isinstance(other, CPF) and self.cpf == other.cpf

    def __str__(self):
        """Retorna uma representação do CPF na forma:

        123.456.789-10

        """

        d = iter("..-")
        s = map(str, self.cpf)
        for i in range(3, 12, 4):
            s.insert(i, d.next())
        r = ''.join(s)
        return r

    def isValid(self):
        """Valida o número de cpf

        """

        if _exceptions(self.cpf):
            return False

        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]


def list_paginator(request, list, number):
    if not list: list = []

    paginator = Paginator(list, number)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    return list


def moeda_pt(numero):
    if not numero:
        return None

    """
    Retorna uma string no formato de moeda brasileira
    """

    try:
        contador = 0
        preco_str = ''
        num = numero.__str__()
        if '.' in num:
            preco, centavos = num.split('.')
        else:
            preco = num
            centavos = '00'

        tamanho = len(preco)
        while tamanho > 0:
            preco_str = preco_str + preco[tamanho - 1]
            contador += 1
            if contador == 3 and tamanho > 1:
                preco_str = preco_str + '.'
                contador = 0
            tamanho -= 1

        tamanho = len(preco_str)
        str_preco = ''
        while tamanho > 0:
            str_preco = str_preco + preco_str[tamanho - 1]
            tamanho -= 1

        return "%s,%s" % (str_preco, centavos)
    except:
        return 'Erro. Nao foi possivel formatar.'


def clean_valor_moeda(valor):
    if not valor or valor == "":
        return 0

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return decimal.Decimal(valor)
