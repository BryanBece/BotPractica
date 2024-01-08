from django.contrib import admin
from .models import *

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuario', 'anioNacimiento', 'comuna', 'genero', 'fecha_ingreso')
    search_fields = ('id_usuario', 'comuna__nombre', 'genero__nombre')
    list_filter = ('comuna', 'genero')

class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)

admin.site.register(Respuesta, RespuestaAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Genero, GeneroAdmin)

