from django.shortcuts import redirect, render

from repository.models import Role

from .access import roles


@roles(*Role.values)
def home(request):
    return redirect(f"{request.user.role.lower()}-dashboard")


# Placeholder dashboards so each role has a landing page; the real ones are FR-014 and the consoles.
@roles(Role.STUDENT)
def student_dashboard(request):
    return render(request, "identity/dashboard.html")


@roles(Role.FACULTY)
def faculty_dashboard(request):
    return render(request, "identity/dashboard.html")


@roles(Role.ADMIN)
def admin_dashboard(request):
    return render(request, "identity/dashboard.html")
