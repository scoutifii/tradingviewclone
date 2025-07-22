from django.contrib import admin
from .models import (Symbol, Ohlc, Technical, News, Event, SyncLog, WatchList, Post, Profile, Comment)

admin.site.register(Symbol)
admin.site.register(Technical)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(SyncLog)
admin.site.register(WatchList)
admin.site.register(Ohlc)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
