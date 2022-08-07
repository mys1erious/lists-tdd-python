from django.contrib import admin
from django.urls import path, include

from lists import urls as list_urls
from lists import views as list_views


urlpatterns = [
    path(
        route='',
        view=list_views.home_page,
        name='home'
    ),
    path(
        route='lists/',
        view=include(list_urls)
    ),

    path('admin/', admin.site.urls),
]
