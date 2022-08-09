from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    if request.method == "GET":
        return render(request, 'home.html')


def view_list(request, pk):
    lst = List.objects.get(id=pk)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=lst)
            item.full_clean()
            item.save()
            return redirect(lst)
        except ValidationError:
            error = 'You cant have an empty list item'

    return render(request, 'list.html', {'list': lst, 'error': error})


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

        return redirect(lst)
