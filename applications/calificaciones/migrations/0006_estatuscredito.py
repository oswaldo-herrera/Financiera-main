# Generated by Django 4.2.7 on 2024-02-13 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calificaciones', '0005_remove_registrocreditos_monto_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstatusCredito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cliente_estatus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_estatus', to=settings.AUTH_USER_MODEL)),
                ('numero_contrato_estatus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contrato', to='calificaciones.registrocreditos')),
            ],
            options={
                'verbose_name': 'Estatus',
                'verbose_name_plural': 'Estatus',
            },
        ),
    ]
