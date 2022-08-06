from django.contrib import admin
from django.urls import path

from lists import views as list_views


urlpatterns = [
    path(
        route='',
        view=list_views.home_page,
        name='home'
    ),
    path(
        route='lists/new',
        view=list_views.new_list,
        name='new_list'
    ),
    path(
        route='lists/the-only-list-in-the-world/',
        view=list_views.view_list,
        name='view_list'
    ),

    path('admin/', admin.site.urls),
]
