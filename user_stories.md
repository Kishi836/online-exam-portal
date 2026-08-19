## 1. Candidate / Student Stories

### US-01: Timed Exam Session & Navigation

> **As a** student,
> **I want to** navigate through MCQ questions with a visible countdown timer,
> **So that** I can pace myself and submit within the allocated time window.

- **Acceptance Criteria:**
    
    - Displays a persistent countdown timer on the screen.
    - Shows a question palette indicating: _Answered_, _Unanswered_, _Marked for Review_, and _Current Question_.
    - When the timer hits `00:00`, the exam auto-locks and submits the candidate's current responses automatically.
        

### US-02: Instant Result & Score Breakdown

> **As a** student,
> **I want to** see my evaluated score and breakdown immediately after submitting (if permitted by the instructor),
> **So that** I can understand my performance without waiting days for manual grading.

- **Acceptance Criteria:**
    
    - Displays overall score, percentage, and pass/fail status immediately upon submission.
    - Provides a section-wise breakdown (e.g., Data Structures, Algorithms).
    - Hides correct answer explanations if the instructor disabled post-exam review.
## 2. Instructor / Examiner Stories

### US-03: MCQ Question Bank Management

> **As an** instructor,
> **I want to** create, categorize, and tag multiple-choice questions with single or multiple correct options,
> **So that** I can build a reusable question pool for different tests.

- **Acceptance Criteria:**
    
    - Supports creating questions with 2 to 6 options.
    - Allows marking single-correct or multi-correct answers.
    - Supports rich text, code snippets, and optional image attachments in both question prompts and answer choices.
    - Supports bulk CSV/JSON upload for rapid question ingestion.
        

### US-04: Test Configuration & Grading Rules

> **As an** instructor,
> **I want to** configure test parameters such as duration, randomized question order, and negative marking,
> **So that** I can customize difficulty and prevent answer sharing among students.

- **Acceptance Criteria:**
    
    - Configurable positive points per correct answer and negative points for incorrect answers (e.g., +4 / -1).
    - Toggle for option shuffling per candidate.
    - Toggle for partial marking on multi-select questions.
        

## 3. Evaluation Engine & System Stories

### US-05: Automated MCQ Evaluation Engine

> **As the** system,
> **I want to** evaluate candidate submissions asynchronously upon completion,
> **So that** final scores are calculated accurately and scaled without server bottlenecks.

- **Acceptance Criteria:**
    
    - Applies negative marking formulas: $\text{Total Score} = (\text{Correct} \times \text{Marks}) - (\text{Incorrect} \times \text{Penalty})$.
    - Unanswered questions award `0` points and do not trigger negative marking.
    - Evaluation job completes within $\le 2$ seconds per submission.
        

### US-06: Basic Anti-Cheating & Focus Loss Tracker

> **As an** administrator,
> **I want to** log tab switching and full-screen exits during an active exam,
> **So that** we can flag suspicious attempts for review.

- **Acceptance Criteria:**
    
    - System detects when the browser window loses focus (`visibilitychange` / `blur` events).
    - Candidate gets a warning dialog on the 1st and 2nd tab switch.
    - On the 3rd violation, the exam auto-submits or flags the attempt as "Suspicious" in the instructor dashboard.
