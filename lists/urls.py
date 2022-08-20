from django.urls import path
from . import views


urlpatterns = [
    path(
        route='new',
        view=views.new_list,
        name='new_list'
    ),
    path(
        route='<int:pk>/',
        view=views.view_list,
        name='view_list'
    ),
    path(
        route='<int:pk>/share',
        view=views.share_list,
        name='share_list'
    ),
    path(
        route='users/<str:email>/',
        view=views.my_lists,
        name='my_lists'
    )
]
