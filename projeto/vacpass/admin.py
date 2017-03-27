from django.contrib import admin
from vacpass.models import *

class UsuariosAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario, UsuariosAdmin)
# Register your models here.
