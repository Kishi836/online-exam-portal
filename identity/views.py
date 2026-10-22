from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.views.decorators.debug import sensitive_post_parameters

from repository.models import Role

from .access import public, roles
from .forms import RegistrationForm


@public
@sensitive_post_parameters("password1", "password2")
def register(request):
    """Create a Student account without ever accepting a role from the browser."""
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError as error:
            # Validation handles normal duplicates. This is the race-condition fallback.
            message = str(error).lower()
            if "roll_number" in message:
                form.add_error("roll_number", "This roll number is already registered")
            else:
                form.add_error("email", "An account with this email already exists")
        else:
            messages.success(request, "Registration successful")
            return redirect("login")
    return render(request, "registration/register.html", {"form": form})


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
