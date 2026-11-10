# GitHub Issue Form Generator Template

Fill in this document, then give it to a coding assistant with this request:

> Generate the GitHub issue-form YAML files described in this document. Create one file per task category under `.github/ISSUE_TEMPLATE/`. Follow the generation rules below.

## Project

- Project name: AIFinalProject
- Repository: `<owner>/<repository>`
- Task title format: `[<Category>] <short task summary>`

## Task Categories and Owners

Replace every placeholder with a real GitHub username, without the `@` prefix. Add or remove rows as needed. Multiple usernames in a row means all listed developers receive the issue; it does not distribute issues between them.

| Category | YAML filename | Description | Default assignees (comma-separated) | Existing labels (optional, comma-separated) |
| --- | --- | --- | --- | --- |
| Backend | backend.yml | APIs, business logic, and data processing | <backend-developer> | |
| Frontend | frontend.yml | User interface and client-side behavior | <frontend-developer> | |
| Testing | testing.yml | Test coverage, verification, and bug reproduction | <testing-developer> | |

Only list labels that already exist in the repository. Leave the labels column blank to omit labels.

## Form Fields

Use these fields in every generated form. Edit the table to customize them.

| Field ID | Label | Input type | Required | Instructions or options |
| --- | --- | --- | --- | --- |
| task | Task description | textarea | Yes | Describe what needs to be built or changed. |
| acceptance | Acceptance criteria | textarea | Yes | List the observable conditions that mean the task is complete. |
| context | Context and dependencies | textarea | No | Link related issues and describe dependencies or relevant files. |
| priority | Priority | dropdown | Yes | Low; Medium; High |

## Generation Rules

1. Create one `.yml` file per category at `.github/ISSUE_TEMPLATE/<YAML filename>`.
2. Use valid GitHub issue-form YAML with top-level `name`, `description`, `title`, `assignees`, and `body` properties.
3. Set `name` to `<Category> task` and `description` to the category description.
4. Set `title` to `[<Category>] `, preserving the trailing space so the reporter can enter a summary.
5. Convert each category's usernames to an `assignees` YAML list. Do not include `@` prefixes.
6. If labels are supplied, emit them as a `labels` list. Otherwise omit `labels`.
7. Convert the field table into `body` entries. Each entry must have `type`, a unique `id`, `attributes.label`, and `validations.required` as a boolean.
8. For textarea fields, put the instructions in `attributes.description`. For dropdown fields, split the semicolon-separated options into an `attributes.options` list.
9. Quote YAML strings when necessary, including titles containing brackets. Use two-space indentation and no tabs.
10. Do not invent usernames, labels, or repository details. If a required placeholder is unfilled, report the missing value before generating files.
11. Inspect existing issue templates before writing. Preserve unrelated files and report any filename conflicts.
12. Report the generated file paths and their default assignees.

## Expected Behavior

When someone creates an issue using a category's form, GitHub automatically assigns it to that category's listed developers. The forms must be committed to the repository's default branch to be available there.

This specification covers fixed assignment by selected issue form. Label-driven routing, rotation, or workload-based assignment requires a separate automation workflow.
