# Generated by Django 4.2.7 on 2024-02-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_alter_tipoprestamo_nombre_prestamo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='pago_mensual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]