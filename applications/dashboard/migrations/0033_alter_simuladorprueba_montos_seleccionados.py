# Generated by Django 4.2.7 on 2024-03-04 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_simuladorprueba_montos_seleccionados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simuladorprueba',
            name='montos_seleccionados',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
