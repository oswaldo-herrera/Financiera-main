# Generated by Django 4.2.7 on 2024-01-09 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_correoscreditogrupal_correo_coordinador'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupocreditopersonal',
            name='aviso_privacidad',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='grupocreditopersonal',
            name='buro_credito',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
