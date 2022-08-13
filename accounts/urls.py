from django.urls import path

from .views import (
    send_login_email,
    login as login_view,
    logout as logout_view
)


urlpatterns = [
    path(
        route='send_login_email',
        view=send_login_email,
        name='send_login_email'
    ),
    path(
        route='login',
        view=login_view,
        name='login'
    ),
    path(
        'logout',
        logout_view,
        name='logout'
    )
]
