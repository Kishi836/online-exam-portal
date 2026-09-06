# M1 Status — Online Exam Portal

**Written:** 2026-09-02, mid-session pause (next class starting)
**Student:** Kshitij G Shettigar · PES1UG24CS240 · Backend & Data Lead
**Repo:** `https://github.com/Kishi836/online-exam-portal` · local `HEAD = 80a0d77`, level with `origin/main`

This file is the full handover. A session that reads it should not need to re-derive anything.

---

## 1. Committed and pushed; not yet on `main`

Everything is on branch `docs/m1-deliverables`, pushed 2026-09-06, open as **PR #1**. It needs one
teammate approval to merge, per `NFR-O-02`. **Until it merges, `main` still shows none of it and
the instructor sees nothing.**

For the record, this was the state at the 2026-09-02 pause, when every one of these files sat
uncommitted on disk:

```
 M docs/CHANGELOG.md        <- CR-01 scope reduction entry
?? Documents/               <- SRS Document.md + Test Plan Document.md
?? docs/02-srs/             <- M1_WORK_SPLIT.md, drafted 2026-08-31, never committed
```

## 2. What the instructor actually asked for (message received 2026-09-02)

Four documents in a folder named **`Documents/`** at the repo root, and **the repository name must
match the project title**:

| # | Document | Owner | State |
|---|---|---|---|
| 1 | **SRS Document** — a table of Functional *and* Non-Functional Requirements | Kartik → revised by Kshitij | **Done** — `Documents/SRS Document.md` |
| 2 | **Test Plan Document** — the shared template | Kshitij | **Done** — `Documents/Test Plan Document.md` |
| 3 | **Use Case Diagram** | Komal | **Done** — `Documents/Use Case Diagram.md` |
| 4 | **Use Case Flow** | Kartik | **Done** — `Documents/Use Case Flow.md` |

Deadline: test cases were said to be **due today (2026-09-02)** — confirm this, it was an "iirc".

**This supersedes `docs/02-srs/M1_WORK_SPLIT.md`.** That draft assumed a full IEEE Std 830-1998 SRS
plus four UML diagrams. The instructor wants a requirements *table*, not the standard document. The
work split is therefore obsolete except as a record of the original plan.

## 3. Done this session

### `Documents/SRS Document.md` — reduced baseline
- **30 functional requirements** (all Must) and **10 non-functional** (5 Product / 2 Organisational
  / 3 External), each with a verification method and priority column.
- Distribution A:3 · B:3 · C:3 · D:3 · E:3 · F:6 · G:3 · H:3 · I:2 · K:1.
- Original `FR-*` / `NFR-*` IDs preserved — **nothing renumbered**, so PRD/SRS/Test Plan/RTM share
  one ID space. Dropped IDs are retired, never reissued.

### `Documents/Test Plan Document.md` — 118 test cases
- 13 use cases, **8–10 cases each**, in the instructor's 9-column template.
- **68 Unit (`UT_001`–`UT_068`) · 37 Integration (`IT_001`–`IT_037`) · 13 System (`ST_001`–`ST_013`)**.
- Verified: no duplicate IDs; all 30 SRS requirements exercised; no test references a dropped
  requirement. Checked by diffing the ID sets — exact match both directions.
- *Actual Result* and *Test Result* deliberately **blank** — no implementation exists, so filling
  them would be fabrication. They get populated at M4.

### `docs/CHANGELOG.md` — CR-01
- Full change-control entry for the scope reduction, plus a line-by-line requirement change table
  recording every drop and merge with its reason.

### `Documents/Use Case Diagram.md` and `Documents/Use Case Flow.md` — written 2026-09-06

- **Use Case Diagram** — four actors (Student, Faculty, Administrator, and **Clock** as the only
  non-human actor), one master diagram plus four subsystem diagrams, all in Mermaid. Records why
  *System* is deliberately **not** drawn as an actor even though the SRS names it in the Actor
  column. Eight justified `«include»` / `«extend»` relationships, each traced to the requirement
  that makes it true. Traceability table: **30 of 30** FRs, each in exactly one use case.
- **Use Case Flow** — all thirteen use cases with main success scenario, alternate flows, exception
  flows and business rules, and the verifying test case ID named against individual steps. Ends
  with an end-to-end lifecycle diagram.
- **Verified mechanically, not by eye:** every test case ID range quoted matches the Test Plan
  exactly (checked by parsing both files); all 118 test IDs unique; all 30 FRs cited exactly once,
  none invented.

## 4. Defects found in the baseline — all still unfixed in the source docs

### 4.1 The requirement counts were wrong
| Document claims | Actual |
|---|---|
| `M1_REQUIREMENTS.md`: "74 total — 38 Must, 24 Should, 12 Could" | **83 — 49 Must, 26 Should, 8 Could** |
| PRD: "79 requirements" | **88 FR IDs** (M1 = PRD minus the five `FR-SYS-*`) |

Counted from the priority column of the eleven module tables. The wrong figures still stand in
`README.md`, the PRD and `M1_REQUIREMENTS.md`. CR-01 records the correction; those three files are
now historical records of the pre-reduction baseline and were deliberately left alone.

