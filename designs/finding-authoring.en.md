---
type: Concept
id: finding-authoring
title: Finding authoring — evidence ledgers and human-controlled claims
description: "Design: an on-demand, immutable evidence ledger gives a finding author a source-linked descriptive analysis of a research-question snapshot, while the finding remains human-authored and AI is limited to non-editing advice and challenge checks."
lang: en
origin: native
status: draft
tags: [design, findings, evidence-ledger, research, ai-assistance, human-review, okf]
applies_to: 0.5.9
timestamp: 2026-08-17T15:21:42Z
generated: { by: codex/gpt-5, at: 2026-08-17T15:21:42Z }
sources:
  - id: evidence-publishing
    resource: https://github.com/evaluchat/knowledge/blob/main/designs/evidence-publishing.en.md
    title: Evidence publishing mechanics — the workspace Evidence action
  - id: research-method
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/research-method.en.md
    title: Research method — how methods use platform capabilities and levers
  - id: measuring-subjective-evidence
    resource: https://github.com/evaluchat/knowledge/blob/main/references/how-to-measure-anything-evidence.md
    title: Measuring Subjective Evidence — Hubbard Reference
  - id: review-protocol
    resource: https://github.com/evaluchat/research/blob/main/governance/review-protocol.en.md
    title: Claim governance — review protocol for findings
---

# Finding authoring — evidence ledgers and human-controlled claims

> Design note (2026-08-17, decision-record status: draft). This is the
> downstream companion to [evidence publishing](evidence-publishing.en.md): it
> turns a set of filed evidence contributions into an inspectable analysis
> surface without allowing an AI assistant to author or approve a finding.

## 1. Problem

Evidence filing makes individual, bounded reports public and comparable. It
does not make twenty submitted reports easy to inspect together. A finding
author needs an accurate answer to basic questions before writing a claim:

- Which evidence contributions addressed this research question at this time?
- Which ones were excluded, missing, challenged, non-comparable, or from the
  same contributor or context?
- What do the structured response distributions and recorded contexts show?
- Which observations or limitations contradict the pattern the author is
  considering?

An AI can help retrieve, tabulate, and challenge an answer, but neither a
system prompt nor a fluent summary makes it impartial. Selecting a claim,
deciding whether evidence is comparable, interpreting a pattern, and accepting
the finding’s scope remain accountable human research decisions.

## 2. Decisions

1. **Ledger before finding.** A finding-authoring session starts from a dated,
   immutable Evidence Ledger for a selected research question. The ledger is a
   descriptive analysis record, never a finding.
2. **On-demand and freshness-gated.** A user explicitly creates a ledger. The
   platform offers the latest ledger only when its input fingerprint matches;
   if any eligible evidence was added, removed, or changed, it offers a new
   ledger instead and marks older ones stale for that scope.
3. **Complete accounting, not a curated sample.** The ledger records every
   eligible contribution in scope and every exclusion with its mechanical
   reason. It never silently omits negative, challenging, incomplete, or
   non-comparable evidence.
4. **AI may analyse and advise, never edit a finding.** The assistant may
   create the ledger, answer questions about it, and test a human-proposed
   claim or challenge. It has no canvas-write, commit, PR, tier, review, or
   publication capability for the finding document.
5. **Findings stay human documents.** The author starts from a basic finding
   skeleton or a copy of an existing finding as a new revision. Only the human
   types or accepts edits. The existing published finding is never overwritten.
6. **Protocol still governs publication.** The deterministic claim checker and
   the Research review protocol determine formal completeness and routing. A
   ledger cannot promote a tier, approve a claim, or substitute for review.

## 3. The two artifacts

| Artifact | Purpose | Authority | Mutability | Publication meaning |
| --- | --- | --- | --- | --- |
| **Evidence Ledger** | Source-linked inventory and descriptive analysis of one evidence snapshot | Platform creates the manifest; AI may render the analysis | Immutable after creation; human annotations live separately | Audit material, not a finding or verdict |
| **Finding draft** | A human’s claim, scope, interpretation, limitations, and review request | Human author | Human-editable only; a published finding is revised by copy | Candidate Research finding, subject to the existing protocol |

