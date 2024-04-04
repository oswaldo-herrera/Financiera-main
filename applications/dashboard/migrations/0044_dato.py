# Generated by Django 4.2.7 on 2024-04-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0043_delete_registropagosmodelos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('employees', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Datos excel',
            },
        ),
    ]