---
name: project-documentation
description: "Create or update two synchronized project artifacts: a canonical Markdown project record and a polished Word project brief. Use for 项目档案, 项目说明书, PROJECT.md, 项目概览, 项目状态, 架构/流程说明, 决策记录, 风险、交付物与下一步整理. Do not use for spreadsheets, slide decks, generic essays, or software API documentation unless the user explicitly wants them documented as a project brief."
---

# Project Documentation

Produce a concise, trustworthy project record for ongoing work and a presentation-ready Word brief when requested. Markdown is the content source; Word is a formatted view of the same approved information.

## Supported Outputs

1. **Markdown 项目档案** — durable, diffable, easy for Codex and humans to update.
2. **Word 项目说明书** — formal `.docx` for review, submission, or sharing.

Do not create additional formats unless the user asks.

## Workflow

1. Inspect the available project sources: `simple-project.json`, existing Markdown/DOCX files, project folders, conversation decisions, audit data, deliverables, and explicit user statements.
2. Read [project-document-structure.md](references/project-document-structure.md). Select only sections relevant to the project; do not fill the document with empty headings.
3. Separate information into confirmed facts, recorded assumptions, pending decisions, and recommendations. Never present a recommendation as completed work.
4. Build one shared content model: overview, objective/scope, current workflow or architecture, status, decisions, deliverables, risks, next steps, version history, and sources.
5. Write or update the Markdown record first. Use [project-record-template.md](assets/project-record-template.md) as a shape, adapting it to the project rather than copying empty sections.
6. Run `scripts/validate_project_markdown.py`. Fix missing structure, unresolved placeholders, duplicate headings, and inconsistent status wording.
7. When Word is requested, load `$documents` and create a `.docx` from the approved Markdown content. Use `standard_business_brief` for ordinary project说明书 or `compact_reference_guide` for dense technical/operator projects.
8. Follow the documents skill's create/edit and render/verify workflow. Render the DOCX to PNG, inspect every page, fix clipping, tables, fonts, spacing, headers, footers, and page breaks, then deliver the final DOCX only.

## Update Rules

- Preserve existing confirmed decisions and version history.
- Replace stale status with the current state; do not append contradictory summaries.
- Add a dated version-record entry describing material changes.
- Keep Markdown and Word semantically synchronized. Layout may differ; facts and decisions may not.
- If source files disagree, surface the conflict instead of choosing silently.

## Output Contract

- Markdown: UTF-8 `.md`, one H1 title, clear section hierarchy, relative links for project-local files when practical.
- Word: `.docx` with title metadata, readable hierarchy, restrained tables, page numbers for multi-page documents, and visual QA completed.
- Both: explicit document version/date, source basis, current status, pending decisions, and next actions.
