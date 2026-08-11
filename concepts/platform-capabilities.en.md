---
type: Concept
id: platform-capabilities
lang: en
origin: native
status: draft
title: Platform capabilities — knob vocabulary as shipped
description: "The Canvas platform's typed capability, knob, telemetry, and apparatus-profile contract for reproducible education research, pinned to a shipped platform version."
tags: [platform, capabilities, knobs, ai-modes, telemetry, apparatus]
applies_to: "0.5.9"
generated: { by: evaluchat-continuation, at: 2026-08-10T10:45:00Z }
sources:
  - id: essays-workflow
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
    title: Essays workflow — proportional drafting unlock (knowledge catalog)
  - id: apparatus-recipe
    resource: https://github.com/evaluchat/knowledge/blob/main/playbooks/apparatus-recipe.en.md
    title: The apparatus recipe (knowledge catalog)
  - id: apparatus-method
    resource: https://github.com/evaluchat/research/blob/main/methods/apparatus.en.md
    title: The apparatus as research instrument (research catalog)
---

# Platform capabilities — public-beta runtime contract

> `applies_to: 0.5.9`. This concept defines the typed capability and knob
> vocabulary that research apparatus specs reference. When the platform changes,
> bump `applies_to`; old evidence stays interpretable because provenance records
> the Canvas and apparatus versions plus resolved configuration.

The public beta treats an apparatus as a reviewed research contract. A catalog
entry declares required capabilities, roles, telemetry, provenance, typed knobs,
dependencies/exclusions, and immutable profiles. Canvas validates the generated
catalog at build time and executes only known built-in implementations. A PR
cannot supply executable code to a running deployment.

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

The first three capabilities are mandatory for every student-facing apparatus.

## Typed knobs

| Knob | Type | Default | Effect |
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

The assignment stores the selected apparatus ID, apparatus version, profile ID,
and resolved configuration snapshot. Teachers cannot change knobs after
selection and later profile publication does not rewrite existing assignments.

## Telemetry boundary

| Stream | Records | Explicitly NOT |
|---|---|---|
| `process_signals` | keystroke bursts, paste volume, canvas edit types | authorship detection; no integrity score; omitted when tracking is false |
| `transcript` | full LLM agent conversation | — |
| `output` | final submission | — |

Process evidence describes *how* work happened, never *who* did it. There is no
integrity/authorship scoring in the platform (see [essays-workflow]); apparatuses that want to
argue about authorship must build their case from the transcript and process signals as evidence,
not from a platform verdict.

## Versioning contract

- `applies_to` pins the platform version whose behaviour this vocabulary describes.
- Apparatus specs carry their own `version` and `min_canvas_version` — the apparatus version is
  independent of the canvas version.
- Evidence provenance records `apparatus: {id, version, configuration}` + `canvas: {version}` so a
  given result is reproducible against the exact platform and knob set that produced it.

[essays-workflow]: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
