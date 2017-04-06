#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
import datetime



class CriarContaForm(forms.Form):
    regex_cpf='^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'
    errmessage_cpf='entre com um cpf válido'
    nome = forms.CharField(label='Nome', max_length=100,required=True)
    cpf = forms.RegexField(regex=regex_cpf,error_messages={'invalid':'errmessage_cpf'}, max_length=14, min_length=14, label='Cpf:', required=True)
    email = forms.EmailField(label='Email:', required=True)
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha:', max_length=100, required=True)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), label='Confirmar senha:', max_length=100, required=True)


    nascimento = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),required=True)
    #teste
