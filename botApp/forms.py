from django import forms
from .models import *


class UsuarioForm(forms.ModelForm):
    Comuna_Usuario = forms.CharField(max_length=50)
    Genero_Usuario = forms.ChoiceField(
        choices=[('', 'Seleccione una opción')] + Genero.GENERO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    SistemaSalud_Usuario = forms.ChoiceField(
        choices=[('', 'Seleccione una opción')] + SistemaSalud.SISTEMA_SALUD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Ocupacion_Usuario = forms.ChoiceField(
        choices=[('', 'Seleccione una opción')] + Ocupacion.OCUPACION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    anioNacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'dark-input'}))

    class Meta:
        model = Usuario
        fields = ['anioNacimiento', 'Comuna_Usuario', 'Genero_Usuario', 'SistemaSalud_Usuario', 'Ocupacion_Usuario']

    def clean_Comuna_Usuario(self):
        comuna_name = self.cleaned_data['Comuna_Usuario']
        comuna, created = Comuna.objects.get_or_create(Nombre_Comuna=comuna_name)
        return comuna

    def clean_Genero_Usuario(self):
        genero_value = self.cleaned_data['Genero_Usuario']
        if genero_value:
            genero, created = Genero.objects.get_or_create(OPC_Genero=genero_value)
            return genero
        return None

    def clean_SistemaSalud_Usuario(self):
        sistema_salud_value = self.cleaned_data['SistemaSalud_Usuario']
        if sistema_salud_value:
            sistema_salud, created = SistemaSalud.objects.get_or_create(OPC_SistemaSalud=sistema_salud_value)
            return sistema_salud
        return None

    def clean_Ocupacion_Usuario(self):
        ocupacion_value = self.cleaned_data['Ocupacion_Usuario']
        if ocupacion_value:
            ocupacion, created = Ocupacion.objects.get_or_create(OPC_Ocupacion=ocupacion_value)
            return ocupacion
        return None

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['pregunta']