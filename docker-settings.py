from __future__ import absolute_import

import os

from readthedocs.projects import constants

from .base import CommunityBaseSettings


def env(variable, default=None):
    return os.environ.get(variable, default)


DOMAIN = env("RTD_DOMAIN", "localhost:8000").split(":")


class DockerSettings(CommunityBaseSettings):
    PRODUCTION_DOMAIN = ":".join(DOMAIN)
    WEBSOCKET_HOST = f"{DOMAIN[0]}:8088"

    DEBUG = env("RTD_DEBUG", False)
    SERVE_DOCS = [constants.PUBLIC, constants.PRIVATE]

    PYTHON_MEDIA = True  # this is temporary until I'll figure out how to force uwsgi to serve media

    @property
    def DATABASES(self):  # noqa
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": env("RTD_DB_NAME", "rtd"),
                "USER": env("RTD_DB_USER", "rtd-user"),
                "PASSWORD": env("RTD_DB_PASS", "rtd-password"),
                "HOST": env("RTD_DB_HOST", "db"),
            }
        }

    DONT_HIT_DB = False

    ACCOUNT_EMAIL_VERIFICATION = "none"
    SESSION_COOKIE_DOMAIN = None
    CACHE_BACKEND = "dummy://"

    SLUMBER_USERNAME = env("RTD_SLUMBER_USER", "slumber")
    SLUMBER_PASSWORD = env("RTD_SLUMBER_PASS", "<slumber-password>")
    SLUMBER_API_HOST = "http://127.0.0.1:8000"
    PUBLIC_API_URL = "http://127.0.0.1:8000"

    REDIS_HOST = env("RTD_REDIS_HOST", "redis")
    REDIS_PORT = env("RTD_REDIS_PORT", "6379")

    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_IGNORE_RESULT = False

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    FILE_SYNCER = "readthedocs.builds.syncers.LocalSyncer"

    CORS_ORIGIN_WHITELIST = ("0.0.0.0:8000",)

    ELASTIC_HOST = env("RTD_ELASTIC_HOST", "elasticsearch")
    ELASTIC_PORT = env("RTD_ELASTIC_PORT", "9200")

    ELASTICSEARCH_DSL_AUTOSYNC = False
    ES_HOSTS = [f"{ELASTIC_HOST}:{ELASTIC_PORT}"]
    ELASTICSEARCH_DSL = {"default": {"hosts": f"{ELASTIC_HOST}:{ELASTIC_PORT}"}}


DockerSettings.load_settings(__name__)
