"""Results views: Faculty publication (FR-026), the results API (FR-025) and the Student scorecard (FR-027)."""
from django.contrib import messages
from django.core.exceptions import PermissionDenied  # noqa: F401  (result_api raises it)
from django.http import JsonResponse  # noqa: F401
from django.shortcuts import get_object_or_404, redirect  # noqa: F401
from django.views.decorators.http import require_GET, require_POST

from attempts.services import result_visible  # noqa: F401
from examsetup.views import _faculty_exam_or_403
from identity.access import roles
from repository.models import Attempt, Role  # noqa: F401

from .services import ResultsNotReady, set_results_published


@roles(Role.FACULTY)
@require_POST
def results_publish(request, exam_id):
    """FR-026: the Faculty of the exam's course publishes (publish=1) or unpublishes (publish=0) its results."""
    exam = _faculty_exam_or_403(request, exam_id)
    publish = request.POST.get("publish") == "1"
    try:
        set_results_published(exam, publish)
    except ResultsNotReady as refusal:
        messages.error(request, str(refusal))
    else:
        messages.success(request, "Results published." if publish else "Results unpublished.")
    return redirect("exam-detail", exam_id=exam.pk)


@roles(Role.STUDENT)
@require_GET
def result_api(request, attempt_id):
    """FR-025: GET /api/results/<attempt_id> -> {"score", "percentage", "passed"} as strings / bool.

    Refused with HTTP 403 -- not 404 -- when the attempt is another Student's (IT_034) or its result
    is not visible yet (IT_033). A refused body must not contain any score figure.
    """
    # TODO(Komal):
    # 1. attempt = get_object_or_404(Attempt.objects.select_related("exam"), pk=attempt_id)
    # 2. raise PermissionDenied if attempt.student_id != request.user.pk, or if not result_visible(attempt).
    #    (PermissionDenied goes through portal.error_handlers.permission_denied, so the body is the generic page.)
    # 3. return JsonResponse with str(attempt.score), str(attempt.percentage), attempt.passed.
    raise NotImplementedError
