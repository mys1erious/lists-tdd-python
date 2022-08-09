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
        Item.objects.create(text=request.POST['item_text'], list=lst)
        return redirect(f'/lists/{lst.id}/')


def add_item(request, pk):
    if request.method == 'POST':
        lst = List.objects.get(id=pk)
        Item.objects.create(text=request.POST['item_text'], list=lst)
        return redirect(f'/lists/{lst.id}/')
