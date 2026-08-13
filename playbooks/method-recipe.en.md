---
type: Playbook
id: method-recipe
lang: en
origin: native
status: draft
title: The method recipe — from research question to published method
description: "Given a research question, specify the Method: the canonical form, an eight-primitive design checklist, a worked example (Essays / ai-assisted-essay), and the rules for recording version and levers."
tags: [evaluchat, canvas, method, recipe, levers, okf]
applies_to: 0.5.9
generated:
  by: cursor-grok/4.6
  at: 2026-08-13T14:48:00Z
sources:
  - id: research-method
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/research-method.en.md
    title: Research method — how methods use platform capabilities and levers (knowledge catalog)
  - id: ai-assisted-essay
    resource: https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/
    title: ai-assisted-essay — published method (research catalog)
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: Threshold calibration — research question (open)
---

# The method recipe — from research question to published method

> **Applies to:** Canvas apps/web **0.5.9** (dev line). Companion to [research-method](../concepts/research-method.en.md); worked example: [essays-workflow](../concepts/essays-workflow.en.md) / [ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/).

## What the recipe is

The recipe is **not** "here's how to build a feature". It is:

> **Given a research question, specify the Method** — which Knowledge-documented levers it selects, the intervention, and the evidence that method will file.

A Method is a published, versioned way of investigating one or more research questions. Knowledge (this catalog) documents what Evaluchat can do. Research documents the question, the method, the evidence, and any later finding. The recipe is how a research question becomes a method specification that uses named platform capabilities.

## The canonical form

> **"This is my research question:** [link(s)]. **This is how I foresee the method working:** [✓ canvas workspace, ✓ AI assistant configured as …, ✓ class and student management, ✓ ability to assign assignments, ✓ …]. **Can you build this for me?"**

The checklist below makes each part of that sentence explicit.

## The design checklist (eight primitives)

Work through each primitive; leave a cell empty if the method genuinely does not need it. This is a **design checklist, not a universal schema** — see [Checklist, not schema](#checklist-not-schema) below.

| # | Primitive | What to specify | Essays (`ai-assisted-essay`) |
|---|---|---|---|
| 1 | **Workspace** | What the learner opens and works in | Split-screen: dialogue panel beside an editable markdown document |
| 2 | **Assistant role** | How the AI is configured, and what it may and may not do | Constrained AI chat: interviews before drafting, acts as developmental editor, may not draft the whole assignment from one prompt |
| 3 | **Knowledge context** | What knowledge the assistant carries into the session | Assignment brief, CAMDLE design constraints, thesis-assessment criteria |
| 4 | **Class and student management** | How learners are organised and enrolled | Teacher-owned classes and rosters; assignments assigned to specific students |
| 5 | **Assignment / submission** | How work is assigned and handed in | Teacher assignment creation + seed catalog; submission unlocks after the defense phase |
| 6 | **Workflow** | The phases the learner passes through | `socratic` → `drafting` → `defense` |
| 7 | **Evidence output** | What measurements are recorded and how they are exported | Process signals (typing, paste, canvas edits, focus) aggregated into `session_summary` events; teacher-facing Engagement Metrics; save-as-evidence export |
| 8 | **Consent / privacy** | What consent and privacy terms the method runs under | Institutional and parental/guardian consent for evidence use; anonymisation before contribution to the research catalog |

## Worked example: Essays as `ai-assisted-essay`

The Essays assignment flow (the [essays-workflow](../concepts/essays-workflow.en.md) concept) is the product-side source of truth for the first published method, [ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/). Mapping the checklist to the actual implementation:

1. **Workspace** — the student's split-screen canvas (dialogue + document).
2. **Assistant role** — drafting support is released conditionally: proportional scaffolding. The model cannot generate the whole assignment from a single prompt; assistance unlocks after sufficient dialogic contribution. This is the **intervention** the method makes.
3. **Knowledge context** — the assignment brief and the CAMDLE design; the assistant assesses the thesis each turn.
4. **Class and student management** — teacher-owned custom assignments and the shared seed catalog; one active session per student per assignment.
5. **Assignment / submission** — assignments resolve from teacher-created assignments or seeds; submission unlocks only after the viva-defense phase.
6. **Workflow** — three phases: `socratic` (thesis interview), `drafting` (milestone-gated co-creation), `defense` (devil's-advocate challenge before submission).
7. **Evidence output** — process signals collected client-side into compact `session_summary` events; teachers see Engagement Metrics on the submission view. Process evidence is explicitly **not** authorship detection — observations for teacher judgment, never an integrity verdict.
8. **Consent / privacy** — evidence contributions carry consent and anonymisation records before entering the research catalog (filed under the method, not in this Knowledge catalog).

The threshold — how much contribution is "enough" — is an **empirical variable**, not a settled value; it is the subject of the [threshold-calibration] research question and is recorded per lever set (see below).

## Checklist, not schema

The eight primitives are a design checklist, not a universal method schema. A second method is expected to expose where the checklist is insufficient: a teacher-side method (for example, an AI assignment stress test) may need input-artefact analysis and comparison engines while *not* needing class management, submission, or defense. **That divergence is evidence the recipe works as an experimental framework**, not a failure of the recipe.

## Recording version and levers

- **Version** the method per the behaviour/evidence contract: a major bump when previous experiments become hard to compare (e.g. what counts as sufficient contribution changes), minor for new capabilities that don't alter existing semantics, patch for implementation fixes. The method version is independent of the canvas version.
- **Record the levers** of every run: threshold, drafting gate, AI assistance, and any other per-method setting. The same method version with different lever values runs materially different interventions.
- **Provenance**: evidence contributions must record `method: {id, version, levers}` and `canvas: {version}` — see the [research-method] concept and the research catalog's [ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/) method. Catalog YAML uses `levers:`; live product APIs and stored snapshots are not renamed in this pass.

## What is not built yet

This playbook is a **specification tool, not a builder**. As of Canvas 0.5.9 there is:

- **no DSL** for methods — the recipe is written in prose and checklists;
- **no builder framework** — the checklist does not generate manifests or code;
- **no plugin runtime** — methods are enabled and versioned by the platform, not installed as independently loadable artifacts; there are no lifecycle hooks, dependency resolution, or sandboxing.

The Essays method is the proof that the pattern can be *named* and *described*; the tooling to *generate* method catalogs is future work relative to this playbook.

[research-method]: https://github.com/evaluchat/knowledge/blob/main/concepts/research-method.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
