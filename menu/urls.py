# menu/urls.py
from django.urls import path
from .views import menu_view, index

urlpatterns = [
    path('get_menu/', menu_view, name='get_menu'),
    path('', index, name='index'),
    # Add more URL patterns as needed
]