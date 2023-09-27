from django.apps import AppConfig


class ContentConfig(AppConfig):
    name = 'qcqualitycontrol.content'

    def ready(self):
        import qcqualitycontrol.content.signals
