from django.conf.urls import url
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index', permanent=True)),
    url(r'^index/$', index, name='index'),
    url(r'^solicitarvacina/$', solicitar_vacina, name='solicitarvacina'),
    url(r'^gerenciarvacina/$', gerenciar_vacina, name='gerenciarvacina'),
    url(r'^meucartao/$', meu_cartao, name='meucartao')
]