---
name: create-skill
description: A meta-skill to scaffold a new migration skill directory with standardized structure and content, based on the provided context (skill name, description). It ensures consistency and readiness for execution and validation by downstream agents.
---

# Skill: create-skill

## Description
A meta-skill used to scaffold a new, standardized migration skill directory within the MAS architecture. It copies the boilerplate structure from the `example` directory and hydrates it with the specific context (skill name, description, target files) to ensure downstream agents (Executor, Validator) can parse and execute the new skill natively.

## Target
* **Scope**: The `.github/skills/` (or `skills/`) directory.
* **Condition**: Triggered when the system is instructed to create, initialize, or scaffold a new migration skill.

## Prerequisites
The Orchestrator must provide the following in the `feature_context`:
1. `new_skill_name` (e.g., `web-dto-migration`, `spring-boot-upgrade`)
2. `new_skill_description` (A brief explanation of what the new skill will accomplish)

---

## Execution Plan (Executor Instructions)

The Executor must perform the following actions sequentially to fulfill this skill.

### Step 1: Scaffold Directory Structure
Read the source tree from `skills/create-skill/example/` and create an identical directory structure under `skills/<new_skill_name>/`. Ensure the following subdirectories are created:
* `skills/<new_skill_name>/reference/`
* `skills/<new_skill_name>/validate/`
* `skills/<new_skill_name>/validate/prompts/`
* `skills/<new_skill_name>/validate/scripts/`

### Step 2: Hydrate and Write Root SKILL.md
1. **Read**: `skills/create-skill/example/SKILL.md`
2. **Edit**: Replace placeholder values with the provided `new_skill_name` and `new_skill_description`. Define the target file extensions or paths based on the context.
3. **Write**: Save to `skills/<new_skill_name>/SKILL.md`

### Step 3: Hydrate and Write References (Executor Rules)
1. **Read**: `skills/create-skill/example/reference/example.prompt.md`
2. **Edit**: Rename the file to reflect its specific rule (e.g., `01-update-annotations.prompt.md`). Inject basic instructions tailored to the new skill's description.
3. **Write**: Save to `skills/<new_skill_name>/reference/<rule_name>.prompt.md`

### Step 4: Hydrate and Write Validation (Validator Rules)
1. **Config**: Copy `skills/create-skill/example/validate/config.yaml` to `skills/<new_skill_name>/validate/config.yaml`. Default `build: false` unless the context explicitly requires compilation verification.
2. **Prompts**: Copy `skills/create-skill/example/validate/prompts/example.prompt.md` to `skills/<new_skill_name>/validate/prompts/01-verify-changes.prompt.md`.
3. **Scripts** (Optional): If the context implies regex or AST scanning, copy `keyword-search` script assets to `skills/<new_skill_name>/validate/scripts/` and grant execution permissions.

### Step 5: Finalize
Report `completed` to the Orchestrator with a summary of the created directory structure.