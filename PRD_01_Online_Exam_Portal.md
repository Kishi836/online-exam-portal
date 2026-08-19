# PRD-01: Online Examination Portal — Multiple-Choice Delivery & Automatic Evaluation

> **Product**: Online Examination System — Jackfruit semester project
> **Course**: UE23CS341A Software Engineering · Assessed for 40 marks
> **Author**: Team of 3 (see §15)
> **Version**: 1.0 | 19 August 2026 | Status: Draft for review
> **Tiers**: S (single course, <100 students) | M (department, <1,000) | L (institution, 5,000+) — see §3 for tier definitions and legend (● Mandatory ◐ Recommended ○ Optional)
> **Downstream**: the committed subset for this semester is in [`docs/01-requirements/M1_REQUIREMENTS.md`](docs/01-requirements/M1_REQUIREMENTS.md)

---

## 1. Problem Statement

Objective examinations in Indian colleges are still largely conducted on paper. A single internal
assessment for one section of 60 students consumes a full working day of faculty time: the paper is
typed and printed under secrecy, question papers and OMR sheets are physically secured and
distributed, invigilators collect and count scripts, and evaluation is done by hand or by feeding
sheets through a scanner that must itself be booked and calibrated. Results reach students three to
seven days later, by which point the teaching moment has passed.

The consequences compound. Manual evaluation introduces scoring errors that surface as grievances
weeks later, with no record of how the original mark was arrived at. Question papers are retyped
from scratch every semester because there is no shared bank, so faculty cannot reuse a good question
or retire a bad one. Re-examinations for absentees require a wholly new paper. And the entire
apparatus assumes physical co-presence — during any disruption to campus operations, objective
assessment simply stops.

The narrow, tractable version of this problem is **objective assessment**: multiple-choice questions
have a deterministic answer key, which means evaluation requires no human judgement at all and can be
performed by software in milliseconds with perfect consistency. This product addresses exactly that
scope, and deliberately does not attempt subjective evaluation.

## 2. Goals & Success Metrics

| Goal | Metric | Target |
|---|---|---|
| Eliminate manual evaluation | Faculty hours spent scoring an objective paper | 0 (from ~4 h per 60-student section) |
| Collapse result turnaround | Time from last submission to publishable result | <60 s (from 3–7 days) |
| Scoring correctness | Discrepancies between system score and independent recomputation | 0 across all attempts |
| No candidate loses work | Attempts losing a response to a crash, timeout or disconnection | 0 |
| Question reuse | Questions authored once and reused in a later examination | ≥60% of a paper by semester 2 of use |
| Paper-setting effort | Time to assemble a 60-question paper from an established bank | <15 min |
| Grievance resolution | Grievances resolvable from system records without physical script retrieval | 100% |
| Fair delivery | Candidates receiving an identical question order | 0 when shuffling is enabled |

## 3. Deployment Tiers

Requirements in §7 are marked against three deployment scales. **The semester deliverable targets
tier S**; M and L requirements document the product's intended growth path and are explicitly not
committed at M1.

| Tier | Deployment | Students | Peak concurrent attempts | Notes |
|---|---|---|---|---|
| **S** | Single course or section | <100 | ≤50 | The academic demonstration target |
| **M** | Department | <1,000 | ≤200 | Load target of NFR-P-01/04 |
| **L** | Institution-wide | 5,000+ | 1,000+ | Requires horizontal scaling and SSO; out of semester scope |

**Legend**: ● Mandatory · ◐ Recommended · ○ Optional

## 4. Stakeholders & Personas

