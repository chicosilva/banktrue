# coding=utf-8
from django import forms
from django.contrib.auth.hashers import check_password, make_password
import calendar
from django.utils.translation import ugettext as _


class ContatoForm(forms.Form):
    
    nome = forms.CharField(label=u'Nome', max_length=50)
    assunto = forms.CharField(label=u'Assunto', max_length=50)
    telefone = forms.CharField(label=u'Nome', max_length=50)
    email = forms.CharField(label=u'E-mail')
    mensagem = forms.CharField(widget=forms.Textarea)


def dict_errors_form(errors):
    errors_dict = {}
    if errors:
        for error in errors:
            e = errors[error]
            errors_dict[error] = unicode(e)

    return errors_dict

class FormEditarSenhaAtual(forms.Form):
    
    senha_atual = forms.CharField(label='Senha atual', max_length=100, widget=forms.PasswordInput(), required=True)
    senha = forms.CharField(label='Nova Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    confirme = forms.CharField(label='Confirme sua Senha', max_length=100, widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.obj = kwargs.pop('obj', None)

        super(FormEditarSenhaAtual, self).__init__(*args, **kwargs)

    def clean(self):

        if not check_password(self.cleaned_data.get('senha_atual'), self.obj.senha):
            raise forms.ValidationError(u"A senha atual não confere.")

        if self.cleaned_data.get('senha') != self.cleaned_data.get('confirme'):
            raise forms.ValidationError(u"As senhas devem ser iguais")

        return self.cleaned_data


class FormEditarSenhaAdmin(forms.Form):
    senha = forms.CharField(max_length=100, widget=forms.PasswordInput(), required=True)

    def clean_senha(self):
        return make_password(self.cleaned_data['senha'])

class FormEditarSenha(forms.Form):
    senha = forms.CharField(label='Nova Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    confirme = forms.CharField(label='Confirme sua Senha', max_length=100, widget=forms.PasswordInput(), required=True)

    def clean(self):
        if self.data['senha'] != self.data['confirme']:
            raise forms.ValidationError(u"As senhas devem ser iguais")

        return self.cleaned_data

    def clean_senha(self):
        return make_password(self.cleaned_data['senha'])


class FormLogin(forms.Form):
    senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(label="e-mail", required=True)

class FormRecuperarSenha(forms.Form):
    email = forms.EmailField(label="e-mail", required=True)

class FormEditarSenhaRecuperacao(forms.Form):
    senha = forms.CharField(label='Nova Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    confirme = forms.CharField(label='Confirme sua Senha', max_length=100, widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(FormEditarSenhaRecuperacao, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data.get('senha') != self.cleaned_data.get('confirme'):
            raise forms.ValidationError(u"As senhas devem ser iguais")

        return self.cleaned_data
