from django.contrib import admin
from django.urls import path
from .views import SymbolChartView, EventsView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Path to render Dashboard / Home page
	path('dashboard', views.dashboard, name='dashboard'),
    # Path to render signup page
	path('signup', views.signup, name='signup'),
    # Path to render login page
    path('login', views.login, name='login'),
    # Path to render logout
    path('logout', views.logout, name='logout'),
    # Path to render markets page
    path('market', views.market, name='market'),
    path('symbol/<str:symbol>', views.symbol, name='symbol'),
    path('autosuggest', views.autosuggest, name='autosuggest'),
    path('create-post/<int:pk>', views.create_post, name='create-post'),
    path('market/<str:symbol>', SymbolChartView.as_view(template_name='chart.html'), name='market'),
    path('get-symbol-id/<str:symbol>', views.get_symbol_id, name='get-symbol-id'),
    path('get-symbol-events', views.get_symbol_events, name='get-symbol-events'),
    path('events', EventsView.as_view(template_name='events.html'), name='events'),
]