# Generated by Django 4.2.7 on 2024-03-06 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calificaciones', '0023_registropagosmodel_archivo_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registropagosmodel',
            name='archivo_pago',
        ),
    ]