| Persona | Role | Primary concern |
|---|---|---|
| **Student / Candidate** | Attempts examinations | That the timer is fair, that no answer is lost, and that the mark is explained |
| **Faculty / Examiner** | Authors questions, sets and schedules papers, publishes results | That paper-setting is fast, evaluation is automatic, and a bad question can be corrected after the fact |
| **Administrator** | Manages users, courses, enrollment and system policy | That only current members of the institution have access, and that every action is auditable |
| **Head of Department** | Owns assessment policy | That the portal enforces departmental rules (pass mark, negative marking) rather than imposing its own |
| **Examination cell** | Holds the official record | That results export cleanly into institutional records and are retained for the statutory period |
| **Institution / Data Fiduciary** | Legally accountable for student data | Compliance with the DPDP Act 2023 and with examination-records retention policy |
| **Development team (3)** | Builds and demonstrates the system | A scope that is buildable, testable and demonstrable within one semester |

## 5. Scope

**In scope**: role-based accounts for Student, Faculty and Administrator · course and enrollment
management · a reusable multiple-choice question bank with topic and difficulty tagging ·
examination authoring, both manual and auto-generated · scheduling within a fixed window ·
server-timed attempt delivery with autosave, palette navigation, resume-after-disconnection and
auto-submission · deterministic automatic evaluation with configurable negative marking and partial
credit · post-hoc answer-key correction with bulk re-evaluation · result publication, scorecards and
answer review · cohort statistics · automated integrity event logging and flagging · an append-only
audit trail · CSV export of results.

**Out of scope**: descriptive or subjective answers and any form of manual grading · rubrics and
moderation workflows · webcam, screen-recording or AI proctoring · biometric or document-based
identity verification · payment collection · adaptive or item-response-theory testing · native
mobile applications · offline attempt mode · plagiarism detection · timetable generation ·
attendance management.

**Boundary note**: integrity monitoring in this product is *evidentiary, not judicial*. The system
records and flags; a human decides. This is a deliberate product position, restated as NFR-E-05.

## 6. User Stories

Eight epics, 36 stories, 178 story points. Summarised here; the full backlog with acceptance
criteria, point estimates and sprint assignment is in `docs/01-requirements/M1_REQUIREMENTS.md` §5.

1. As a **Student**, I want to register with my institutional email and roll number so that I am identified as a genuine candidate of my college. *(Epic 1)*
2. As **any user**, I want to sign in and land on a dashboard appropriate to my role so that I only see what concerns me. *(Epic 1)*
3. As **Faculty**, I want to enroll my students into my course so that only my class can see and attempt my exams. *(Epic 2)*
4. As **Faculty**, I want to write multiple-choice questions tagged by topic and difficulty so that I build a reusable bank instead of retyping papers every semester. *(Epic 3)*
5. As **Faculty**, I want to assemble a paper by picking from the bank — or by stating how many easy, medium and hard questions I need per topic and letting the system pick — so that setting a paper takes minutes. *(Epic 4)*
6. As **Faculty**, I want to schedule an exam for a fixed window and publish it so that students know exactly when they may attempt it. *(Epic 4)*
7. As a **Student**, I want a countdown timer and a palette showing what I have answered, skipped or marked for review so that I can manage my time across the paper. *(Epic 5)*
8. As a **Student**, I want every answer saved the moment I select it, and my attempt resumable with time intact after a disconnection, so that a network problem never becomes an academic penalty. *(Epic 5)*
9. As **Faculty**, I want each student to receive a different question and option order so that copying from a neighbouring screen gains nothing. *(Epic 5)*
10. As **Faculty**, I want every submitted paper scored automatically against the answer key so that I never evaluate an objective paper by hand again. *(Epic 6)*
11. As **Faculty**, I want to correct a wrong answer key after the exam and have every affected paper re-scored automatically so that one bad key does not mean re-evaluating the whole class. *(Epic 6)*
12. As a **Student**, I want my scorecard with per-question marks and an answer review so that the exam teaches me something after it ends. *(Epic 7)*
13. As **Faculty**, I want class statistics and per-question correct-answer rates so that I can tell which questions were bad rather than which students were weak. *(Epic 7)*
14. As **Faculty**, I want tab-switching logged and excessive violations flagged for my review so that I decide on malpractice, not the software. *(Epic 8)*
15. As an **Administrator**, I want every score change recorded with who changed it and what it was before so that any grievance is settled from the record. *(Epic 8)*

