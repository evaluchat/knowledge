## Pull request — type of change

- [ ] **New concept** — documents a shipped product behaviour
- [ ] **Spec change** — updates a version-pinned specification (`applies_to` / `stale_after` updated)
- [ ] **Translation** — new or updated `<slug>.<lang>.md` (`origin: translation`, `generated.by` set; NO `verified: human:` unless actually human-reviewed)
- [ ] **Correction** — fixes an error in existing content
- [ ] **Other** — describe below

## Description

<!-- What does this PR change and why? Which canvas version does it describe? -->

## Checklist

- [ ] `id` equals the filename slug; `lang` matches the filename suffix (`.en.md` for English)
- [ ] Frontmatter complete: `type`, `id`, `lang`, `title`, `description`, `status` (+ `applies_to`/`stale_after` where version-sensitive)
- [ ] `generated.by` set for agent-authored content; no fabricated `verified: human:`
- [ ] CI lint passes
- [ ] Content is product truth only — no research claims, no competitive content, no internal strategy
- [ ] License: I agree to license this contribution under MIT
