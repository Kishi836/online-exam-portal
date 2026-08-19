# Project Changelog

A phase-by-phase record of how this project developed. Every milestone, requirement change and
scope decision is logged here so the evolution of the work — not only its final state — can be
presented at the end of the semester.

Format: newest first. Requirement changes cite the requirement ID and the reason.

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
| — | — | *No changes since baseline* | — | — |
