# Generated by Django 4.2.7 on 2024-03-05 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_remove_simuladorprueba_montos_seleccionados'),
        ('users', '0063_user_fecha_proximo_viernes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='simulador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='simulador', to='dashboard.simuladorprueba'),
        ),
    ]
