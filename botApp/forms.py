from django import forms
from .models import *



class FormularioForm(forms.ModelForm):
        class Meta:
            model = Formulario
            fields = '__all__'