from django.urls import path
from .views import new_list, view_list, my_lists


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
        route='users/<str:pk>/',
        view=my_lists,
        name='my_lists'
    )
]