## 7. Functional Requirements

Requirement identifiers are **module-prefixed** rather than flat, because this product carries 74
requirements across 11 modules and a flat sequence would not survive later insertion. The same
identifiers are used unchanged in M1, in the SRS and in the RTM, giving a single traceability space
from this document through to test cases.

### 7.1 Module A — User Management & Authentication

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-AUTH-01 | Student self-registration: name, institutional email, roll number, password | ● | ● | ● |
| FR-AUTH-02 | Email verification link before account activation | ◐ | ● | ● |
| FR-AUTH-03 | Email/password authentication with session establishment | ● | ● | ● |
| FR-AUTH-04 | Account lockout: 5 failed attempts in 15 min → 15 min lock | ● | ● | ● |
| FR-AUTH-05 | Password reset by single-use, 15-minute email link | ● | ● | ● |
| FR-AUTH-06 | Role-based access control — Student, Faculty, Administrator — enforced on every screen and endpoint | ● | ● | ● |
| FR-AUTH-07 | One active session per Student; new login invalidates the previous | ● | ● | ● |
| FR-AUTH-08 | Self-service profile edit, excluding role and roll number | ◐ | ● | ● |
| FR-AUTH-09 | 30-minute idle session timeout, suspended during an active attempt | ◐ | ● | ● |
| FR-AUTH-10 | Administrator creates, deactivates and reactivates accounts | ● | ● | ● |

### 7.2 Module B — Course & Enrollment Management

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-CRS-01 | Course master: code, title, semester; create, edit, archive | ● | ● | ● |
| FR-CRS-02 | Assign one or more Faculty to a Course | ● | ● | ● |
| FR-CRS-03 | Individual student enrollment into a Course | ● | ● | ● |
| FR-CRS-04 | Enrollment gates examination visibility and attempt eligibility | ● | ● | ● |
| FR-CRS-05 | Bulk CSV import of students and enrollments, all-or-nothing with per-row reporting | ◐ | ● | ● |

### 7.3 Module C — Question Bank Management

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-QB-01 | Single-correct MCQ: stem, 2–6 options, exactly one correct | ● | ● | ● |
| FR-QB-02 | Multiple-correct question (MSQ) with two or more correct options | ◐ | ● | ● |
| FR-QB-03 | True/False question as a two-option MCQ | ◐ | ● | ● |
| FR-QB-04 | Mandatory metadata: course, topic, difficulty (Easy/Medium/Hard), positive marks, negative marks | ● | ● | ● |
| FR-QB-05 | Immutability of questions in published or attempted exams; edits create a new version | ● | ● | ● |
| FR-QB-06 | Bulk CSV import against a defined template, rejecting the file if any row is invalid | ◐ | ● | ● |
| FR-QB-07 | Search and filter by course, topic, difficulty and stem keyword | ● | ● | ● |
| FR-QB-08 | Faculty scoped to questions of their assigned courses only | ● | ● | ● |
| FR-QB-09 | Optional per-question explanation, shown during post-result review | ○ | ◐ | ● |
| FR-QB-10 | Student-view preview of a question | ○ | ◐ | ● |

### 7.4 Module D — Examination Authoring

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-EX-01 | Examination master: title, course, duration, declared total marks, instructions | ● | ● | ● |
| FR-EX-02 | Manual question selection from the bank | ● | ● | ● |
| FR-EX-03 | Auto-generation of a paper from per-topic, per-difficulty question counts | ◐ | ● | ● |
| FR-EX-04 | Publication blocked when computed marks ≠ declared total | ● | ● | ● |
| FR-EX-05 | Per-exam policy: negative marking, question shuffle, option shuffle, backward navigation, pass mark | ● | ● | ● |
| FR-EX-06 | Draft → Published lifecycle; only published exams visible to Students | ● | ● | ● |
| FR-EX-07 | Question set frozen once the window opens or any attempt exists | ● | ● | ● |
| FR-EX-08 | Clone an existing examination into a new draft | ○ | ◐ | ● |

