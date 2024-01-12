from django.contrib import admin
from .models import *


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                    'Ocupacion_Usuario')
    search_fields = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                     'Ocupacion_Usuario')
    list_filter = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                   'Ocupacion_Usuario')


admin.site.register(Usuario, UsuarioAdmin)