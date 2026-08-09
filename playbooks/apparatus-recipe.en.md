---
type: Playbook
id: apparatus-recipe
lang: en
origin: native
status: draft
title: The apparatus recipe — from research question to built apparatus
description: "Given a research question, specify the intervention and the measurement apparatus: the canonical form, an eight-primitive design checklist, a worked example (Essays), and the rules for recording version and configuration."
tags: [evaluchat, canvas, apparatus, recipe, okf]
applies_to: 0.5.9
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-09T16:40:00Z
sources:
  - id: research-apparatus
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/research-apparatus.en.md
    title: Research apparatus — reproducible research on Canvas (knowledge catalog)
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: Threshold calibration — research question (open)
---

# The apparatus recipe — from research question to built apparatus

> **Applies to:** Canvas apps/web **0.5.9** (dev line). Companion to [research-apparatus](../concepts/research-apparatus.en.md); worked example: [essays-workflow](../concepts/essays-workflow.en.md).

## What the recipe is

The recipe is **not** "here's how to build a feature". It is:

> **Given a research question, specify the intervention and the measurement apparatus.**

An apparatus is a reproducible configuration of Canvas capabilities, workflows, and measurements designed to investigate one or more research questions and produce specified evidence. The recipe is the way a research question becomes such a specification.

## The canonical form

> **"This is my research question:** [link(s)]. **This is how I foresee the apparatus working:** [✓ canvas workspace, ✓ AI assistant configured as …, ✓ class and student management, ✓ ability to assign assignments, ✓ …]. **Can you build this for me?"**

The checklist below makes each part of that sentence explicit.

## The design checklist (eight primitives)

Work through each primitive; leave a cell empty if the apparatus genuinely does not need it. This is a **design checklist, not a universal schema** — see [Checklist, not schema](#checklist-not-schema) below.

| # | Primitive | What to specify | Essays (Apparatus #1) |
|---|---|---|---|
| 1 | **Workspace** | What the learner opens and works in | Split-screen: dialogue panel beside an editable markdown document |
| 2 | **Assistant role** | How the AI is configured, and what it may and may not do | Constrained AI chat: interviews before drafting, acts as developmental editor, may not draft the whole assignment from one prompt |
| 3 | **Knowledge context** | What knowledge the assistant carries into the session | Assignment brief, CAMDLE design constraints, thesis-assessment criteria |
| 4 | **Class and student management** | How learners are organised and enrolled | Teacher-owned classes and rosters; assignments assigned to specific students |
| 5 | **Assignment / submission** | How work is assigned and handed in | Teacher assignment creation + seed catalog; submission unlocks after the defense phase |
| 6 | **Workflow** | The phases the learner passes through | `socratic` → `drafting` → `defense` |
| 7 | **Evidence output** | What measurements are recorded and how they are exported | Process signals (typing, paste, canvas edits, focus) aggregated into `session_summary` events; teacher-facing Engagement Metrics; save-as-evidence export |
| 8 | **Consent / privacy** | What consent and privacy terms the apparatus runs under | Institutional and parental/guardian consent for evidence use; anonymisation before contribution to the research catalog |

## Worked example: Essays as Apparatus #1

The Essays assignment flow (the [essays-workflow](../concepts/essays-workflow.en.md) concept) is **Apparatus #1** — the first instance of the pattern. Mapping the checklist to the actual implementation:

1. **Workspace** — the student's split-screen canvas (dialogue + document).
2. **Assistant role** — drafting support is released conditionally: proportional scaffolding. The model cannot generate the whole assignment from a single prompt; assistance unlocks after sufficient dialogic contribution. This is the **intervention** the apparatus makes.
3. **Knowledge context** — the assignment brief and the CAMDLE design; the assistant assesses the thesis each turn.
4. **Class and student management** — teacher-owned custom assignments and the shared seed catalog; one active session per student per assignment.
5. **Assignment / submission** — assignments resolve from teacher-created assignments or seeds; submission unlocks only after the viva-defense phase.
6. **Workflow** — three phases: `socratic` (thesis interview), `drafting` (milestone-gated co-creation), `defense` (devil's-advocate challenge before submission).
7. **Evidence output** — process signals collected client-side into compact `session_summary` events; teachers see Engagement Metrics on the submission view. Process evidence is explicitly **not** authorship detection — observations for teacher judgment, never an integrity verdict.
8. **Consent / privacy** — evidence contributions carry consent and anonymisation records before entering the research catalog (see the research catalog's evidence-bundle provenance template).

The threshold — how much contribution is "enough" — is an **empirical variable**, not a settled value; it is the subject of the [threshold-calibration] research question and is recorded per configuration (see below).

## Checklist, not schema

The eight primitives are a design checklist, not a universal apparatus schema. A second apparatus is expected to expose where the checklist is insufficient: a teacher-side apparatus (for example, an AI assignment stress test) may need input-artefact analysis and comparison engines while *not* needing class management, submission, or defense. **That divergence is evidence the recipe works as an experimental framework**, not a failure of the recipe.

## Recording version and configuration

- **Version** the apparatus per the behaviour/evidence contract: a major bump when previous experiments become hard to compare (e.g. what counts as sufficient contribution changes), minor for new capabilities that don't alter existing semantics, patch for implementation fixes. The apparatus version is independent of the canvas version.
- **Record the configuration** of every run: threshold, defense required or optional, AI modes, and any other per-apparatus setting. The same apparatus version with different configurations runs materially different interventions.
- **Provenance**: evidence contributions must record `apparatus: {id, version, configuration}` and `canvas: {version}` — see the [research-apparatus] concept and the research catalog's `methods/apparatus.en.md`.

## What is not built yet

This playbook is a **specification tool, not a builder**. As of Canvas 0.5.9 there is:

- **no DSL** for apparatuses — the recipe is written in prose and checklists;
- **no builder framework** — the checklist does not generate manifests or code;
- **no plugin runtime** — apparatuses are enabled and versioned by the platform, not installed as independently loadable artifacts; there are no lifecycle hooks, dependency resolution, or sandboxing.

The Essays apparatus is the proof that the pattern can be *named* and *described*; the tooling to *generate* apparatuses is future work.

[research-apparatus]: https://github.com/evaluchat/knowledge/blob/main/concepts/research-apparatus.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