### 7.5 Module E — Scheduling & Access Control

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-SCH-01 | Schedule a published exam with window start and end date-times | ● | ● | ● |
| FR-SCH-02 | Reject a window shorter than the exam duration | ● | ● | ● |
| FR-SCH-03 | Student dashboard of Upcoming, Live and Completed exams | ● | ● | ● |
| FR-SCH-04 | Attempt start gated on server time, enrollment and absence of a prior submission | ● | ● | ● |
| FR-SCH-05 | Configurable late-entry cutoff, default 15 min after window start | ◐ | ● | ● |
| FR-SCH-06 | Reschedule or cancel before the window opens | ◐ | ● | ● |
| FR-SCH-07 | Per-student additional-time allowance (accessibility) | ◐ | ● | ● |

### 7.6 Module F — Examination Delivery

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-ATT-01 | Attempt record stamped with server start time, created before the paper is delivered | ● | ● | ● |
| FR-ATT-02 | Countdown timer derived from server clock, never the client clock | ● | ● | ● |
| FR-ATT-03 | One question at a time with a four-state navigation palette | ● | ● | ● |
| FR-ATT-04 | Select, change and clear a response before submission | ● | ● | ● |
| FR-ATT-05 | Autosave every response to the server within 5 s, with no explicit save action | ● | ● | ● |
| FR-ATT-06 | Mark for review, and unmark | ◐ | ● | ● |
| FR-ATT-07 | Auto-submission at zero remaining time, retaining persisted responses | ● | ● | ● |
| FR-ATT-08 | Resume an interrupted attempt with original remaining time and restored responses | ● | ● | ● |
| FR-ATT-09 | Pre-submission confirmation summary of answered / unanswered / marked counts | ◐ | ● | ● |
| FR-ATT-10 | Per-student question and option ordering, stored with the attempt for exact reconstruction | ● | ● | ● |
| FR-ATT-11 | Rejection of a second concurrent attempt of the same exam | ● | ● | ● |

### 7.7 Module G — Automatic Evaluation & Scoring

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-EVL-01 | Fully automatic evaluation on submission, no human intervention | ● | ● | ● |
| FR-EVL-02 | Full marks for a correct single-correct response; configured deduction for an incorrect one | ● | ● | ● |
| FR-EVL-03 | Zero marks and no negative marking for unattempted questions | ● | ● | ● |
| FR-EVL-04 | MSQ scoring: full marks only on exact set match, otherwise the configured partial-credit rule | ◐ | ● | ● |
| FR-EVL-05 | Total, percentage and Pass/Fail against the configured pass mark | ● | ● | ● |
| FR-EVL-06 | Evaluation of a 100-question attempt completed within 5 s | ● | ● | ● |
| FR-EVL-07 | Post-exam answer-key correction with bulk re-evaluation and before/after audit entries | ◐ | ● | ● |
| FR-EVL-08 | Post-exam question drop with re-evaluation excluding the dropped question | ◐ | ● | ● |
| FR-EVL-09 | Raw responses retained so any published score can be recomputed and justified | ● | ● | ● |

### 7.8 Module H — Results & Answer Review

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-RES-01 | Results withheld from Students until Faculty publishes | ● | ● | ● |
| FR-RES-02 | Faculty publish and unpublish results per examination | ● | ● | ● |
| FR-RES-03 | Student scorecard: total, percentage, Pass/Fail, per-question marks | ● | ● | ● |
| FR-RES-04 | Answer review with own response, correct option(s) and explanation, when enabled | ◐ | ● | ● |
| FR-RES-05 | Cohort statistics: mean, median, highest, lowest, pass %, per-question correct rate | ◐ | ● | ● |
| FR-RES-06 | CSV export of examination results | ● | ● | ● |
| FR-RES-07 | Student scorecard download as PDF | ○ | ◐ | ● |
| FR-RES-08 | Student answer-key challenge within a configurable window, default 48 h | ○ | ◐ | ● |
| FR-RES-09 | Faculty review of a challenge; acceptance triggers FR-EVL-07 | ○ | ◐ | ● |

