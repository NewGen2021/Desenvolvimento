from django.db import models
from django.utils.translation import gettext as _
from common.services import json_to_safe_html_string
from cria_coworking.models import *


# Create your models here.
class TemplateIndex(models.Model):
    client_id = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='client_id', blank=True, null=True)
    has_carousel_slides = models.PositiveIntegerField(blank=True, null=True)
    has_services = models.PositiveIntegerField(blank=True, null=True)
    has_contact = models.PositiveIntegerField(blank=True, null=True)
    about_us = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(_('Template index de %s') % self.client_id.nome)

    class Meta:
        db_table = 'template_index'


class ResourceButtons(models.Model):
    BUTTON_CHOICES = (
        (1, _('Botão de agendamento')),
    )
    client_id = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='client_id', blank=True, null=True)
    button_tipo = models.IntegerField(null=False, choices=BUTTON_CHOICES)
    text = models.JSONField()

    def __str__(self):
        tipo = None
        for choice in self.BUTTON_CHOICES:
            if self.button_tipo == choice[0]:
                tipo = choice[1]
                break
        return str('%s' % tipo)

    class Meta:
        db_table = 'resource_buttons'


class ResourceCarouselSlide(models.Model):
    client_id = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='client_id', blank=True, null=True)
    id_index = models.ForeignKey(TemplateIndex, models.DO_NOTHING, db_column='id_index', blank=True, null=True)
    id_button = models.ForeignKey(ResourceButtons, models.DO_NOTHING, db_column='id_button', blank=True, null=True)
    text = models.JSONField()
    image = models.ImageField(null=True, blank=True, upload_to="template_index")

    def get_button_json(self):
        return json_to_safe_html_string(self.id_button.text) if self.id_button else ''

    def get_button_type(self):
        return 0 if not self.id_button else self.id_button.button_tipo

    class Meta:
        db_table = 'resource_carousel_slides'


class ResourceServices(models.Model):
    client_id = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='client_id', blank=True, null=True)
    bootstrap_icon = models.CharField(max_length=64)
    text = models.JSONField()

    class Meta:
        db_table = 'resource_services'


class InstanceConfig(models.Model):
    client_id = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='client_id', blank=True, null=True)
    color_palette = models.JSONField()
    client_logo = models.ImageField(null=True, blank=True, upload_to="client_logo")
    showing_company_name = models.CharField(max_length=32)

    class Meta:
        db_table = 'instance_config'
