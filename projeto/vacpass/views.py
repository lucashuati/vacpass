from django.conf import settings
from django.shortcuts import render, redirect

from .forms import CriarContaForm


def index(request):
    return render(request, 'vacpass/index.html', {"basedir": settings.BASE_DIR})


def solicitar_vacina(request):
    pass


def gerenciar_vacina(request):
    pass


def meu_cartao(request):
    pass


def criar_conta(request):
    form = CriarContaForm()
    if request.POST:
        form = CriarContaForm(request.POST)
        if form.is_valid():
            return redirect('login')

    return render(request, 'registration/criarconta.html',{'form':form})
