# Generated by Django 4.2.7 on 2024-02-05 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_productocreditogrupal_monto_credito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plazo',
            name='interes_moratorio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]