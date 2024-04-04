# Generated by Django 4.2.7 on 2023-12-05 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_solicitud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bandeja_Solicitud',
                'verbose_name_plural': 'Bandeja_Solicitudes',
            },
        ),
    ]