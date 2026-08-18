---
type: Concept
id: evidence-contribution
lang: en
origin: native
status: stable
title: 'Evidence contribution — filing a concluded run to research'
description: 'How the Evaluchat workspace Evidence action turns a concluded method run into an owned canvas thread, captures frozen-run provenance beside typed owner judgements, and files a single consent-checked Evidence Contribution into the research catalog via a bot-authored PR — as shipped.'
tags: [evaluchat, evidence, methods, workspace, research, github, okf]
applies_to: 0.5.9
sources:
  - id: evidence-roles
    resource: https://github.com/evaluchat/research/blob/main/governance/evidence-roles.en.md
    title: 'Shared evidence roles — how every method files a run (research catalog)'
  - id: contribution-ladder
    resource: https://github.com/evaluchat/research/blob/main/governance/contribution-ladder.en.md
    title: 'The contribution ladder — how teachers contribute to research'
  - id: method-recipe
    resource: https://github.com/evaluchat/knowledge/blob/main/playbooks/method-recipe.en.md
    title: 'The method recipe — from research question to published method'
  - id: evidence-publishing-design
    resource: https://github.com/evaluchat/knowledge/blob/main/designs/evidence-publishing.en.md
    title: 'Evidence publishing mechanics — design decisions'
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-18T15:00:00Z
---

> This is the implementation source of truth for the workspace **Evidence**
> action as shipped on the Canvas dev line (0.5.9). It graduates the
> [evidence-publishing design][evidence-publishing-design] (draft) into a
> shipped-product concept. It describes what the product does; claims about
> learning effects remain the research catalog's business, not this one.

# Evidence contribution — filing a concluded run to research

> **Applies to:** Canvas apps/web **0.5.9** (dev line), the Evaluchat public
> beta environment. The Evidence action is implemented and E2E-verified on the
> dev line; production cutover of this build was still in progress at the time
> of writing.

## Overview

When a method run concludes, a teacher or researcher can turn it into a
**research evidence contribution** without leaving the canvas. The workspace
**Evidence** button on a concluded method item opens an *owned canvas thread*
pre-filled from the run's **frozen snapshot** — the method identity and the
levers the run actually used, the canvas version, and the run's timing and
collection counts. The owner fills the subjective fields (context, narrative
observations, missing data, reflection, limitations) and declares a consent and
anonymisation status. On submit, the server assembles one timestamped
`Evidence Contribution` document and files it into the research catalog via a
**bot-authored pull request** (Valery Bot.ha).

The design goal is that **provenance is derived, never typed**: the machine
records what actually happened from the frozen run, and the human records what
they observed and judged. The product never implies an evidence contribution is
peer-reviewed research — a declared `stage` routes anything above
*documented-experience* to independent human review, and nothing stronger than
the evidence (and its consent record) is ever published.

## The Evidence button and the evidence thread

- On a **concluded method workspace item**, an **Evidence** action creates a
  canvas thread bound to that item. The thread's document content is the
  method's `evidence_template`, resolved from the apparatus catalog entry — the
  platform renders **exactly the template of the method version the run used**
  (no drift, no cross-version mixing). Launch is canonical; there are no UI
  dropdowns for choosing a template.
- The thread is an **owned thread, not a workspace item**: it uses the same
  server-stamped ownership markers as any workspace thread, but it is **not
  entered into the workspace manifest** and not listed as a workspace item.
  The method item stores an `evidenceThreads` reference (thread id + status)
  so the owner can resume an in-progress evidence thread.
- The thread's status lifecycle is `draft → submitted → filed`. A `submitted`
  or `filed` thread **locks**: editable fields become read-only and the
  values-persistence write stops, so a filed contribution cannot be silently
  mutated.

## Form-aware canvas: frozen provenance beside typed judgement

The evidence template is a **mixed-authority form**. Two kinds of fields:

1. **Frozen-run (read-only) fields** — server-resolved from the stamped run
   snapshot and rendered read-only (`read_only: true` plus a `source:` path).
   For the canonical `ai-assisted-essay` template these include: method id and
   version, the workspace-item GUID, profile id, the **resolved levers as
   actually run**, canvas version, started/concluded timestamps, participant
   and collection counts, and — where that run recorded them — analytics,
   process-signal, and assignment-outcome summaries plus the transcript
   retention declaration. The owner cannot edit these. **Provenance is
   derived, never typed.**
