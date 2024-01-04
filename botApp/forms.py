from django import forms
from .models import Formulario

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['anioNacimiento', 'comuna', 'genero']
        widgets = {
            'anioNacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
