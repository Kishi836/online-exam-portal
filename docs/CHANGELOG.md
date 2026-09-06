# Project Changelog

A phase-by-phase record of how this project developed. Every milestone, requirement change and
scope decision is logged here so the evolution of the work — not only its final state — can be
presented at the end of the semester.

Format: newest first. Requirement changes cite the requirement ID and the reason.

---

## 2026-09-02 — CR-01: Requirement baseline reduced; M1 deliverables repackaged

**Milestone:** M1 (extended scope, per instructor). **Sprint:** 0.

### Change request CR-01 — scope reduction

The M1 baseline of **83 functional and 27 non-functional requirements** exceeded what a team of
three can implement, test and demonstrate in one semester. The committed set is reduced to
**30 functional and 10 non-functional requirements** — the demo-critical core covering the full
examination lifecycle from registration through to a published scorecard.

| | Before | After | Dropped |
|---|---|---|---|
| Functional | 83 (49 Must, 26 Should, 8 Could) | **30** (all Must) | 53 |
| Non-functional | 27 (13 Product, 7 Organisational, 7 External) | **10** (5 P, 2 O, 3 E) | 17 |

**Impact.** Scope only; no schedule change. The RTM shrinks to 30 rows. Test coverage is unaffected
in kind — every retained requirement still carries at least one test case, satisfying NFR-O-05.
Requirement identifiers are **unchanged**; a dropped requirement's ID is retired and never reissued,
so the PRD, SRS, Test Plan and RTM continue to share one identifier space.

**One requirement was amended rather than dropped:** `FR-EX-01` now carries the per-examination
policy attributes — negative marking, question and option shuffling, and the pass mark — that
previously sat in `FR-EX-05`. The behaviour is unchanged; two requirements became one.

### Corrected counts

The M1 baseline stated *"74 total — 38 Must, 24 Should, 12 Could"* and the PRD stated
*"79 requirements"*. Counting the priority column of the eleven module tables gives **83
requirements — 49 Must, 26 Should, 8 Could**, and the PRD defines **88** FR identifiers (M1 being
the PRD set minus the five `FR-SYS-*` entries). The stated totals were wrong and are superseded by
this entry; they remain uncorrected in `README.md`, the PRD and `M1_REQUIREMENTS.md`, which are now
historical records of the pre-reduction baseline.

### Added

- `Documents/SRS Document.md` — the reduced baseline as a table of 30 functional and 10
  non-functional requirements, with a verification method against each.
- `Documents/Test Plan Document.md` — 118 test cases across 13 use cases (68 Unit, 37 Integration,
  13 System), 8–10 per use case, written to the template issued by the instructor. *Actual Result*
  and *Test Result* are left blank pending implementation.
- `Documents/Use Case Diagram.md` — the use case model: four actors, the system boundary, thirteen
  use cases and their `«include»` / `«extend»` relationships, drawn in Mermaid. Carries a
  use-case-to-requirement traceability table covering **30 of 30** functional requirements, each
  appearing in exactly one use case.
- `Documents/Use Case Flow.md` — the main success scenario, alternate flows, exception flows and
  business rules of all thirteen use cases, with the verifying test case named against each step,
  plus the end-to-end lifecycle diagram.

The four deliverables share one use case identifier space, `UC-01`–`UC-13`, and one requirement
identifier space, so the SRS, the use case model, the flows, the test plan and the RTM cross-check
against each other by identifier alone. Verified mechanically: every test case ID range quoted in
the use case model matches the Test Plan exactly, and all 118 test case IDs are unique.

### Deliverable repackaging

The instructor's message of 2026-09-02 requires four documents in a `Documents/` folder at the
repository root, and that the repository name match the project title:

| Document | Owner | State |
|---|---|---|
| SRS Document — FR and NFR table | Kartik → revised by Kshitij | Done |
| Test Plan Document | Kshitij | Done |
| Use Case Diagram | Komal | Done |
| Use Case Flow | Kartik | Done |

This supersedes the full IEEE Std 830-1998 SRS and the four-diagram UML set assumed by
`docs/02-srs/M1_WORK_SPLIT.md`; the instructor's requirement is a requirements **table**, not the
full standard document.

### Outstanding

- Repository is named `online-exam-portal`; the project title is *Online Examination Portal*. Rename
  required.
- `user_stories.md` at the repository root defines `US-01`–`US-06` with meanings that collide with
  the baseline's `US-01`–`US-36`, and carries no requirement traceability. To be withdrawn.
- The `README.md` **Working agreements** and **Team** sections were removed by commit `9d3a8b6` and
  need restoring.

---

## 2026-08-19 — M1: Requirements baselined

**Milestone:** M1 — Requirements Commitment. **Sprint:** 0.

### Added

- `PRD_01_Online_Exam_Portal.md` — Product Requirements Document, v1.0. Problem statement, goals and
  success metrics, deployment tiers (S/M/L), stakeholders, scope, 15 headline user stories, 79
  requirements across 12 modules, non-functional requirements, security and compliance, data and
  integration architecture, risks, phased rollout, dependencies, open questions.
- `docs/01-requirements/M1_REQUIREMENTS.md` — the formally specified committed subset: 74 functional
  requirements (38 Must, 24 Should, 12 Could), non-functional requirements classified as
  Product/Organisational/External with measurable metrics, security requirements derived through a
  Security Risk Assessment, 36 user stories across 8 epics totalling 178 story points, RTM seed,
  milestone plan, validation approach.
- `README.md`, `docs/CHANGELOG.md`.

### Scope decisions

