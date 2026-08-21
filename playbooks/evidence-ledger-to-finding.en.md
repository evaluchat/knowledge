---
type: Playbook
id: evidence-ledger-to-finding
title: "Researcher workflow: from Evidence Ledger to Finding"
description: Draft task guide for selecting a Method, generating and publishing an Evidence Ledger Snapshot, and using it in a human-authored Finding.
lang: en
origin: native
status: draft
tags: [evidence-ledger, findings, workflow, researcher, workspace]
applies_to: "dev@649268e"
stale_after: 2026-09-20
timestamp: 2026-08-20T10:10:33+02:00
source_commit: 649268e
release_channel: dev
generated: { by: codex/gpt-5, at: 2026-08-20T10:10:33+02:00 }
---

# Researcher workflow: from Evidence Ledger to Finding

> Draft task guide for the Evaluchat `dev` environment. The screens and
> labels described here correspond to commit `649268e`; production has not yet
> been promoted to this version.

## Before you start

To create a useful Ledger, you need a published Method version with a resolved
evidence template and accepted evidence. If you intend to publish, make sure
you have the required repository access and can make the consent and
anonymisation confirmations truthfully.

Keep your research questions separate. Choose them independently for the later
Finding; the Ledger flow will not choose or suggest them as part of generation.

## 1. Create an Evidence Ledger

1. Open **Create workspace item**.
2. Choose **Evidence Ledger**.
3. Select a Method card marked **Ledger ready**.
4. Confirm the Method version, evidence-template version, and accepted-evidence
   baseline count.

If a Method is unavailable, read the reason shown on its card. You cannot
bypass the selector by entering a Method ID, and a missing template or empty
accepted-evidence set cannot produce a Ledger.

## 2. Configure and check the scope

The configuration Canvas shows the fixed Method/template identity and controls
for the template's declared ledger dimensions.

1. Choose values in the multi-select controls, or enter inclusive minimum and
   maximum values for declared date/number fields.
2. Treat `unknown` as an explicit value when it is offered.
3. Read `unavailable` as “this field was not present in that historical
   evidence,” not as a value to guess.
4. Review the **Scope preview** and its exact predicate.
5. Check the count in every bucket before generating.

The preview accounts for **Included**, **Outside declared scope**, **Unknown**,
**Unavailable**, and **Resolver exclusion**. If the preview is stale after a
filter change, **Generate ledger** remains unavailable until the server has
recomputed it.

Do not expect controls for narrative prose, outcomes, sentiment, or
AI-generated classifications. They are outside this Ledger's declared scope.

## 3. Generate and inspect the snapshot

Select **Generate ledger** once the preview represents the scope you want. The
result is a sealed, read-only Ledger Snapshot.

Work through the five views:

| View | Check |
| --- | --- |
| Scope | Does the predicate and bucket accounting describe the intended slice? |
| Evidence | Can you follow the included contributions back to their sources? |
| Descriptive views | What distributions or patterns are actually present? |
| Comparability | Which differences make a comparison unsafe or limited? |
| Counterevidence & gaps | What contradicts a simple reading, and what remains unanswered? |

Also check the sealed header for the Method/template versions, source commit,
input fingerprint, resolver/render versions, and generation time. These values
help you identify exactly which evidence the snapshot describes.

Remember that the snapshot is not a conclusion, claim, confidence score,
causal result, or integrity verdict. There are no edit controls because the
snapshot is immutable.

## 4. Publish the selected snapshot

1. Select **Publish** from the snapshot.
2. On the dedicated Publish page, review the breadcrumb and full-page status.
3. Complete the access, consent, and anonymisation confirmations.
4. Select **Create draft PR**.
5. Follow the publication status until it is **Merged** if you want to use the
   Ledger in the Finding picker.

The flow may auto-approve and auto-merge an eligible system-generated Ledger
after its integrity checks pass. Otherwise, the publication remains a draft PR
for human merge. Only a merged Ledger is available to the Finding picker.

If a previous PR was closed, use the publication flow to create a new one.

## 5. Start the Finding draft

Create a Finding using the light Finding starter. Write the human-controlled
parts yourself:

1. State the claim you want to examine.
2. Select one or more published research questions.
3. Use the published-ledger picker to add one or more merged Ledgers.
4. Describe the declared scope and how it relates to the questions.
5. Write your interpretation.
6. Record counterevidence, alternative explanations, and limitations.

The picker inserts a reference card and the Ledger's identity, path,
Method/template identity, source commit, and input fingerprint. It does not
turn the reference into support for your claim automatically. There is no
required one-to-one mapping between research questions and Ledgers in this
light flow; explain the relationship in your own scope and interpretation.

## 6. Resolve validation messages

Before a Finding can be published, linking validation checks the references you
selected:

- a Ledger path must resolve to a merged `type: Evidence Ledger` artifact;
- its Method and evidence-template identity must match the reference;
- its `source_commit` and `input_fingerprint` must be present and matching; and
- each declared research question must resolve to a published Research
  Question artifact.

If validation fails, return to the publication status or picker rather than
editing provenance by hand. A Ledger that has not merged is not yet a published
source.

## Expected boundaries

The workflow keeps scope and publication decisions explicit. It does not let
an assistant change filters, generate or publish a Ledger, choose your Finding
claim, derive research questions, or decide a review outcome.

## Related documentation

- [Evidence Ledger and Finding workflow](/concepts/evidence-ledger-and-finding-workflow.en.md)
- [Evidence Ledger workspace and light Finding authoring](/designs/finding-authoring-ux.en.md)