### 7.9 Module I — Examination Integrity

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-INT-01 | Timestamped logging of every focus-loss event during an active attempt | ● | ● | ● |
| FR-INT-02 | Warning per event; auto-submission beyond a configurable threshold, default 3 | ◐ | ● | ● |
| FR-INT-03 | Copy, paste and context menu disabled within the examination screen | ◐ | ● | ● |
| FR-INT-04 | Attempts exceeding the violation threshold flagged to Faculty with the supporting event log | ◐ | ● | ● |
| FR-INT-05 | IP address and user-agent recorded per attempt | ◐ | ● | ● |
| FR-INT-06 | Distinct per-student question and option ordering when shuffling is enabled | ● | ● | ● |
| FR-INT-07 | Correct-answer data excluded from every payload served during an active attempt | ● | ● | ● |

### 7.10 Module J — Notifications

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-NTF-01 | Email to enrolled students when an examination is scheduled | ◐ | ● | ● |
| FR-NTF-02 | Email to affected students when results are published | ◐ | ● | ● |
| FR-NTF-03 | In-application notification centre | ○ | ◐ | ● |

### 7.11 Module K — Administration & Audit

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-ADM-01 | Audit entry — actor, action, entity, timestamp, changed values — on every mutation of users, questions, exams, keys and results | ● | ● | ● |
| FR-ADM-02 | Administrator view of the audit log, filterable by actor, entity type and date range | ◐ | ● | ● |
| FR-ADM-03 | System-wide configurable defaults: session timeout, lockout policy, late-entry cutoff, violation threshold | ◐ | ● | ● |
| FR-ADM-04 | Administrator dashboard: users by role, exams by state, attempts today | ○ | ◐ | ● |

### 7.12 Module L — Scale & Integration *(product roadmap — not committed at M1)*

| # | Requirement | S | M | L |
|---|---|---|---|---|
| FR-SYS-01 | Institutional single sign-on via SAML 2.0 or OIDC against the campus identity provider | ○ | ◐ | ● |
| FR-SYS-02 | LTI 1.3 integration so examinations launch from within the institutional LMS | ○ | ○ | ● |
| FR-SYS-03 | Horizontal scaling of the application tier behind a load balancer, with a shared session store | ○ | ○ | ● |
| FR-SYS-04 | Item analysis: per-question difficulty index and discrimination index computed across cohorts | ○ | ◐ | ● |
| FR-SYS-05 | Multi-language rendering of question stems and interface strings | ○ | ○ | ◐ |

**Requirement counts** — committed (Modules A–K): 74 · roadmap (Module L): 5 · **total 79**.

## 8. Non-Functional Requirements

Classified per the course taxonomy as **Product**, **Organisational** and **External**. Each carries a
measure so that it is verifiable rather than aspirational; full verification methods are in
M1 §3.

