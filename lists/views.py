from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, NewListForm


User = get_user_model()


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
    form = NewListForm(data=request.POST)
    if form.is_valid():
        lst = form.save(owner=request.user)
        return redirect(lst)
    return render(request, 'lists/home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'lists/my_lists.html', {'owner': owner})
