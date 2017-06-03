from django.contrib import admin

from vacpass.forms import VacinaForm, DoseForm
from vacpass.models import Usuario, Vacina, DoseVacina


@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    pass


class DoseInline(admin.TabularInline):
    form = DoseForm
    model = DoseVacina
    extra = 0


@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    form = VacinaForm
    inlines = [DoseInline]