| Area | Class | Requirement |
|---|---|---|
| Speed | Product | 95% of responses within 2 s at 200 concurrent attempts; autosave round trip within 1 s; evaluation of a 100-question attempt within 5 s |
| Capacity | Product | ≥200 concurrent attempts (M tier) and a bank of ≥50,000 questions without breaching the speed target |
| Reliability | Product | ≤1 attempt in 1,000 failing through system fault |
| Availability | Product | ≥99.5% across the total duration of published examination windows |
| Robustness | Product | Service restored within 60 s of an unplanned restart; every in-progress attempt resumable with responses intact and correct remaining time; zero probability of a partially written submission |
| Ease of use | Product | Unaided mock attempt after ≤5 min orientation; ≥90% task success across 10 test users; every screen within 3 clicks of the dashboard |
| Portability | Product | Latest two versions of Chrome, Edge and Firefox on Windows, macOS and Linux; usable at ≥360 px viewport width; ≤5% browser-specific front-end code |
| Maintainability | Product | ≥70% unit-test line coverage of evaluation and scoring; cyclomatic complexity ≤10 per function |
| Process | Organisational | Scrum, 2-week sprints, all ceremony artefacts committed; feature branches only, every merge peer-reviewed; no direct commits to `main` |
| Documentation | Organisational | SRS per IEEE Std 830-1998; RTM updated every phase; UML use-case, class and sequence diagrams before the corresponding implementation |
| Quality gates | Organisational | Linter in CI with build-breaking failures; every Must-priority FR linked to at least one functional test case in the RTM; tagged demonstrable increment each sprint |
| Privacy | External | DPDP Act 2023 — consent at registration, purpose limitation, erasure within 30 days of request |
| Retention | External | Responses and results retained ≥3 years per examination-records policy, then purged |
| Accessibility | External | WCAG 2.1 Level AA — full keyboard operability of the attempt flow, ≥4.5:1 contrast, labelled option controls |
| Interoperability | External | Results exportable as LMS-importable CSV; question bank importable and exportable as CSV |
| Ethics | External | Violation flags are advisory evidence for a human decision; the system never declares malpractice or voids a result on its own |
| Configurability | External | Window, pass mark, negative marking, late entry and violation threshold configurable at run time, never hard-coded |
| Environment | External | Deployable within the speed target on a single 2 vCPU / 4 GB Linux virtual machine |

## 9. Security, Regulatory & Compliance Requirements

Security requirements are derived through a Security Risk Assessment — assets and stakeholders,
threats and attackers, risk categorisation, SMART objectives — set out in full in M1 §4. The
highest-rated risks and their controls:

| Risk | Rating | Control |
|---|---|---|
| Correct answers read from the client payload during an attempt | **High** | SEC-03: answer keys and explanations excluded from every Student-role payload while an attempt is active |
| Score altered by direct API call or payload tampering | **High** | SEC-10: all scoring server-side from stored responses; client-supplied scores rejected |
| Another candidate's attempt or result reached by changing an identifier | **High** | SEC-04: server-side authorisation on every request, verifying role *and* resource ownership |
| Paper or key retrieved before the window opens | **High** | SEC-09: questions inaccessible to Students pre-window, keys inaccessible until publication |
| SQL injection or stored XSS through a question stem | **High** | SEC-06 parameterised queries only; SEC-07 output encoding and Content-Security-Policy |
| Credential theft leading to impersonation | Medium | SEC-01 Argon2id/bcrypt(≥12) hashing; SEC-05 lockout after 5 failures in 15 min |
| Session hijacking | Medium | SEC-08: ≥128-bit tokens, HttpOnly, Secure, SameSite=Strict, rotated on login; SEC-02 TLS 1.2+ |
| Personal-data breach | Medium | SEC-12: AES-256 at rest, encrypted backups |
| Denial of service during a window | Medium | SEC-13: 100 requests/min per session rate limit |
| Insider score modification without trace | Medium | SEC-11: append-only audit log, not editable by any role including Administrator |

| Instrument | Obligation | Where addressed |
|---|---|---|
| **Digital Personal Data Protection Act, 2023** | Consent, purpose limitation, erasure on request, breach notification; the institution is the Data Fiduciary | NFR-E-01, SEC-12; consent captured at FR-AUTH-01 |
| **Institutional examination-records policy** | Answer scripts and results retained for the statutory period before purge | NFR-E-02 |
| **UGC / university examination regulations** | Documented evaluation procedure, a defined grievance route, and reproducibility of any declared mark | FR-EVL-09, FR-RES-08/09, FR-ADM-01 |
| **Rights of Persons with Disabilities Act, 2016** | Reasonable accommodation in examinations, including compensatory time | FR-SCH-07, NFR-E-03 |
| **WCAG 2.1 Level AA** | Accessible delivery of the attempt interface | NFR-E-03 |
| **OWASP ASVS L1** | Baseline application security verification for an internet-facing system | SEC-01 to SEC-14, SO-5 |

