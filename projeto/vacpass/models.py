from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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
    CPF = models.CharField(max_length=15)
    nome = models.CharField(max_length=50)
    certidao = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao = models.ForeignKey(Cartao)

    def get_absolute_url(self):
        return reverse('editdep', args=[str(self.id)])

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    nome = models.CharField(max_length=50)
    funcionalidade = models.CharField(max_length=500, default="")
    publico_alvo = models.CharField(max_length=500, default="")
    disponibilidade = models.CharField(max_length=500, default="")
    proibitivos = models.CharField(max_length=500, default="")
    preco = models.FloatField(default=0)
    cartao = models.ManyToManyField(Cartao, through="ControleVencimento")

    def doses(self):
        return DoseVacina.objects.filter(vacina=self)

    def __str__(self):
        return self.nome


class ControleVencimento(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    data = models.DateField()
    vencimento = models.DateField()

    def __str__(self):
        return self.vencimento


class DoseVacina(models.Model):
    dose = models.IntegerField()
    idade = models.CharField(max_length=50)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)

    def __str__(self):
        return "dose {}: {} ".format(self.dose, self.idade)