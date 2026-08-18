---
type: Concept
id: overview
lang: en
origin: native
status: stable
title: 'Platform documentation — overview'
description: 'A reader-facing starting point for the Evaluchat platform documentation: what this knowledge site is, who it is for, and where to start depending on what you are trying to do.'
tags: [evaluchat, documentation, overview, concepts, platform]
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-18T16:00:00Z
sources:
  - id: concepts-index
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/index.md
    title: 'Concepts — the platform documentation index'
  - id: platform-capabilities
    resource: https://github.com/evaluchat/knowledge/blob/main/concepts/platform-capabilities.en.md
    title: 'Platform capabilities — public-beta runtime contract'
  - id: research-catalog
    resource: https://github.com/evaluchat/research
    title: 'Evaluchat research catalog'
---

# Platform documentation — overview

Welcome to the Evaluchat **platform documentation**. This is the user-facing
reference for what Evaluchat does and how it works — the features, the
confidentiality and integrity model, and the research layer that turns
classroom writing work into accountable, reproducible evidence.

Everything on this site is **product truth**: it describes Evaluchat as it is
built and shipped, not a wish list. Research questions and claims live in the
[research catalog][research-catalog], not here.

## What Evaluchat is

Evaluchat is an **open-source, AI-native writing workspace** built for
education. Students work through constrained, conversational assignments on a
split-screen canvas; the AI acts as a writing coach rather than a ghostwriter.
The writing process — prompts, drafting choices, and the finished work — doubles
as **language evidence**, and reviewed research apparatuses let educators and
researchers run structured classroom writing workflows whose outputs are
accountable and reproducible.

Three ideas run through everything here:

1. **Proportional assistance** — the AI does less when the student
   contributes less. Drafting support is gated behind the student's own ideas,
   evidence, questions, and language (the [CAMDLE][essays] mechanism).
2. **Honest integrity, not surveillance** — Evaluchat records *process signals*
   (engagement, drafts) as context for human judgement. It produces no
   "cheating" score and does no proctoring.
3. **Research with a spine** — every published method names the levers it
   uses and requires an evidence contract, so that anything claimed is backed
   by what actually ran.

## Where to start

Depending on what you are trying to do, jump straight to the right document:

**You are a teacher or administrator setting up classroom writing work**
- [Essays workflow — proportional drafting unlock][essays] — how the essays
  feature actually behaves for students, session by session.
- [Platform capabilities — public-beta runtime contract][capabilities] — the
  AI modes, drafting gates, and telemetry you can configure.

**You are a researcher planning or running a study**
- [Research method — how methods use platform capabilities and levers][method]
  — how a Research catalog method selects named levers documented here.
- [Evidence contribution — filing a concluded run to research][evidence] —
  how to turn a concluded classroom run into a consent-checked, revertible
  evidence contribution via a bot-authored pull request.

**You are self-hosting or evaluating the product**
- Review the [capabilities contract][capabilities] to know what the runtime
  guarantees, including the telemetry boundary.

## Browsing the rest of this site

The site mirrors the GitHub repository tree, section by section:

| Section | What it is |
|---------|------------|
| **[Concepts](/concepts/index.html)** | What the platform is and how its features work — you are here. |
| **[Designs](/designs/index.html)** | Decision notes for platform features — marked *draft* until the feature ships (some graduate to a Concept once shipped). |
| **[Playbooks](/playbooks/index.html)** | How to specify a Method on Canvas capabilities. |
| **Research catalog** | Research truth — questions, theory, methods, evidence, findings ([evaluchat/research][research-catalog]). |

Each concept page carries a small reference block (type, status, versions) at
the top and the human explanation below; `status: draft` means a document is a
design/under revision and describes intent rather than shipped behaviour.

## Version note

This overview is intentionally **version-independent**: it is a navigation and
positioning page, not a description of any single Canvas build. Each concept it
links to carries its own `applies_to` pin (the Canvas version whose behaviour it
describes), so behaviour-specific truth always resolves at the leaf, never in
this aggregate. Treat this page as current until a linked concept is deprecated.

## Contributing

This documentation is open. Corrections and additions are made through pull
requests to the [knowledge repository](https://github.com/evaluchat/knowledge);
see `CONTRIBUTING.md` there for the house rules (product truth only, provenance
recorded, no fabricated verification).

[essays]: https://github.com/evaluchat/knowledge/blob/main/concepts/essays-workflow.en.md
[capabilities]: https://github.com/evaluchat/knowledge/blob/main/concepts/platform-capabilities.en.md
[method]: https://github.com/evaluchat/knowledge/blob/main/concepts/research-method.en.md
[evidence]: https://github.com/evaluchat/knowledge/blob/main/concepts/evidence-contribution.en.md
[research-catalog]: https://github.com/evaluchat/research
