# Generated by Django 4.2.7 on 2024-04-01 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0043_delete_registropagosmodelos'),
        ('users', '0065_alter_user_simulador'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroCreditosModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_credito', models.DateField(blank=True, null=True)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_registro', to='dashboard.prestamo')),
                ('usuarios', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_registro', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
