# AGENT.md — Consumer-Agent Contract

This file is a machine-readable navigation contract for **agents reading this catalog** (RAG systems, copilots, Canvas knowledge context, research assistants). Follow these rules to read the catalog correctly.

## 1. Discover
Read `index.md` first, then `catalog.json` (once built). Filter by `type`, `tags`, `lang`, and `status` to find what you need. `index.md` is the human listing; `catalog.json` is the machine listing.

## 2. Identity
`id` is the stable concept identity. The filename is one representation of that concept: `essays-workflow.es.md` = concept `essays-workflow`, Spanish representation. Never infer identity from filename stems alone; `id` survives renames, splits, and deprecations.

## 3. Language
Pick the representation matching the requested `lang`; fall back to the `en` representation of the same `id` if the requested language is missing. `origin: native` means the content was originally authored in that language; `origin: translation` means it was derived from another language's version (typically agent-generated).

## 4. Trust
Derive trust from `verified` and `status`:
- `generated.by` present, no `verified` → machine-produced/machine-confirmed — treat as unverified.
- `verified: { by: human:<id> }` → human-reviewed.
- `status: draft` means unproven or unstable — do not cite as settled fact.
- `status: stable` + `applies_to` means "matches the shipped version named" — do not apply to other versions.
- Evidence contributions carry a `stage` (contribution ladder rung); findings carry a tier per the research catalog's governance.

## 5. Epistemics
Observation ≠ inference ≠ claim. In evidence bundles, `observations`/`results` are what happened/measured, `reflection` is interpretation, `limitations` is what we don't know. A Finding requires its evidence chain and tier (see research catalog governance). In this knowledge catalog, content describes what the product does — it is not research evidence.

## 6. Relationships
Follow markdown links as typed edges: question → hypothesis → intervention → evidence → claim, with challenge/replication edges. Cross-repo edges use `resource:` URLs in `sources` (absolute GitHub URLs) — OKF links are bundle-relative and cannot cross repos.

## 7. Provenance
Cite `sources` + `generated`/`verified` when you use content. Attribute per-claim where the frontmatter supports it. Never strip provenance when quoting.

## 8. Missing translations
Never fabricate content in a language you were asked for but that doesn't exist. Either request a translation (issue template) or fall back to the `en` representation — but say so.

## Related
- [CONTRIBUTING.md](CONTRIBUTING.md) — house conventions for writing
- [AGENTS.md](AGENTS.md) — contract for AI contributors
- Research catalog: https://github.com/evaluchat/research — read its `AGENT.md` for research-truth navigation
