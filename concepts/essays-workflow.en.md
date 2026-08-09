---
type: Concept
id: essays-workflow
lang: en
origin: native
status: stable
title: 'Essays workflow — proportional drafting unlock'
description: 'How the Evaluchat essays feature gates drafting support behind dialogic contribution (CAMDLE), as implemented in Canvas — the implementation source of truth.'
tags: [evaluchat, essays, canvas, camdle, teaching-prototype]
applies_to: 0.5.9
sources:
  - id: camdle-theory
    resource: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
    title: 'CAMDLE — research question and theory (unproven)'
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: 'Threshold calibration — research question (open)'
  - id: white-paper
    resource: https://docs.evaluchat.com/research/camdle-white-paper.pdf
    title: 'CAMDLE white paper'
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-09T14:00:00Z
---

# Essays workflow — proportional drafting unlock

> **Applies to:** Canvas apps/web **0.5.9** (dev line), the Evaluchat teaching prototype built on the open-canvas fork. This concept documents the essays feature as shipped in that version.

## Overview

The essays workflow is Evaluchat's student-facing writing experience: a constrained AI chat paired with a drafting canvas. Students work in a split-screen interface — a dialogue panel beside an editable markdown document — that deliberately mirrors the interaction habits of consumer AI tools. It is a familiar, conversational, prompt-driven experience, not a lockdown exam browser.

The core constraint: the model cannot generate the whole assignment from a single prompt. Drafting support is released conditionally, after the student has contributed enough ideas, evidence, questions, and language through dialogue — the CAMDLE design (see [camdle-theory]). The workflow keeps the student's conceptual and linguistic work visible and consequential: what the student does in the dialogue determines what assistance becomes available.

## Session phases

A session progresses through three phases, tracked at runtime by a `phase_state` value: `socratic`, `drafting`, `defense`.

### Phase 1 — Socratic gate

The AI interviews the student to establish understanding before any essay text lands on the canvas. Direct "write my essay" requests are rejected; instead, the assistant extracts the student's raw intuition into a structured thesis. After each turn the assistant assesses the thesis (`assessThesis`); when the contribution is sufficient, `phase_state` transitions to `drafting` and writing assistance becomes available.

### Phase 2 — Milestone-gated co-creation

In the drafting phase, the student works on the split-screen canvas with the AI acting as a developmental editor rather than a ghostwriter. The document records a revision timeline ("document DNA") that distinguishes student-written content from AI-suggested edits, so who contributed what remains visible. Once enough thesis material exists, the AI may draft introductory text or milestone sections onto the canvas for the student to review, accept, or revise.

### Phase 3 — Viva defense

Before submission, the AI challenges a key argument from the student's essay — a chat-based devil's-advocate defense. Submission unlocks only after the student has successfully defended the argument.

## Session and assignment rules

- One active session per student per assignment.
- Session statuses: `not_started`, `in_progress`, `submitted`, `abandoned`.
- Active thread selection prefers the incomplete non-abandoned thread, then the submitted non-abandoned one; abandoned threads are skipped. Opening an assignment attaches to that thread rather than spawning duplicates.
- `/student` lists the student's assignments with status-aware actions (resume, review, start).

Assignments resolve from two sources:

1. **Custom assignments** — teacher-owned assignments, created and listed on the teacher side, assigned to specific students.
2. **Seed catalog** — shared starter templates loaded at runtime from a JSON file (`data/teaching/seed-assignments.json`), not hardcoded into the app bundle. Seeds appear on `/student` only when registered for that student.

## Process evidence

A client-side tracking aggregator collects process signals and emits compact `session_summary` events (~300 bytes) periodically and on unload — not per-keystroke API traffic. Summaries include:

- keystrokes and typing bursts (groups of keystrokes close together, burst word counts and duration)
- paste, copy, and cut events (paste volume, copied/cut content)
- canvas edits (insertions, deletions, replaces)
- focus and blur counts, visibility-hidden events

Teachers see these as **Engagement Metrics** on the submission view. A high paste ratio (e.g. more than ~30% pasted) may surface as a descriptive badge — a conversation starter, not a verdict.

**Boundary: process evidence is not authorship detection.** These are mechanical observations about how work came together; they do not prove who authored a sentence or whether learning occurred. Evaluchat produces no integrity score, no "cheating" flag, and no automated integrity verdict of any kind. Signals are context for human judgment: teachers read them alongside the transcript, the draft, and the assignment context, and decide what, if anything, is worth discussing with the student. Engagement metrics, not integrity flags; process signals, not cheating indicators. The product does no proctoring (no webcam, lockdown, or screen recording), and it cannot detect off-device or mediated behaviour such as retyping, dictation, paper notes, or assistance from a second device.

## Proportional scaffolding and the unlock threshold

Drafting support is released conditionally on dialogic contribution — proportional scaffolding. The amount of contribution required to unlock assistance (the threshold) is an **empirical variable**, not a settled value: what counts as sufficient contribution, and how that varies by task type, proficiency level, language background, and learner strategy, is an open research question ([threshold-calibration]). The mechanism's purpose is to require time and interaction with the material before generation unlocks; whether that produces learning outcomes is a hypothesis under investigation, not a product claim.

## Status and versioning

This concept pins `applies_to: 0.5.9` — the Canvas apps/web version on the dev line at the time of writing (0.5.8 was the production deploy). It describes behaviour as shipped in that version; newer versions may change behaviour. Treat this concept as **stale** once the pinned version is superseded by a newer release that changes the behaviour described here.

When the pinned version is superseded, update this concept via a pull request to the knowledge repository: bump `applies_to` to the new version, adjust the body to match the newer behaviour, and note the change. Keep `status: stable` only while the description matches a shipped version.

[camdle-theory]: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
