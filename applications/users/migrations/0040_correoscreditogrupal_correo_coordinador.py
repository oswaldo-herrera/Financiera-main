# Generated by Django 4.2.7 on 2024-01-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_user_firma_digital_personal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='correoscreditogrupal',
            name='correo_coordinador',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]