| Decision | Rationale |
|---|---|
| Multiple-choice only; no descriptive answers or manual grading | Fixed by the assigned topic. Also removes the highest-effort, least-testable part of an exam system |
| Three actors — Student, Faculty, Administrator; **no separate Proctor** | Integrity monitoring is automated and reviewed by Faculty; a proctor role would only exist to serve live proctoring, which is out of scope |
| MSQ and True/False treated as MCQ variants, not separate types | Same data model and same evaluator; near-zero additional cost for a visibly richer question bank |
| Implementation stack deliberately **not** fixed at M1 | A requirement states *what*, not *how* (Lecture 7 §6). Stack is a Sprint 0 decision, to be recorded here as an addendum |
| Proctoring, analytics beyond basic statistics, adaptive testing excluded | Semester capacity for a team of 3; each is a genuine risk of an incomplete demonstration |
| Requirement IDs are module-prefixed (`FR-AUTH-01`) rather than flat | 74 requirements across 11 modules; a flat sequence would not survive later insertion. Same ID space is reused in the PRD, the SRS and the RTM |

### Designated scope-release valves

If sprints run tight, these are dropped in order, none of which affects a Must-priority requirement:
`FR-RES-08`/`FR-RES-09` (answer-key challenge) → `FR-EX-03` (auto-generated papers) →
`FR-RES-07` (PDF scorecard) → `FR-NTF-03` (in-app notification centre).

### Open at close of M1

The five open questions in PRD §14 — negative-marking convention, violation-threshold behaviour,
actual retention period, demonstration infrastructure, and the MSQ partial-credit rule — remain to be
resolved with the course instructor before Sprint 2.

---

## Requirement change log

Changes to a baselined requirement are raised as a change request, assessed for impact on scope,
schedule and the RTM, and recorded below.

| Date | Req ID | Change | Reason | Impact |
|---|---|---|---|---|
| 2026-09-02 | All 26 Should-priority FRs | **Dropped** | CR-01 scope reduction — not demonstrable within semester capacity for a team of three | RTM rows retired; IDs not reissued |
| 2026-09-02 | All 8 Could-priority FRs | **Dropped** | CR-01 — stretch tier, already designated scope-release valves | None; none was committed for implementation |
| 2026-09-02 | `FR-AUTH-04`, `FR-AUTH-05`, `FR-AUTH-07`, `FR-AUTH-10` | **Dropped** | CR-01 — account lockout, password reset, single-session enforcement and Administrator account lifecycle are auth hygiene rather than examination-portal core | Administrator remains an actor through `FR-CRS-01` and `FR-ADM-01` |
| 2026-09-02 | `FR-CRS-02` | **Merged into `FR-CRS-01`** | Faculty-to-Course assignment is part of course maintenance | None; behaviour retained |
| 2026-09-02 | `FR-QB-07`, `FR-QB-08` | **Dropped** | CR-01 — bank search/filter and per-course Faculty scoping; the latter is subsumed by `FR-AUTH-06` RBAC | Reduced Faculty convenience; access control unaffected |
| 2026-09-02 | `FR-EX-05` | **Merged into `FR-EX-01`** | Per-examination policy values folded into examination creation | None; behaviour retained |
| 2026-09-02 | `FR-EX-04`, `FR-EX-07` | **Dropped** | CR-01 — total-marks validation and post-window question-set freeze | Loses two integrity guards; accepted risk, recorded here |
| 2026-09-02 | `FR-SCH-02` | **Dropped** | CR-01 — window-length validation against duration | A misconfigured window is possible; Faculty responsibility |
| 2026-09-02 | `FR-ATT-04`, `FR-ATT-10`, `FR-ATT-11` | **Dropped** | CR-01 — response select/change/clear is implied by `FR-ATT-03` and `FR-ATT-05`; shuffling and concurrent-attempt rejection dropped | Loses per-student paper shuffling, previously US-24 |
| 2026-09-02 | `FR-EVL-03` | **Merged into `FR-EVL-02`** | The unattempted-question rule stated alongside the positive and negative marking rules | None; behaviour retained |
| 2026-09-02 | `FR-EVL-06`, `FR-EVL-09` | **Dropped** | CR-01 — the 5-second evaluation budget is retained as `NFR-P-03`; raw-response retention dropped as a stated requirement | Evaluation timing still verified via `NFR-P-03` |
| 2026-09-02 | `FR-RES-06` | **Dropped** | CR-01 — CSV export of results | Loses the LMS hand-off path; `NFR-E-04` dropped with it |
| 2026-09-02 | `FR-INT-06` | **Dropped** | CR-01 — distinct per-student question ordering, dropped with `FR-ATT-10` | Copying from a neighbouring screen is no longer countered |
| 2026-09-02 | `NFR-P-02`, `NFR-P-05`, `NFR-P-06`, `NFR-P-08`, `NFR-P-09`, `NFR-P-10`, `NFR-P-12`, `NFR-P-13` | **Dropped** | CR-01 — eight Product NFRs; speed, capacity, robustness and portability retained | Security requirements `SEC-01`–`SEC-14` leave the committed set with `NFR-P-13` |
| 2026-09-02 | `NFR-O-01`, `NFR-O-03`, `NFR-O-04`, `NFR-O-06`, `NFR-O-07` | **Dropped** | CR-01 — process obligations beyond version control and traceability | `NFR-O-03`'s SRS/RTM/UML obligation is superseded by the instructor's own deliverable list |
| 2026-09-02 | `NFR-E-02`, `NFR-E-04`, `NFR-E-05`, `NFR-E-07` | **Dropped** | CR-01 — retention period, CSV schema, evidentiary-flagging position and the target VM constraint | The evidentiary-not-judicial stance survives as a design position, no longer a stated requirement |
