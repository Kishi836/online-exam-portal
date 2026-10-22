from django.urls import path

from . import views

urlpatterns = [
    path("faculty/exams/", views.exam_list, name="exam-list"),
    path("faculty/exams/new/", views.exam_create, name="exam-create"),
    path(
        "faculty/exams/<int:exam_id>/",
        views.exam_detail,
        name="exam-detail",
    ),
    path(
        "faculty/exams/<int:exam_id>/edit/",
        views.exam_edit,
        name="exam-edit",
    ),
    path(
        "faculty/exams/<int:exam_id>/questions/",
        views.exam_add_questions,
        name="exam-add-questions",
    ),
    path(
        "faculty/exams/<int:exam_id>/publish/",
        views.exam_publish,
        name="exam-publish",
    ),
]
