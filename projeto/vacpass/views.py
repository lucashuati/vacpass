from django.conf import settings
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'vacpass/index.html', {"basedir": settings.BASE_DIR})


def solicitar_vacina(request):
    pass


def gerenciar_vacina(request):
    pass


def meu_cartao(request):
    pass