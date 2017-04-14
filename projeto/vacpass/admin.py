from django.contrib import admin

from vacpass.forms import VacinaForm
from vacpass.models import Usuario, Vacina, DoseVacina


@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    pass


class DoseInline(admin.TabularInline):
    model = DoseVacina
    extra = 0


@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    form = VacinaForm
    inlines = [DoseInline]
