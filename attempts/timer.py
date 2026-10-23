from datetime import timedelta

from django.utils import timezone


def remaining_seconds(attempt, now=None):
    """FR-017: return non-negative time left from server-stamped attempt data."""
    current_time = now or timezone.now()
    deadline = attempt.started_at + timedelta(minutes=attempt.exam.duration_minutes)
    return max(0, int((deadline - current_time).total_seconds()))
