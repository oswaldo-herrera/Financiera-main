# Generated by Django 4.2.7 on 2024-02-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_simulador_tipo_credito'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPrestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo prestamo',
                'verbose_name_plural': 'Prestamos',
            },
        ),
    ]
