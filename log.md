# Knowledge Catalog — Update Log

## 2026-08-17
* **Addition**: Added `designs/` section (new category) + `designs/evidence-publishing.en.md` (Concept, draft, applies_to 0.5.9) — design decisions for the workspace Evidence action: single-file `evidence-template.md` per method, canvas-thread instantiation, submit-to-PR filing into the method's evidence directory via Valery Bot.ha, machine-checked auto-merge for documented-experience bundles, two-sided publishing gate (method PRs require an evidence template). Design only — no implementation.

## 2026-08-13
* **Terminology**: Renamed `concepts/research-apparatus.en.md` → `concepts/research-method.en.md` (`id: research-method`) and `playbooks/apparatus-recipe.en.md` → `playbooks/method-recipe.en.md` (`id: method-recipe`). Short deprecated stubs remain at the old paths/ids so existing GitHub URLs do not 404. Public prose uses Method and levers; live product APIs and stored snapshots are unchanged. Two-catalog story (Knowledge = product truth; Research = questions → methods → evidence → findings) written into README, `index.md`, and CONTRIBUTING. `platform-capabilities.en.md` and essays-workflow positioning blocks updated. Knowledge `templates/` remain workspace items only (Getting Started, Assignment brief) — no evidence-bundle.
* **Addition**: Added `playbooks/oss-issues-board-policy.en.md` (Playbook, stable) + index line — Model 1 issue/board policy for the evaluchat OSS repo: issues = user-reported bugs + enhancement feature requests (public roadmap); internal notes/tech debt = board drafts, never issues; board columns, automations ("Item closed" → Done, "Pull request linked" → In progress), reopen-doesn't-restore quirk; PR-body `Closes #N` linking. Public statement in evaluchat/evaluchat CONTRIBUTING.md.

## 2026-08-11
* **Platform capabilities — public-beta runtime contract**: `concepts/platform-capabilities.en.md` extended from knob vocabulary to the typed capability/knob/profile contract (required capabilities, typed knobs with dependencies/exclusions, immutable profile semantics, assignment snapshot rule, telemetry boundary incl. tracking-off) pinned to Canvas 0.5.9. `concepts/index.md` and `CONTRIBUTING.md` updated (apparatus/runtime checklist line).

## 2026-08-10
* **Addition**: Added `concepts/platform-capabilities.en.md` (Concept, draft, applies_to 0.5.9) — the knob vocabulary apparatus specs reference: AI modes (none/chat-only/constrained/full), drafting gates (none/discussion-first/thesis-approved), telemetry boundary (process_signals/transcript/output, no authorship detection, no integrity score), versioning contract (apparatus version independent of canvas version; provenance records both).

## 2026-08-09
* **Addition**: Added `concepts/research-apparatus.en.md` (Concept, draft, applies_to 0.5.9) — the research apparatus pattern: definition, four-dimension invariant (knowledge / manifest / research method / code), epistemic spine (apparatus / intervention / measurement / evidence), capabilities-and-phases contract, versioning as behaviour/evidence contract, Apparatus → Version → Configuration → Experiment, configuration-in-provenance.
* **Addition**: Added `playbooks/apparatus-recipe.en.md` (Playbook, draft) + `playbooks/index.md` — the canonical form, eight-primitive design checklist, worked example (Essays), checklist-not-schema guidance, version/configuration recording rules, and the "what is not built yet" note (no DSL, no builder framework, no plugin runtime).
* **Positioning**: `concepts/essays-workflow.en.md` + `.es.md` gained a top-of-file positioning block naming them the implementation source of truth for **Apparatus #1 (Essays / CAMDLE apparatus)** with a link to research-apparatus. Implementation facts byte-identical apart from the block; the `.es.md` remains `origin: translation`, no `verified`.
* **Indexes**: `concepts/index.md`, root `index.md` (new Research apparatus section) updated.
