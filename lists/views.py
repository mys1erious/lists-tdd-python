from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView, DetailView

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


def share_list(request, pk):
    if request.method == 'POST':
        lst = get_object_or_404(List, pk=pk)

        sharee_email = request.POST.get('sharee', '')
        try:
            user_to_share = User.objects.get(email=sharee_email)
            lst.shared_with.add(user_to_share)
            return redirect(lst)
        except User.DoesNotExist:
            return redirect(lst)


class HomePageView(FormView):
    template_name = 'lists/home.html'
    form_class = ItemForm


class NewListView(CreateView):
    template_name = 'lists/home.html'
    form_class = NewListForm

    def form_valid(self, form):
        lst = form.save(owner=self.request.user)
        return redirect(lst)


class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'lists/list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)

