"""Attempt Session Manager (SAD 3.1): business operations on an attempt, called by its views."""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from evaluation.engine import evaluate
from repository.models import Answer, Attempt, Exam, Option


class AttemptClosed(Exception):
    """A change refused because the attempt is already submitted (FR-020); the message is the Test Plan's wording."""


def submit(attempt, at=None):
    """The only way an attempt becomes submitted -- manual submit and FR-020's auto-submit both call this.

    FR-022: evaluation runs in the same transaction, so a submitted attempt never lacks a score.
    The conditional update makes a second submit (a double click, or racing the auto-submit) a no-op.
    """
    with transaction.atomic():
        if Attempt.objects.filter(pk=attempt.pk, submitted_at__isnull=True).update(submitted_at=at or timezone.now()):
            evaluate(attempt)
    attempt.refresh_from_db()


def expires_at(attempt):
    """FR-020: the server-stamped start plus the exam's duration; nothing from the client enters it."""
    return attempt.started_at + timedelta(minutes=attempt.exam.duration_minutes)


def remaining_seconds(attempt, now=None):
    """FR-017: non-negative time remaining from the server clock."""
    current_time = now or timezone.now()
    return max(0, int((expires_at(attempt) - current_time).total_seconds()))


def close_if_expired(attempt):
    """FR-020: submit an overdue attempt, stamped at its expiry rather than whenever it was noticed (UT_052).

    There is no background job: every request that touches an attempt calls this first, so an attempt
    left with the browser closed is submitted the next time anyone looks at it (IT_026).
    """
    # ponytail: no sweep for attempts nobody opens again; results views (FR-024+) call this per attempt
    if attempt.submitted_at is None and timezone.now() >= expires_at(attempt):
        submit(attempt, at=expires_at(attempt))
    return attempt


def save_answer(attempt, question_id, option_id):
    """Store the Student's choice for one question; refused once the attempt is submitted or out of time.

    Raises Option.DoesNotExist if the option is not one of that question's options in this exam.
    """
    if close_if_expired(attempt).submitted_at:
        raise AttemptClosed("This attempt has already been submitted")
    option = Option.objects.get(pk=option_id, question_id=question_id, question__exams=attempt.exam)
    Answer.objects.update_or_create(attempt=attempt, question_id=question_id, defaults={"option": option})


def visible_exams(student):
    """FR-006: the published exams of the courses this Student is enrolled in. The one place this rule lives."""
    return Exam.objects.filter(course__students=student, status=Exam.Status.PUBLISHED).select_related("course")


def dashboard_groups(student, now=None):
    """FR-014: the Student's visible exams split into Upcoming, Live and Completed, by server time only.

    - Upcoming: no window yet, or server time is before window_start.
    - Live: the window is open and the Student has no submitted attempt.
    - Completed: the Student has submitted, or the window has ended.

    `now` is for tests; the dashboard passes nothing, so the server clock decides (IT_018).
    """
    now = now or timezone.now()
    groups = {"upcoming": [], "live": [], "completed": []}
    submitted = set(
        Attempt.objects.filter(student=student, submitted_at__isnull=False).values_list("exam_id", flat=True)
    )
    for exam in visible_exams(student).order_by("window_start", "title"):
        # TODO(Kartik): put `exam` into exactly one of the three lists, using the rules in the docstring.
        # Check "submitted" first: a submitted exam is Completed even while its window is still open (UT_038).
        pass
    return groups
