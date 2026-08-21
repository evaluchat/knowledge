---
type: Concept
id: evidence-ledger-and-finding-workflow
title: Evidence Ledger and Finding workflow
description: Draft user-facing overview of creating a scoped Evidence Ledger Snapshot, publishing it, and using published ledgers in a human-authored Finding.
lang: en
origin: native
status: draft
tags: [evidence-ledger, findings, workspace, research, github]
applies_to: "dev@649268e"
stale_after: 2026-09-20
timestamp: 2026-08-20T10:10:33+02:00
source_commit: 649268e
release_channel: dev
generated: { by: codex/gpt-5, at: 2026-08-20T10:10:33+02:00 }
---

# Evidence Ledger and Finding workflow

> User-facing documentation draft. This describes the Evidence Ledger and
> light Finding functionality currently available on the Evaluchat `dev`
> environment at commit `649268e`. Production has not been promoted to this
> version yet.

## The short version

An Evidence Ledger lets you inspect a declared slice of accepted evidence for
one exact Method version. You choose the scope, review the server-calculated
preview, and generate an immutable Ledger Snapshot. You can then publish that
snapshot to the research repository and cite it from a human-authored Finding.

The flow is:

```text
Ledger-ready Method
        ↓
Evidence Ledger configuration
        ↓
Immutable Ledger Snapshot
        ↓
Published Evidence Ledger
        ↓
Finding starter
```

Research questions remain a separate human choice. Evaluchat does not derive
questions from a ledger.

## What each step means

| Step | What you do | What the product records |
| --- | --- | --- |
| Choose a Method | Select one ledger-ready Method version | The exact Method and evidence-template versions, plus the accepted-evidence baseline |
| Set the scope | Use the dimensions declared by that template | A typed filter configuration and its exact predicate |
| Preview | Check the counts and missingness before generating | Server-calculated scope buckets and the current predicate |
| Generate | Create the ledger | A sealed, source-linked Ledger Snapshot with deterministic identity and fingerprints |
| Publish | Confirm access, consent, and anonymisation, then create the PR | A draft or merged research-repository artifact |
| Author a Finding | Write the claim and interpretation yourself, then select merged ledgers | A light Finding draft with references to published Evidence Ledgers |

## Select a ledger-ready Method

Start from **Create workspace item → Evidence Ledger**. The selector lists
Method versions that have both:

- a resolved evidence template; and
- accepted evidence to inspect.

The card shows the Method version, template version, accepted-evidence count,
and either **Ledger ready** or the mechanical reason it is unavailable. The
version is explicit: selecting a different version changes the available
dimensions and clears the current configuration. Earlier generated snapshots
are not changed.

One Ledger is based on one Method version and its one resolved evidence-template
version. To inspect another Method, create another Ledger. A Ledger has no
research-question field.

## Choose a declared scope

The configuration Canvas renders controls from `ledger_dimension` metadata in
the selected evidence template. Depending on the declared field, you can use:

- multi-select controls for enumerated facts; or
- inclusive minimum and maximum values for dates and numbers.

`unknown` is a real recorded value. `unavailable` means that older evidence did
not contain the field; it is not a guessed value. You cannot filter by prose,
outcome, sentiment, or an AI-generated classification.

The **Scope preview** is calculated by the server. It shows the exact predicate
and counts in these buckets:

| Bucket | Meaning |
| --- | --- |
| Included | Evidence that matches the declared filters |
| Outside declared scope | Evidence that does not match the filters |
| Unknown | Evidence with an explicit unknown value for a selected dimension |
| Unavailable | Evidence from before a selected field was available |
| Resolver exclusion | Evidence excluded by the resolver for a mechanical reason |

The **Generate ledger** action is enabled only when the preview matches the
current configuration. Filter values are selected explicitly in the Canvas,
and the server rejects forged or undeclared filter requests.

## Read the Ledger Snapshot

Generating a Ledger creates a read-only snapshot. Its header identifies the
Ledger, Method and template versions, exact predicate, source commit, resolver
and render versions, input fingerprint, generation time, and bucket counts.

The snapshot has five views:

1. **Scope** — what was included and why.
2. **Evidence** — the source-linked contributions in scope.
3. **Descriptive views** — distributions and other descriptive summaries.
4. **Comparability** — warnings about differences that limit comparisons.
5. **Counterevidence & gaps** — contradictions, missing information, and what
   the available record cannot answer.

A Ledger Snapshot is descriptive evidence about a declared scope. It is not a
conclusion, claim, confidence score, causal result, or integrity verdict. The
snapshot cannot be edited after generation.

## Publish a snapshot

Use the **Publish** link on the snapshot. Publishing opens a dedicated,
breadcrumb-navigated page where you reconfirm access, consent, and
anonymisation before any public write. The page reports one of these states:

- **Unpublished** — no publication has been created.
- **Draft PR** — a research-repository pull request exists and still needs its
  eligible merge path completed.
- **Merged** — the Evidence Ledger is now published and can be selected by the
  Finding picker.

Eligible system-generated Ledgers can be automatically approved and merged
when the integrity checks pass. A non-eligible Ledger remains a draft PR for
human merge. A closed publication PR can be republished from the same flow.

## Use a published Ledger in a Finding

The light Finding flow starts from a normal Finding document, not a separate
claim-authoring workbench. The starter provides sections for:

- Claim
- Research questions
- Evidence ledgers
- Declared scope
- Interpretation
- Counterevidence and alternatives
- Limitations

The published-ledger picker lists only merged `Evidence Ledger` artifacts. When
you choose one, it adds a reference card and records its identity, path, Method
and template versions, source commit, and input fingerprint.

You write the claim, choose the research questions, explain the relationship
between the questions and evidence, and record the interpretation. The picker
does not infer research questions from a Ledger, and the Finding flow does not
assign a claim or tier using AI.

Before publication, linking validation checks that every selected Ledger is a
merged `Evidence Ledger` with matching Method/template identity,
`source_commit`, and `input_fingerprint`. Each declared research question must
also resolve to a published Research Question artifact.

## What this functionality does not do

- It does not turn a Ledger into a conclusion or a Finding.
- It does not derive research questions from evidence.
- It does not search prose for unsupported filters.
- It does not silently treat `unknown` or `unavailable` as a known value.
- It does not let the assistant edit a configuration, snapshot, or Finding.
- It does not make a human review or publication decision on your behalf.

## Related documentation

- [Researcher workflow: from Evidence Ledger to Finding](/playbooks/evidence-ledger-to-finding.en.md)
- [Evidence Ledger workspace and light Finding authoring](/designs/finding-authoring-ux.en.md)
- [Finding authoring — evidence ledgers and human-controlled claims](/designs/finding-authoring.en.md)