### 4.2 Kartik's `SRS_table.pdf` (commit `80a0d77`) — superseded but still in the repo
- Only **40 of 83** requirements; **14 Must-priority requirements missing**: `FR-AUTH-10`,
  `FR-QB-08`, `FR-EX-06`, `FR-EX-07`, `FR-SCH-02`, `FR-SCH-03`, `FR-ATT-04`, `FR-ATT-11`,
  `FR-EVL-03`, `FR-EVL-05`, `FR-EVL-09`, `FR-RES-02`, `FR-RES-06`, `FR-INT-06`.
- **Zero NFRs** — the instructor explicitly asked for both FR and NFR.
- IDs renamed `FR-*` → `SRS-*`, breaking the RTM ID space (the work-split rule said do not renumber).
- It is a **PDF** — no git diff, no evidence trail, and the course grades the process.
- Sits at repo root, not in `Documents/`.
- **Worth keeping from it:** the *Verification Method* and *Tier Scope* column idea. Verification
  Method is carried into the new SRS document.

**Decision needed:** delete `SRS_table.pdf`, or keep it beside the new Markdown SRS.

### 4.3 `user_stories.md` (root) contradicts the PRD — recommend withdrawing it
Defines `US-01`–`US-06` with meanings that **collide** with the baseline's `US-01`–`US-36`, and
carries no FR traceability. Six substantive contradictions:

| # | The file says | Baseline says |
|---|---|---|
| 1 | Score shown **immediately on submission** | `FR-RES-01` — withheld until Faculty publishes |
| 2 | "Section-wise breakdown" | No section concept; `FR-RES-03` is per-question |
| 3 | Evaluation **≤ 2 s**, asynchronous | `FR-EVL-06` / `NFR-P-03` — **≤ 5 s** |
| 4 | Integrity flags go to **Administrator** | `FR-INT-04` — Faculty; M1 has no Proctor role |
| 5 | "3rd violation auto-submits" | `FR-INT-02` — *exceeds* a threshold of 3, i.e. the 4th |
| 6 | Palette: Answered / Unanswered / Marked / **Current Question** | `FR-ATT-03` — Not Visited / Not Answered / Answered / Marked. **Not Visited is missing** |

Plus unsanctioned scope presented as settled: rich text, code snippets and image attachments in
questions; JSON upload; MSQ partial marking (a Should whose rule is still an open question).

Merging it would propagate all six contradictions. Point at `M1_REQUIREMENTS.md` §5 instead.

### 4.4 README regression
Commit `9d3a8b6` deleted the **Working agreements** section and the **Team** roles table from
`README.md`, and pasted the six user stories into the middle of the document. The deleted rule
includes *"Feature branches only — no direct commits to `main`"* — which is also the rule that
commit broke. **Restore both sections.**

## 5. Next actions, in order

1. ~~**Commit and push** this session's work.~~ Done 2026-09-06 on branch `docs/m1-deliverables`
   via a PR, per the working agreement — **one teammate approval is needed to merge it to `main`.**
   Until it merges, the instructor sees nothing on `main`.
2. **Get one teammate to review the PR** — Komal on the Use Case Diagram, Kartik on the Use Case
   Flow. The PR approval satisfies `NFR-O-02` and is itself a graded process artefact.
3. **Rename the GitHub repo** to match the project title — `Online-Examination-Portal`. Old links
   redirect, so it is safe.
4. **Restore the README** Working agreements and Team sections.
5. **Withdraw `user_stories.md`** and decide the fate of `SRS_table.pdf`.
6. **Confirm the deadline** and whether Markdown-in-repo is acceptable or she wants Word/PDF.

## 6. Open questions still unanswered by the instructor

Three PRD §14 questions leave specific expected values in the test plan provisional — flagged in
its §8:

- **Negative-marking convention** — flat deduction or a fraction of the question's marks. The test
  plan assumes a **flat 0.5** (`UT_054`, `UT_056`, `IT_031`).
- **Pass-mark boundary** — the test plan assumes **inclusive**, so 40.0% against a 40% pass mark is
  a Pass (`UT_057`).
- **Submission format** — repo Markdown, or Word/PDF.

## 7. Separate track — do not confuse the two

The **SE Lab** work is a different scenario entirely: **Problem Statement #52, Community Tool &
Equipment Library**, individual, in repo `Kishi836/SE_PES1UG24CS240`. Lab 1 and Lab 2 are both
submitted. Outstanding there:

- **Live demo of the Lab 2 Jira workspace to the instructor** — required for full marks.
- Delete the stray auto-created sprint `Sprint 2 - Deposit Settlemen 2` first, so the board shows
  exactly two sprints.
- **New:** the teacher wants the Jira work replicated on GitHub — a real GitHub Project board with
  epics, stories and sprints, not just commits. Details not yet supplied.

See `..\Lab\Lab - 1\LAB1_STATUS.md` and `..\Lab\Lab - 2\LAB2_STATUS.md`.
