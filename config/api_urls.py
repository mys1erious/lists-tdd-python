from django.urls import path, include
from lists import api


urlpatterns = [
    # path(
    #     route='lists/<int:pk>/',
    #     view=api.list,
    #     name='api_list'
    # )
    path(
        route='',
        view=include(api.router.urls)
    )
]