```text
Accepted evidence indexed by question
        │
        ▼
Deterministic scope + input fingerprint ── unchanged ──► reopen latest ledger
        │ changed
        ▼
Timestamped Evidence Ledger (immutable, source-linked)
        │
        ├── AI: descriptive analysis + claim/challenge advice only
        ▼
Human-only Finding draft (new skeleton or revision copy)
        │
        ▼
Claim checker + human review + PR workflow
```

### 3.1 Evidence Ledger

The platform creates a ledger from public, indexed evidence that resolves to
the selected research question. It may include twenty evidence contributions
or any other number; no arbitrary count is a substitute for the contribution
ladder’s tier and independence requirements.

The ledger has a timestamped identity and an **input fingerprint** over a
canonical, sorted manifest. At minimum the manifest records:

| Ledger field | Purpose |
| --- | --- |
| `research_question` and question version/path | Declares the question the ledger serves |
| `created_at`, repository commit, resolver and ledger-template versions | Reproduces the time, source state, and mechanism |
| Included contributions | Path/ID, content or Git blob hash, method/version, stage, contributor/context grouping, and applicable resolved levers |
| Excluded candidates | Path/ID and mechanical reason: unlinked question, invalid/missing provenance, out-of-scope filter, inaccessible, or not yet accepted |
| Query and scope | Method, version, date, stage, language, and context filters; no hidden ranking or relevance filter |
| Input fingerprint | Detects additions, removals, or changes after the ledger was made |
| Prompt and model policy versions | Makes AI-assisted rendering inspectable without treating it as verification |

The rendered ledger contains only descriptive, source-linked material:

- inventory, inclusion/exclusion counts, missingness, and contribution stages;
- distributions of versioned structured items, retaining `not-applicable` and
  `insufficient-information` responses;
- method versions, resolved levers, settings, contributor/context clustering,
  and comparability warnings;
- explicitly labelled owner observations and reflections, with a transparent
  narrative-coding record if they are grouped;
- a counterevidence register: negative responses, challenges, contradictions,
  and plausible alternative explanations; and
- evidence gaps and questions that the available record cannot answer.

It must not contain a finding, an efficacy conclusion, a causal inference, a
teacher-population claim, an integrity verdict, or an undisclosed inference
from prose. Every non-trivial displayed value links to the included source
record(s), calculation, or explicit `insufficient evidence` state.

### 3.2 Freshness and archival

Ledger creation is on-demand, not a background auto-publication job. Before
opening the session, the resolver recomputes the canonical manifest for the
requested question and scope.

- **Same fingerprint:** reopen the existing ledger, preserving its timestamp.
- **Different fingerprint:** show that evidence has changed and offer a new
  ledger. The prior ledger remains readable, labelled with its old scope.
- **No eligible evidence:** create no analytic summary; explain what is missing
  and link the author back to the evidence collection path.

The live ledger is a protected canvas thread owned by the author and their
organisation. When a human submits a finding for review, the exact ledger
manifest and rendered ledger are attached to the review packet or exported as
a timestamped, source-linked analysis artifact. The repository placement for
that archival copy is an implementation decision, but its content and input
fingerprint must not change after the finding review begins.

## 4. Finding-authoring session

The author opens a second canvas document from either:

- a basic **Finding skeleton** with headings for claim, scope, evidence,
  limitations, alternatives, and review; or
- a **revision copy** of an existing finding, with a visible predecessor link
  and no mutation of the published source.

The finding starts with a reference to the chosen ledger, but this reference
does not assert that the ledger supports any particular claim. The human must
write the claim, define the scope, decide which evidence is comparable, explain
their interpretation, and choose whether to seek review or publication.

### 4.1 Assistant contract

The assistant receives the immutable ledger and, only when the human asks, the
specific draft passage or proposed claim they want checked. It may:

