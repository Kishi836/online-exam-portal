"""Integrity views: focus-loss capture and the Faculty integrity page (FR-028), the Admin audit viewer (FR-030)."""
from django.shortcuts import render
from django.views.decorators.http import require_GET

from identity.access import roles
from repository.models import AuditEntry, Role


@roles(Role.ADMIN)
@require_GET
def audit_log(request):
    """FR-030: Read-only audit log, newest first, with optional entity filters."""
    entries = AuditEntry.objects.select_related("actor")

    entity = request.GET.get("entity", "").strip()
    entity_id = request.GET.get("entity_id", "").strip()

    if entity:
        entries = entries.filter(entity=entity)

    if entity_id.isdigit():
        entries = entries.filter(entity_id=int(entity_id))

    entries = entries[:500]

    return render(
        request,
        "integrity/audit_log.html",
        {"entries": entries},
    )
