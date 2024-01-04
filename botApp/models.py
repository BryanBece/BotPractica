from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Formulario(models.Model):
    def validate_fecha_nacimiento(value):
        if value.year <= 1930 or timezone.now().year - value.year < 18:
            raise ValidationError('La persona debe tener más de 18 años y haber nacido después de 1930.')

    anioNacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        validators=[validate_fecha_nacimiento]
    )
    comuna = models.CharField(max_length=100)
    genero = models.CharField(max_length=10)
    usuario = models.CharField(max_length=50)
    fecha_ingreso = models.DateField(auto_now_add=True)
