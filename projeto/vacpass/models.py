from __future__ import unicode_literals

from django.db import models


class Cartao(models.Model):
    nome = models.CharField(max_length=12)

    def __str__(self):
        return self.nome


# Create your models here.
class Usuario(models.Model):
    CPF = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    nascimento = models.DateField()
    cartao = models.ForeignKey(Cartao)

    def __str__(self):
        return self.nome


class Dependente(models.Model):
    CPF = models.CharField(max_length=11)
    nome = models.CharField(max_length=50)
    certidao = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao = models.ForeignKey(Cartao)

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    nome = models.CharField(max_length=50)
    cartao = models.ManyToManyField(Cartao, through="ControleVencimento")

    def __str__(self):
        return self.nome


class ControleVencimento(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    data = models.DateField()
    vencimento = models.DateField()

    def __str__(self):
        return self.vencimento


class doseVacina(models.Model):
    dose = models.IntegerField()
    duracaoMeses = models.IntegerField()
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
