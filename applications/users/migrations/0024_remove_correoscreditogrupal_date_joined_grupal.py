# Generated by Django 4.2.7 on 2023-12-27 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_correoscreditogrupal_curp_texto_grupal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correoscreditogrupal',
            name='date_joined_grupal',
        ),
    ]
