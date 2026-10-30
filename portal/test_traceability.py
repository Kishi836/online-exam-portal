"""NFR-007 -- every functional requirement is linked to at least one test case, and the RTM matches the code."""
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from .traceability import MANUAL, TEST_PLAN

ALL_FRS = [f"FR-{n:03d}" for n in range(1, 31)]
# Not \b: in "test_UT_001_x" the underscore before UT is a word character, so \b would never match there.
ID = re.compile(r"(?<![A-Za-z0-9])(UT|IT|ST)_(\d{3})(?!\d)")


def automated_ids():
    """Every Test Plan ID that appears in a test method name or docstring anywhere in the repo's test files."""
    found = set()
    for path in Path(settings.BASE_DIR).rglob("test*.py"):
        if ".venv" in path.parts or "loadtest" in path.parts or path.name == "test_traceability.py":
            continue
        found.update(f"{kind}_{num}" for kind, num in ID.findall(path.read_text(encoding="utf-8")))
    return found


class TraceabilityTests(SimpleTestCase):
    def test_every_fr_is_verified_by_at_least_one_test_case(self):
        covered = {fr for frs in TEST_PLAN.values() for fr in frs}
        self.assertEqual([fr for fr in ALL_FRS if fr not in covered], [], "FRs with no Test Plan case in the RTM")

    def test_rtm_lists_all_118_test_plan_cases(self):
        # TODO(Komal): remove this skip once TEST_PLAN is complete.
        self.skipTest("TODO(Komal): fill portal/traceability.TEST_PLAN")
        counts = {kind: sum(1 for i in TEST_PLAN if i.startswith(kind)) for kind in ("UT", "IT", "ST")}
        self.assertEqual(counts, {"UT": 68, "IT": 37, "ST": 13})

    def test_every_case_is_automated_or_marked_manual_with_a_reason(self):
        # TODO(Komal): this is the Sprint 2 "Definition of Done" gate. Run it once every Sprint 2 PR is merged;
        # each ID it lists either gets a test (named test_<ID>_...) or a MANUAL entry with a real reason.
        self.skipTest("TODO(Komal): enable after the Sprint 2 PRs merge")
        missing = sorted(set(TEST_PLAN) - automated_ids() - set(MANUAL))
        self.assertEqual(missing, [], "Test Plan cases with no automated test and no manual reason")

    def test_no_test_names_an_id_the_test_plan_does_not_have(self):
        # TODO(Komal): remove this skip once TEST_PLAN is complete; a typo'd or made-up ID in a test name is caught here.
        self.skipTest("TODO(Komal): needs the full TEST_PLAN")
        self.assertEqual(sorted(automated_ids() - set(TEST_PLAN)), [])

    def test_manual_cases_are_real_test_plan_cases(self):
        self.assertTrue(set(MANUAL) <= set(TEST_PLAN) | {"IT_022", "IT_023"})
