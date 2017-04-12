from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from vacpass.models import Usuario, Cartao, Dependente
from .forms import CriarContaForm, DependenteForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import *



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


def gerenciar_dep(request):
    form = DependenteForm()
    if request.POST:
        form = DependenteForm(request.POST)
        if form.is_valid():
            cartao = Cartao()
            cartao.save()
            dependente = form.save(commit=False)
            dependente.cartao = cartao
            dependente.usuario = request.user.usuario
            dependente.save()

    dependentes = Dependente.objects.filter(usuario=request.user.usuario)
    return render(request, 'vacpass/gerenciarDep.html', {'form': form, 'dependentes': dependentes})


def edit_dep(request):
    form = DependenteForm()
    dependentes = Dependente.objects.filter(usuario=request.user.usuario)
    return render(request, 'vacpass/editDep.html', {'form': form, 'dependentes': dependentes})


class DepUpdate(UpdateView):
    model = Dependente
    fields = ['CPF', 'nome', 'certidao']
    template_name_suffix = '_update_form'


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
            exits_cpf = User.objects.filter(username=cpf)
            exits_email = User.objects.filter(email=email)
            has_error = False;
            if (exits_email.count() > 0):
                form.add_error('email','Ja existe um usuario com esse Email')
                has_error = True
            if (exits_cpf.count() > 0):
                form.add_error('cpf', 'Ja existe um usuario com esse CPF')
                has_error = True
            if (senha != confirmacao):
                form.add_error('confirmar_senha', 'Senhas nao coincidem')
                has_error = True
            if (len(senha) < 6):
                form.add_error('senha', 'Senha deve conter pelo menos seis digitos')
                has_error = True
            if not has_error:
                user = User.objects.create_user(cpf, email, senha, first_name=nome)
                newUser = Usuario(nascimento=nascimento, cartao=cartao, django_user=user)
                newUser.save()
                return render(request, 'registration/login.html', {'form': AuthenticationForm(), 'new_user': True})

            return render(request, 'registration/criarconta.html', {'form': form})

    return render(request, 'registration/criarconta.html', {'form': form})
