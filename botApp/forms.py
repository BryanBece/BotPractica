from django import forms
from .models import *

class RespuestaForm(forms.ModelForm):
    comuna = forms.CharField(max_length=50)
    genero = forms.ChoiceField(
        choices=[('', 'Seleccione una opción')] + Genero.GENERO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    anioNacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'dark-input'}))

    class Meta:
        model = Respuesta
        fields = ['anioNacimiento', 'comuna', 'genero']

    def clean_comuna(self):
        comuna_name = self.cleaned_data['comuna']
        comuna, created = Comuna.objects.get_or_create(nombre=comuna_name)
        return comuna

    def clean_genero(self):
        genero_value = self.cleaned_data['genero']
        if genero_value:
            genero, created = Genero.objects.get_or_create(nombre=genero_value)
            return genero
        return None
