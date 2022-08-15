from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List
from .forms import ItemForm, ExistingListItemForm


def home_page(request):
    if request.method == "GET":
        return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, pk):
    lst = List.objects.get(id=pk)
    form = ExistingListItemForm(for_list=lst)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=lst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lst)

    return render(request, 'lists/list.html', {'form': form, 'list': lst})


def new_list(request):
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            lst = List.objects.create()
            form.save(for_list=lst)
            return redirect(lst)

        return render(request, 'lists/home.html', {'form': form})


def my_lists(request, pk):
    return render(request, 'lists/my_lists.html')
