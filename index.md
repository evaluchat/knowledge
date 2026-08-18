---
okf_version: "0.2"
---
# Evaluchat Knowledge Catalog

Open, multilingual, PR-able knowledge about what Evaluchat Canvas does and how it works — product truth, not opinion.

| Knowledge (this repo) | Research |
|-----------------------|----------|
| Product truth | Research truth |
| What Evaluchat can do | What we are investigating |
| Features, capabilities, workspace templates | Theory → questions → methods → evidence → findings |

A **Method** in the research catalog selects named **levers** documented here. Evaluchat runs that profile; this catalog does not store classroom evidence.

## Catalog sections

| Section | Purpose |
|---------|---------|
| [Concepts](/concepts/index.md) | What the product is and how its features work (implementation source of truth) |
| [Designs](/designs/index.md) | Design decision notes for platform features — rationale and agreed mechanics before implementation (draft) |
| [Templates](https://knowledge.evaluchat.org/templates/) | Reviewed Markdown starters for the Evaluchat workspace (Getting Started, Assignment brief) |
| Prompts | Exact wording of prompts as shipped, versioned (Phase 2 — planned) |
| [Playbooks](/playbooks/index.md) | How to specify a Method on Canvas capabilities — the method recipe (draft) |
| References | Pointer concepts linking to the research catalog (Phase 2 — planned) |

## Language note

Frontmatter is the machine/catalogue layer and is **always English**. Content bodies may be written in any language (see `lang` per file). English is the discovery language, not necessarily the source language.

## Repository layout

| File | Purpose |
|------|---------|
| `index.md` | This listing |
| `log.md` | Change log (newest first) |
| `README.md` | Repo intro for humans |
| `CONTRIBUTING.md` | House conventions for contributors |
| `AGENTS.md` | Contributor-agent contract (for AI editors) |
| `AGENT.md` | Consumer-agent contract (for AI readers) |
| `LICENSE` | MIT (docs + scripts) |

## Methods

- [Research method — how methods use platform capabilities and levers](/concepts/research-method.en.md) — the two-catalog pattern (concept).
- [Platform capabilities — public-beta runtime contract](/concepts/platform-capabilities.en.md) — AI modes, drafting gates, telemetry boundary, typed levers (concept, `applies_to: 0.5.9`).
- [The method recipe — from research question to published method](/playbooks/method-recipe.en.md) — how to specify a Method (playbook).
- Published method (research truth): https://github.com/evaluchat/research/blob/main/methods/ai-assisted-essay/

## Related

- Research catalog (research truth — questions, methods, evidence, findings): https://github.com/evaluchat/research
- OKF v0.2 — portable knowledge format
