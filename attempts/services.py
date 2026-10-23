"""Attempt Session Manager (SAD 3.1): business operations on an attempt, called by its views."""
from django.db import transaction
from django.utils import timezone

from evaluation.engine import evaluate
from repository.models import Attempt


def submit(attempt):
    """The only way an attempt becomes submitted -- manual submit and FR-020's auto-submit both call this.

    FR-022: evaluation runs in the same transaction, so a submitted attempt never lacks a score.
    The conditional update makes a second submit (a double click, or racing the auto-submit) a no-op.
    """
    with transaction.atomic():
        if Attempt.objects.filter(pk=attempt.pk, submitted_at__isnull=True).update(submitted_at=timezone.now()):
            evaluate(attempt)
    attempt.refresh_from_db()
