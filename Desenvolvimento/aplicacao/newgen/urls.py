from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
import sys

urlpatterns = []
if not settings.AUTOMATIC_TEST:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('gere_coworking.urls')),
        path('', include('rest_api.urls')),
        # path('', include('cria_coworking.urls')),
        # path(r'^i18n/', include('django.conf.urls.i18n')),
    ]
    urlpatterns += i18n_patterns (
        path('', include('gere_coworking.urls')),
        path('', include('rest_api.urls')),
        # path('', include('cria_coworking.urls')),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
else:
    from tests.conf_tests import tests_local as tl
    if hasattr(tl, 'current_app') and tl.current_app == 'cria_coworking':
        urlpatterns = [path('', include('cria_coworking.urls'))]
        urlpatterns += i18n_patterns (path('', include('cria_coworking.urls')),)
    else:
        urlpatterns = [path('', include('gere_coworking.urls'))]
        urlpatterns += i18n_patterns (path('', include('gere_coworking.urls')),)