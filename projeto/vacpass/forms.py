#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
import datetime

from django.forms import ModelForm

from vacpass.models import Dependente


class CriarContaForm(forms.Form):
    regex_cpf = '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
    errmessage_cpf = 'entre com um cpf válido'
    nome = forms.CharField(label='Nome', max_length=100, required=True)
    cpf = forms.RegexField(regex=regex_cpf, error_message=errmessage_cpf, max_length=14, min_length=14, label='Cpf:',
                           required=True)
    email = forms.EmailField(label='Email:', required=True)
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha:', max_length=100, required=True)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), label='Confirmar senha:', max_length=100,
                                      required=True)
    this_year = datetime.date.today().year
    nascimento = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, this_year - 18)), required=True)


class EditarContaForm(forms.Form):
    nome = forms.CharField(label='Nome:', max_length=100, required=True)
    email = forms.EmailField(label='Email:', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha:', required=False)


class EditPassForm(forms.Form):
    nova_senha = forms.CharField(label = 'Nova Senha:', widget=forms.PasswordInput())
    confirmacao = forms.CharField(label='Confirmacao:', widget=forms.PasswordInput())
    senha = forms.CharField(label = 'Senha Antiga:', widget=forms.PasswordInput())


class ExcluirContaForm(forms.Form):
    senha = forms.CharField(label='Senha:', widget=forms.PasswordInput())

class DependenteForm(ModelForm):
    class Meta:
        model = Dependente
        fields = ['CPF', 'nome', 'certidao']
