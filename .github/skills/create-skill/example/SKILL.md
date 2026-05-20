---
name: example
description: An example skill that demonstrates how to document a skill for the `create-skill` subdirectory. It serves as a template for creating new skills with standardized structure and content.
---

# Skill: example

This is an example `SKILL.md` that demonstrates how to document a skill for the `create-skill` subdirectory.

## When to use

- Use this file when you want to document an automated task, script, or subworkflow so it is discoverable and reusable.
- The file should briefly explain the skill's purpose, trigger conditions, inputs/outputs, and usage examples.

## Description

This skill shows how to add or update a small tool in the repository (for example, a keyword search script).
It covers:
- Purpose: search code or text for keywords and produce a report.
- Use cases: code-quality checks, migration validation, scanning for TODO/FIXME markers, etc.

## Inputs

- Optional parameters: target file or directory path, keywords YAML file, CLI options (recursive, regex, output format, etc.).

## Outputs

- Console output (text or JSON)
- Optional: write a report file (text or JSON)