2. **Owner-editable field** — typed by declared field type (`text`, `textarea`,
   `select`, `number`, `date`): institution and classroom context, assignment
   genre, learner proficiency/age band, instruction and writing language,
   implementation duration and deviation, narrative observations, results,
   missing data, reflection, limitations, and the contribution role fields
   (stage + consent/anonymisation) below. Typed fields are the contract —
   ordinal owner judgements use named, versioned options, never free prose
   where a typed field is declared.

The template's `layoutMarkdown` is what the canvas renders (the evidence-role
sections plus a "Results — missing or unavailable data" section), and its
`assistant.guidance` feeds the writing agent via the proxy: help the owner
describe **only their concluded run**, never infer, invent, or expose student
information, and **render the frozen system-authored fields exactly as
provided** — never altering, duplicating, or adding system measurements.

Unavailable telemetry is handled honestly: a frozen field whose value the run
did not record is rendered as **"not recorded"**, never invented — this is
what the "missing or unavailable data" section is for.

## Consent and anonymisation gates

Submission is gated on explicit, machine-checkable declarations. Required
fields include `contribution_stage`, `publication_authorisation`,
`anonymisation_status`, and `data_sharing_limits`. A **negative or uncertain
privacy declaration blocks submission** — the owner cannot file evidence that
is not explicitly cleared to publish and to share.

## Submit → Evidence Contribution → bot PR

On submit the server (Valery Bot.ha, using a scoped GitHub token) assembles a
**single markdown file** at `methods/<id>/evidence/<ISO-timestamp>.en.md`:

- frontmatter with `type: Evidence Contribution`, `id` = the timestamp slug,
  `lang: en`, `status: draft`, `stage` (the declared contribution stage),
  `generated.by` (with AI-assistance disclosure where the assistant helped
  draft), the consent keys (`publication_authorisation`,
  `anonymisation_status`, `data_sharing_limits`), and
  `method: {id, version, levers, canvas}` provenance;
- the filled evidence-role sections;
- the provenance block.

The server opens a **pull request** into the configured destination repo
(default `evaluchat/research`; private-repo destinations later use the same
flow). The research `okf-lint` CI runs on the PR. One of two outcomes:

- **Auto-merge** — only when all of: provenance + consent declarations are
  present and machine-checked, the declared `stage` ≤ *documented-experience*,
  and `okf-lint` passes. The control that justifies skipping manual approval is
  the baked-in provenance/consent/stage validation, not "trust the bot".
- **Human review** — anything above *documented-experience* (e.g. a teacher
  declaring a *structured experiment*), or a failed machine check, routes to
  the independent human review protocol, with a bot comment explaining why.

After a successful merge the evidence thread's status becomes `filed` and the
method item records the evidence-contribution URL.

## What this feature is not

- It does **not** merge dev/test data into the public catalog: on a dev or test
  run the owner declares a stage above *documented-experience* so the bot opens
  the PR for human review and the test PR can be closed, never merged.
- It does **not** publish research claims: a `stage` above the evidence is
  routed to human review, AI may only draft structure (disclosed via
  `generated.by`), and the contribution — with its consent record — is the
  workspace owner's.
- It is **not** a platform-owned evidence database: publication is a GitHub PR
  into the research catalog, which remains the source of truth.
- It does **not** conduct synthesis or A/B analysis. A single-case, subjective
  teacher questionnaire can be filed as a *documented experience*; finding
  authoring is a separate, later design.

## Status and versioning

This concept pins `applies_to: 0.5.9`, the Canvas apps/web version on the dev
line on which the Evidence action shipped. It describes behaviour as shipped in
that build; newer versions may change behaviour. Treat this concept as **stale**
once the pinned version is superseded by a release that changes the behaviour
described here, and update via a pull request to the knowledge repository.

The companion decision record remains [designs/evidence-publishing.en.md][evidence-publishing-design]
(draft), which captures the agreed mechanics and open forks not yet built.

[evidence-publishing-design]: https://github.com/evaluchat/knowledge/blob/main/designs/evidence-publishing.en.md
