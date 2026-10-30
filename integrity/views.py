"""Integrity views: focus-loss capture and the Faculty integrity page (FR-028), the Admin audit viewer (FR-030)."""
from django.shortcuts import render  # noqa: F401
from django.views.decorators.http import require_GET

from identity.access import roles
from repository.models import AuditEntry, Role  # noqa: F401


@roles(Role.ADMIN)
@require_GET
def audit_log(request):
    """FR-030: read-only list of audit entries, newest first, filterable by ?entity=Exam&entity_id=7 (ST_013).

    There is deliberately no edit or delete view, form or button anywhere for audit rows (IT_037).
    """
    # TODO(Komal): entries = AuditEntry.objects.select_related("actor"); apply the two optional filters
    # from request.GET (entity_id only if it .isdigit()); cap at 500 rows; render "integrity/audit_log.html".
    raise NotImplementedError
