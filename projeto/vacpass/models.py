from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Usuario(models.Model):
    CPF = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    def __str__(self):
        return self.nome

class Dependente(models.Model):
    CPF = models.CharField(max_length=11)
    nome = models.CharField(max_length=50)
    certidao = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class Cartao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE)
    def __str__(self):
        return self.usuario


class Vacina(models.Model):
    nome = models.CharField(max_length=50)
    dose = models.IntegerField(default = 0)
    cartao = models.ManyToManyField(Cartao, through="ControleVencimento")
    def __str__(self):
        return self.nome


class ControleVencimento(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete= models.CASCADE)
    vacina = models.ForeignKey(Vacina, on_delete= models.CASCADE)
    data = models.DateField()
    vencimento = models.DateField()
    def __str__(self):
        return self.vencimento
