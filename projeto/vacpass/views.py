# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import *
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DetailView
from django.views.generic.edit import DeleteView
from django_tables2 import RequestConfig

from vacpass.filters import *
from vacpass.tables import *
from .forms import *


def calcula_dict(cartao):
    vacinas_user = ControleVencimento.objects.filter(cartao=cartao).order_by('dose')
    dose_dict = {}
    for vac in vacinas_user:

        data_validade = vac.validade()
        vacina_nome = vac.dose.vacina.nome
        if vacina_nome in dose_dict:
            dose_dict[vacina_nome].append([vac.dose, vac.data.strftime("%d/%m/%y"), data_validade.strftime("%d/%m/%y"),
                                           vac.dose.vacina.num_doses()])
        else:
            dose_dict[vacina_nome] = [[vac.dose, vac.data.strftime("%d/%m/%y"), data_validade.strftime("%d/%m/%y"),
                                       vac.dose.vacina.num_doses()]]

    return dose_dict


# Calculo das novas vacinas de um usuario
def calcula_novas_vacinas(dose_dict=False):
    return [v for v in Vacina.objects.all() if v.nome not in dose_dict]


def index(request):
    return render(request, 'vacpass/index.html', {"basedir": settings.BASE_DIR})


def solicitar_revisao(request, vacina_pk):
    vacina = Vacina.objects.get(id=vacina_pk)
    form = SolicitacaoRevisaoForm(request.POST or None)
    solicitado = False
    if request.POST:
        if form.is_valid():
            texto = form.cleaned_data['texto']
            solicitante = request.user.usuario
            revisao = Solicitacao(texto=texto, vacina=vacina, solicitante=solicitante)
            revisao.save()
            messages.info(
                request,
                "Sua sugestão foi recebida e será avaliada por um de nossos colaboradores. Aguarde contato por email."
            )
            solicitado = True

    context = {'form': form, 'vacina': vacina, 'solicitado': solicitado}
    return render(request, 'vacpass/vacina/solicitar_revisao.html', context)


def solicitar_vacina(request):
    form = RecomedacaoForm()
    template = 'vacpass/solicitacoes/recomendar.html'
    context = {'form': form}

    if request.POST:
        form = RecomedacaoForm(request.POST)
        if form.is_valid():
            vacina = form.cleaned_data['vacina']
            texto = form.cleaned_data['texto']
            solicitante = Usuario.objects.get(django_user=request.user)
            s = Solicitacao(vacina_id=vacina, texto=texto, solicitante=solicitante)
            s.save()
            messages.success(
                request,
                'Sua sugestão foi recebida e será avaliada por um de nossos colaboradores. Aguarde contato por email.'
            )
    return render(request, template, context)


