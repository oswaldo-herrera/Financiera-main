# Generated by Django 4.2.7 on 2024-01-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0044_grupocreditopersonal_productocreditogrupal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='buro_credito',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
