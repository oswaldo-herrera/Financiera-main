# Generated by Django 4.2.7 on 2024-02-22 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_tipoprestamo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoprestamo',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.IntegerField(blank=True, null=True)),
                ('plazo', models.CharField(blank=True, max_length=50, null=True)),
                ('tiempo_pago', models.IntegerField(blank=True, null=True)),
                ('interes', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tipo_prestamo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.tipoprestamo')),
            ],
            options={
                'verbose_name': 'Credito',
                'verbose_name_plural': 'Creditos',
            },
        ),
    ]