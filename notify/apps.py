from django.apps import AppConfig


class NotifyConfig(AppConfig):
    name = 'notify'
    verbose_name = 'Notifications'

    def ready(self):
    	import notify.signals
