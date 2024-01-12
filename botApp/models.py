from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Comuna(models.Model):
    Nombre_Comuna = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre_Comuna


class Genero(models.Model):
    FEMENINO = 'Femenino'
    MASCULINO = 'Masculino'
    OTRO = 'Otro'

    GENERO_CHOICES = [
        ('1', FEMENINO),
        ('2', MASCULINO),
        ('3', OTRO),
    ]

    OPC_Genero = models.CharField(max_length=50, choices=GENERO_CHOICES)

    def __str__(self):
        return self.OPC_Genero

class SistemaSalud(models.Model):
    FONASA = 'Fonasa'
    ISAPRE = 'Isapre'
    OTRO = 'Otro'

    SISTEMA_SALUD_CHOICES = [
        ('1', FONASA),
        ('2', ISAPRE),
        ('3', OTRO),
    ]

    OPC_SistemaSalud = models.CharField(max_length=50, choices=SISTEMA_SALUD_CHOICES)

    def __str__(self):
        return self.OPC_SistemaSalud

class Ocupacion(models.Model):
    DUENIACASA = 'Dueña de Casa'
    TRABAJADOR = 'Trabajadora'
    DESEMPLEADO = 'Desempleada'
    OTRO = 'Otro'

    OCUPACION_CHOICES = [
        ('1', DUENIACASA),
        ('2', TRABAJADOR),
        ('3', DESEMPLEADO),
        ('4', OTRO),
    ]

    OPC_Ocupacion = models.CharField(max_length=50, choices=OCUPACION_CHOICES)

    def __str__(self):
        return self.OPC_Ocupacion

class Usuario(models.Model):
    anioNacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    id_usuario = models.IntegerField()
    Comuna_Usuario = models.ForeignKey(Comuna, on_delete=models.PROTECT)
    Genero_Usuario = models.ForeignKey(Genero, on_delete=models.PROTECT)
    SistemaSalud_Usuario = models.ForeignKey(SistemaSalud, on_delete=models.PROTECT)
    Ocupacion_Usuario = models.ForeignKey(Ocupacion, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id_usuario} - {self.anioNacimiento}'

class Pregunta(models.Model):
    pregunta = models.CharField(max_length=200)

    def __str__(self):
        return self.pregunta

class OPC_Respuesta(models.Model):
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    OPC_Respuesta = models.CharField(max_length=200)

    def __str__(self):
        return self.OPC_Respuesta

class RespuestaUsuario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    id_opc_respuesta = models.ForeignKey(OPC_Respuesta, on_delete=models.CASCADE)
    fecha_respuesta = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id_usuario} - {self.id_pregunta} - {self.id_opc_respuesta}'
