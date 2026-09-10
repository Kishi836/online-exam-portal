# Use Case Flows — Online Examination Portal

Companion document to the PlantUML use case diagram. Each use case below is written in
standard IEEE-style flow-of-events format (Preconditions, Basic Flow, Alternate Flows,
Exception Flows, Postconditions) so it can be dropped directly into the M2 SRS.

---

## UC-1: Attempt Timed Exam
**Primary Actor:** Student
**Related use cases included/extended:** Navigate via Question Palette, Autosave Responses,
Mark Question for Review, Resume After Disconnection, Submit Exam

**Preconditions**
- Student is authenticated and enrolled in the course/exam.
- Current time falls within the scheduled exam window.
- Student has not already submitted this attempt.

**Basic Flow**
1. Student selects the scheduled exam from "View Scheduled Exams."
2. System validates the exam window and starts a server-side timer for the configured duration.
3. System renders the first question and the question palette (Answered / Unanswered / Marked
   for Review / Current Question).
4. Student selects an answer option(s) for the current question.
5. System records the response and autosaves it to the server (`<<include>> Autosave Responses`).
6. System updates the palette status for that question to "Answered."
7. Student navigates to the next/previous question via the palette or Next/Previous controls.
8. Steps 4–7 repeat until the student has attempted all questions or chooses to submit.
9. Student clicks "Submit Exam."
10. System executes UC-2 (Submit Exam).

**Alternate Flows**
- **A1 — Mark for Review:** At step 4, student marks the question for review instead of (or in
  addition to) answering. System sets palette status to "Marked for Review" (or "Answered +
  Marked for Review"). Flow resumes at step 7.
- **A2 — Resume After Disconnection:** If the student's session drops (network loss, browser
  crash, tab closed), the timer continues server-side. On re-authentication within the exam
  window, system restores the last autosaved state (question position, all responses, palette
  status) and resumes the countdown from the correct remaining time. Flow resumes at step 4.
- **A3 — Option Shuffling Active:** If the faculty enabled per-candidate option shuffling
  (US-04), system renders options in a candidate-specific randomized order at step 3, while
  preserving the correct-answer mapping internally.

**Exception Flows**
- **E1 — Timer Expires (00:00):** At any point in steps 4–8, if the countdown reaches zero,
  system immediately locks all inputs and auto-submits the current response set
  (`<<extend>> Auto-Submit on Timer Expiry`). Flow proceeds to UC-2 without student action.
- **E2 — Third Focus-Loss Violation:** If UC-6 (Monitor Focus Loss) reports a 3rd violation
  during the attempt, system either force-submits the attempt or flags it as "Suspicious"
  (per faculty configuration) and proceeds to UC-2.
- **E3 — Autosave Failure:** If autosave fails (e.g., transient network error), system retries
  with backoff and displays a non-blocking "reconnecting" indicator; student may continue
  answering locally until connectivity is restored. If unresolved by end of exam window, E1
  applies.

**Postconditions**
- All responses are persisted server-side.
- Exam attempt status transitions to "Submitted" and is queued for evaluation (UC-3).

---

## UC-2: Submit Exam
**Primary Actor:** Student (or System, on timeout/violation)

**Preconditions**
- An exam attempt is in progress (UC-1).

**Basic Flow**
1. Actor triggers submission (manual click, timer expiry, or violation threshold).
2. System displays a confirmation prompt summarizing answered/unanswered/marked-for-review
   counts (manual submission only).
3. Student confirms submission.
4. System freezes the response set, stops the timer, and marks the attempt as "Submitted"
   with a server-side timestamp.
5. System dispatches the attempt to the Evaluation Engine (UC-3) asynchronously.
6. System displays a submission acknowledgment to the student.

**Alternate Flows**
- **A1 — Auto-Submit (no confirmation):** For timer expiry or violation-triggered submission,
  step 2–3 are skipped; system submits immediately and notifies the student that the exam was
  auto-submitted and why.

**Postconditions**
- Attempt is immutable and queued for grading.

---

## UC-3: Automated MCQ Evaluation
**Primary Actor:** Evaluation Engine (System)
**Related:** Submit Exam (trigger), Apply Negative Marking Formula (include)

**Preconditions**
- An attempt has status "Submitted."
- An answer key exists for every question in the paper.

**Basic Flow**
1. System dequeues the submitted attempt from the evaluation queue.
2. For each question, system compares the candidate's selected option(s) against the stored
   answer key.
3. System applies the configured grading rule per question:
   - Correct → `+marks`
   - Incorrect → `-penalty` (if negative marking enabled)
   - Unanswered → `0`, no penalty
4. For multi-select questions, system applies partial-marking rules if enabled by faculty.
5. System aggregates section-wise and overall scores, and computes percentage and pass/fail
   status against the configured cutoff.
6. System persists the scorecard and marks the attempt "Evaluated."
7. System completes the evaluation within ≤2 seconds of dequeue (NFR).

**Alternate Flows**
- **A1 — Results Not Yet Published:** Evaluation completes and is stored, but is not shown to
  the student until faculty explicitly publishes results (UC-7).

