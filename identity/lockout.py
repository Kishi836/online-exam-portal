"""NFR-012: lock an account for 15 minutes after 5 failed sign-ins within 15 minutes.

Failures are counted per email typed -- also for emails with no account, so the lockout message
doesn't reveal which emails exist. The values live in settings, not in this code (NFR-010 spirit).
"""
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from repository.models import SignInFailure


def _window():
    return timedelta(minutes=settings.SIGNIN_LOCK_MINUTES)


def is_locked(email, now=None):
    """True while `email` has SIGNIN_LOCK_THRESHOLD or more failures in the last SIGNIN_LOCK_MINUTES."""
    now = now or timezone.now()
    # TODO(Komal): count SignInFailure rows for email.lower() with at > now - _window(); compare to the threshold.
    # Because the window slides, the lock lifts by itself 15 minutes after the 5th failure.
    raise NotImplementedError


def record_failure(email):
    """One failed sign-in for `email` (stored lower-cased)."""
    # TODO(Komal): create the SignInFailure row.
    raise NotImplementedError


def clear(email):
    """A successful sign-in wipes the count, so old failures can't add up with new ones."""
    SignInFailure.objects.filter(email=email.lower()).delete()
