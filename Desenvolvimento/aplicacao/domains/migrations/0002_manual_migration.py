# Generated by Django 3.2.6 on 2021-10-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Domain',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelTable(
            name='Domain',
            table='domain',
        ),
    ]
