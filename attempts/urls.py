
from django.urls import path

from . import views

urlpatterns = [
    path(
        "student/exams/",
        views.student_exam_list,
        name="student-exam-list",
    ),
    path(
        "student/exams/<int:exam_id>/",
        views.student_exam_detail,
        name="student-exam-detail",
    ),
]
