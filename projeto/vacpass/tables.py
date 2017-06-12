from django.urls import reverse
from django.utils.safestring import mark_safe
from django_tables2 import tables
from django_tables2.utils import Accessor

from vacpass.models import Vacina, DoseVacina, Solicitacao, Dependente


def truncar(long_str):
    if len(long_str) > 23:
        return long_str[:20]+'...'
    else:
        return long_str


class VacinaTable(tables.Table):
    class Meta:
        model = Vacina
        exclude = ['id']
    doses = tables.columns.Column()
    nome = tables.columns.LinkColumn(accessor='nome')

    def render_doses(self, record):
        return DoseVacina.objects.filter(vacina=record).count()

    def render_funcionalidade(self, record):
        return truncar(record.funcionalidade)

    def render_publico_alvo(self, record):
        return truncar(record.publico_alvo)

    def render_disponibilidade(self, record):
        return truncar(record.disponibilidade)

    def render_proibitivos(self, record):
        return truncar(record.proibitivos)

    def render_preco(self, record):
        return 'gratuito' if record.preco == 0 else record.preco


class DoseTable(tables.Table):
    class Meta:
        model = DoseVacina
        exclude = ['id', 'vacina']


class SolicitacaoTable(tables.Table):
    class Meta:
        model = Solicitacao
    vacina = tables.columns.Column(accessor='nome_vacina')
    solicitante = tables.columns.LinkColumn(viewname='admin:vacpass_usuario_change', args=[Accessor('solicitante.id')])
    tipo = tables.columns.BooleanColumn(accessor='is_revisao', yesno='Revisão,Nova vacina')
    status = tables.columns.LinkColumn(accessor='status', viewname='consultarsolicitacao', args=[Accessor('id')])

    def render_texto(self, record):
        return truncar(record.texto)

    def render_vacina(self, record):
        nome = record.nome_vacina()
        if Vacina.objects.filter(nome=nome).exists():
            return mark_safe('<a href={}>{}</a>'.format(reverse('consultarvacina', args=[record.vacina.id]), nome))
        else:
            return nome


class DependenteTable(tables.Table):
    class Meta:
        model = Dependente
        exclude = ['id', 'tipo', 'ndocumento', 'cartao']
    documento = tables.columns.Column(accessor='documento')
    editar = tables.columns.LinkColumn(text='editar', viewname='editardependente', args=[Accessor('id')])
    excluir = tables.columns.LinkColumn(text='excluir', viewname='excluirdependente', args=[Accessor('id')])
