---
type: Concept
id: overview
lang: en
origin: native
status: stable
title: 'Evaluchat — open research infrastructure for AI in education'
description: 'A reader-facing introduction to Evaluchat: an open-source, Markdown-native workspace for defining, running, and inspecting research methods about AI in education, with human-authored findings.'
tags: [evaluchat, documentation, overview, research, ai-in-education, open-source]
timestamp: 2026-08-20T11:51:54+02:00
generated:
  by: codex/gpt-5
  at: 2026-08-20T11:51:54+02:00
sources:
  - id: evaluchat-dev-site
    resource: https://dev.evaluchat.org/
    title: 'Evaluchat dev site'
  - id: research-catalog
    resource: https://research.evaluchat.org/
    title: 'Evaluchat research catalog'
  - id: research-method
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/research-method.en.md
    title: 'Research method — how methods use platform capabilities and levers'
  - id: evidence-ledger-and-finding-workflow
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/evidence-ledger-and-finding-workflow.en.md
    title: 'Evidence Ledger and Finding workflow'
---

# Evaluchat — open research infrastructure for AI in education

Evaluchat is an **open-source research platform for AI in education**. It is a
Markdown-native workspace where researchers, teachers, builders, and
policymakers can define, run, inspect, and improve methods for investigating
how education changes when AI is available.

When AI is part of the work, a completed answer is not enough evidence on its
own. It may not show what someone understood, decided, explained, or could do
without assistance. Evaluchat does not prescribe an answer to those questions.
It makes competing approaches visible, testable, and open to challenge.

Methods, their settings, and the evidence they generate are versioned and
inspectable. People—not the platform or an AI assistant—remain responsible for
research questions, interpretation, findings, and review. The goal is public,
collaborative, and accessible research infrastructure that lets evidence travel
between classrooms, research, policy, and product work.

## The research cycle

Evaluchat supports a continuing research cycle rather than a one-way data
pipeline:

```text
Theory
  → Research question
    → Method + evidence template
      → Evidence generation
        → Evidence Ledger
          → Human-authored findings
            → Research questions and theory
```

Each stage has a distinct job:

| Stage | Role in the cycle |
| --- | --- |
| **Theory** | Offers constructs and possible explanations. It remains open to challenge rather than becoming a platform assumption. |
| **Research question** | States what is being investigated. Questions belong in the [research catalog][research-catalog], not in a workspace configuration. |
| **Method + evidence template** | A versioned Method specifies an intervention using platform capabilities; its evidence template defines the structured record needed when a run concludes. Together they make the investigation inspectable before evidence is collected. |
| **Evidence generation** | A Method runs in the workspace. Its frozen run provenance and a contributor's typed observations can become a consent-checked [Evidence Contribution][evidence-contribution] in the research catalog. |
| **Evidence Ledger** | Accepted evidence for one exact Method and evidence-template version can be scoped into a source-linked, immutable [Ledger Snapshot][ledger-workflow]. A Ledger is descriptive material, not a conclusion. |
| **Human-authored findings** | A person selects published Ledgers and research questions, writes the claim, scope, interpretation, counterevidence, and limitations, then submits it to the applicable review process. |
| **Research questions and theory** | Findings, challenges, replications, and negative results can refine a question or theory and begin the next pass through the cycle. |

The arrows do not impose a hidden one-to-one mapping. In particular, a Ledger
has no research-question field: it records a reproducible scope for one
Method/template pair. A Finding independently declares one or more research
questions and cites one or more published Ledgers; its human author explains
their relationship.

## The workspace's role

The Evaluchat Workspace is the common surface on which this work can happen. It
is Markdown-native, supports AI assistance when wanted, and keeps documents,
method settings, and provenance available for inspection. A Method selects the
specific platform capabilities it needs; Evaluchat is not limited to one kind
of classroom activity or one theory of learning.

