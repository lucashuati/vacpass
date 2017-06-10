#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from vacpass.models import *


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
    nova_senha = forms.CharField(label='Nova Senha:', widget=forms.PasswordInput())
    confirmacao = forms.CharField(label='Confirmacao:', widget=forms.PasswordInput())
    senha = forms.CharField(label='Senha Antiga:', widget=forms.PasswordInput())


class RecuperaSenhaForm(forms.Form):
    email = forms.EmailField(label='Email:', required=True)


class ExcluirContaForm(forms.Form):
    senha = forms.CharField(label='Senha:', widget=forms.PasswordInput())


class DeletaDoseForm(forms.Form):
    dose = forms.IntegerField()
    vacina = forms.CharField()


class RenovaVacinaForm(forms.Form):
    rdata = forms.DateField()
    dose = forms.IntegerField()
    rvacina = forms.CharField(max_length=100)

    def clean_data(self):
        data_input = self.cleaned_data['data']
        if data_input > datetime.date.today():
            raise ValidationError('Esse dia ainda nem chegou amigao')
        return self.cleaned_data['data']


class NovaVacinaCartaoForm(forms.Form):
    vacina = forms.CharField(widget=forms.Select(), label='Vacina', max_length=500)
    data = forms.DateField()


class DependenteForm(ModelForm):
    class Meta:
        model = Dependente
        fields = ['tipo', 'nome', 'ndocumento']

    def clean(self):
        stipo = self.cleaned_data['tipo']
        sndoc = self.cleaned_data['ndocumento']
        nd = Dependente.objects.filter(tipo=stipo, ndocumento=sndoc).exclude(pk=self.instance.id)
        if nd.count() > 0:
            raise ValidationError('documento existente')

        return self.cleaned_data


class VacinaForm(ModelForm):
    class Meta:
        model = Vacina
        exclude = []

    nome = forms.CharField(max_length=50)
    funcionalidade = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    publico_alvo = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    disponibilidade = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    proibitivos = forms.CharField(max_length=500, widget=forms.Textarea, required=False,
                                  label='Contra-indicações e Precauções')
    preco = forms.FloatField


class DoseForm(forms.ModelForm):
    class Meta:
        model = DoseVacina
        exclude = ['dose', 'vacina', 'cartao']

    def clean_duracao_meses(self):
        data = self.cleaned_data['duracao_meses']
        if data < 1:
            raise forms.ValidationError('A duração da dose deve se de no mínimo um mês')
        return data


class SolicitacaoRevisaoForm(forms.Form):
    texto = forms.CharField(required=True, max_length=512, widget=forms.Textarea(attrs={
        'cols': '80',
        'rows': '5',
        'style': "resize:none",
        'placeholder': 'Descreva brevemente a sugestão de melhoria'
    }))


class RespostaSolicitacaoForm(forms.Form):
    nao_pendente = [x for x in Solicitacao.STATUS if x[0] != Solicitacao.PENDENTE]
    situacao = forms.ChoiceField(choices=nao_pendente, label="Nova situação:", initial=1)
    texto = forms.CharField(required=True, label="", widget=forms.Textarea(attrs={
        'cols': '80',
        'rows': '10',
        'style': "resize:none",
        'placeholder': 'Resposta para o solicitante'
    }))