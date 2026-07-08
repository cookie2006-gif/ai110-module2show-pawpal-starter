# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    My initial UML had five classes arranged around a simple pipeline: setup → input → output. `Owner` and `Pet` capture context, `Task` captures the work to be done, and `Scheduler` transforms tasks into a `DailyPlan`. An `Owner` has many `Pet`s, each `Pet` has many `Task`s, and the `Scheduler` consumes tasks plus the owner's time budget to produce one `DailyPlan` per day.

- What classes did you include, and what responsibilities did you assign to each?
    **`Owner`** — stores the user's name and daily time budget (the main scheduling constraint).
    **`Pet`** — stores name, species, age, and health notes; belongs to one `Owner`.
    **`Task`** — stores name, duration (minutes), priority (high/medium/low), type (walk/feed/med/grooming/enrichment), and optional preferred time window; belongs to one `Pet`.
    **`Scheduler`** — holds the scheduling logic: sorts tasks by priority, fits them into the time budget, resolves conflicts, and drops tasks that don't fit.
    **`DailyPlan`** — the output object: scheduled tasks with start times, skipped tasks with reasons, and total time used versus budget.

**b. Design changes**

- Did your design change during implementation?
    Yes.
- If yes, describe at least one change and why you made it.
    I originally planned to store the scheduled start time directly on the `Task` object. During implementation this got messy — the same `Task` needed different times on different days, and mutating it made tests unreliable. I introduced a small `ScheduledTask` wrapper (task reference + start time) that lives inside `DailyPlan`, keeping `Task` immutable as a pure definition. This let me generate multiple plans from the same task list without side effects and made the scheduler much easier to test.

    A second change came from an AI-assisted review of `pawpal_system.py`. The reviewer flagged that `ScheduledTask` only carried `(start_time, task)`, which meant a multi-pet owner could not tell which pet each scheduled task belonged to — `DailyPlan.summary()` would print "Walk 8:00" without saying whose walk. I extended `ScheduledTask` to also hold a `Pet` reference, and applied the same fix to `DailyPlan.skipped` (now `list[tuple[Pet, Task, str]]`) so skip reasons stay pet-attributed. At the same time I dropped the redundant `tasks` parameter from `Scheduler.build_plan()`: `Owner` already carries pets, and each pet carries its tasks, so a separate flat list was a second source of truth that could silently disagree with `owner.pets[*].tasks`. It also would have forced the flat list to lose the pet-of-origin — which was the root cause of the pet-linkage bug above. The signature is now `build_plan(owner: Owner) -> DailyPlan`, and the scheduler iterates pets → tasks internally, which is what preserves the pet linkage in the first place.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
