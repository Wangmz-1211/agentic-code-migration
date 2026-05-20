# Migration MAS Global Instructions
Minimal behavior rules. Do / Don't only. This applies to all agents in the workspace.

## 1. Delegation & Architecture
* **Strict Role Boundaries:** Delegate tasks strictly according to the active agent file's frontmatter (Orchestrator to Executors, Executors to Validator). Never cross lines or attempt another agent's role.
* **Isolated Verification:** Never self-verify. Executors must not run build tools or evaluate semantic-driven searches directly. All code validation is owned exclusively by the Validator.
* **Concurrency Control:** Never run two edit-capable agent invocations against the same file concurrently. Parallelism is permitted *only* across different files.
* **Contract Integrity:** Always pass the minimal structured contract using the standard `skill` parameter. If a dependency is missing, halt and return `blocked`.

## 2. Skills And Terminology
* **Authoritative Source:** The selected `skill` configuration (`<skill>/SKILL.md`) is the final authoritative migration contract. Never improvise rules or code heuristics outside of it.
* **Structured Rule Parsing:** Executors must read rules exclusively from `<skill>/reference/`. Validators must read validation rules exclusively from `<skill>/validate/` (including `config.yaml`, `prompts/`, and `scripts/`).
* **Language Policy:** Never allow any prompt's internal language-policy section to override the active workspace, agent, or caller language settings.

## 3. Editing & Context Discipline
* **Preserve Trivia:** Keep surrounding whitespace, comments, line endings, and trailing newlines exactly as they were in the original source file. Do not normalize untouched code.
* **Scope Localization:** Touch the smallest contiguous region possible. Never silently widen the edit scope into unrelated methods or files.
* **Long-File Strategy:** Prefer method-scoped or region-scoped actions over loading whole files. For multi-method targets, execute edits bottom-up: private helpers first, then public callers. Class-level modifications (imports, fields) must be handled in a dedicated pass.
* **Context Budget:** Minimize tokens by using lazy-loading. Load rule prompt bodies and validation sources *only* during active evaluation, and drop them from working memory immediately after.

## 4. Verification Sources & Logs
* **Validator Autonomy:** The Validator evaluates code soundness using only three valid sources: `build` tools, `script:<name>` executions, and `prompt:<path>` semantic-driven searches. 
* **Evidence Over Speculation:** Trust structured findings and build tool compiler diagnostics over speculative "already satisfied" conclusions.
* **Log Discipline:** Never dump full build logs or raw file dumps into reports. Enforce the per-rule finding cap (max 20) and total findings cap (max 100) strictly.

## 5. Loop Budget & Autonomy
* **No Mid-Batch Interruption:** Do not call `vscode/askQuestion` or prompt for human feedback in the middle of an active execution batch. 
* **Automated Loop Budgets:** * The Executor ↔ Validator edit loop is limited to a maximum of 5 cycles per file invocation. 
  * The Orchestrator batch retry policy is limited to a maximum of 3 total attempts per file path.
* **Escalation Protocol:** When an ambiguity or unresolvable error occurs, return `needs_review` with a precise issue and tentative recommendation. Orchestrator handles escalation via `custom_instructions` before final human deferral.