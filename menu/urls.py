# menu/urls.py
from django.urls import path
from .views import menu_view, index

urlpatterns = [
    path('get_menu/', menu_view, name='get_menu'), # to fetch get_menu function from backend
    path('', index, name='index'),  # for frontend html
]