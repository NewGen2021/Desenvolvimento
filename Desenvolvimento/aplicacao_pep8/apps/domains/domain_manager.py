import json
from django.core.management import call_command


def get_domain_json_or_create() -> dict:
    try:
        f = open('local/domain.json', 'r')
        return json.load(f)
    except FileNotFoundError:
        call_command('updatejsondomain')
        f = open('local/domain.json', 'r')
        return json.load(f)


def insert_new_domain(domain: str, domain_name: str = None) -> tuple:
    """
        Insert a new domain in domains.json, if the operation is successed, return (True, 'Successed')
        Otherwise return (False, 'Existing domain')
    """
    domain_json: dict = get_domain_json_or_create()
    if domain in domain_json.keys():
        return False, 'Existing domain'
    try:
        f = open('domain.json', 'w')
    except FileNotFoundError:
        return True, 'json does not exist'
    f[domain] = {'domain': domain, 'isActive': False, 'name': domain_name if domain_name else domain}
    f.write(str(json.dumps(domain_json)))
    f.close()
    return True, 'Successed'


def get_domain(request):
    host = request.get_host()
    j = get_domain_json_or_create()
    if host not in j.keys():
        return None
    return j[host]
