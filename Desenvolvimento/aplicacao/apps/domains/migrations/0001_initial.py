# Generated by Django 3.2.6 on 2021-09-19 13:22

from django.db import migrations, models
import domains.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=128, unique=True)),
                ('name', models.CharField(max_length=128)),
            ],
            managers=[
                ('objects', domains.models.DomainManager()),
            ],
        ),
    ]