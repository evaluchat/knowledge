---
type: Concept
id: platform-capabilities
lang: en
origin: native
status: draft
title: Platform capabilities — public-beta runtime contract
description: "The Canvas platform's typed capability, lever, telemetry, and method-profile contract for reproducible education research, pinned to a shipped platform version."
tags: [platform, capabilities, levers, ai-modes, telemetry, method]
applies_to: "0.5.9"
generated: { by: cursor-grok/4.6, at: 2026-08-13T14:48:00Z }
sources:
  - id: essays-workflow
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
    title: Essays workflow — proportional drafting unlock (knowledge catalog)
  - id: method-recipe
    resource: https://github.com/evaluchat/knowledge/blob/main/playbooks/method-recipe.en.md
    title: The method recipe (knowledge catalog)
  - id: ai-assisted-essay
    resource: https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/
    title: ai-assisted-essay — published method (research catalog)
---

# Platform capabilities — public-beta runtime contract

> `applies_to: 0.5.9`. This concept defines the typed capability and lever
> vocabulary that research method specs reference. When the platform changes,
> bump `applies_to`; old evidence stays interpretable because provenance records
> the Canvas and method versions plus resolved levers.

The public beta treats a Method as a reviewed research contract. A catalog
entry declares required capabilities, roles, telemetry, provenance, typed levers,
dependencies/exclusions, and immutable profiles. Canvas validates the generated
catalog at build time and executes only known built-in implementations. A PR
cannot supply executable code to a running deployment.

This catalog calls the named switches **levers**. Live product APIs and stored
assignment snapshots are unchanged in this pass (existing field names such as
`apparatusId` remain as shipped).

Minimum viable student workflow: assignment context, student authoring, and
submission. Profiles that disable every meaningful activity are invalid.

## Required capabilities

| Capability | Meaning |
|---|---|
| `assignment-context` | Student can read the task and treatment context |
| `student-authoring` | Student has an authoring surface independent of AI generation |
| `submission` | Student can submit work for teacher review |
| `ai-dialogue` | Reviewed AI conversation route is available |
| `ai-canvas-actions` | Reviewed AI generation/edit actions are available |
| `drafting-gate` | A gate policy can control drafting assistance |
| `process-tracking` | Process telemetry can be captured under consent/policy |

The first three capabilities are mandatory for every student-facing method.

## Typed levers

| Lever | Type | Default | Effect |
|---|---|---|---|
| `ai_assistance` | boolean | `true` | allow or disable agent calls |
| `ai_canvas_actions` | boolean | `true` | allow or disable AI generation/edit routes; requires AI assistance when enabled |
| `drafting_gate` | enum | `discussion-first` | `none`, `discussion-first`, or `thesis-approved` |
| `threshold` | integer 0–100 | `4` | visible contributions before the escape hatch |
| `tracking` | boolean | `true` | capture/display process telemetry |

Dependencies, exclusions, ranges, and enum values are validated against the
resolved profile before an assignment can be created.

## Drafting gates

| Gate | Unlock condition | Notes |
|---|---|---|
| `none` | immediate | drafting available from the start |
| `discussion-first` | prior dialogic contribution | the current shipped behaviour (see [essays-workflow]) |
| `thesis-approved` | assess-thesis pass | supported by the contract; profile-specific |

The gate is the mechanism that turns a pedagogical constraint into a research variable: the
drafting-unlock threshold is configurable and pre-registerable per experiment (see
[threshold-calibration]).

## Immutable profile examples

The generated Essays catalog publishes these valid profiles:

- `canonical-constrained-dialogue` — AI dialogue/actions, discussion-first gate,
  threshold 4, tracking on;
- `gate-off` — drafting from the start, threshold 0;
- `ai-off` — local authoring and submission without agent calls;
- `canvas-actions-off` — AI dialogue while canvas generation/edit actions are
  disabled;
- `tracking-off` — canonical treatment without process telemetry.

The assignment stores the selected method identity, method version, profile ID,
and resolved configuration snapshot. Teachers cannot change levers after
selection and later profile publication does not rewrite existing assignments.
Stored snapshots keep the field names the live app already reads.

## Telemetry boundary

| Stream | Records | Explicitly NOT |
|---|---|---|
| `process_signals` | keystroke bursts, paste volume, canvas edit types | authorship detection; no integrity score; omitted when tracking is false |
| `transcript` | full LLM agent conversation | — |
| `output` | final submission | — |

Process evidence describes *how* work happened, never *who* did it. There is no
integrity/authorship scoring in the platform (see [essays-workflow]); methods that want to
argue about authorship must build their case from the transcript and process signals as evidence,
not from a platform verdict.

## Versioning contract

- `applies_to` pins the platform version whose behaviour this vocabulary describes.
- Method specs carry their own `version` and `min_canvas_version` — the method version is
  independent of the canvas version.
- Evidence provenance in the research catalog records `method: {id, version, levers}` +
  `canvas: {version}` so a given result is reproducible against the exact platform and lever
  set that produced it. That catalog shape does not rename live product APIs.

[essays-workflow]: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