The Workspace is also useful by itself: people can use it for ordinary Markdown
work, classroom activities, or other collaborative tasks without collecting
research evidence. Those uses are welcome, but they are incidental to
Evaluchat's primary purpose: making AI-in-education research methods easier to
create, run, share, scrutinise, and improve.

## Assistance without outsourcing judgement

AI assistance can lower the barrier to participating in the research process:
it can help people work with Markdown, understand a Method or template, explain
declared evidence-scope options, and surface gaps or counterevidence in a
Ledger. That assistance is bounded. It does not choose a research question,
change a Ledger's filters, generate or publish a Ledger, write a Finding,
approve a claim, or make a research decision on a person's behalf.

This separation keeps the practical plumbing accessible without confusing AI
help with evidence, interpretation, authorship, or review.

## The first complex workflow is an example, not the platform

The CAMDLE-related [AI-assisted essay method][ai-assisted-essay] is the first
complex workflow supported by Evaluchat. Its corresponding [Essays workflow][essays]
shows one way a Method can compose workspace capabilities for a particular
research question. CAMDLE is a theory under investigation in the research
catalogue—not a core Evaluchat feature, a default method, or the purpose of the
platform.

Future methods can use different interventions, activities, measurements, and
evidence contracts. Their differences are part of what the platform is designed
to make public and comparable.

## Where to start

**You want to explore or contribute research**

- Start with the [research catalog][research-catalog] for theories, questions,
  published Methods, evidence, governance, and findings.
- Read [Research method][research-method] to see how a Method uses documented
  platform capabilities and carries an evidence contract.
- Follow the [Evidence Ledger to Finding playbook][ledger-playbook] when a
  Method has accepted evidence ready to inspect.

**You are planning or running an educational activity**

- Use a published Method as the accountable way to run an investigation, then
  use the [Evidence Contribution workflow][evidence-contribution] to record a
  concluded run when consent and publication conditions are met.
- Consult the [platform capabilities][capabilities] to understand the
  configurable behaviour and telemetry boundary a Method may select.

**You are building, evaluating, or governing AI-in-education work**

- Inspect the open methods, provenance, Ledgers, findings, and review trail in
  the [research catalog][research-catalog].
- Use the documentation and design records to understand what the platform
  currently does, what remains a design decision, and how to contribute an
  improvement.

## Browse this documentation

| Section | What it covers |
| --- | --- |
| **[Concepts](/concepts/index.html)** | Shipped product truth: Workspace capabilities and user-facing workflows. |
| **[Designs](/designs/index.html)** | Draft decisions and intended mechanics for platform features; consult the linked Concept when a design has graduated to shipped behaviour. |
| **[Playbooks](/playbooks/index.html)** | Practical guides for specifying Methods and moving from evidence to a Finding. |
| **[Research catalog][research-catalog]** | Research truth: theory, questions, Methods, evidence, Ledgers, findings, and governance. |

Behaviour-specific Concepts carry their own version and release-context fields.
This overview intentionally describes the platform's purpose and research model;
follow those linked records for the exact behaviour of a particular dev build.

## Contributing

Evaluchat's knowledge and research are open for inspection and contribution.
Corrections and platform-documentation updates are made through pull requests to
the [knowledge repository](https://github.com/evaluchat/knowledge). Research
questions, evidence, findings, and their review belong in the
[research catalog][research-catalog].

[research-catalog]: https://research.evaluchat.org/
[research-method]: /concepts/research-method.en.md
[evidence-contribution]: /concepts/evidence-contribution.en.md
[ledger-workflow]: /concepts/evidence-ledger-and-finding-workflow.en.md
[ledger-playbook]: /playbooks/evidence-ledger-to-finding.en.md
[capabilities]: /concepts/platform-capabilities.en.md
[essays]: /concepts/essays-workflow.en.md
[ai-assisted-essay]: https://research.evaluchat.org/methods/ai-assisted-essay/index.html
