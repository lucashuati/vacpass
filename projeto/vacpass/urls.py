from django.conf.urls import url
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index', permanent=True)),
    url(r'^index/$', index, name='index'),
    url(r'^solicitarvacina/$', solicitar_vacina, name='solicitarvacina'),
    url(r'^gerenciarvacina/$', gerenciar_vacina, name='gerenciarvacina'),
    url(r'^meucartao/$', meu_cartao, name='meucartao'),
    url('^contas/criar_conta', criar_conta, name="criarconta"),
    url(r'^gerenciardependente/$', gerenciar_dep, name = "gerenciardependente"),
    url(r'^editdep/(?P<pk>\d+)$', DepUpdate.as_view(template_name='vacpass/editDep.html'), name = "editdep")
]