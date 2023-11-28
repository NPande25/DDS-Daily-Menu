from django.shortcuts import render
from django.http import JsonResponse
from .dining1 import get_menu

def menu_view(request):
    lunch, dinner = get_menu()
    menu_data = {'lunch': lunch, 'dinner': dinner}
    return JsonResponse(menu_data)


def index(request):
    return render(request, 'menu/index.html')