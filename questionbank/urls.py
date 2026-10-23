from django.urls import path

from . import views

urlpatterns = [
    path("faculty/questions/", views.question_list, name="question-list"),
    path("faculty/questions/new/", views.question_create, name="question-create"),
    path("api/questions", views.question_api, name="question-api"),
]
