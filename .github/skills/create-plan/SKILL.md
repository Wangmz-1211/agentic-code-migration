---
name: create-plan
description: A meta-skill used by the Orchestrator to break down complex, large-scale migration requests into a structured, autonomous execution plan. It groups independent targets into parallel batches and defines the exact routing specifications (skill and executor tier) required for each task.
---

# Skill: create-plan

## Description
A meta-skill used by the Orchestrator to break down complex, large-scale migration requests into a structured, autonomous execution plan. It groups independent targets into parallel batches and defines the exact routing specifications (skill and executor tier) required for each task.

## Prerequisites
The user must provide:
1. A raw list of target files or directories.
2. An overarching goal or context for the migration.
3. (Optional) Hints regarding required skills or custom routing constraints.

---

## Execution Plan (Orchestrator Instructions)

When invoked with `create-plan`, you must act purely as a Planner. Do NOT dispatch any Executors yet. Follow these steps sequentially:

### Step 1: Analyze and Decompose
Review the user's provided target files and hints. Break the overall goal down into file-level (or directory-level) tasks. 
* Identify which `skill` is required for each task.
* Determine the appropriate Executor tier (`Executor` for simple tasks, `Executor - Pro` for complex or multi-pass tasks).

### Step 2: Formulate Batches (Parallelism Strategy)
Group the decomposed tasks into Execution Batches (`batch_id`). 
* **Rule of Independence:** All tasks sharing the same `batch_id` MUST be fully independent and capable of running in parallel without race conditions. 
* Tasks with dependencies must be placed in sequentially higher `batch_id`s.

### Step 3: Flag Ambiguities
If any task lacks sufficient context to determine the correct skill or routing, or involves high-risk global state changes, set its status to `needs_review`. Use `vscode/askQuestion` to present these specific blockers to the user.

### Step 4: Generate the Plan Document
Create or update a tracking document (e.g., `migration-plan.md`) in the workspace root or a designated `.github/plans/` directory. You MUST strictly use the following Markdown table structure for the plan:

```markdown
# Migration Execution Plan
**Goal:** [Brief summary of the overall task]
**Status Tracking:** The Orchestrator must update the `Status` column after each batch execution.

| Task ID | Batch ID | Target File/Scope | Assigned Skill | Routing Spec | Status | Notes / Review Reason |
|---------|----------|-------------------|----------------|--------------|--------|-----------------------|
| T-01    | 1        | src/.../A.java    | web-dto        | Executor     | queued | Ready                 |
| T-02    | 1        | src/.../B.java    | web-dto        | Executor     | queued | Ready                 |
| T-03    | 2        | src/.../Core.java | db-migration   | Executor Pro | needs_review | Confirm DB dialect? |

```

### Step 5: Finalize

Report `completed` to the user and present the generated Markdown plan. Stop execution. Wait for the user to approve the plan or resolve `needs_review` items before actually beginning `Batch 1`.

---

## Hard Boundaries

* **No Execution:** This skill is strictly for planning. Do not dispatch file-level tasks to Executors while running this skill.
* **Strict Status Enum:** Use ONLY `queued`, `in_progress`, `completed`, `needs_review`, `blocked`, or `failed` in the Status column. Do not invent new statuses like "pending" or "done".