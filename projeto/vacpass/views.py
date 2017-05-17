from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DetailView
from django_tables2 import RequestConfig
from django.core.mail import send_mail

import constants
from vacpass.filters import VacinaFilter
from vacpass.models import Usuario, Cartao
from vacpass.tables import VacinaTable, DoseTable
from .forms import *
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

#!/usr/bin/env python
# -*- coding: utf-8 -*-

def index(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return render(request, 'vacpass/index.html', {"basedir": settings.BASE_DIR})


def solicitar_vacina(request):
    pass


def meu_cartao(request):
    return render(request, 'vacpass/cartaoVacina.html', {})


def buscar_vacina(request):
    filter = VacinaFilter(request.GET, Vacina.objects.all())
    table = VacinaTable(filter.qs)
    RequestConfig(request).configure(table)
    if not filter.qs.exists():
        messages.warning(request, constants.noresult)
    context = {'table': table, 'filter': filter}

    return render(request, 'vacpass/vacina/buscar.html', context)


class ConsultarVacina(DetailView):
    model = Vacina
    template_name = 'vacpass/vacina/consultar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dosetable = DoseTable(self.object.dosevacina_set.all())
        RequestConfig(self.request).configure(dosetable)
        context.update(dosetable=dosetable)
        return context


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
    form_class = DependenteForm
    template_name = 'vacpass/editDep.html'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        messages.success(self.request, "O dependente foi editado")
        return reverse(gerenciar_dep)

class DepExclude(DeleteView):
    model = Dependente
    template_name = 'vacpass/excluiDep.html'
    fields = ['nome']


    def get_success_url(self):
        messages.success(self.request, "O dependente foi excluido")
        return reverse(gerenciar_dep)




class ContaUpdate(UpdateView):
    model = User
    fields = ['first_name', 'email']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        return super(ContaUpdate, self).form_valid(form)

    def get_success_url(self):
        return '../gerenciardependente/'


def excluir_conta(request):
    form = ExcluirContaForm()

    if request.POST:
        form = ExcluirContaForm(request.POST)
        if form.is_valid():
            pass_field = form.cleaned_data['senha']
            if request.user.check_password(pass_field):
                user = request.user
                user.delete()
                messages.info(request, "Sua conta foi excluida.")
                return redirect('login')
            else:
                form.add_error('senha', 'Senha Incorreta')

    return render(request, 'vacpass/deletarConta.html', {'form': form})


def editar_senha(request):
    form = EditPassForm()

    if request.POST:
        form = EditPassForm(request.POST)
        if form.is_valid():
            senha_nova = form.cleaned_data['nova_senha']
            confirmacao = form.cleaned_data['confirmacao']
            senha_antiga = form.cleaned_data['senha']
            has_error = False
            if len(senha_nova) < 6:
                form.add_error('nova_senha', 'A senha deve ter pelo menos 6 digitos')
                has_error = True
            if senha_nova != confirmacao:
                form.add_error('confirmacao', 'Senhas nao coincidem')
                has_error = True
            if not request.user.check_password(senha_antiga):
                form.add_error('senha', 'Senha Incorreta')
                has_error = True
            if not has_error:
                request.user.set_password(senha_nova)
                request.user.save()
                dependentes = Dependente.objects.filter(usuario=request.user.usuario)
                messages.info(request, 'Sua senha foi atualizada')
                return render(request, 'vacpass/gerenciarDep.html', {'form': DependenteForm(), 'dependentes': dependentes})

    return render(request, 'vacpass/editPass.html', {'form': form})

def editar_conta(request):
    form = EditarContaForm()
    email_field = form.fields['email']
    name_field = form.fields['nome']
    email_field.initial = request.user.email
    name_field.initial = request.user.first_name
    if request.POST:
        form = EditarContaForm(request.POST)
        if form.is_valid():
            email_new = form.cleaned_data['email']
            name_new = form.cleaned_data['nome']
            pass_field = form.cleaned_data['password']
            user = request.user
            if email_field.initial != email_new:
                has_error = False
                exits_email = User.objects.filter(email=email_new)
                if exits_email.count() > 0:
                    form.add_error('email','Email ja existe')
                    has_error = True
                if not request.user.check_password(pass_field):
                    form.add_error('password', 'Senha Incorreta')
                    has_error = True
                if has_error:
                    return render(request, 'vacpass/editarConta.html', {'form': form})
                else:
                    user.email = email_new
            user.first_name = name_new
            user.save()
            dependentes = Dependente.objects.filter(usuario=request.user.usuario)
            messages.info(request, 'Usuario editado com sucesso')
            return render(request, 'vacpass/gerenciarDep.html', {'form': DependenteForm(), 'dependentes': dependentes})

    return render(request, 'vacpass/editarConta.html', {'form': form})


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
            has_error = False
            if exits_email.count() > 0:
                form.add_error('email', 'Ja existe um usuario com esse Email')
                has_error = True
            if exits_cpf.count() > 0:
                form.add_error('cpf', 'Ja existe um usuario com esse CPF')
                has_error = True
            if senha != confirmacao:
                form.add_error('confirmar_senha', 'Senhas nao coincidem')
                has_error = True
            if len(senha) < 6:
                form.add_error('senha', 'Senha deve conter pelo menos seis digitos')
                has_error = True
            if not has_error:
                user = User.objects.create_user(cpf, email, senha, first_name=nome)
                new_user = Usuario(nascimento=nascimento, cartao=cartao, django_user=user)
                new_user.save()
                messages.info(request, 'Usuario criado com sucesso, agora basta realizar seu login')
                return render(request, 'registration/login.html', {'form': AuthenticationForm()})

            return render(request, 'registration/criarconta.html', {'form': form})

    return render(request, 'registration/criarconta.html', {'form': form})


def recupera_senha(request) :
    form = RecuperaSenha()
    email_field = form.fields['email']
    if request.POST:
        form = RecuperaSenha(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            valid_email = User.objects.filter(email=email)
            has_error = False
            if not valid_email.exists():
                form.add_error('email', 'Email nao cadastrado')
                has_error = True
            if not has_error:
               #senha =  User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789')
               senha_nova = 'aabb1234'
               user = User.objects.get(email= email)
               user.set_password(senha_nova)
               user.save()
               texto = 'Sua Nova senha gerada: ' + senha_nova + ' \n\nPara colocar a senha desejada, entre na aba alterar senha do seu perfil e siga os passos descritos\n\n Vacpass Company '
               send_mail('Recuperacao de Senha', texto, settings.EMAIL_HOST_USER, [email])
               messages.info(request, 'Nova senha enviada para seu e-mail')
               return render(request, 'registration/login.html', {'form': AuthenticationForm()})

        return render(request, 'vacpass/recuperaSenha.html', {'form': form})
    else:
        return render(request, 'vacpass/recuperaSenha.html', {'form': form})