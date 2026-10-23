from django.urls import path

from . import views

urlpatterns = [
    path("api/attempts", views.start_attempt, name="attempt-start"),
    path("attempts/<int:pk>/", views.attempt_paper, name="attempt-paper"),
    path("attempts/<int:pk>/submit", views.submit_attempt, name="attempt-submit"),
    path("api/attempts/<int:pk>/answers", views.save_answer, name="attempt-answer"),
    path("api/attempts/<int:pk>/remaining", views.attempt_remaining, name="attempt-remaining"),
]
