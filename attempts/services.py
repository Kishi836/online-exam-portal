"""Attempt Session Manager (SAD 3.1): business operations on an attempt, called by its views."""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from evaluation.engine import evaluate
from repository.models import Answer, Attempt


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


def result_visible(attempt):
    """FR-025: a Student sees a score only once the attempt is submitted and Faculty has published results."""
    return attempt.submitted_at is not None and attempt.exam.results_published


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


def save_answer(attempt, question_id, option_id, marked_for_review=None):
    """FR-019: store, change or clear (option_id None) one response; refused once submitted or out of time.

    `marked_for_review` None leaves the flag as it is. Raises Question.DoesNotExist or Option.DoesNotExist
    for a question outside this exam or an option outside that question.
    """
    if close_if_expired(attempt).submitted_at:
        raise AttemptClosed("This attempt has already been submitted")
    question = attempt.exam.questions.get(pk=question_id)
    fields = {"option": None if option_id is None else question.options.get(pk=option_id)}
    if marked_for_review is not None:
        fields["marked_for_review"] = marked_for_review
    Answer.objects.update_or_create(attempt=attempt, question=question, defaults=fields)
