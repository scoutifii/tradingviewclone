from django.apps import AppConfig
from django.conf import settings


class TradingviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tradingview'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from tradingview_clone import operator
            operator.start()
            