def solicitacoes(request):
    solicitacoes_pendentes = Solicitacao.objects.filter(status=Solicitacao.PENDENTE)
    solicitacoes_nao_pendentes = Solicitacao.objects.exclude(status=Solicitacao.PENDENTE)

    pendentes_filter = SolicitacaoFilter(request.GET, solicitacoes_pendentes, id_formulario=1)
    resolvidas_filter = SolicitacaoFilter(request.GET, solicitacoes_nao_pendentes, id_formulario=2)

    if not pendentes_filter.qs.exists() and not pendentes_filter.is_empty():
        messages.warning(request, 'Nenhuma solicitação pendente para os filtros selecionados')

    if not resolvidas_filter.qs.exists() and not resolvidas_filter.is_empty():
        messages.warning(request, 'Nenhuma solicitação resolvida para os filtros selecionados')

    pendentes_table = SolicitacaoTable(pendentes_filter.qs)
    resolvidas_table = SolicitacaoTable(resolvidas_filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(pendentes_table)
    RequestConfig(request, paginate={'per_page': 10}).configure(resolvidas_table)

    context = {'pendentes_filter': pendentes_filter, 'resolvidas_filter': resolvidas_filter,
               'pendentes_table': pendentes_table, 'resolvidas_table': resolvidas_table}
    return render(request, 'vacpass/solicitacoes/solicitacoes.html', context)


class ConsultaSolicitacao(View):
    form_class = RespostaSolicitacaoForm
    template_name = 'vacpass/solicitacoes/consultar.html'

    def gerar_texto_email(self, solicitante, respondente, resposta, solicitacao):
        tipo_solicitacao = "revisão para a vacina {}" if solicitacao.is_revisao() else "nova vacina ({})"
        tipo_solicitacao = tipo_solicitacao.format(solicitacao.vacina_id)
        texto = "Honorável {},\n\n".format(solicitante)
        texto += "Sua solicitação de {} foi respondida. Segue a resposta:\n".format(tipo_solicitacao)
        texto += "{}\nResposta escrita por {}.\n".format(resposta, respondente)
        texto += "A situação da solicitação agora é {}.".format(solicitacao.get_status_display())
        texto += "\n\nAtenciosamente, \nVacPass"
        return texto

    def post(self, request, solicitacao_pk):
        form = self.form_class(request.POST)
        solicitacao = Solicitacao.objects.get(id=solicitacao_pk)
        if form.is_valid():
            solicitante_user = solicitacao.solicitante.django_user
            texto = self.gerar_texto_email(
                solicitante_user.first_name,
                request.user.first_name,
                form.cleaned_data['texto'],
                solicitacao
            )
            assunto = 'VacPass - Aviso de resposta de solicitação'
            send_mail(assunto, texto, settings.EMAIL_HOST_USER, [solicitante_user.email])
            solicitacao.status = form.cleaned_data['situacao']
            solicitacao.save()
            messages.success(request, "Solicitação {} foi respondida com sucesso.".format(solicitacao_pk))
            return redirect(reverse(solicitacoes))

    def get(self, request, solicitacao_pk):
        form = self.form_class()
        solicitacao = Solicitacao.objects.get(id=solicitacao_pk)
        return render(request, self.template_name, {'form': form, 'solicitacao': solicitacao})


def reabrir_solicitacao(request, solicitacao_pk):
    solicitacao = Solicitacao.objects.get(id=solicitacao_pk)
    if solicitacao.status != Solicitacao.PENDENTE:
        messages.success(request, "Solicitação {} foi reaberta.".format(solicitacao_pk))
        solicitacao.status = Solicitacao.PENDENTE
        solicitacao.save()
    else:
        messages.warning(request, "Solicitação {} já estava aberta.".format(solicitacao_pk))
    return redirect("consultarsolicitacao", solicitacao_pk)


def renova_vacina(request):
    usuario = Usuario.objects.get(django_user=request.user)
    cartao = usuario.cartao
    dependentes = Dependente.objects.filter(usuario=request.user.usuario)

    error = False
    if request.POST:
        form = RenovaVacinaForm(request.POST)

        if form.is_valid():
            data_input = form.cleaned_data['rdata']
            vacina = form.cleaned_data['rvacina']
            vacina = Vacina.objects.get(nome=vacina)

            dose = form.cleaned_data['dose']
            dose_ant = DoseVacina.objects.get(vacina=vacina, dose=dose - 1)
            dose = DoseVacina.objects.get(vacina=vacina, dose=dose)
            data_anterior = ControleVencimento.objects.get(cartao=cartao, dose=dose_ant).data
            if data_input > datetime.date.today():
                error = 'Esta data ainda nao chegou'
            if data_anterior > data_input:
                error = 'Data anterior a ultima dose'
            if not error:
                newControle = ControleVencimento(cartao=cartao, dose=dose, data=data_input)
                newControle.save()

    if not error:
        return redirect('meucartao')

    dose_dict = calcula_dict(cartao)
    vacinas = calcula_novas_vacinas(dose_dict)

    return render(request, 'vacpass/cartao/cartao_vacina.html',
                  {'dependetes': dependentes, 'vacinas': vacinas, 'doses': dose_dict, 'formNew': NovaVacinaCartaoForm(),
                   'formRenova': RenovaVacinaForm(),
                   'errorRenova': error})


def nova_vacina(request):
    usuario = Usuario.objects.get(django_user=request.user)
    cartao = usuario.cartao
    dependentes = Dependente.objects.filter(usuario=request.user.usuario)

    error = False
    if request.POST:
        form = NovaVacinaCartaoForm(request.POST)

        if form.is_valid():
            data_input = form.cleaned_data['data']
            vacina_pk = form.cleaned_data['vacina']
            if data_input > datetime.date.today():
                error = 'Esta data ainda nao chegou'
            else:
                vacina = Vacina.objects.get(pk=vacina_pk)
                dose = DoseVacina.objects.get(vacina=vacina, dose=1)
                newControle = ControleVencimento(cartao=cartao, dose=dose, data=data_input)
                newControle.save()

    if not error:
        return redirect('meucartao')

    dose_dict = calcula_dict(cartao)
    vacinas = calcula_novas_vacinas(dose_dict)

    return render(request, 'vacpass/cartao/cartao_vacina.html',
                  {'dependetes': dependentes, 'vacinas': vacinas, 'doses': dose_dict, 'formNew': NovaVacinaCartaoForm(),
                   'formRenova': RenovaVacinaForm(), 'horaAtual': datetime.date.today().strftime("%d/%m/%y"),
                   'errorAdd': error})


def deletar_dose(request, string="empty", ndose=0):
    form = DeletaDoseForm()
    sucess = False
    if request.POST:
        form = DeletaDoseForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['vacina']
            dose = form.cleaned_data['dose']
            vacina = Vacina.objects.get(nome=nome)
            d = DoseVacina.objects.get(dose=dose, vacina=vacina)
            c = Usuario.objects.get(django_user=request.user).cartao
            ControleVencimento.objects.get(dose=d, cartao=c).delete()
            sucess = True

    context = {'form': form, 'vacina': string, 'dose': ndose, 'removida': sucess}
    return render(request, 'vacpass/cartao/deletar_dose.html', context)


def meu_cartao(request):
    usuario = Usuario.objects.get(django_user=request.user)
    cartao = usuario.cartao
    dependentes = Dependente.objects.filter(usuario=request.user.usuario)

    formNew = NovaVacinaCartaoForm()
    formRenova = RenovaVacinaForm()

    if formRenova.is_valid():
        dose = formRenova.cleaned_data['dose']
        data_input = formRenova.cleaned_data['rdata']
        vacina = formRenova.cleaned_data['rvacina']
        vacina = Vacina.objects.get(nome=vacina)
        dose = DoseVacina.objects.get(vacina=vacina, dose=dose)

        newControle = ControleVencimento(cartao=cartao, dose=dose, data=data_input)
        newControle.save()

    # Cria os vencimento
    dose_dict = calcula_dict(cartao)
    vacinas = calcula_novas_vacinas(dose_dict)

    return render(request, 'vacpass/cartao/cartao_vacina.html',
                  {'dependetes': dependentes, 'vacinas': vacinas, 'doses': dose_dict, 'formNew': formNew,
                   'formRenova': formRenova, 'horaAtual': datetime.date.today().strftime("%d/%m/%y")})


def buscar_vacina(request):
    filter = VacinaFilter(request.GET, Vacina.objects.all())
    table = VacinaTable(filter.qs)
    RequestConfig(request).configure(table)
    if not filter.qs.exists():
        messages.warning(request, 'Nenhum resultado encontrado')
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


def gerenciar_conta(request):
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

    dependentes_table = DependenteTable(Dependente.objects.filter(usuario=request.user.usuario))
    RequestConfig(request, paginate={'per_page': 10}).configure(dependentes_table)
    return render(request, 'vacpass/conta/gerenciar_conta.html', {'form': form, 'dependentes_table': dependentes_table})


class DependenteUpdate(UpdateView):
    model = Dependente
    form_class = DependenteForm
    template_name = 'vacpass/conta/editar_dependente.html'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        messages.success(self.request, "O dependente foi editado")
        return reverse(gerenciar_conta)


class DependenteExclude(DeleteView):
    model = Dependente
    template_name = 'vacpass/conta/excluir_dependente.html'
    fields = ['nome']

    def get_success_url(self):
        messages.success(self.request, "O dependente foi excluido")
        return reverse(gerenciar_conta)


class ContaUpdate(UpdateView):
    model = User
    fields = ['first_name', 'email']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(gerenciar_conta)


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

    return render(request, 'vacpass/conta/deletar_conta.html', {'form': form})


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
                update_session_auth_hash(request, request.user)
                messages.info(request, 'Sua senha foi atualizada')
                return redirect(reverse(gerenciar_conta))

    return render(request, 'vacpass/conta/editar_senha.html', {'form': form})


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
                    form.add_error('email', 'Email ja existe')
                    has_error = True
                if not request.user.check_password(pass_field):
                    form.add_error('password', 'Senha Incorreta')
                    has_error = True
                if has_error:
                    return render(request, 'vacpass/conta/editar_conta.html', {'form': form})
                else:
                    user.email = email_new
            user.first_name = name_new
            user.save()
            messages.info(request, 'Usuario editado com sucesso')
            return redirect('gerenciarconta')

    return render(request, 'vacpass/conta/editar_conta.html', {'form': form})


def criar_conta(request):
    form = CriarContaForm()
    if request.POST:
        form = CriarContaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cartao = Cartao(nome="cartao do " + nome)
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
                cartao.save()
                user = User.objects.create_user(cpf, email, senha, first_name=nome)
                new_user = Usuario(nascimento=nascimento, cartao=cartao, django_user=user)
                new_user.save()
                messages.info(request, 'Usuario criado com sucesso, agora basta realizar seu login')
                return render(request, 'registration/login.html', {'form': AuthenticationForm()})

            return render(request, 'registration/criarconta.html', {'form': form})

    return render(request, 'registration/criarconta.html', {'form': form})


def recupera_senha(request):
    form = RecuperaSenhaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            if not User.objects.filter(email=email).exists():
                form.add_error('email', 'Email nao cadastrado')
            else:
                senha_nova = User.objects.make_random_password(length=10)
                user = User.objects.get(email=email)
                user.set_password(senha_nova)
                user.save()
                texto = 'Geramos sua nova senha: {}' \
                        '\n\nCaso deseje alterar para uma de sua preferencia,"' \
                        ' entre no seu perfil e clique na aba alterar senha seguindo os passos descritos."' \
                        '\n\n Vacpass Company 2017.'.format(senha_nova)
                send_mail('Recuperacao de Senha', texto, settings.EMAIL_HOST_USER, [email])
                messages.info(request, 'Nova senha enviada para seu e-mail')
                return render(request, 'registration/login.html', {'form': AuthenticationForm()})

    return render(request, 'vacpass/recuperar_senha.html', {'form': form})

