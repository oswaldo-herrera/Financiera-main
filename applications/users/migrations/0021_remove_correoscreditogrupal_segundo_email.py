# Generated by Django 4.2.7 on 2023-12-26 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_rename_email2_correoscreditogrupal_segundo_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correoscreditogrupal',
            name='segundo_email',
        ),
    ]