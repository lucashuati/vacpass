#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Cartao(models.Model):
    nome = models.CharField(max_length=12)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    nascimento = models.DateField()
    cartao = models.ForeignKey(Cartao)

    def __str__(self):
        return self.django_user.first_name


class Dependente(models.Model):
    CHOICES = [('CPF', 'CPF'), ('RG', 'RG'), ('certidao', 'certidao')]

    tipo = models.CharField(max_length=10, choices=CHOICES)
    nome = models.CharField(max_length=50)
    ndocumento = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao = models.ForeignKey(Cartao)

    def get_absolute_url(self):
        return reverse('editdep', args=[str(self.id)])

    def get_url(self):
        return reverse('excluidep', args = [str(self.id)])

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    funcionalidade = models.CharField(max_length=500, default="")
    publico_alvo = models.CharField(max_length=500, default="")
    disponibilidade = models.CharField(max_length=500, default="")
    proibitivos = models.CharField(max_length=500, default="")
    preco = models.FloatField(default=0)

    def doses(self):
        return DoseVacina.objects.filter(vacina=self)

    def num_doses(self):
        return len(self.doses())

    def get_absolute_url(self):
        return reverse('consultarvacina', args=[str(self.id)])

    def __str__(self):
        return self.nome


class DoseVacina(models.Model):
    dose = models.IntegerField()
    idade = models.CharField(max_length=50)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    duracao_meses = models.IntegerField()
    cartao = models.ManyToManyField(Cartao, through="ControleVencimento")

    ordering = ['vacina']

    def __str__(self):
        return "dose {}: {} ".format(self.dose, self.idade)


class ControleVencimento(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE)
    dose = models.ForeignKey(DoseVacina, on_delete=models.CASCADE)
    data = models.DateField()
    avisado = models.BooleanField(default=False)
    dias_para_notificacao = 30

    def validade(self):
        dias = 365 * self.dose.duracao_meses / 12
        delta_validade = datetime.timedelta(dias)
        return self.data + delta_validade

    def dias_para_renovacao(self):
        return self.validade() - datetime.date.today()

    def vacina(self):
        return self.dose.vacina

    def __str__(self):
        return str(self.dose) + " Válido até " + str(self.data)


class Solicitacao(models.Model):
    PENDENTE = 1
    RESOLVIDO = 2
    NEGADA = 3
    STATUS = (
        (PENDENTE, "Pendente"),
        (RESOLVIDO, "Resolvido"),
        (NEGADA, "Negada")
    )

    texto = models.TextField()
    datahora = models.DateTimeField(auto_now_add=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE, null=True, to_field='nome')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    status = models.IntegerField(default=PENDENTE, choices=STATUS)

    def is_revisao(self):
        return Vacina.objects.filter(nome=self.vacina_id).exists()

    def nome_vacina(self):
        return self.vacina_id
