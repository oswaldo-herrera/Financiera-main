# Generated by Django 4.2.7 on 2024-01-02 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_grupocreditopersonal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correoscreditogrupal',
            name='email_credito_grupal',
            field=models.TextField(),
        ),
    ]
