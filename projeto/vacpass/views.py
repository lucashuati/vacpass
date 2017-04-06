from django.conf import settings
from django.shortcuts import render, redirect
from vacpass.models import Usuario, Cartao
from .forms import CriarContaForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from datetime import date



def index(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
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
            CREATE_ERRO=[]
            exits_cpf = User.objects.filter(username=cpf)
            exits_email = User.objects.filter(email=email)
            delta_days = date.today()-nascimento;
            if(exits_email.count() > 0):
                CREATE_ERRO.append(1)
                form.add_error('email', "Erros?")
            if(exits_cpf.count() > 0):
                CREATE_ERRO.append(2)
            if(senha != confirmacao):
                CREATE_ERRO.append(3)
            if(len(senha) < 6):
                CREATE_ERRO.append(4)

            if(len(CREATE_ERRO) == 0):
                user = User.objects.create_user(cpf, email, senha, first_name=nome)
                newUser = Usuario(nascimento=nascimento, cartao=cartao, django_user=user)
                newUser.save()
                # return redirect('login')

                return render(request, 'registration/login.html',{'form':AuthenticationForm(), 'login_criado':True})
            else:
                return render(request, 'registration/criarconta.html',{'form':form, 'CREATE_ERRO':CREATE_ERRO})

    return render(request, 'registration/criarconta.html',{'form':form})
