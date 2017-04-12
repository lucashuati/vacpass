from django.contrib import admin

from vacpass.forms import VacinaForm
from vacpass.models import Usuario, Vacina


@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    form = VacinaForm
    pass
