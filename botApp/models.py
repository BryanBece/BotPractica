from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Comuna(models.Model):
    Nombre_Comuna = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre_Comuna


class Genero(models.Model):
    FEMENINO = "Femenino"
    MASCULINO = "Masculino"
    OTRO = "Otro"

    GENERO_CHOICES = [
        (FEMENINO, "Femenino"),
        (MASCULINO, "Masculino"),
        (OTRO, "Otro"),
    ]

    OPC_Genero = models.CharField(max_length=50, choices=GENERO_CHOICES)

    def __str__(self):
        return self.OPC_Genero


class SistemaSalud(models.Model):
    FONASA = "Fonasa"
    ISAPRE = "Isapre"
    OTRO = "Otro"

    SISTEMA_SALUD_CHOICES = [
        (FONASA, "Fonasa"),
        (ISAPRE, "Isapre"),
        (OTRO, "Otro"),
    ]

    OPC_SistemaSalud = models.CharField(max_length=50, choices=SISTEMA_SALUD_CHOICES)

    def __str__(self):
        return self.OPC_SistemaSalud


class Ocupacion(models.Model):
    DUENIACASA = "Dueña de Casa"
    TRABAJADOR = "Trabajadora"
    OTRO = "Otro"

    OCUPACION_CHOICES = [
        (DUENIACASA, "Dueña de Casa"),
        (TRABAJADOR, "Trabajadora"),
        (OTRO, "Otro"),
    ]

    OPC_Ocupacion = models.CharField(max_length=50, choices=OCUPACION_CHOICES)

    def __str__(self):
        return self.OPC_Ocupacion


class Usuario(models.Model):
    AnioNacimiento = models.CharField(max_length=200, verbose_name="Fecha de Nacimiento")
    Id_manychat = models.CharField(max_length=200)
    Rut = models.CharField(max_length=10)
    Whatsapp = models.CharField(max_length=200)
    Comuna_Usuario = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    Genero_Usuario = models.ForeignKey(Genero, on_delete=models.CASCADE)
    SistemaSalud_Usuario = models.ForeignKey(SistemaSalud, on_delete=models.CASCADE)
    Ocupacion_Usuario = models.ForeignKey(Ocupacion, on_delete=models.CASCADE)
    Fecha_Ingreso = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_manychat}"


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
    id_manychat = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    id_opc_respuesta = models.ForeignKey(OPC_Respuesta, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_manychat} - {self.id_pregunta} - {self.id_opc_respuesta}"


