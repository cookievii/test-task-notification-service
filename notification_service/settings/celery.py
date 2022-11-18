import os

from celery import Celery

PROJ = "settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJ + ".settings")
app = Celery(PROJ)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
