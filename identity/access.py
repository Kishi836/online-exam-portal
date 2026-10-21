"""FR-003: every screen and endpoint is restricted to the roles authorised for it.

Default deny: a view that declares no roles is refused to everyone, so a forgotten
decorator fails closed instead of open.

    @roles(Role.FACULTY)
    def question_list(request): ...
"""
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


def roles(*allowed):
    """Allow only signed-in users holding one of the `allowed` Role values."""

    def decorate(view):
        view.allowed_roles = frozenset(str(role) for role in allowed)
        return view

    return decorate


def public(view):
    """Open to everyone, signed in or not -- sign-in, sign-out and registration only."""
    view.is_public = True
    return view


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # The Django admin site does its own is_staff check.
        if getattr(view_func, "is_public", False) or request.resolver_match.app_name == "admin":
            return None
        if not request.user.is_authenticated:
            if request.path.startswith("/api/"):
                return JsonResponse({"detail": "Authentication required."}, status=401)
            return redirect_to_login(request.get_full_path())
        if request.user.role not in getattr(view_func, "allowed_roles", ()):
            raise PermissionDenied("You are not authorised to view this page.")
        return None
