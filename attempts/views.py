from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from identity.access import roles
from repository.models import Attempt, Role

from .timer import remaining_seconds


@roles(Role.STUDENT)
def attempt_remaining(request, attempt_id):
    """Return an attempt owner's remaining time from the server clock."""
    attempt = get_object_or_404(Attempt.objects.select_related("exam"), pk=attempt_id)
    if attempt.student_id != request.user.id:
        raise PermissionDenied("You are not authorised to view this attempt.")
    return JsonResponse({"remaining_seconds": remaining_seconds(attempt)})
