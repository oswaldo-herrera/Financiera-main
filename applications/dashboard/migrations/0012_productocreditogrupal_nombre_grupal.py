# Generated by Django 4.2.7 on 2024-02-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_simulador_interest_moratorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='productocreditogrupal',
            name='nombre_grupal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
