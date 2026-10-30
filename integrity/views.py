"""Integrity views: focus-loss capture and the Faculty integrity page (FR-028), the Admin audit viewer (FR-030)."""
from django.http import HttpResponse, JsonResponse  # noqa: F401
from django.shortcuts import get_object_or_404, render  # noqa: F401
from django.views.decorators.http import require_GET, require_POST

from attempts.services import AttemptClosed  # noqa: F401
from examsetup.views import _faculty_exam_or_403  # noqa: F401
from identity.access import roles
from repository.models import Attempt, Role  # noqa: F401

from . import services  # noqa: F401


@roles(Role.STUDENT)
@require_POST
def focus_lost(request, pk):
    """FR-028: POST /api/attempts/<pk>/focus-lost from the attempt page. No body is read. 204 on success."""
    # TODO(Kartik):
    # 1. attempt = get_object_or_404(Attempt, pk=pk, student=request.user)   (another Student's -> 404)
    # 2. services.record_focus_loss(attempt); on AttemptClosed return JsonResponse({"detail": ...}, status=409)
    # 3. return HttpResponse(status=204)
    raise NotImplementedError


@roles(Role.FACULTY)
@require_GET
def exam_integrity(request, exam_id):
    """FR-028: the course's Faculty sees every attempt's focus-loss count and server timestamps. A human decides."""
    exam = _faculty_exam_or_403(request, exam_id)
    # TODO(Kartik): render "integrity/exam_integrity.html" with exam and services.events_by_attempt(exam),
    # and add a link to this page from examsetup/templates/examsetup/exam_detail.html for published exams.
    raise NotImplementedError
