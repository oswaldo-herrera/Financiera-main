# Generated by Django 4.2.7 on 2024-02-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_productocreditogrupal_nombre_grupal'),
    ]

    operations = [
        migrations.AddField(
            model_name='plazo',
            name='nombre_credito',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]