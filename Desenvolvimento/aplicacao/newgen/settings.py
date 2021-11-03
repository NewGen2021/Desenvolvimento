from pathlib import Path
import sys
import os
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
import newgen.databases as db

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTOMATIC_TEST = False
if 'test' in sys.argv:
    AUTOMATIC_TEST = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4x57g(r^*u^2pu=sl8j4i&!rg=93@u!m-!duorv%n##wwqc$p-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #QUANDO FOR SUBIR NO >>GITHUB<<, DEIXE COMO "FALSE" PARA O DEPLOY FUNCIONAR E NÃO CAIR O SERVER

# ALLOWED_HOSTS = ['127.0.0.1', 'newgenapp.link', 'www.newgenapp.link', 'testtest.com', 'www.testtest.com', 'newgen.testtest.com']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'payments.apps.PaymentsConfig',
    
    # Third-parties
    'crispy_forms',
    'django_hosts',
    'rest_framework',
    'mercadopago',
    'mathfilters', 

    # Custom
    'cria_coworking',
    'gere_coworking',
    'domains',
    'rest_api',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'domains.middleware.CurrentDomainMiddleware',
    'domains.middleware.GetMatchingDatabase',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'newgen.urls'

ROOT_HOSTCONF = 'newgen.hosts'

DEFAULT_HOST = 'www'
MAIN_HOST = 'newgenapp.link'

TEMPLATE_BASE = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_BASE],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['django_hosts.templatetags.hosts_override']
        },
    },
]

# TEMPLATES['OPTIONS']['builtins'] = ['django_hosts.templatetags.hosts_override']

WSGI_APPLICATION = 'newgen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = db.get_databases()


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Auth configuration

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = f'/{get_language()}/accounts/loginSystem'
LOGOUT_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = "bootstrap4"


LANGUAGES = (
    ('pt-br', _('Português')),
    ('en', _('Inglês'))
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

DATABASE_ROUTERS = ['newgen.routers.DataBaseRouter',]

# Configurações de envio do e-mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "newgenoficial2021@gmail.com"
EMAIL_HOST_PASSWORD = "jchxwrmlxaypxgei"


# MERCADO PAGO
# env = environ.Env()
# env.read_env(str(BASE_DIR / ".env"))
# MERCADO_PAGO_PUBLIC_KEY = env("MERCADO_PAGO_PUBLIC_KEY")
# MERCADO_PAGO_ACCESS_TOKEN = env("MERCADO_PAGO_ACCESS_TOKEN")
# env = environ.Env()
# env.read_env(str(BASE_DIR / ".env"))
MERCADO_PAGO_PUBLIC_KEY = "TEST-3857db53-06c2-4bfc-a9a5-bec2dd9d1579"
MERCADO_PAGO_ACCESS_TOKEN = "TEST-3187563733455134-101000-ca1efb8cc24fb6c2fe39239b997dde91-378451579"
