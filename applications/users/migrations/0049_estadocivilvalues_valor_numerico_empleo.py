# Generated by Django 4.2.7 on 2024-01-23 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_rename_celular_user_empleo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadocivilvalues',
            name='valor_numerico_empleo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
