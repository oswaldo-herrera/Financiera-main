# Generated by Django 4.2.7 on 2023-12-27 00:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_rename_email_correoscreditogrupal_email_credito_grupal'),
    ]

    operations = [
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='curp_texto_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='date_joined_grupal',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='estado_civil_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='first_name_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='genero_grupal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='last_name_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='nacionalidad_grupal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='pais_grupal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='rfc_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='second_name_grupal',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]