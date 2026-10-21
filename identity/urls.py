from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student/", views.student_dashboard, name="student-dashboard"),
    path("faculty/", views.faculty_dashboard, name="faculty-dashboard"),
    path("admin/", views.admin_dashboard, name="admin-dashboard"),
]
