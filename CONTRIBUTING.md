# Contributing to the Evaluchat Knowledge Catalog

Thank you for contributing. This catalog is open, multilingual, and PR-able: anyone can propose a change, and CI checks structure automatically. This file is the house convention — please read it before opening a pull request.

## What belongs here

**Product truth only.** This repository documents what Evaluchat Canvas currently does and how it is implemented: features, behaviour, prompts as shipped, role/API mechanics, method runtime contracts, and versioned specifications. It is not a place for opinions, marketing claims, competitive comparisons, or internal strategy.

Knowledge is product truth (what Evaluchat can do: features, capabilities, workspace templates). Research is research truth (questions → methods → evidence → findings). A Method in the research catalog selects **levers** whose meaning is defined here. Research questions, methods, evidence, and claims belong in the [research catalog](https://github.com/evaluchat/research). Classroom evidence and executable product templates stay in their own repos.

## Multilingual convention (house spec)

OKF v0.2 defines no language mechanism; this convention supplies one and is enforced by CI.

### Two-layer split

| Layer | Where | Language |
|-------|-------|----------|
| Catalogue/machine layer | YAML frontmatter: `type`, `id`, `title`, `description`, `tags`, `lang`, `status`, `generated`, `verified`, `sources`, `origin` | **Always English** |
| Content layer | Markdown body (H1 onwards) | Any language, per `lang` |

**English is the machine/catalogue language — not necessarily the epistemic source language.** A teacher's native-language description of how they use the product is first-class content; the English summary is generated for discovery.

### Required fields

- **`lang: <BCP-47>` — REQUIRED** on every non-reserved `.md` file (`en`, `es`, `fr`, `zh-CN`, `pt-BR`, …). CI validates plausibility only (regex `^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$`).
- **`id: <slug>` — REQUIRED, stable, language-independent.** The concept group's identity. The filename is one representation: `essays-workflow.es.md` = concept `essays-workflow`, Spanish representation. CI validates `id` equals the filename slug. `id` survives title changes, splits, and merges — never infer identity from filenames.
- **Filename suffix carries the language**: `<slug>.<bcp47>.md` for **ALL** languages, including English. **This is a settled decision — not to be revisited.** Rationale: with native-origin content, "bare filename = English" would make English the implicit default even when English is the *generated* summary of a native-language contribution. Uniform suffixes keep every language symmetric.
- **`title`/`description`: English** (index/snippet layer). Optional `title_local`: native display name.
- **`origin: native | translation`** — optional. `native` (default) = content originally authored in `lang`; `translation` = derived from another language's version (typically agent-generated, machine-confirmed until human-verified).
- **`translations:` is NOT maintained by humans.** Language lists are derived by tooling from `id` + `lang` across the tree (emitted in `catalog.json`). If present in frontmatter it is cache only; CI may warn on asymmetry but never fails on it.

### Consumer fallback rule

Tooling filters by `lang`, and falls back to the same `id`'s `en` representation. Catalogues list each `id` once with language badges.

## Translation quality rides trust tiers

- Agent-generated translation → `generated: { by: <agent>/<version> }`, `origin: translation` → trust tier: **machine-confirmed**.
- Human-checked → add `verified: { by: human:<id>, at: <ISO> }` → trust tier: **human-reviewed**.
- No extra machinery; machine structuring can never masquerade as human review.

## Frontmatter template

```yaml
---
type: Concept            # Concept | Specification | Prompt Template | Playbook | Reference | Pattern
id: <slug>               # MUST equal the filename slug
title: English Title
title_local: Native title   # optional
lang: en                # BCP-47; MUST match the filename suffix
origin: native          # native (default) | translation
description: One-line English summary.  # REQUIRED
tags: [tag1, tag2]
status: draft           # draft | stable | deprecated
applies_to: 0.5.9       # REQUIRED for spec/prompt concepts — the canvas version this describes
stale_after: <ISO date> # for version-sensitive content
generated: { by: <producer>/<version>, at: <ISO> }   # REQUIRED for agent-authored content
verified: { by: human:<id>, at: <ISO> }              # ONLY for human-reviewed content
sources:
  - id: <source-id>
    resource: <https URL>
    title: <source title>
---
```

## House rules

- `status: draft | stable | deprecated` — `stable` means "matches a shipped version", not "eternally true".
- `applies_to: <canvas-version>` on specification/prompt concepts; `stale_after` for version-sensitive content. Behaviour changes → new PR.
- Exact prompts, when published, are published **as shipped** — never "improved" for display.
- Evidence-style content does not belong in this repo (see research catalog). If your contribution is an observation about classroom use, it belongs there.
- Never fabricate `verified: human:` — only a real human review can add it.

## Licensing terms for contributions

This repository is **MIT-licensed** (docs + scripts). By submitting a pull request you agree that your contribution is licensed under MIT and may be redistributed by the repository, with attribution preserved in git history. If your contribution includes material you do not have the right to license, do not submit it.

## PR checklist

- [ ] Type of change: spec / translation / correction / new concept / other
- [ ] `id` equals the filename slug; `lang` matches the filename suffix
- [ ] Frontmatter complete: `type`, `id`, `lang`, `title`, `description`, `status` (+ `applies_to`/`stale_after` where version-sensitive)
- [ ] `generated.by` set for agent-authored content; no `verified: human:` unless actually human-reviewed
- [ ] CI lint passes (it runs automatically on the PR)
- [ ] Content is product truth only — no research claims, no competitive content, no internal strategy
- [ ] Method/runtime changes state the supported Canvas version, capability and lever contract, and privacy boundary

## CI

A minimal lint (`scripts/okf_lint.py`) runs on every PR and push: hard errors on missing/mismatched frontmatter fields, warnings for link and index issues. If CI fails, fix the reported issue and push again.
