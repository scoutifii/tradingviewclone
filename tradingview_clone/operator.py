from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events 
from tradingview.views import (
    _get_posted_symbol_data, 
    _get_posted_ohlc_data, 
    _get_posted_technical_data, 
    _get_posted_news_data,
    _get_posted_events_data
    )
from tradingview.models import Symbol


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', seconds=300, name='symbol')
    def auto_symbol():
        _get_posted_symbol_data()

    @scheduler.scheduled_job('interval', seconds=300, name='ohlc')
    def auto_ohlc():
        symbols = Symbol.objects.all()
        for symbol in symbols:
            _get_posted_ohlc_data(symbol.id)

    @scheduler.scheduled_job('interval', seconds=900, name='technical')
    def auto_technical():
        symbols = Symbol.objects.all()
        for symbol in symbols:
            _get_posted_technical_data(symbol.id)

    @scheduler.scheduled_job('interval', seconds=3600, name='news')
    def auto_news():
        symbols = Symbol.objects.all()
        for symbol in symbols:
            _get_posted_news_data(symbol.id)

    @scheduler.scheduled_job('interval', seconds=300, name='events')
    def auto_events():
        symbols = Symbol.objects.all()
        for symbol in symbols:
            _get_posted_events_data(symbol.id)

    scheduler.start()