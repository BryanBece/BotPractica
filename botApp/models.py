from django.db import models

# Create your models here.


listGenero = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
    ('Otro', 'Otro'),
]

class Formulario(models.Model):
    anioNacimiento = models.CharField(max_length=50)
    #anioNacimiento = models.IntegerField()
    comuna = models.CharField(max_length=50)
    genero = models.CharField(max_length=50, choices=listGenero)

    def __str__(self):
        return self.anioNacimiento + ' ' + self.comuna + ' ' + self.genero