"""NFR-007: the Requirements Traceability Matrix in code -- every Test Plan case ID and the FRs it verifies.

Source of truth: Documents/Test_Plan.pdf, sections 6.x (one table per use case) and 7 (coverage summary).
Read the IDs from the PDF itself, row by row: copy-pasting its tables scrambles the columns.
portal/test_traceability.py checks this table against the test suite, so the RTM can't silently go stale.
"""

# Test Plan ID -> the FR IDs its "Test case description" column names.
# TODO(Komal): fill in ALL 118 rows (68 UT, 37 IT, 13 ST) from Documents/Test_Plan.pdf.
# The rows below are already checked against the PDF; keep them.
TEST_PLAN = {
    "UT_043": ["FR-018"],
    "UT_044": ["FR-018"],
    "IT_021": ["FR-018"],
    "UT_059": ["FR-025"],
    "UT_060": ["FR-026"],
    "UT_061": ["FR-026"],
    "UT_062": ["FR-027"],
    "UT_063": ["FR-027"],
    "IT_032": ["FR-025"],
    "IT_033": ["FR-025"],
    "IT_034": ["FR-026", "FR-027"],
    "ST_012": ["FR-025", "FR-026", "FR-027"],
    "UT_064": ["FR-028"],
    "UT_065": ["FR-028"],
    "UT_066": ["FR-028"],
    "UT_067": ["FR-028"],
    "UT_068": ["FR-030"],
    "IT_035": ["FR-029"],
    "IT_036": ["FR-030"],
    "IT_037": ["FR-030"],
    "ST_013": ["FR-028", "FR-029", "FR-030"],
}

# Test Plan IDs that are run by hand, with the reason they can't be a Django test. Everything else must be automated.
MANUAL = {
    "IT_022": "Measures the browser's 5 s network budget for autosave; the server half is automated under FR-019.",
    "IT_023": "Kills the browser process mid-attempt; the server half (no saved answer lost) is automated under FR-021.",
    # TODO(Komal): add any other case that genuinely needs a human or a real browser, with its reason.
}
