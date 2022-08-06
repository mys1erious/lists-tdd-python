from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    if request.method == "GET":
        return render(request, 'home.html')


def view_list(request):
    if request.method == "GET":
        items = Item.objects.all()
        return render(request, 'list.html', {'items': items})


def new_list(request):
    if request.method == 'POST':
        lst = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=lst)
        return redirect('/lists/the-only-list-in-the-world/')
