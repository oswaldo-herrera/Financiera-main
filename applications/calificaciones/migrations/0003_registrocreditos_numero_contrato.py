# Generated by Django 4.2.7 on 2024-02-06 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calificaciones', '0002_remove_registrocreditos_monto_credito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrocreditos',
            name='numero_contrato',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
