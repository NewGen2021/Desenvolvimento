from django import template

register = template.Library()
from django.conf import settings


@register.simple_tag
def get_image_url(image):
    try:
        return "%s%s" % (settings.MEDIA_URL, image.decode('utf-8'))
    except AttributeError:
        print('AAAAAAAAAAAAAAA')
        print(image)
