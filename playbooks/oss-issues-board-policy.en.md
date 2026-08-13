---
type: Playbook
id: oss-issues-board-policy
lang: en
origin: native
status: stable
title: OSS repository issue & board policy (Model 1)
description: "How evaluchat/evaluchat GitHub issues and the Evaluchat Board are managed: issues are user-reported bugs and enhancement feature requests only (the public roadmap); internal notes and tech debt live on the project board as drafts; board columns, automations and quirks."
tags: [evaluchat, oss, github, issues, project-board, policy, governance]
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-13T08:34:45Z
sources:
  - id: contributing
    resource: https://github.com/evaluchat/evaluchat/blob/main/CONTRIBUTING.md
    title: CONTRIBUTING.md — Issues and the project board (public statement of this policy)
  - id: board
    resource: https://github.com/users/evaluchat/projects/1
    title: Evaluchat Board (GitHub Projects v2)
---

# OSS repository issue & board policy (Model 1)

> Operating policy for the evaluchat/evaluchat GitHub repository, adopted 2026-08-13.
> The public-facing statement lives in CONTRIBUTING.md ("Issues and the project board").
> This playbook is the internal operating version: how to keep the issue list and board clean.

## The model in one line

**Issues are the public record; the board is the execution state machine; internal notes never become issues.**

This is "Model 1" of the three conventions found in major OSS projects (VS Code / Home Assistant = Model 1, Kubernetes = Model 2 with a separate enhancements repo, Astro / Prisma = Model 3 with Discussions for feature requests). Model 1 was chosen because the issue tracker is the only public surface external people can search, upvote and comment on — that is how the first external contributor (waghgauri14, issue #23) found the project.

## Issue policy

- **Bug reports** — user-reported problems against the live published main-branch code. Must be reproducible: steps, expected vs actual, environment.
- **Feature requests** — labelled `enhancement`. These are the public roadmap. Keep them open until delivered or explicitly closed `not planned`.
- **Never issues** — internal project notes, tech-debt musings, uncommitted ideas. They become **board drafts** (Backlog column). The issue list is not a notes dump.
- **Closing** — always with a reason: `completed` when the work shipped (comment citing the merged PR, e.g. "Shipped in #8"), `not_planned` when converted to a board note.
- **Shipped-but-open trap** — issues migrated from board drafts can postdate the PRs that shipped them (2026-08-10 board hygiene did this to #19/#24/#26/#28/#29/#30/#31). Verify the feature exists on main, then close with the PR citation.
  - **Root cause (full story, 2026-08-10)**: the hygiene run converted ALL seeded board drafts into issues with a generic stub body ("Migrated from Canvas Board draft…") and default Backlog status — including the ~10 drafts already marked Done with "Shipped in PR #N" bodies. Only #32 was closed at migration time. Four more victims were found 2026-08-13: #20 (PR #4, LaTeX-delimiter math), #21 (PR #2, Mermaid), #22 (PR #1, toolbar — also redesigned in PR #13), #33 (PR #3, inline KaTeX). Lesson: before converting drafts → issues, carry over the draft's status and body verbatim; verify "shipped" claims against merged PRs + the main tree (e.g. MathInlineExtension.ts, MermaidBlock.tsx, CustomFormattingToolbar.tsx).
  - **Overlap note**: #20 (display + LaTeX-delimiter math) and #33 (inline KaTeX) were the display/inline halves of the same private-repo feature (MathInlineExtension.ts, built 2026-07-09); they shipped as separate backport PRs #4/#3 and were closed as separate shipped items — do not merge duplicates post-hoc.

## Board mechanics

- **Columns**: Backlog → Ready → In progress → In review → Done. Fields: Priority (P0–P2), Size (XS–XL).
- **Automations** (all enabled): "Item closed" → moves to Done; "Pull request linked to issue" → moves to In progress; "Item added to project"; "Auto-close issue"; "Pull request merged".
- **Quirk (observed 2026-08-13, #36)**: reopening a closed issue does NOT move its board item back out of Done — the board item must be moved manually.
- **PRs are not board items.** The functionality a PR delivers is rendered on the board as issue items or drafts, not as the PR node itself.
- Linking: put `Closes #N` in the PR body — the issue auto-closes on merge and the automation moves the item.

## Workflow notes

- When a PR delivers an open issue, link it (`Closes #N` in the PR body) — the trail is the point.
- Triage regularly; closing-as-not-planned beats a polluted issue list.
- Issue open/closed state and board status are independent: an issue stays open until shipped; the board column tracks execution.

## History

- 2026-08-12 — first external engagement: waghgauri14 commented on #23 (repo-identity confusion from the rename). Rename context: evaluchat/canvas → evaluchat/evaluchat (a major commercial LMS named Canvas); old URL 301-redirects; in-repo stale references cleaned by the rename-completion commit inside PR #13.
- 2026-08-13 — policy adopted. Cleanup: 7 shipped issues closed with PR citations (#5–#11), 4 internal notes (#25/#27/#34/#35) closed and converted to Backlog drafts, #44 (CodeRabbit backlog) converted likewise, PR #13 linked to #22 via `Closes #22`.
