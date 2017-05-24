from django.conf.urls import url
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index', permanent=True)),
    url(r'^index/$', index, name='index'),
    url(r'^solicitarvacina/$', solicitar_vacina, name='solicitarvacina'),
    url(r'^solicitacoes/$', solicitacoes, name='solicitacoes'),
    url(r'^vacinas/buscar/$', buscar_vacina, name='buscarvacina'),
    url(r'^vacinas/consultar/(?P<pk>\d+)/$', ConsultarVacina.as_view(), name='consultarvacina'),
    url(r'^meucartao/$', meu_cartao, name='meucartao'),
    url('^contas/criar_conta', criar_conta, name="criarconta"),
    url(r'^gerenciardependente/$', gerenciar_dep, name="gerenciardependente"),
    url(r'^editdep/(?P<pk>\d+)$', DepUpdate.as_view(), name="editdep"),
    url(r'^excluidep/(?P<pk>\d+)$', DepExclude.as_view(), name="excluidep"),
    url(r'^editconta/', editar_conta, name="editconta"),
    url(r'^deleteconta/', excluir_conta, name="deleteconta"),
    url(r'^editpass/', editar_senha, name="editpass"),
    url(r'^recuperarsenha/',recupera_senha, name="recuperasenha")
]