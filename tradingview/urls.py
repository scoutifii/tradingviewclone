from django.contrib import admin
from django.urls import path
from .views import PostView, CommentView
from . import views

urlpatterns = [
	# Path to render index page
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
    path('markets/<str:pk>', views.markets, name='markets'),
    path('symbol-data', views.update_symbol_data, name='symbol-data'),
    path('posts', PostView.as_view(), name='posts'),
    path('post-list', PostView.as_view(), name='post-list'),
    path('comments<str:pk>', CommentView.as_view(), name='comments'),
    path('create-post', views.create_post, name='create-post'),
]