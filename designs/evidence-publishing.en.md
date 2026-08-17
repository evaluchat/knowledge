---
type: Concept
id: evidence-publishing
title: Evidence publishing mechanics — the workspace Evidence action
description: "Design: evidence definition becomes an integral, required part of every Method; the workspace Evidence action renders a versioned Form Template and files its completed evidence packet as a single timestamped document into the method's evidence directory via a bot-authored PR."
lang: en
origin: native
status: draft
tags: [design, evidence, methods, workspace, github, okf]
applies_to: 0.5.9
timestamp: 2026-08-17T15:21:42Z
generated: { by: codex/gpt-5, at: 2026-08-17T15:21:42Z }
sources:
  - id: evidence-roles
    resource: https://github.com/evaluchat/research/blob/main/governance/evidence-roles.en.md
    title: Shared evidence roles — how every method files a run (research catalog)
  - id: contribution-ladder
    resource: https://github.com/evaluchat/research/blob/main/governance/contribution-ladder.en.md
    title: The contribution ladder — how teachers contribute to research
  - id: method-recipe
    resource: https://github.com/evaluchat/knowledge/blob/main/playbooks/method-recipe.en.md
    title: The method recipe — from research question to published method
  - id: platform-capabilities
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/platform-capabilities.en.md
    title: Platform capabilities — public-beta runtime contract
  - id: measuring-subjective-evidence
    resource: https://github.com/evaluchat/knowledge/blob/main/references/how-to-measure-anything-evidence.md
    title: Measuring Subjective Evidence — Hubbard Reference
---

# Evidence publishing mechanics

> Design note (2026-08-17, decision-record status: draft). This document captures agreed
> design decisions for making evidence filing an integral, default part of the workspace
> method lifecycle. Design only — no implementation exists yet.

## 1. Problem

Methods publish to `evaluchat/research` today without an enforceable evidence contract, and
filing evidence is a manual, human-only task (a contributor copies an `evidence-template/`
directory and fills eight role files by hand). The platform has no A/B machinery and, for the
assignment stress test in particular, evidence is inherently a single-case, subjective
teacher/researcher questionnaire — one assignment evaluated at a time. There is no product
surface that turns a concluded method run into a filed evidence bundle.

Goals (per Cronje, 2026-08-17):

1. **Evidence definition becomes an integral part of the method** and a hard prerequisite for
   publishing the method.
2. **Filing evidence becomes a default feature of the workspace item lifecycle** — an "Evidence"
   action on a workspace item of kind `method` that instantiates the method's evidence template
   and, on submit, files the completed document into the method's evidence directory
   (`methods/<id>/evidence/`).
3. Publication goes through GitHub (private repos first-class in future, a path to public
   sharing), not a platform-owned database.

## 2. Decisions (Cronje, 2026-08-17)

1. **Single file**: one `evidence-template.en.md` per method, at
   `methods/<id>/evidence-template.en.md`, replacing the current `evidence-template/` directory
   (eight role files + index collapse into one structured markdown document). The English suffix
   follows the Research catalog’s settled filename convention.
2. **Instantiation**: the Evidence button on an existing method workspace item creates a **canvas
   thread** from the Form Template — a form-aware canvas editing experience, except the thread is
   **not a separate workspace item** (not listed in the workspace manifest). Frozen run values are
   read-only fields; owner judgements use reviewed typed fields, including prose textareas.
3. **Submit**: after the template's sections are filled in, submit opens a **PR** into the research
   repo, creating an instance under `methods/<id>/evidence/` — minimally **one file, a timestamp
   with `.md` extension**. PR always; a rule may skip manual PR approval for system-orchestrated
   submissions whose controls are baked into the process.
4. **Slug**: timestamp, optionally linked to the workspace-item GUID. No PII in the GUID; access
   security comes from ownership enforcement, not from GUID secrecy.
5. **Bot identity**: Valery Bot.ha.

## 3. Resulting shape

```
methods/<id>/
  <id>.en.md            # method spec — declares evidence_template
  evidence-template.en.md  # NEW single-file, versioned Form Template
  evidence/
    index.md            # existing registry (unchanged)
    2026-08-17T14-30-00Z.md   # filed instances, timestamp-slugged
```

### 3.1 `evidence-template.en.md`

A single markdown document with YAML frontmatter (the pinned contract), declared Form Template
fields, and body sections for the eight evidence roles. It is a mixed-authority form: trusted
system fields are frozen from the concluded run; typed owner fields capture the subjective evidence
that may later be aggregated. Frontmatter (illustrative):

```yaml
type: Form Template
id: evidence-template
version: 1.0.0
lang: en
locale: en
template_kind: form
applies_to_method: ai-assignment-stress-test@0.1.0
default_stage: documented-experience
fields:
  method_id:
    type: text
    read_only: true
    source: frozen_run.method.id
  threshold_fit:
    type: select
    options: [much-too-low, about-right, much-too-high, insufficient-information]
  observations:
    type: textarea
generated: { by: <producer>, at: <iso> }   # AI-assistance disclosure when applicable
```

Body sections render the declared `{{field}}` values and map to the evidence roles:

- **Question** — the research question this method serves (pre-filled, read-only link).
- **Context** — typed discipline, task genre, proficiency and institution context plus a bounded
  narrative context. No student identifiers.
