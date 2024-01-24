from rest_framework import serializers
from .models import *


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
        
class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = "__all__"