## 10. Data & Integration Architecture

**Core entities**: `User` (with role) · `Course` · `Enrollment` (User ↔ Course) · `Question`
(versioned, owning its `Option` set and correct-answer flags) · `Exam` (owning an ordered
`ExamQuestion` set and its policy configuration) · `Schedule` (window) · `Attempt` (owning the
per-student question and option ordering) · `Response` (Attempt ↔ Question ↔ selected options) ·
`Result` (computed, publishable) · `IntegrityEvent` · `AuditEntry` (append-only).

**Design positions that follow from the requirements**:

- **The answer key never crosses the client boundary during an attempt.** The paper served to a
  candidate is a projection of `Question` that omits correctness flags entirely (FR-INT-07, SEC-03).
- **Time is server-owned.** `Attempt.started_at` is the single source of truth for remaining time;
  the client renders a countdown but never determines expiry (FR-ATT-02, FR-ATT-08).
- **Scoring is a pure function** of (`Response` set, `Question` key set, `Exam` policy). It holds no
  state of its own, which is what makes re-evaluation after a key correction (FR-EVL-07) a simple
  re-invocation rather than a repair, and what makes it independently testable to the 70% coverage
  bar of NFR-P-12.
- **Question immutability under use.** A question referenced by a published or attempted exam is
  copy-on-write versioned (FR-QB-05), so a historical attempt always reconstructs exactly.
- **The audit log is append-only** at the storage layer, not merely by convention (SEC-11).

**Integration surfaces**: CSV in for students, enrollments and questions · CSV out for results, in a
schema agreed with the examination cell · SMTP out for notifications · SAML 2.0 / OIDC and LTI 1.3
are roadmap surfaces (FR-SYS-01, FR-SYS-02), deliberately not built at S tier.

**Deliberate technology non-decision**: the implementation stack is not fixed in this PRD, because a
requirement states *what*, not *how*. Binding constraints only: a browser-reachable web application
over HTTPS, a relational store (scoring, enrollment and audit are inherently relational), and
deployability on the 2 vCPU / 4 GB demonstration VM. The stack is chosen in Sprint 0 and recorded as
an addendum under change control.

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Concurrency defects surface only under load, late in the semester | Demo fails at the worst moment | Load-test from Sprint 3, not at the end; NFR-P-01/04 have explicit numeric targets to test against |
| Candidate loses answers to a disconnection | Directly breaches the product's central promise | Autosave within 5 s (FR-ATT-05) plus server-side resume (FR-ATT-08); fault-injection test in NFR-P-07 |
| Client-side timer trusted by mistake during implementation | Candidates gain or lose time; exam invalid | Timer requirement written as server-derived (FR-ATT-02); explicit test case in the RTM |
| Answer key leaks through an over-broad API response | Exam integrity destroyed, unrecoverable | SEC-03 plus SO-1: automated response-inspection suite asserting zero key fields, run in CI |
| Auto-generation algorithm (FR-EX-03) proves harder than estimated | Sprint 3 overruns | Marked Should; the manual selection path (FR-EX-02) fully satisfies the demo without it |
| Scope creep toward proctoring | Semester lost to computer vision | Explicitly out of scope in §5; no proctor actor exists in the model |
| Three-person team, uneven availability during internals | Sprint commitments missed | Documented ownership areas (§15), peer review on every PR, Should/Could items as the release valve |
| Answer-key challenge flow (FR-RES-08/09) squeezed in Sprint 4 | Incomplete feature at demo | Designated scope-release valve; dropping it affects no Must requirement |

## 12. Phased Rollout

Phases map directly onto sprints; each ends with a tagged, demonstrable increment (NFR-O-06).

1. **Phase 1 — Foundation** *(Sprint 1)*: Modules A and B. Accounts, RBAC, courses, enrollment.
   Demonstrable: three roles sign in and see different dashboards.
2. **Phase 2 — Authoring** *(Sprint 2)*: Modules C and D, plus scheduling (E). Question bank, paper
   assembly, publication. Demonstrable: a faculty member sets and schedules a real paper.