- **Intervention** — resolved levers (pre-filled), assignment artefact reference, probe protocol.
- **Observations** — teacher/researcher narrative, verbatim, any language.
- **Results** — system-authored, method-defined structured measurements (pinned per method
  version) and explicit missing-data record.
- **Reflection** — interpretation, kept separate from observations.
- **Limitations** — scope, missing data, competing explanations.
- **Provenance** — consent + anonymisation declarations (mandatory), `method: {id, version,
  levers, canvas}` (pre-filled, read-only, from the frozen run snapshot).
- **Stage** — contribution-ladder rung the contributor declares.

The Form Template renderer uses the declared field types (`select`, `number`, `date`, `text`, and
`textarea`) and requiredness. Narrative evidence remains prose in designated textareas; ordinal
owner judgements use named, versioned options so later work can retain their distribution instead
of inferring a score from prose. The `assistant.guidance` is a protected instruction that preserves
the system/owner and observation/reflection boundaries.

### 3.2 The Evidence button → canvas thread

- On a workspace item of kind `method` (a concluded run), an **Evidence** action creates a canvas
  thread bound to that item.
- The thread's document content = the method's `evidence-template.en.md`, with its read-only
  fields **pre-filled from the frozen run snapshot**: method id/version, resolved levers (as
  actually run, not the current default profile), canvas version, question links, collection
  denominator, and permitted aggregate analytics. The owner cannot edit these — provenance is
  derived, never typed.
- The thread is **owned by the method item's owner and the org**, exactly like any existing
  workspace thread (`withOwnedThreadMetadata` ownership markers), but it is **not entered into
  the manifest** / not listed as a workspace item.
- The method item stores an `evidenceThreads` reference (thread id + status) so the UI can
  resume/reopen an in-progress evidence thread.
- **GUID access safety**: the workspace-item GUID is already high-entropy (`wi_...`) and thread
  access is already governed by server-stamped ownership metadata in the proxy
  (`withOwnedThreadMetadata` path) — not by guessing. The evidence thread uses the same
  enforcement: a user can only open an evidence thread whose ownership markers match their own
  account. The GUID appears in the evidence filename/PR only as a traceable reference to the run;
  it is not an access token, and ownership checks apply to both the evidence thread and the run
  item it cites, so no cross-user lookup is possible through it.

### 3.3 Submit → PR → file

1. **Submit** on the evidence canvas validates: public-contribution authorisation is confirmed,
   anonymisation is confirmed, required fields are complete, and the system-authored provenance
   block is present. A negative or uncertain privacy declaration blocks submission.
2. The submit assembles a **single markdown file**:
   `methods/<id>/evidence/<ISO-timestamp>.md` — frontmatter (type, id, lang, affected-run GUID,
   `stage`, `generated.by` incl. AI-assistance disclosure if the assistant helped draft) + the
   filled sections + the provenance block.
3. The server (Valery Bot.ha) opens a **PR** into the configured destination repo (default
   `evaluchat/research`; private repo destination later, same flow).
4. On PR open, okf-lint CI runs. **Auto-merge rule** (system-orchestrated submissions): if
   (a) provenance + consent declarations are present and machine-checked, (b) the bundle's
   declared stage ≤ documented-experience, (c) okf-lint passes, then the bot may merge the PR
   without manual approval. Anything above documented-experience (e.g. a teacher declaring a
   structured experiment) routes to the human review protocol. The control that justifies
   skipping approval is the baked-in provenance/consent/stage validation, not "trust the bot".
5. The evidence thread's status updates to `filed (PR merged)` with the PR URL; the method item
   records the evidence contribution URL.

### 3.4 Catalog mirroring (platform side)

- The catalog generator mirrors `evidence_template` (id, version, source content) into the
  generated method entry — same pattern as `run_brief_template`. The Evidence button resolves the
  template from the catalog entry, so the platform renders exactly the template of the method
  **version** the run used (no drift, no cross-version mixing).
- The build-time validator requires a valid evidence template: a method without one cannot ship in
  the catalog. Research-side okf-lint enforces the same for method PRs. Two-sided gate — matches
  "prerequisite before publishing".

## 4. What this design does NOT do

- Files documented-experience bundles (one assignment, human narrative). No synthesis, no A/B, no
  hidden measurement. [Finding authoring](finding-authoring.en.md) is the separate downstream
  design for source-linked analysis and human-controlled finding drafts.
- No claim stronger than the evidence: `stage` routes anything above documented-experience to the
  existing review protocol. AI may draft structure (disclosed via `generated.by`) but the
  contribution is the workspace owner's; claims/interpretation remain human.
- No platform-owned evidence database; publication is a GitHub PR into the research catalog.

## 5. Remaining fork

1. Auto-merge scope: documented-experience-and-below only; structured experiments require human
   review.

## 6. Sequencing (when design is settled)

1. Research repo: single-file `evidence-template.en.md` convention + `evidence_template:` pointer in
   method frontmatter + okf-lint gate.
2. Research repo: migrate the remaining methods to `evidence-template.en.md`; the first typed
   template is `ai-assisted-essay`.
3. Platform: catalog generator mirrors evidence template; validator requires it.
4. Platform: Evidence button → owned canvas thread (not manifest-listed) + submit assembler + bot
   PR + auto-merge rule.
5. Private repo destination + public promotion step.
