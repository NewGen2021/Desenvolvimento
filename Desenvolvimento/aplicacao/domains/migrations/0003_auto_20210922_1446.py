# Generated by Django 3.2.6 on 2021-09-22 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0002_auto_20210919_1037'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='domain',
            table='domain',
        ),
        migrations.DeleteModel(
            name='Administrador',
        ),
    ]
