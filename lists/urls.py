from django.urls import path
from .views import new_list, view_list, add_item


urlpatterns = [
    path(
        route='new',
        view=new_list,
        name='new_list'
    ),
    path(
        route='<int:pk>/',
        view=view_list,
        name='view_list'
    ),
    path(
        route='<int:pk>/add_item',
        view=add_item,
        name='add_item'
    ),
]
