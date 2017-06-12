from django.conf.urls import url
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index', permanent=True)),
    url(r'^index/$', index, name='index'),
    url(r'^contas/criarconta/$', criar_conta, name='criarconta'),
    url(r'^contas/recuperarsenha/$', recupera_senha, name='recuperasenha'),

    url(r'^conta/gerenciar/$', gerenciar_conta, name='gerenciarconta'),
    url(r'^conta/dependente/editar/(?P<pk>\d+)/$', DependenteUpdate.as_view(), name='editardependente'),
    url(r'^conta/dependente/excluir/(?P<pk>\d+)/$', DependenteExclude.as_view(), name='excluirdependente'),
    url(r'^conta/editarconta/$', editar_conta, name='editarconta'),
    url(r'^conta/deletarconta/$', excluir_conta, name='deletarconta'),
    url(r'^conta/editarsenha/$', editar_senha, name='editarsenha'),

    url(r'^solicitacoes/solicitacoes/$', solicitacoes, name='solicitacoes'),
    url(r'^solicitacoes/solicitacao/(?P<solicitacao_pk>\d+)/$', ConsultaSolicitacao.as_view(), name='consultarsolicitacao'),
    url(r'^solicitacoes/solicitacao/(?P<solicitacao_pk>\d+)/reabrir/$', reabrir_solicitacao, name='reabrirsolicitacao'),
    url(r'^solicitacoes/solicitarvacina/$', solicitar_vacina, name='solicitarvacina'),

    url(r'^vacinas/consultar/(?P<vacina_pk>\d+)/solicitar_revisao/$', solicitar_revisao, name='solicitarrevisao'),
    url(r'^vacinas/buscar/$', buscar_vacina, name='buscarvacina'),
    url(r'^vacinas/consultar/(?P<pk>\d+)/$', ConsultarVacina.as_view(), name='consultarvacina'),

    url(r'^cartao/meucartao/$', meu_cartao, name='meucartao'),
    url(r'^cartao/deletardose/(?P<string>.+)/(?P<ndose>[0-9])/', deletar_dose, name='deletardose'),
    url(r'^cartao/novavacina/$', nova_vacina, name='novavacina'),
    url(r'^cartao/renovavacina/$', renova_vacina, name='renovarvacina'),
]