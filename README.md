# Evaluchat Knowledge Catalog

Open knowledge about how **Evaluchat Canvas** works — the product's features, prompts, and behaviour as actually shipped, documented so that teachers, developers, researchers, and AI agents can inspect, question, and improve it.

This is the **product truth** half of Evaluchat's open knowledge platform:

| Knowledge (this repo) | Research |
|-----------------------|----------|
| Product truth | Research truth |
| What Evaluchat can do | What we are investigating |
| Features, capabilities, workspace templates | Theory → questions → methods → evidence → findings |

- **Knowledge** documents the platform: capabilities, workflows, and **workspace templates** such as Getting Started and Assignment brief. Those templates are product building blocks Evaluchat instantiates.
- **Research** documents investigations: a question, a **Method** that uses named platform features, the evidence that method produced, and any finding a human later claims.

A Method selects **levers** (named switches such as `ai_assistance`, `drafting_gate`, `threshold`) whose meaning is defined here. Evaluchat **runs** that profile. It does not own research truth. This catalog does not store classroom evidence. The research catalog does not store executable product templates.

The two repositories are deliberately separated. Private strategy never appears in either.

## Format

OKF v0.2 — Markdown files with YAML frontmatter. Each concept has a stable `id`, a `lang`, and a `status`. Frontmatter is always English (the catalogue/machine layer); the content body can be written in any language, per `lang`.

**Multilingual by design.** A Spanish teacher's contribution is first-class content, not a "translation to be done". English summaries exist for discovery; `origin: native | translation` records which is which, and trust tiers record whether a translation is machine-confirmed or human-reviewed.

## Layout

```
concepts/   # feature concepts — the implementation source of truth
templates/  # workspace templates (Getting Started, Assignment brief)
prompts/    # exact prompt wording, versioned (Phase 2)
playbooks/  # how to specify a Method on Canvas capabilities
references/ # pointers to the research catalog (Phase 2)
```

## How to contribute

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the house conventions (frontmatter rules, language rules, PR checklist). The short version:

1. Concepts are Markdown + YAML frontmatter — no build step, no tooling.
2. Every file needs `type`, `id`, `lang`, `title`, `description`, `status`.
3. Open a pull request; CI validates structure automatically.
4. Version-sensitive content pins `applies_to: <canvas-version>` and `stale_after`.

## License

MIT — the docs and any scripts in this repository are MIT-licensed (see [`LICENSE`](LICENSE)). Contributions are accepted under the same terms; by opening a pull request you agree to license your contribution under MIT.

## Related

- Live research catalog: https://research.evaluchat.org
- Live knowledge catalog: https://knowledge.evaluchat.org
- Research catalog: https://github.com/evaluchat/research
- Evaluchat: https://evaluchat.org
- OKF v0.2 — the portable knowledge format these catalogs use
