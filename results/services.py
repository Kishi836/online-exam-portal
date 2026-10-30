"""Results (SAD 3.1): business operations on published results. The visibility rule is attempts.services.result_visible."""
from django.utils import timezone


class ResultsNotReady(Exception):
    """FR-026: results can only be released once the examination window has ended."""


def set_results_published(exam, published, now=None):
    """FR-026: publish (True) or unpublish (False) the results of `exam`. Unpublishing never touches a score (UT_061).

    Refuse with ResultsNotReady("Results can be published only after the examination window closes")
    when publishing an exam with no window, or whose window_end is still in the future (server time).
    Unpublishing is always allowed.
    """
    now = now or timezone.now()
    # TODO(Komal): the refusal above, then save only the results_published field:
    #     exam.save(update_fields=["results_published"])
    # FR-030: once your audit PR is on main, record ("publish_results" / "unpublish_results") here too.
    raise NotImplementedError
