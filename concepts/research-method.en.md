---
type: Concept
id: research-method
lang: en
origin: native
status: draft
title: Research method — how methods use platform capabilities and levers
description: "A Method is a published, versioned way of investigating a research question: it selects Knowledge-documented levers, Evaluchat applies that profile in a workspace, and evidence is filed under that method in the research catalog."
tags: [evaluchat, canvas, method, levers, research, okf]
applies_to: 0.5.9
generated:
  by: cursor-grok/4.6
  at: 2026-08-13T14:48:00Z
sources:
  - id: ai-assisted-essay
    resource: https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/
    title: ai-assisted-essay — published method (research catalog)
  - id: camdle-theory
    resource: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
    title: CAMDLE — research question and theory (unproven)
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: Threshold calibration — research question (open)
---

# Research method — how methods use platform capabilities and levers

> **Applies to:** Canvas apps/web **0.5.9** (dev line). Draft concept — Knowledge documents what Evaluchat can do; a Method in the research catalog selects those capabilities. First published method: [ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/) (product side: [essays-workflow](essays-workflow.en.md)).

## Two catalogs

| Knowledge (this repo) | Research |
|---|---|
| Product truth | Research truth |
| What Evaluchat can do | What we are investigating |
| Features, capabilities, workspace templates | Theory → questions → methods → evidence → findings |

Evaluchat **runs** a method profile. It does not own research truth. This catalog does not store classroom evidence. The research catalog does not store executable product templates.

A Method is not a folder of methodology essays. It is the object a teacher adds to a workspace: versioned, profiled, measurable.

## Definition

> **A Method is a published, versioned way of investigating one or more research questions.** It selects named **levers** (platform features documented here), Evaluchat applies that profile in a workspace, and when the run concludes, evidence is filed under that method.

```text
Theory / question
    → Method  (published way of investigating that question)
         → selects levers  (which Knowledge-documented features this run engages)
         → Evaluchat applies that profile in a workspace
         → when the run concludes, evidence is filed under that method
    → Finding  (a human claim, reviewed; not the raw export)
```

A Method is **not** "a configured surface". The user-interface surface is an implementation consequence, not the definition. The common denominator is **instrumentation + workflow**: what the learner experiences is a workflow, what the method records is a measurement, and what the researcher receives is specified evidence.

A Method may address one research question, several related questions, or one question through several experimental variants. The Essays method ([ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/)), for example, investigates the threshold-calibration question; a future method may address two.

**Levers** are the named switches on a method (`ai_assistance`, `drafting_gate`, `threshold`, …). This catalog defines what each lever *means* on the platform (see [platform-capabilities](platform-capabilities.en.md)). The method spec in the research catalog says which levers this investigation uses, defaults, and immutable profiles. Same method version + different lever values = different intervention; evidence must record the resolved values.

This pass does **not** rename live product APIs or stored assignment snapshots. Catalog language is Method and levers; existing field names the app already reads remain as shipped.

## What each catalog owns

| Catalog | Owns | Does not own |
|---|---|---|
| **Knowledge** | Capabilities, lever meanings, workflows, workspace templates (Getting Started, Assignment brief) | Classroom evidence, findings, research questions |
| **Research** | Questions, method specs, evidence contracts, review, findings | Executable Canvas templates, product prompt text as shipped |

**Guardrail: generated enablement JSON must never become a second knowledge system.** The payload the platform consumes to enable and version a method carries only what the runtime needs. Description, meaning, and measurement semantics live in these OKF concepts and in the research method spec — no duplicated prose in JSON.

## The epistemic spine

Four terms are easy to conflate. Keeping them distinct is how evidence is produced:

| Term | What it is | Example |
|---|---|---|
| **Method** | What is intended to be investigated (the published profile) | Essays: dialogic constraint before drafting |
| **Intervention** | What the method actually does to the user's workflow | Drafting unlocks after N dialogic contributions |
| **Measurement** | What the method records (mechanism, not evidence) | Engagement Metrics / process signals |
| **Evidence** | What can subsequently be submitted to Research | "Student spent 12 min in Socratic phase" (observation) |

