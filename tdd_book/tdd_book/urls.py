from django.contrib import admin
from django.urls import path

from .views import tst_view

urlpatterns = [
    path('admin/', admin.site.urls),
]
