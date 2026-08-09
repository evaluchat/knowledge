---
type: Concept
id: research-apparatus
lang: en
origin: native
status: draft
title: Research apparatus — reproducible research on Canvas
description: "A research apparatus is a reproducible configuration of Canvas capabilities, workflows, and measurements designed to investigate one or more research questions and produce specified evidence — the four-dimension invariant, epistemic spine, versioning and configuration model."
tags: [evaluchat, canvas, apparatus, research, okf]
applies_to: 0.5.9
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-09T16:40:00Z
sources:
  - id: apparatus-method
    resource: https://github.com/evaluchat/research/blob/main/methods/apparatus.en.md
    title: The apparatus as research instrument — measurement, observation, evidence (research catalog)
  - id: camdle-theory
    resource: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
    title: CAMDLE — research question and theory (unproven)
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: Threshold calibration — research question (open)
---

# Research apparatus — reproducible research on Canvas

> **Applies to:** Canvas apps/web **0.5.9** (dev line). Draft concept — the pattern is defined here and instantiated by the Essays apparatus (see [essays-workflow](essays-workflow.en.md)).

## Definition

> **A Research Apparatus is a reproducible configuration of Canvas capabilities, workflows, and measurements designed to investigate one or more research questions and produce specified evidence.**

An apparatus is **not** "a configured surface". The user-interface surface is an implementation consequence, not the definition. The common denominator of an apparatus is **instrumentation + workflow**: what the learner experiences is a workflow, what the apparatus records is a measurement, and what the researcher receives is specified evidence.

An apparatus may address one research question, several related questions, or one question through several experimental variants — there is no one-to-one constraint between apparatus and question. The Essays apparatus, for example, investigates the threshold-calibration question; a future apparatus may address two.

## The four dimensions

An apparatus has four distinct dimensions. Never conflate them:

| Dimension | Representation | Answers |
|---|---|---|
| **Knowledge** | OKF knowledge concept (`research-apparatus` + a per-apparatus concept) | What is this apparatus? |
| **Manifest** | Catalog manifest (`apparatus.json`) | How does the platform enable and version it? |
| **Research method** | OKF research method (per-apparatus method in the research catalog) | What does it measure? |
| **Code** | Canvas implementation | How does it actually run? |

```
                    Research Question
                          │
             ┌────────────┴────────────┐
             ↓                         ↓
       Knowledge concept         Research method
        "what it is"             "what it measures"
             │                         │
             └────────────┬────────────┘
                          ↓
                    Apparatus
                          │
                    ┌─────┴─────┐
                    ↓           ↓
                 Manifest      Code
                "enable it"  "run it"
```

**Guardrail: the manifest must never become a second knowledge system.** The manifest carries only what the platform needs to enable and version the apparatus. Description, meaning, and measurement semantics live in the OKF concepts — no duplicated prose in JSON.

## The epistemic spine

Four terms are easy to conflate. Keeping them distinct is central to how evidence is produced:

| Term | What it is | Example |
|---|---|---|
| **Apparatus** | What is intended to be investigated (the configured workflow) | Essays apparatus: dialogic constraint before drafting |
| **Intervention** | What the apparatus actually does to the user's workflow | Drafting unlocks after N dialogic contributions |
| **Measurement** | What the apparatus records (mechanism, not evidence) | Engagement Metrics / process signals |
| **Evidence** | What can subsequently be submitted to Research | "Student spent 12 min in Socratic phase" (observation) |

"Engagement Metrics" is a *measurement mechanism*, not evidence. "Student spent 12 minutes in Socratic phase" is an *observation*. "Students who spent 12 minutes learned more" is a *claim* — and claims need the findings machinery of the research catalog. This separation is enforced in the evidence-bundle shape (observations/results vs reflection vs limitations).

## Composition: primitives and capabilities

Canvas primitives — documents, workspaces, AI sessions, knowledge context, workflows, activities — are the substrate an apparatus composes. Class and student management, assignments, and submission are **capabilities** an apparatus may or may not use; they are optional modules, not part of the definition.

The apparatus contract is expressed in capabilities, roles, and workflow phases:

- **Capabilities, not routes.** `student-workspace`, `teacher-assignment-management`, `evidence-export` — NOT `/student`, `/teacher`. Routes are implementation details; the Canvas host decides how capabilities map onto UI, routes, and APIs. Otherwise the contract would couple to a specific web framework — exactly the coupling Canvas should abstract away.
- **Workflow phases, not agent nodes.** `phases: [socratic, drafting, defense]` — NOT `nodes: [assess-thesis]`. The contract describes observable behaviour; agent-graph node names are implementation. This preserves freedom to rewrite the agent architecture later.

## Versioning: the behaviour and evidence contract

What is versioned is the **behaviour and evidence contract** — not the UI, not the code layout:

| Version | Changes when | Examples |
|---|---|---|
| **major** | Changes that make previous experiments difficult or impossible to compare | What counts as "sufficient dialogic contribution" changes; phase semantics change |
| **minor** | New capabilities that don't alter existing semantics | A new assignment type is added; a role gains a surface |
| **patch** | Implementation fixes with no change to experimental semantics | A rendering bug fix; copy changes |

Consequence: **apparatus version ≠ canvas version.** Canvas 0.5.9 may ship the Essays apparatus at 0.5.9; later the Essays apparatus may be 0.6 (a research measurement changed) while Canvas stays 0.5.9 — or vice versa. That decoupling is valuable for longitudinal research: the apparatus version is what evidence must cite.

## Configuration: Apparatus → Version → Configuration → Experiment

Two teachers using "Essays v0.5.9" may run materially different interventions:

| Teacher A | Teacher B |
|---|---|
| threshold = 3 contributions | threshold = 5 contributions |
| defense = required | defense = optional |
| AI mode = Socratic | AI mode = Socratic + adversarial |

Same apparatus, same version — **different configurations**. Treating both as "Essays v0.5.9" would corrupt any comparison. The model is:

```
Apparatus → Version → Configuration → Experiment
```

Configuration is a first-class concept in the manifest vocabulary (`configuration: {threshold, defense_required, ai_modes, ...}`), defined per apparatus in its manifest or concept — not a universal schema.

### Configuration is part of provenance

An evidence contribution must record the actual apparatus configuration used:

```yaml
apparatus:
  id: ai-assisted-essay
  version: 0.5.9
  configuration:
    threshold: 3
    defense_required: true
    ai_modes: [socratic, critique]
  canvas:
    version: 0.5.9
```

The evidence graph becomes: `Question → Apparatus → Version → Configuration → Intervention → Evidence`. Because the pre-registered question, apparatus, and configuration all predate the evidence, this strengthens the research catalog's direction-of-fit machinery.

## The recipe

The [apparatus recipe](../playbooks/apparatus-recipe.en.md) is a design checklist for specifying a new apparatus from a research question: workspace, assistant role, knowledge context, class and student management, assignment/submission, workflow, evidence output, and consent/privacy. The recipe provides a consistent way to describe and build research apparatuses on Canvas. It is an experimental framework, not a universal schema — a second apparatus is expected to diverge from the checklist where its questions demand different instrumentation.

## Status

`status: draft`. The pattern is defined here and instantiated by the Essays apparatus ([essays-workflow](essays-workflow.en.md)) as **Apparatus #1**; the instrument view lives in the research catalog ([apparatus-method]). Nothing in this document describes a plugin framework — apparatuses are enabled and versioned by the platform, not installed as independently loadable artifacts.
