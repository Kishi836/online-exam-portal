"""Attempt Session Manager (SAD 3.1): starting an attempt and delivering its paper."""
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from identity.access import roles
from repository.models import Attempt, Exam, Role


class NotEligible(Exception):
    """A start refused for a reason the Student is told (FR-015); the message is the Test Plan's wording."""


def start(exam, student):
    """FR-015 then FR-016: refuse if ineligible, else return the student's attempt, created on the server's clock."""
    if exam.status != Exam.Status.PUBLISHED or not exam.course.students.filter(pk=student.pk).exists():
        raise PermissionDenied  # FR-006: an exam the student may not see is a 403, not a message
    now = timezone.now()
    if exam.window_start is None or exam.window_end is None or now < exam.window_start:
        raise NotEligible("This examination has not opened yet")
    if now >= exam.window_end:
        raise NotEligible("This examination has closed")
    attempt, _ = Attempt.objects.get_or_create(exam=exam, student=student)  # one row per student (DB constraint)
    if attempt.submitted_at:
        raise NotEligible("You have already submitted this examination")
    return attempt


def paper(attempt):
    """FR-016/FR-029: the questions in exam order; options carry only id and text, never is_correct."""
    questions = attempt.exam.questions.order_by("examquestion__order")
    # ponytail: one options query per question; fine at 25-100 questions, prefetch if NFR-001 says otherwise
    return [{"id": q.id, "stem": q.stem, "options": list(q.options.values("id", "text"))} for q in questions]


@roles(Role.STUDENT)
@require_POST
def start_attempt(request):
    exam_id = request.POST.get("exam", "")
    if not exam_id.isdigit():
        raise Http404
    try:
        attempt = start(get_object_or_404(Exam, pk=exam_id), request.user)
    except NotEligible as refusal:
        return render(request, "attempts/refused.html", {"message": str(refusal)}, status=403)
    return redirect("attempt-paper", attempt.pk)


@roles(Role.STUDENT)
def attempt_paper(request, pk):
    # Another student's attempt is a 404 too, so attempt ids reveal nothing.
    attempt = get_object_or_404(Attempt, pk=pk, student=request.user, submitted_at__isnull=True)
    return render(request, "attempts/paper.html", {"attempt": attempt, "questions": paper(attempt)})
