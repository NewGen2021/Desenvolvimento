from django.conf import settings
from django_hosts import patterns, host
from django.http import HttpResponseRedirect
# from django.contrib.sites.models import Site
import sys

host_cache = ''

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'newgenapp.link', 'cria_coworking.urls', name='newgen'),
    host(r'(\w+)', settings.ROOT_URLCONF, name='custom_host'),
)
