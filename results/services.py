"""Results (SAD 3.1): business operations on published results. The visibility rule is attempts.services.result_visible."""
from django.utils import timezone


class ResultsNotReady(Exception):
    """FR-026: results can only be released once the examination window has ended."""


def set_results_published(exam, published, now=None):
    """Publish or unpublish results without modifying any attempt scores.

    Refuse publication when the examination has no window_end or its
    window_end is still in the future. Unpublishing is always allowed.
    """
    now = now or timezone.now()

    if published and (
        exam.window_end is None or exam.window_end > now
    ):
        raise ResultsNotReady(
            "Results can be published only after the examination window closes"
        )

    exam.results_published = published
    exam.save(update_fields=["results_published"])
