# Generated by Django 4.2.7 on 2024-03-04 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_remove_simuladorprueba_nombre_prestamo_seleccionado'),
    ]

    operations = [
        migrations.AddField(
            model_name='simuladorprueba',
            name='montos_seleccionados',
            field=models.TextField(blank=True, null=True),
        ),
    ]