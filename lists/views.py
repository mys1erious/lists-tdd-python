from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    if request.method == "GET":
        return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, pk):
    lst = List.objects.get(id=pk)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=lst)
            return redirect(lst)

    return render(request, 'list.html', {'form': form, 'list': lst})


def new_list(request):
    if request.method == 'POST':
        form = ItemForm(data=request.POST)

        if form.is_valid():
            lst = List.objects.create()
            Item.objects.create(text=request.POST['text'], list=lst)
            return redirect(lst)

        return render(request, 'home.html', {'form': form})

