from __future__ import unicode_literals

from django.apps import AppConfig


class VacpassConfig(AppConfig):
    name = 'vacpass'

    def ready(self):
        # Necessário para o celery funcionar, não remova
        from . import signalactions
        from . import tasks

