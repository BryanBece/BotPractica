from django.contrib import admin
from .models import *


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                    'Ocupacion_Usuario')
    search_fields = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                     'Ocupacion_Usuario')
    list_filter = ('id', 'anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario',
                   'Ocupacion_Usuario')

                   
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pregunta')
    search_fields = ('id', 'pregunta')
    list_filter = ('id', 'pregunta')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Pregunta, PreguntaAdmin)

