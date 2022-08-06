from django.contrib import admin
from django.urls import path

from lists import views as list_views


urlpatterns = [
    path(
        route='',
        view=list_views.home_page,
        name='home'
    ),

    path('admin/', admin.site.urls),
]
