# Generated by Django 5.0.1 on 2024-02-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botApp', '0024_usuario_referencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiTabla',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Texto')),
                ('texto', models.CharField(max_length=200)),
            ],
        ),
    ]
