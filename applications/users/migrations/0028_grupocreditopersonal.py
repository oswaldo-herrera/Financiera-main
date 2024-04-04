# Generated by Django 4.2.7 on 2023-12-29 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_correoscreditogrupal_cuarto_email_grupal_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoCreditoPersonal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('second_name', models.CharField(blank=True, max_length=30, null=True)),
                ('fecha_nac', models.DateField(blank=True, null=True)),
                ('curp_texto', models.CharField(blank=True, max_length=30, null=True)),
                ('curp', models.FileField(blank=True, null=True, upload_to='users/')),
                ('rfc', models.CharField(blank=True, max_length=30, null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, null=True)),
                ('genero', models.CharField(blank=True, max_length=100, null=True)),
                ('nacionalidad', models.CharField(blank=True, max_length=100, null=True)),
                ('pais', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=100, null=True)),
                ('celular', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_dependientes', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono_particular', models.CharField(blank=True, max_length=100, null=True)),
                ('documento_ine', models.FileField(blank=True, null=True, upload_to='users/')),
                ('calle_numero', models.CharField(blank=True, max_length=100, null=True)),
                ('colonia', models.CharField(blank=True, max_length=100, null=True)),
                ('cp', models.CharField(blank=True, max_length=100, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo_vivienda', models.CharField(blank=True, max_length=100, null=True)),
                ('años_radicando', models.CharField(blank=True, max_length=100, null=True)),
                ('comprobante_domicilio', models.FileField(blank=True, null=True, upload_to='users/')),
            ],
        ),
    ]
