from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    if request.method == "GET":
        return render(request, 'home.html')


def view_list(request, pk):
    if request.method == "GET":
        lst = List.objects.get(id=pk)
        return render(request, 'list.html', {'list': lst})


def new_list(request):
    if request.method == 'POST':
        lst = List.objects.create()
        item = Item(text=request.POST['item_text'], list=lst)

        try:
            item.full_clean()
            item.save()
        except ValidationError:
            lst.delete()
            error = 'You cant have an empty list item'
            return render(request, 'home.html', {'error': error})

        return redirect(f'/lists/{lst.id}/')


def add_item(request, pk):
    if request.method == 'POST':
        lst = List.objects.get(id=pk)
        Item.objects.create(text=request.POST['item_text'], list=lst)
        return redirect(f'/lists/{lst.id}/')
