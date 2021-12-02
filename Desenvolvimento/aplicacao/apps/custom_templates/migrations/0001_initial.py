# Generated by Django 3.2.6 on 2021-11-03 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cria_coworking', '0001_manual_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceButtons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_tipo', models.IntegerField(choices=[(1, 'Botão de agendamento')])),
                ('text', models.JSONField()),
                ('client_id', models.ForeignKey(blank=True, db_column='client_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cria_coworking.administrador')),
            ],
            options={
                'db_table': 'resource_buttons',
            },
        ),
        migrations.CreateModel(
            name='TemplateIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_carousel_slides', models.PositiveIntegerField(blank=True, null=True)),
                ('has_services', models.PositiveIntegerField(blank=True, null=True)),
                ('has_contact', models.PositiveIntegerField(blank=True, null=True)),
                ('about_us', models.JSONField()),
                ('client_id', models.ForeignKey(blank=True, db_column='client_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cria_coworking.administrador')),
            ],
            options={
                'db_table': 'template_index',
            },
        ),
        migrations.CreateModel(
            name='ResourceServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bootstrap_icon', models.CharField(max_length=64)),
                ('text', models.JSONField()),
                ('client_id', models.ForeignKey(blank=True, db_column='client_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cria_coworking.administrador')),
            ],
            options={
                'db_table': 'resource_services',
            },
        ),
        migrations.CreateModel(
            name='ResourceCarouselSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.JSONField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='template_index')),
                ('client_id', models.ForeignKey(blank=True, db_column='client_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cria_coworking.administrador')),
                ('id_button', models.ForeignKey(blank=True, db_column='id_button', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_templates.resourcebuttons')),
                ('id_index', models.ForeignKey(blank=True, db_column='id_index', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_templates.templateindex')),
            ],
            options={
                'db_table': 'resource_carousel_slides',
            },
        ),
        migrations.CreateModel(
            name='InstanceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_palette', models.JSONField()),
                ('client_logo', models.ImageField(blank=True, null=True, upload_to='client_logo')),
                ('showing_company_name', models.CharField(max_length=32)),
                ('client_id', models.ForeignKey(blank=True, db_column='client_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cria_coworking.administrador')),
            ],
            options={
                'db_table': 'instance_config',
            },
        ),
    ]
