# M1 — Work Split Plan (draft, not yet agreed with the team)

**Status:** drafted 2026-08-31. Not sent to the team yet. Two decisions still open.

## Revised M1 scope (per instructor, 2026-08-31)

M1 is no longer just the requirements commitment. It now requires:

| Item | State |
|---|---|
| FR as a table | Done — 74 FRs across 11 module tables in `docs/01-requirements/M1_REQUIREMENTS.md` §2 |
| NFR as a table | Done — Product / Organisational / External tables, §3 |
| SRS (IEEE Std 830-1998) | Not started |
| UML — use case, class, sequence, activity | Not started |
| Team leader, also acting as Scrum Master | Not decided |

Deadline: end of week (Fri 2026-09-04).

## Split

An SRS is one document, so nobody edits a shared file. Each member writes their own
section files; one member assembles. Split follows the roles already committed in
`M1_REQUIREMENTS.md` §7.

| Owner | SRS sections | Diagrams |
|---|---|---|
| **Kshitij** — backend/data | §3.2 Functional Requirements (lift FR tables, add pre/post-conditions), §3.4 Logical Database Requirements | Class diagram |
| **Kartik** — frontend/UX | §3.1 External Interface Requirements (user / hardware / software / comms) | Use case diagram, Activity diagram (attempt lifecycle: start → autosave → submit → violation path) |
| **Komal** — QA/docs | §1 Introduction, §2 Overall Description, §3.3 Performance, §3.6 Software System Attributes (lift NFR tables), RTM update, **assembles the SRS** | Sequence diagrams ×2 (take exam; auto-evaluate & publish) |

If Komal also takes the lead role, move §3.3 Performance to Kartik — his load is otherwise
the heaviest, and the NFR tables are already written so it is mostly a lift.

## File layout (chosen to avoid merge conflicts)

```
docs/02-srs/
  SRS_Online_Exam_Portal.md              # assembled Thursday
  sections/01_introduction.md            # Komal
  sections/02_overall_description.md     # Komal
  sections/03_1_external_interfaces.md   # Kartik
  sections/03_2_functional.md            # Kshitij
  sections/03_3_performance.md           # Komal
  sections/03_4_database.md              # Kshitij
  sections/03_6_attributes.md            # Komal
  diagrams/usecase.md  class.md  activity.md  sequence.md
```

Diagrams in **Mermaid** inside `.md` — renders on GitHub, diffs in git, exports to PNG for
the deck. Not draw.io: binary files leave no evidence trail, and the course grades the
documented process.

## Schedule

| Day | Work |
|---|---|
| Mon 31 Aug | Decide the lead. Agree the SRS skeleton. Lead pushes empty section files so nobody is blocked. |
| Tue 1 – Wed 2 Sep | Parallel authoring. Branch per person (`srs/<name>`); nobody touches another's file. |
| Thu 3 Sep | Merge all three, assemble the SRS, cross-review — each member reviews the other two (satisfies NFR-O-02 peer review and is itself a marked process artefact). |
| Fri 4 Sep | Fix review comments, update the RTM, append the M1 entry to `docs/CHANGELOG.md`, tag `m1`. |

## Ground rules

- Branch per person: `srs/kshitij`, `srs/kartik`, `srs/komal`.
- Edit only your own files. Need a change elsewhere? Message the owner, don't edit.
- Reuse requirement IDs exactly (`FR-AUTH-01`, `NFR-P-03`, …). The RTM depends on that ID
  space — do not renumber.
- IEEE Std 830-1998 section numbering, per the Lecture 9 slides (`Unit 1/09_SRS_RTM.pdf`).
- Small, frequent commits. The process is graded, not only the final document — one evening
  of 12 commits reads worse than four days of steady ones.
- Push by Wednesday night. Thursday is review day, not writing day.

## Open decisions

1. **Team leader / Scrum Master.** Recommendation: **Komal**. The Scrum Master is a
   facilitator, not the technical boss — ceremonies, blockers, artefact upkeep — which is
   already his committed role (sprint artefacts, CI, demo script). Making the heaviest
   implementer the SM means ceremonies get dropped first when code runs late. Kshitij stays
   technical owner and repo owner.
2. **Submission format.** Is the repo Markdown acceptable, or does the instructor want a
   Word/PDF submission? Someone needs to confirm with her.
