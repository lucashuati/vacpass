from django.contrib import admin
from vacpass.models import Usuario


class UsuariosAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usuario, UsuariosAdmin)

