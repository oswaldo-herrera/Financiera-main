# Generated by Django 4.2.7 on 2024-03-05 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calificaciones', '0018_alter_registropagosmodel_num_contrato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registropagosmodel',
            name='numero_contrato',
        ),
        migrations.AddField(
            model_name='registropagosmodel',
            name='estatus_num_contrato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estatus_num_contrato', to='calificaciones.registrocreditos'),
        ),
    ]
