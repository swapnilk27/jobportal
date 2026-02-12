from django.urls import path

from .views import *

urlpatterns = [
    path("my-applications/", my_applications, name="my_applications"),
    path(
        "application/<int:app_id>/status/<str:status>/",
        update_application_status,
        name="update_application_status",
    ),
    path("withdraw/<int:app_id>/", withdraw_application, name="withdraw_application"),
]
