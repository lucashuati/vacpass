from django_tables2 import tables

from vacpass.models import Vacina, DoseVacina

def truncar(long_str):
    return long_str[:20]+'...'


class VacinaTable(tables.Table):
    class Meta:
        model = Vacina
        exclude = ['id']
    doses = tables.columns.Column()

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