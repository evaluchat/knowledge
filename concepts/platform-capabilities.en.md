---
type: Concept
id: platform-capabilities
lang: en
origin: native
status: draft
title: Platform capabilities — knob vocabulary as shipped
description: "The Canvas platform's configurable surface for research apparatuses: AI modes, drafting gates, and telemetry, pinned to a shipped platform version. Apparatus specs reference this vocabulary for their knobs."
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

# Platform capabilities — knob vocabulary as shipped

> `applies_to: 0.5.9`. This concept defines the **knob vocabulary** that research apparatus specs
> reference in their frontmatter (`knobs:`). An apparatus spec says `ai_mode: constrained`; this
> concept says what that *mechanically means* in the pinned platform version. When the platform
> changes, bump `applies_to` and adjust the tables below — old evidence stays interpretable because
> provenance records the version its configuration ran under.

## AI modes

| Mode | Chat | Canvas edits | Notes |
|---|---|---|---|
| `none` | — | — | no AI panel in the workspace |
| `chat-only` | ✓ | — | advisor; cannot touch the document |
| `constrained` | ✓ | gated | drafting unlocks per `drafting_gate` policy |
| `full` | ✓ | ✓ | unconstrained co-editing |

`constrained` is the CAMDLE-relevant mode: the AI participates in dialogue freely, but its
contribution to the canvas document is gated behind the drafting policy.

## Drafting gates

| Gate | Unlock condition | Notes |
|---|---|---|
| `none` | immediate | drafting available from the start |
| `discussion-first` | prior dialogic contribution | the current shipped behaviour (see [essays-workflow]) |
| `thesis-approved` | assess-thesis pass | planned; not shipped in 0.5.9 |

The gate is the mechanism that turns a pedagogical constraint into a research variable: the
drafting-unlock threshold is configurable and pre-registerable per experiment (see
[threshold-calibration]).

## Telemetry boundary

| Stream | Records | Explicitly NOT |
|---|---|---|
| `process_signals` | keystroke bursts, paste volume, canvas edit types | authorship detection; no integrity score |
| `transcript` | full LLM agent conversation | — |
| `output` | final submission | — |

Process evidence describes *how* work happened, never *who* did it. There is no
integrity/authorship scoring in the platform (see [essays-workflow]); apparatuses that want to
argue about authorship must build their case from the transcript and process signals as evidence,
not from a platform verdict.

## Versioning contract

- `applies_to` pins the platform version whose behaviour this vocabulary describes.
- Apparatus specs carry their own `version` and `min_platform` — the apparatus version is
  independent of the canvas version.
- Evidence provenance records `apparatus: {id, version, configuration}` + `canvas: {version}` so a
  given result is reproducible against the exact platform and knob set that produced it.

[essays-workflow]: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