3. **Phase 3 — Delivery** *(Sprint 3)*: Modules F and I. Attempt experience, autosave, resume,
   shuffling, integrity logging. Demonstrable: a candidate sits a paper and survives a forced
   disconnection. Load testing begins here.
4. **Phase 4 — Evaluation & Results** *(Sprint 4)*: Modules G, H, J and K. Automatic scoring,
   re-evaluation, publication, scorecards, statistics, audit. Demonstrable: end-to-end, from paper
   set to result published.
5. **Phase 5 — Roadmap** *(not committed)*: Module L. SSO, LTI, horizontal scaling, item analysis.

## 13. Prerequisites & External System Dependencies

> **Legend**: 🔴 Required · 🟡 Integrates if present (degraded mode defined) · ⚪ Optional

| Dependency | Type | If absent |
|---|---|---|
| Hosting VM (2 vCPU / 4 GB Linux) | 🔴 | No deployment; local-only demonstration, which weakens the availability and load evidence |
| TLS certificate for the deployment host | 🔴 | SEC-02 unmet; the system must not carry credentials or answer keys over plain HTTP |
| NTP-synchronised server clock | 🔴 | Every timing rule (FR-ATT-02, FR-SCH-04) becomes unreliable |
| SMTP relay | 🟡 | Notifications (FR-NTF-01/02) and email verification (FR-AUTH-02) degrade to in-app only; account activation falls back to Administrator approval |
| Institutional student/course data | 🟡 | Administrator seeds accounts and enrollments by CSV (FR-CRS-05) instead of a feed |
| Institutional LMS | 🟡 | Results delivered as CSV export (FR-RES-06) for manual upload rather than direct integration |
| Campus identity provider (SAML/OIDC) | ⚪ | Local password authentication (FR-AUTH-03) is fully self-contained; SSO is roadmap only |
| Candidate devices with a supported browser | 🔴 | Out of the system's control; stated as an assumption, mitigated by the ≥360 px and cross-browser requirements |

**Bottom line**: the product has **no hard dependency on any existing institutional system**. It is
self-contained at tier S — a VM, a certificate and a synchronised clock. SMTP and LMS integration
improve it; neither gates go-live.

## 14. Open Questions

- Which negative-marking convention does the department actually use — a flat deduction per wrong
  answer, or a fraction of the question's marks? FR-EX-05 supports both; the default needs a decision.
- Should a candidate who exhausts the violation threshold have the attempt auto-submitted (current
  FR-INT-02) or merely flagged? Auto-submission is the stricter reading and the more contestable one.
- What is the institution's actual retention period for objective answer scripts — the 3 years
  assumed in NFR-E-02 is a placeholder pending the examination cell's confirmation.
- Is the demonstration expected on institutional infrastructure or on a self-provisioned VM? This
  determines whether NFR-E-07 is a constraint or merely a budget.
- For MSQ partial credit (FR-EVL-04), which rule — proportional to correct options selected, or
  all-or-nothing with no partial credit? Affects the scoring engine's test matrix.

## 15. Team & Ownership

| Member | Role | Owns |
|---|---|---|
| Member 1 | Backend & data lead | Schema, authentication and RBAC, attempt lifecycle, evaluation engine, audit log, unit tests |
| Member 2 | Frontend & UX lead | Attempt interface, palette and timer, faculty authoring screens, accessibility (NFR-E-03), usability testing |
| Member 3 | QA, docs & delivery lead | SRS and RTM, UML diagrams, test plan and cases, CI and linting, load and security testing, sprint artefacts, demo script |

All three review every pull request (NFR-O-02) and share the sprint ceremonies and the final viva.

---

## Document Control

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 19 Aug 2026 | Initial PRD — problem, goals, tiers, 79 requirements, NFRs, security, rollout | Team |

Changes to a baselined requirement are raised as a change request, assessed for impact on scope,
schedule and the RTM, and recorded in [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
