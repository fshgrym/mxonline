from django.conf import settings
from appconf import AppConf


class AppCoreAppConf(AppConf):

    ANONYMOUS_REQUIRED_REDIRECT_URL = getattr(settings, 'APPCORE_ANONYMOUS_REQUIRED_REDIRECT_URL', '/')

