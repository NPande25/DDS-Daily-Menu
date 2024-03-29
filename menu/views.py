from django.shortcuts import render
from django.http import JsonResponse
# Import from backend:
from .getmenu import get_menu

# connects front/back ends by pulling function from getmenu.py
def menu_view(request):
    menu_data = get_menu()
    print("in menu view:", menu_data)
    return JsonResponse(menu_data)


def index(request):
    return render(request, 'menu/index.html')