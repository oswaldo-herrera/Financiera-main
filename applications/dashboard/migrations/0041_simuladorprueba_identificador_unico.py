# Generated by Django 4.2.7 on 2024-03-13 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0040_simuladorprueba_fecha_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='simuladorprueba',
            name='identificador_unico',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
