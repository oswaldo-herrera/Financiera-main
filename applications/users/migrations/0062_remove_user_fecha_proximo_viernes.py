# Generated by Django 4.2.7 on 2024-02-01 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0061_user_fecha_proximo_viernes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fecha_proximo_viernes',
        ),
    ]
