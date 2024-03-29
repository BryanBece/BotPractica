# Generated by Django 5.0.1 on 2024-01-24 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botApp', '0010_rename_pruebaapi_prueba'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Prueba',
        ),
        migrations.RemoveField(
            model_name='respuestausuario',
            name='id_usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='anioNacimiento',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='id_usuario',
        ),
        migrations.AddField(
            model_name='respuestausuario',
            name='id_manychat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='botApp.usuario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='Id_manychat',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='Rut',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='Whatsapp',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ocupacion',
            name='OPC_Ocupacion',
            field=models.CharField(choices=[('Dueña de Casa', 'Dueña de Casa'), ('Trabajadora', 'Trabajadora'), ('Otro', 'Otro')], max_length=50),
        ),
        migrations.AlterField(
            model_name='respuestausuario',
            name='id_opc_respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.opc_respuesta'),
        ),
        migrations.AlterField(
            model_name='respuestausuario',
            name='id_pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.pregunta'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Comuna_Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.comuna'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Genero_Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.genero'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Ocupacion_Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.ocupacion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='SistemaSalud_Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botApp.sistemasalud'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='AnioNacimiento',
            field=models.CharField(default=1, max_length=200, verbose_name='Fecha de Nacimiento'),
            preserve_default=False,
        ),
    ]