- locate and explain cited evidence, distributions, missingness, and methods;
- build a claim-coverage table linking a *human-proposed* statement to
  supporting, contradicting, and insufficient evidence;
- identify scope drift, causal language, selection bias, non-independence,
  unreported `not-applicable` responses, and omitted counterexamples;
- propose review questions and explain the contribution-ladder or claim-checker
  requirements; and
- help the author record a challenge or an uncertainty without resolving it.

It may not:

- write into the finding canvas, amend a published finding, or submit a PR;
- choose the finding’s claim, evidence subset, tier, status, authors, or review
  outcome;
- represent evidence as proof, fill gaps with plausible detail, or suppress
  contradictory evidence; or
- make an ethical, scientific, or publication decision on the human’s behalf.

The UI enforces this with read-only AI access to the finding document and
separate advice responses: there is no assistant edit, patch, save, or publish
tool for the finding. If a human later incorporates AI-generated language or
analysis materially, the finding records the required `generated.by`
disclosure; human authorship and human review remain distinct from that
disclosure.

### 4.2 Prompt and output controls

A system prompt is necessary but insufficient. The implementation couples it
with deterministic source and citation controls:

1. The assistant may use only the selected ledger, its frozen manifest, and
   source records referenced by that manifest; it has no unbounded repository
   or web search context.
2. It must label each response as **descriptive**, **challenge**,
   **insufficient evidence**, or **human decision required**. It must cite the
   ledger source IDs for factual assertions.
3. It must return counterevidence and limitations before a positive pattern,
   and say when a requested comparison is not valid.
4. A deterministic post-check rejects source references outside the manifest
   and marks advice with unresolved citations as unusable.
5. The session stores the policy, model, prompt-template, ledger fingerprint,
   and response IDs so a reviewer can inspect the assistance trail.

These controls reduce silent cherry-picking and invented evidence; they do not
turn model output into an impartial verdict.

## 5. Review and challenge behaviour

The existing Research review protocol remains authoritative. The ledger should
make its requirements easier to inspect, not duplicate or override them.

| Situation | Required behaviour |
| --- | --- |
| New or modified in-scope evidence after the ledger | Mark the finding draft stale; require a refreshed ledger or a human-recorded exclusion rationale before review proceeds |
| Open challenge or contradiction | Put it in the ledger’s counterevidence register and show it in claim advice; never hide it to improve a claim |
| Human requests a causal, universal, or efficacy claim | Explain that the ledger cannot establish it and route to the relevant research design and human review requirements |
| Finding reaches `supported` | Human review remains mandatory; no ledger or AI output can auto-approve it |
| AI-assisted text materially affects the finding | Preserve the human `authors` record and add the required generation disclosure; disclose assistance to reviewers |

## 6. Non-goals

- This is not automated research adjudication, peer review, or a truth engine.
- It does not make twenty voluntary documented experiences representative,
  independent, causal, or sufficient for a supported finding.
- It does not read raw student work, raw transcripts, private analytics, or
  unmerged submissions into an authoring session.
- It does not replace the method evidence contract, contribution ladder,
  challenge process, deterministic claim checker, or human accountability.

## 7. Delivery sequence

1. Define the canonical evidence resolver and manifest/fingerprint format.
2. Implement protected, timestamped ledger threads and source-linked
   descriptive renderer.
3. Add freshness detection and the no-new-evidence/reopen-latest decision.
4. Implement a human-only Finding skeleton/revision canvas and read-only AI
   advice surface.
5. Add citation, counterevidence, and stale-ledger checks to the claim-review
   packet; decide the Research archival location for ledger snapshots.
6. Test with synthetic evidence sets containing contradictory, missing,
   non-comparable, and clustered contributions before using classroom evidence.

# Citations

[1] [Evidence publishing mechanics](evidence-publishing.en.md)

[2] [Claim governance — review protocol for findings](https://github.com/evaluchat/research/blob/main/governance/review-protocol.en.md)

[3] [Measuring Subjective Evidence — Hubbard Reference](https://github.com/evaluchat/knowledge/blob/main/references/how-to-measure-anything-evidence.md)
