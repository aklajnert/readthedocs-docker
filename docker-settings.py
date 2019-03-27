from __future__ import absolute_import

import os

from .base import CommunityBaseSettings

DOMAIN = os.environ.get('RTD_DOMAIN')


class DockerSettings(CommunityBaseSettings):
    PRODUCTION_DOMAIN = DOMAIN
    WEBSOCKET_HOST = 'localhost:8088'

    @property
    def DATABASES(self):  # noqa
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'rtd',
                'USER': 'rtd-user',
                'PASSWORD': 'rtd-password',
                'HOST': 'db',
            }
        }

    DONT_HIT_DB = False

    ACCOUNT_EMAIL_VERIFICATION = 'none'
    SESSION_COOKIE_DOMAIN = None
    CACHE_BACKEND = 'dummy://'

    SLUMBER_USERNAME = 'slumber'
    SLUMBER_PASSWORD = '<slumber-password>'
    SLUMBER_API_HOST = 'http://127.0.0.1:8000'
    PUBLIC_API_URL = 'http://127.0.0.1:8000'

    BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_IGNORE_RESULT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    CORS_ORIGIN_WHITELIST = (
        '0.0.0.0:8000',
    )

    ELASTICSEARCH_DSL_AUTOSYNC = False


DockerSettings.load_settings(__name__)
