# Generated by Django 5.0.1 on 2024-01-25 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botApp', '0015_rename_opc_respuesta_preguntaopcionrespuesta'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RespuestaUsuario',
            new_name='UsuarioRespuesta',
        ),
    ]