"Engagement Metrics" is a *measurement mechanism*, not evidence. "Student spent 12 minutes in Socratic phase" is an *observation*. "Students who spent 12 minutes learned more" is a *claim* — and claims need the findings machinery of the research catalog. This separation is enforced in that catalog's evidence contract (observations/results vs reflection vs limitations). Evidence belongs to exactly one method; findings may cite several methods.

## Composition: primitives and capabilities

Canvas primitives — documents, workspaces, AI sessions, knowledge context, workflows, activities — are the substrate a method composes. Class and student management, assignments, and submission are **capabilities** a method may or may not use; they are optional modules, not part of the definition.

The method contract is expressed in capabilities, roles, and workflow phases:

- **Capabilities, not routes.** `student-workspace`, `teacher-assignment-management`, `evidence-export` — NOT `/student`, `/teacher`. Routes are implementation details; the Canvas host decides how capabilities map onto UI, routes, and APIs. Otherwise the contract would couple to a specific web framework — exactly the coupling Canvas should abstract away.
- **Workflow phases, not agent nodes.** `phases: [socratic, drafting, defense]` — NOT `nodes: [assess-thesis]`. The contract describes observable behaviour; agent-graph node names are implementation. This preserves freedom to rewrite the agent architecture later.

## Versioning: the behaviour and evidence contract

What is versioned is the **behaviour and evidence contract** — not the UI, not the code layout:

| Version | Changes when | Examples |
|---|---|---|
| **major** | Changes that make previous experiments difficult or impossible to compare | What counts as "sufficient dialogic contribution" changes; phase semantics change |
| **minor** | New capabilities that don't alter existing semantics | A new assignment type is added; a role gains a surface |
| **patch** | Implementation fixes with no change to experimental semantics | A rendering bug fix; copy changes |

Consequence: **method version ≠ canvas version.** Canvas 0.5.9 may ship the Essays method at 0.5.9; later the Essays method may be 0.6 (a research measurement changed) while Canvas stays 0.5.9 — or vice versa. That decoupling is valuable for longitudinal research: the method version is what evidence must cite.

## Levers: Method → Version → Levers → Experiment

Two teachers using "Essays v0.5.9" may run materially different interventions:

| Teacher A | Teacher B |
|---|---|
| threshold = 3 contributions | threshold = 5 contributions |
| `drafting_gate` = `thesis-approved` | `drafting_gate` = `discussion-first` |
| `ai_assistance` = on | `ai_assistance` = on, `ai_canvas_actions` = off |

Same method, same version — **different lever values**. Treating both as "Essays v0.5.9" would corrupt any comparison. The model is:

```
Method → Version → Levers → Experiment
```

Levers are first-class in the method spec (`levers: {threshold, drafting_gate, ai_assistance, ...}`), defined per method — not a universal schema. Knowledge defines the platform meaning of each name; the method says which subset this investigation uses.

### Levers are part of provenance

An evidence contribution must record the actual method and resolved lever values:

```yaml
method:
  id: ai-assisted-essay
  version: 0.5.9
  levers:
    ai_assistance: true
    ai_canvas_actions: true
    drafting_gate: discussion-first
    threshold: 3
    tracking: true
  canvas:
    version: 0.5.9
```

The evidence graph becomes: `Question → Method → Version → Levers → Intervention → Evidence`. Because the pre-registered question, method, and lever values all predate the evidence, this strengthens the research catalog's direction-of-fit machinery. Catalog provenance uses `method:` and `levers:`; live stored snapshots may still use existing product field names.

## The recipe

The [method recipe](../playbooks/method-recipe.en.md) is a design checklist for specifying a new method from a research question: workspace, assistant role, knowledge context, class and student management, assignment/submission, workflow, evidence output, and consent/privacy. The recipe provides a consistent way to describe methods that use Canvas capabilities. It is an experimental framework, not a universal schema — a second method is expected to diverge from the checklist where its questions demand different instrumentation.

## Status

`status: draft`. The pattern is defined here. The Essays workflow ([essays-workflow](essays-workflow.en.md)) is the product-side source of truth for the first published method, [ai-assisted-essay](https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/). Nothing in this document describes a plugin framework — methods are enabled and versioned by the platform, not installed as independently loadable artifacts.
