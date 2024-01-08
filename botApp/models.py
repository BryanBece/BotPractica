from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    FEMENINO = 'Femenino'
    MASCULINO = 'Masculino'
    OTRO = 'Otro'

    GENERO_CHOICES = [
        ('1', FEMENINO),
        ('2', MASCULINO),
        ('3', OTRO),
    ]

    nombre = models.CharField(max_length=50, choices=GENERO_CHOICES)


    def __str__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Respuesta(models.Model):
    def validate_fecha_nacimiento(value):
        if value.year <= 1930 or timezone.now().year - value.year < 18:
            raise ValidationError('La persona debe tener más de 18 años y haber nacido después de 1930.')

    anioNacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        validators=[validate_fecha_nacimiento]
    )
    id = models.AutoField(primary_key=True)
    id_usuario = models.IntegerField()
    fecha_ingreso = models.DateField(auto_now_add=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id_usuario} - {self.anioNacimiento}'
