"""Attempt Session Manager (SAD 3.1): starting an attempt and delivering its paper."""
import math

from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from identity.access import roles
from repository.models import Attempt, Exam, Option, Role

from . import services
from .services import AttemptClosed, close_if_expired, expires_at, remaining_seconds


class NotEligible(Exception):
    """A start refused for a reason the Student is told (FR-015)."""


def start(exam, student):
    """FR-015 then FR-016: create or return a server-stamped eligible attempt."""
    if exam.status != Exam.Status.PUBLISHED or not exam.course.students.filter(pk=student.pk).exists():
        raise PermissionDenied
    now = timezone.now()
    if exam.window_start is None or exam.window_end is None or now < exam.window_start:
        raise NotEligible("This examination has not opened yet")
    if now >= exam.window_end:
        raise NotEligible("This examination has closed")
    attempt, _ = Attempt.objects.get_or_create(exam=exam, student=student)
    if close_if_expired(attempt).submitted_at:
        raise NotEligible("You have already submitted this examination")
    return attempt


def paper(attempt):
    """FR-016/FR-029: ordered question payload with only option identifiers and text."""
    questions = attempt.exam.questions.order_by("examquestion__order")
    return [
        {"id": question.id, "stem": question.stem, "options": list(question.options.values("id", "text"))}
        for question in questions
    ]


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
    attempt = close_if_expired(get_object_or_404(Attempt, pk=pk, student=request.user))
    if attempt.submitted_at:
        timed_out = attempt.submitted_at == expires_at(attempt)
        return render(request, "attempts/submitted.html", {"attempt": attempt, "timed_out": timed_out})
    saved = dict(attempt.answers.values_list("question_id", "option_id"))
    questions = [{**question, "saved": saved.get(question["id"])} for question in paper(attempt)]
    expires_in = math.ceil((expires_at(attempt) - timezone.now()).total_seconds())
    return render(request, "attempts/paper.html", {"attempt": attempt, "questions": questions, "expires_in": expires_in})


@roles(Role.STUDENT)
def attempt_remaining(request, pk):
    attempt = get_object_or_404(Attempt.objects.select_related("exam"), pk=pk, student=request.user)
    attempt = close_if_expired(attempt)
    return JsonResponse({"remaining_seconds": remaining_seconds(attempt)})


@roles(Role.STUDENT)
@require_POST
def save_answer(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk, student=request.user)
    question_id = request.POST.get("question", "")
    option_id = request.POST.get("option", "")
    if not (question_id.isdigit() and option_id.isdigit()):
        return JsonResponse({"detail": "A question and an option are required."}, status=400)
    try:
        services.save_answer(attempt, int(question_id), int(option_id))
    except AttemptClosed as refusal:
        return JsonResponse({"detail": str(refusal)}, status=409)
    except Option.DoesNotExist:
        return JsonResponse({"detail": "That option does not belong to this question."}, status=400)
    return JsonResponse({"saved": True})


@roles(Role.STUDENT)
@require_POST
def submit_attempt(request, pk):
    attempt = close_if_expired(get_object_or_404(Attempt, pk=pk, student=request.user))
    services.submit(attempt)
    return redirect("attempt-paper", attempt.pk)
