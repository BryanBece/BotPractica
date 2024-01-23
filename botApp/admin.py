from django.contrib import admin
from .models import *


class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "anioNacimiento",
        "Comuna_Usuario",
        "Genero_Usuario",
        "SistemaSalud_Usuario",
        "Ocupacion_Usuario",
    )
    search_fields = (
        "id",
        "anioNacimiento",
        "Comuna_Usuario",
        "Genero_Usuario",
        "SistemaSalud_Usuario",
        "Ocupacion_Usuario",
    )
    list_filter = (
        "id",
        "anioNacimiento",
        "Comuna_Usuario",
        "Genero_Usuario",
        "SistemaSalud_Usuario",
        "Ocupacion_Usuario",
    )


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta")
    search_fields = ("id", "pregunta")
    list_filter = ("id", "pregunta")


class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "id_usuario",
        "id_pregunta",
        "id_opc_respuesta",
        "fecha_respuesta",
    )
    search_fields = (
        "id",
        "id_usuario",
        "id_pregunta",
        "id_opc_respuesta",
        "fecha_respuesta",
    )
    list_filter = (
        "id",
        "id_usuario",
        "id_pregunta",
        "id_opc_respuesta",
        "fecha_respuesta",
    )


class OPC_RespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "id_pregunta", "OPC_Respuesta")
    search_fields = ("id", "id_pregunta", "OPC_Respuesta")
    list_filter = ("id", "id_pregunta", "OPC_Respuesta")


class ComunaAdmin(admin.ModelAdmin):
    list_display = ("id", "Nombre_Comuna")
    search_fields = ("id", "Nombre_Comuna")
    list_filter = ("id", "Nombre_Comuna")


class GeneroAdmin(admin.ModelAdmin):
    list_display = ("id", "OPC_Genero")
    search_fields = ("id", "OPC_Genero")
    list_filter = ("id", "OPC_Genero")


class SistemaSaludAdmin(admin.ModelAdmin):
    list_display = ("id", "OPC_SistemaSalud")
    search_fields = ("id", "OPC_SistemaSalud")
    list_filter = ("id", "OPC_SistemaSalud")


class OcupacionAdmin(admin.ModelAdmin):
    list_display = ("id", "OPC_Ocupacion")
    search_fields = ("id", "OPC_Ocupacion")
    list_filter = ("id", "OPC_Ocupacion")


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)
admin.site.register(OPC_Respuesta, OPC_RespuestaAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(SistemaSalud, SistemaSaludAdmin)
admin.site.register(Ocupacion, OcupacionAdmin)
