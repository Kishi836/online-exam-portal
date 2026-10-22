# Attempt Session Manager (FR-015 -- FR-021, FR-029). Every view needs @roles(...) from identity.access.
from django.urls import path

from . import views

urlpatterns = [
    path("api/attempts", views.start_attempt, name="attempt-start"),
    path("attempts/<int:pk>/", views.attempt_paper, name="attempt-paper"),
]
