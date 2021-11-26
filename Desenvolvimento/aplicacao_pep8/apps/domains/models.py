from django.db import models
from django.http.request import split_domain_port
from django.utils.translation import gettext as _
import common.models_choices as c
import sys

DOMAINS_CACHE = {}


class DomainManager(models.Manager):
    use_in_migrations = True

    def _get_domain_by_id(self, domain_id):
        if domain_id not in DOMAINS_CACHE:
            domain = self.get(pk=domain_id)
            DOMAINS_CACHE[domain_id] = domain
        return DOMAINS_CACHE[domain_id]

    def _get_domain_by_request(self, request):
        host = request.get_host()
        try:
            if host not in DOMAINS_CACHE:
                DOMAINS_CACHE[host] = self.get(domain__iexact=host)
            return DOMAINS_CACHE[host]
        except Domain.DoesNotExist:
            return None
            # domain, port = split_domain_port(host)
            # if domain not in DOMAINS_CACHE:
            #     DOMAINS_CACHE[domain] = self.get(domain__iexact=domain)
            # return DOMAINS_CACHE[domain]

    def get_active(self, request=None, domain_id=None):
        if domain_id:
            return self._get_domain_by_id(domain_id).isActive
        elif request:
            return self._get_domain_by_request(request).isActive

    def get_current(self, request=None, domain_id=None):
        if domain_id:
            return self._get_domain_by_id(domain_id)
        elif request:
            return self._get_domain_by_request(request)

    @staticmethod
    def clear_cache():
        global DOMAINS_CACHE
        DOMAINS_CACHE = {}

    def get_by_natural_key(self, domain):
        return self.get(domain=domain)


class Domain(models.Model):
    domain = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    isActive = models.BooleanField(default=False)
    objects = DomainManager()

    def __str__(self):
        return str(f'{self.domain}')

    class Meta:
        db_table = 'domain'
