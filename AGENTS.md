# AGENTS.md — Contributor-Agent Contract

This file governs **AI-assisted contributors** editing this repository (copilots, Canvas "save as evidence" agents, and any other agent that writes or proposes content here). Humans contributing via PRs follow [CONTRIBUTING.md](CONTRIBUTING.md); the rules below are the machine-readable version of the same house conventions.

## Identity and provenance

- Always set `generated: { by: <producer>/<version>, at: <ISO timestamp> }` on content you author or structure. `<producer>` is your own identifier (e.g. `opencode-go/deepseek-v4-flash`, `canvas-save-as-evidence/0.1`). Never omit it, and never attribute your work to a different producer.
- **Never fabricate `verified: { by: human:<id> }`.** Only a real human review can add the `verified` field. If you are an agent, you are not a human reviewer, ever.
- Never edit or remove an existing `verified` field.
- `origin: translation` content must carry `generated.by`; translations you produce are machine-confirmed until a human verifies them.

## Epistemic separation

- Keep observation and inference separate in structure and wording. If you are structuring evidence content (research repo), `observations.md`/`results.md` state what happened/measured; `reflection.md` states interpretation; `limitations.md` states what we do not know.
- Do not upgrade the epistemic status of content: structuring or summarising is not verification, and agent output is never a "finding" on its own.
- This repo (knowledge) is product truth only: describe what the product does as shipped. Research claims belong in the research catalog.

## House-convention checklist (Part B)

- `lang` present and plausible BCP-47; filename suffix `<slug>.<lang>.md` matches `lang` — including `.en.md` for English (settled, do not "simplify").
- `id` equals the filename slug; `title`/`description` in English; `type` from the controlled vocabulary; `status: draft | stable | deprecated`.
- `applies_to`/`stale_after` on version-sensitive content; verify the version you cite before pinning it.
- Do not hand-maintain `translations` lists — they are derived by tooling.

## Process

- Validate before finishing: run `python3 scripts/okf_lint.py` and fix hard errors.
- Prefer a PR over a direct push; if you push directly, keep commits conventional and scoped.
- When in doubt about whether content is product truth vs research vs strategy, leave it out or flag it for a human — never guess it into the public catalog.
