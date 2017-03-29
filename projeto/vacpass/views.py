from django.conf import settings
from django.shortcuts import render, redirect
from vacpass.models import Usuario, Cartao
from .forms import CriarContaForm
from django.contrib.auth.models import User

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
            cartao = Cartao.objects.get(pk=1)
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']
            confirmacao = form.cleaned_data['confirmar_senha']
            nascimento = form.cleaned_data['nascimento']
            email = form.cleaned_data['email']
            user = User.objects.create_user(cpf, email, senha, first_name=nome)
            newUser = Usuario(nascimento=nascimento, cartao=cartao, django_user=user)
            newUser.save()
            return redirect('login')

    return render(request, 'registration/criarconta.html',{'form':form})
