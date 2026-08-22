---
okf_version: "0.2"
---

# Designs

Design decision notes for Evaluchat platform features. These documents record the
rationale, constraints, and agreed mechanics for a feature before implementation —
design intent, not shipped product truth. A design graduates to a `concepts/`
specification once the feature ships.

| Design | Status | What it covers |
|--------|--------|----------------|
| [Evidence publishing mechanics](/designs/evidence-publishing.en.md) | draft · **graduated** | Evidence definition as an integral part of a Method, the workspace Evidence action, and the submit-to-PR filing flow into the research catalog — **shipped**; see [Evidence contribution concept](/concepts/evidence-contribution.en.md) |
| [Finding authoring — evidence ledgers and human-controlled claims](/designs/finding-authoring.en.md) | draft | On-demand immutable evidence ledgers, freshness detection, and a human-only finding canvas with read-only AI advice |
| [Evidence Ledger workspace and light Finding authoring](/designs/finding-authoring-ux.en.md) | draft | Create-workspace-item flow, template-rendered fact filters, immutable ledger snapshots, GitHub publication, and a lightweight Finding starter that cites published ledgers |
| [GitHub research workspaces — trust boundary, OAuth, tokens, and retention](/designs/github-research-workspaces.en.md) | draft | Two-app trust boundary, PKCE OAuth, AES-256-GCM token envelope, zero server retention, and browser-memory-only cache policy for v0.8 private GitHub research workspaces |