**Exception Flows**
- **E1 — Missing/Ambiguous Answer Key:** If a question lacks a valid answer key at evaluation
  time, system flags the attempt as "Evaluation Error" and notifies faculty; does not block
  evaluation of the remaining questions.

**Postconditions**
- Scorecard (overall, section-wise, per-question) exists and is ready for publication.

---

## UC-4: Create & Configure MCQ Question
**Primary Actor:** Faculty
**Related:** Tag & Categorize Questions (include), Bulk Upload Questions (extend)

**Preconditions**
- Faculty is authenticated with question-authoring permissions.

**Basic Flow**
1. Faculty opens the Question Bank and selects "Create Question."
2. Faculty enters the question prompt (rich text, optional code snippet/image).
3. Faculty adds 2–6 answer options (rich text, optional images).
4. Faculty marks one or more options as correct (single- or multi-correct).
5. Faculty assigns tags/categories (e.g., topic, difficulty, course).
6. System validates the question (minimum options, at least one correct answer marked).
7. System saves the question to the reusable question bank.

**Alternate Flows**
- **A1 — Bulk Upload:** Instead of steps 2–6, faculty uploads a CSV/JSON file of questions.
  System validates each record against the schema, imports valid records into the question
  bank, and reports validation errors for rejected records.

**Exception Flows**
- **E1 — Validation Failure:** If a question has fewer than 2 options, no correct answer
  marked, or malformed rich content, system rejects the save and displays field-level errors.

**Postconditions**
- Question is available for assembly into papers.

---

## UC-5: Configure Test & Schedule Exam
**Primary Actor:** Faculty
**Related:** Assemble Question Paper, Configure Negative Marking (include), Configure Option
Shuffling (include)

**Preconditions**
- Sufficient tagged questions exist in the bank for the target paper.

**Basic Flow**
1. Faculty assembles a paper manually (selecting questions) or automatically (by tag/difficulty
   quota).
2. Faculty sets duration, positive marks per question, and negative marking penalty (if any).
3. Faculty toggles option shuffling per candidate.
4. Faculty toggles partial marking for multi-select questions.
5. Faculty sets the exam window (start/end date-time) and enrolls the eligible student cohort.
6. System validates configuration (e.g., duration > 0, window in the future, paper non-empty).
7. System schedules the exam and notifies enrolled students.

**Exception Flows**
- **E1 — Invalid Window/Empty Paper:** System blocks scheduling and prompts faculty to correct
  the configuration.

**Postconditions**
- Exam is visible to enrolled students under "View Scheduled Exams" once the window opens.

---

## UC-6: Monitor Focus Loss & Flag Suspicious Attempt
**Primary Actor:** Administrator (rule owner) / System (detection)
**Related:** Log Tab Switch / Blur Event (include), Flag Suspicious Attempt (extend)

**Preconditions**
- A student's exam attempt is in progress (UC-1).

**Basic Flow**
1. Client detects a `visibilitychange` or `blur` event during the active attempt.
2. System logs the event with timestamp against the attempt.
3. On the 1st and 2nd occurrence, system displays a warning dialog to the student and
   increments the violation counter.
4. On the 3rd occurrence, system either auto-submits the attempt (E1 of UC-1) or flags the
   attempt as "Suspicious" — per the faculty/administrator's configured policy — and records
   the flag reason and event log.
5. Flagged attempts appear in the Administrator/Faculty review dashboard with the full event
   timeline.

**Alternate Flows**
- **A1 — Reviewer Overrides Flag:** Administrator or Faculty reviews the flagged attempt's
  evidentiary log and manually clears or upholds the flag; the system does not auto-invalidate
  a result — a human decides.

**Postconditions**
- Violation events are permanently logged and linked to the attempt for audit purposes.

---

## UC-7: Publish Results
**Primary Actor:** Faculty

**Preconditions**
- Attempt(s) have status "Evaluated" (UC-3).

**Basic Flow**
1. Faculty opens the results dashboard for a scheduled exam.
2. Faculty reviews cohort statistics (average, distribution, pass rate).
3. Faculty optionally reviews/clears any flagged attempts (UC-6, A1) before publishing.
4. Faculty toggles whether post-exam answer/explanation review is visible to students.
5. Faculty clicks "Publish Results."
6. System makes scorecards visible to the respective students (UC "View Score & Breakdown")
   and locks the answer key from further edits for that paper.

**Postconditions**
- Students can view their scores; visibility of correct-answer explanations matches the
  faculty's toggle setting.

---

### Traceability note
Each flow above maps to the corresponding `usecase` node in the PlantUML diagram
(`UC_AttemptExam`, `UC_Evaluate`, `UC_CreateQ`, `UC_ConfigTest`/`UC_ScheduleExam`,
`UC_MonitorFocus`/`UC_FlagAttempt`, `UC_PublishResults`) and can seed the RTM (Requirements
Traceability Matrix) referenced in `M1_REQUIREMENTS.md`.
