from django.urls import path
from . import views


urlpatterns = [
    path(
        route='new',
        view=views.NewListView.as_view(),
        name='new_list'
    ),
    path(
        route='<int:pk>/',
        view=views.ViewAndAddToList.as_view(),
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
