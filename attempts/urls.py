from django.urls import path

from . import views

urlpatterns = [
    path("api/attempts/<int:attempt_id>/remaining", views.attempt_remaining, name="attempt-remaining"),
]
