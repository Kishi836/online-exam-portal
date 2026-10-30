"""FR-030 -- the append-only audit trail (Test Plan UT_068, IT_036, IT_037, ST_013)."""
from django.db import DatabaseError, connection, transaction
from django.test import TestCase
from django.urls import reverse

from portal.testkit import World
from repository import audit
from repository.models import AppendOnly, AuditEntry, Exam


class AuditTests(TestCase):
    def setUp(self):
        self.world = World()

    def test_record_stores_actor_action_entity_time_and_changes(self):
        entry = audit.record(self.world.fac_a, "update", self.world.exam, {"title": ["EXM_1", "EXM_2"]})
        self.assertEqual((entry.actor, entry.action, entry.entity, entry.entity_id), (self.world.fac_a, "update", "Exam", self.world.exam.pk))
        self.assertEqual(entry.changes, {"title": ["EXM_1", "EXM_2"]})
        self.assertIsNotNone(entry.at)

    def test_UT_068_an_edit_records_old_and_new_values(self):
        # The Test Plan edits a question's stem; question edits arrive with FR-009, so this uses the exam edit,
        # which is on main. Add the question version of this test in FR-009's PR.
        Exam.objects.filter(pk=self.world.exam.pk).update(status=Exam.Status.DRAFT)
        self.client.force_login(self.world.fac_a)
        # TODO(Komal): POST exam-edit with every ExamForm field (copy from examsetup/tests.py) and title "EXM_2";
        # then exactly one AuditEntry for ("Exam", exam.pk) with actor FAC_A and changes["title"] == ["EXM_1", "EXM_2"].
        self.skipTest("TODO(Komal): UT_068")

    def test_IT_036_every_mutation_class_writes_an_entry(self):
        # TODO(Komal): through the real views (self.client), create a user (register), a course (as ADM_A),
        # a question (as FAC_A) and an examination, then submit an attempt (evaluation = the result).
        # Assert AuditEntry has at least one row for each entity: User, Course, Question, Exam, Attempt.
        self.skipTest("TODO(Komal): IT_036")

    def test_IT_037_audit_rows_cannot_be_changed_or_deleted(self):
        entry = audit.record(None, "create", self.world.exam)
        with self.assertRaises(AppendOnly):
            entry.action = "tampered"
            entry.save()
        with self.assertRaises(AppendOnly):
            entry.delete()
        with self.assertRaises(AppendOnly):
            AuditEntry.objects.filter(pk=entry.pk).update(action="tampered")
        with self.assertRaises(AppendOnly):
            AuditEntry.objects.all().delete()
        # Even raw SQL that skips the ORM is stopped by the triggers in migration 0006.
        with self.assertRaises(DatabaseError), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute("UPDATE repository_auditentry SET action = 'tampered'")
        with self.assertRaises(DatabaseError), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute("DELETE FROM repository_auditentry")
        self.assertEqual(AuditEntry.objects.get(pk=entry.pk).action, "create")

    def test_ST_013_admin_reads_the_log_filtered_to_one_exam(self):
        audit.record(self.world.fac_a, "publish", self.world.exam)
        audit.record(self.world.fac_a, "create", self.world.course)
        self.client.force_login(self.world.adm_a)
        response = self.client.get(reverse("audit-log"), {"entity": "Exam", "entity_id": self.world.exam.pk})
        self.assertEqual(response.status_code, 200)
        # TODO(Komal): the page shows the "publish" entry and not the Course one; a Faculty or Student gets 403.
        self.skipTest("TODO(Komal): ST_013")
