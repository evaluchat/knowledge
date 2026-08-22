---
type: Concept
id: github-research-workspaces
title: GitHub research workspaces — trust boundary, OAuth, tokens, and retention
description: "Design: v0.8 private GitHub research workspaces use two independent GitHub Apps, PKCE OAuth with one-time state, AES-256-GCM token envelopes, zero server-side content retention, and browser-memory-only caching."
lang: en
origin: native
status: draft
tags: [design, github, research-workspaces, oauth, privacy, security, okf]
applies_to: 0.8.0
timestamp: 2026-08-22T00:00:00Z
generated: { by: cursor/composer-2.5, at: 2026-08-22T00:00:00Z }
sources:
  - id: github-research-threat-model
    resource: https://github.com/evaluchat/research/blob/main/governance/github-research-threat-model.en.md
    title: GitHub research workspaces — threat model (research catalog)
  - id: research-repository-contract
    resource: https://github.com/evaluchat/evaluchat/blob/feat/v08-01-contract/packages/shared/src/research-repository.ts
    title: v1 GitHub research repository contract (Zod schemas)
---

# GitHub research workspaces — trust boundary, OAuth, tokens, and retention

> Design note (2026-08-22, decision-record status: draft). Consolidates ADR-0001
> through ADR-0005 for Evaluchat v0.8 private GitHub research workspaces. Design
> intent and platform guarantees — not contributor setup. Threat model and
> verification obligations live in
> [github-research-threat-model.en.md](https://github.com/evaluchat/research/blob/main/governance/github-research-threat-model.en.md).

## 1. Problem

Evaluchat must edit a researcher's selected private repository and, only after
an explicit publication confirmation, create a draft pull request in the public
`evaluchat/research` catalogue. The platform must:

- prevent a credential compromise on either path from crossing the private/public
  boundary;
- bind GitHub App user authorization to the initiating browser session;
- protect bearer tokens at rest and through rotation;
- retain no private repository content outside the repository itself; and
- keep private content out of HTTP caches and browser persistence.

## 2. Two-app trust boundary (ADR-0001)

### Decision

Use two independently configured GitHub Apps:

1. The user-facing **Evaluchat Research Workspace App** is installed only on
   repositories selected by the researcher. It requests:
   - Metadata: read
   - Contents: read and write
2. The operator-controlled **Evaluchat Catalogue Publisher App** is installed
   only on `evaluchat/research`. It requests:
   - Metadata: read
   - Contents: write
   - Pull requests: write

The workspace app never receives Pull requests, Administration, Workflows,
email, or broad account permissions. The publisher app never receives access
to a researcher's private repository. Installation access tokens are minted
just in time for the selected installation and are never persisted.

Repository creation is a GitHub-hosted hand-off from the Private Research
Starter template with private visibility preselected. Evaluchat does not ask
for Administration permission to create repositories.

Publication stops at a `draft: true` pull request. Evaluchat does not ready,
approve, or merge a public-catalogue pull request.

### Consequences

- A workspace credential cannot publish to the catalogue, and a publisher
  credential cannot read a private workspace.
- Operators must manage two app registrations, keys, installations, and
  revocation procedures.
- Implementation must reject any installation or repository ID outside
  the app's expected trust domain before requesting an installation token.

## 3. OAuth flow — PKCE and one-time state (ADR-0002)

Product sign-in does not grant private-repository access. The Research
Workspace App requires a separate GitHub App user authorization.

### Decision

The Research Workspace App uses GitHub's OAuth web application flow with:

- a fresh high-entropy PKCE verifier and `S256` challenge per attempt;
- a fresh high-entropy `state` value per attempt;
- server-side state that binds the attempt to the authenticated Evaluchat user,
  intended return location, PKCE verifier, creation time, and expiry;
- an exact redirect URI allowlist and an HTTPS callback outside local
  development;
- atomic, one-time consumption of `state` before the authorization code is
  exchanged; and
- a short expiry, after which the attempt fails closed and must restart.

The callback rejects missing, mismatched, expired, already-consumed, or
wrong-user state. Neither authorization codes nor PKCE verifiers are written to
logs, analytics, browser storage, or error-reporting context. A callback
failure does not fall back to an unbound token exchange.

The stored post-callback destination is either a server-defined route ID or a
validated relative Evaluchat path. The OAuth redirect-URI allowlist constrains
where GitHub may return the authorization response; it does not constrain the
post-callback destination, which is validated independently.

### Consequences

- Capturing an authorization code alone is insufficient to complete the flow.
- Callback replay and login-CSRF attempts fail at one-time state consumption.
- Multiple tabs may start separate flows, but each callback is valid only for
  its own state record and verifier.

## 4. Token envelope and rotation (ADR-0003)

The workspace app needs an expiring GitHub user access token so commits are
attributable to the researcher and constrained by both user and installation
permissions. GitHub's current default lifetimes are eight hours for a user
access token and six months for its refresh token. GitHub rotates both values
during refresh.

### Decision

The authorization-code exchange accepts only an expiring user-token response.
At issuance, the flow requires non-empty string values for `access_token` and
`refresh_token`, positive integer values for `expires_in` and
`refresh_token_expires_in`, and `token_type: "bearer"`. Any response that is
missing a field or contains an empty, mistyped, non-positive, or otherwise
invalid value is rejected and requires reauthorization. GitHub omits the
expiry and refresh fields when user-token expiration is disabled; Evaluchat
never persists that non-expiring credential response.

Persist access and refresh tokens only inside a dedicated server-side
AES-256-GCM envelope. Each encrypted field records:

- an envelope version;
- a non-secret key identifier (`kid`);
- a unique 96-bit nonce;
- ciphertext; and
- the 128-bit authentication tag.

The 256-bit encryption key is supplied by the server's secret manager or
runtime environment and is never stored beside ciphertext. Authenticated
additional data binds the envelope to its credential record, token kind, app,
and envelope version so ciphertext cannot be swapped between records.

Refresh begins before access-token expiry and is serialized per credential.
GitHub rotation invalidates both the previous access token and the previous
refresh token, so the GitHub call and local credential commit cannot be treated
as an end-to-end atomic transaction. Before invoking GitHub rotation, Evaluchat
writes a durable blocked marker for the credential version. A successful local
commit atomically replaces both encrypted tokens and their expiries with
GitHub's rotated values before clearing that marker. Old values are not retained
after that commit.

If the process fails after GitHub rotation but before the local commit,
recovery keeps the binding blocked and reconciles which complete credential set
GitHub actually accepts instead of assuming atomic success or failure. It
commits the accepted rotated set if recoverable; otherwise it requires
reauthorization. Key rotation decrypts using the recorded `kid` and re-encrypts
under the active key. Installation access tokens are generated just in time and
never stored.

Authentication-tag failure, an unknown `kid`, refresh rejection, a missing
rotated token, or an interrupted/ambiguous refresh fails closed. Evaluchat
marks the binding blocked and requires reconciliation or reauthorization; it
does not continue with guessed or partially updated credentials.

### Consequences

- Database disclosure does not reveal plaintext GitHub credentials without the
  separately managed encryption key.
- Operations must retain old decryption keys only for the bounded period needed
  to rewrap existing envelopes, then retire them.
- Storage work must use compare-and-swap or equivalent serialization to
  prevent concurrent refreshes from overwriting the newest rotated token.
- Revocation and rotation failure behavior is expanded in the
  [research threat model](https://github.com/evaluchat/research/blob/main/governance/github-research-threat-model.en.md).

## 5. No server-side content retention (ADR-0004)

The private Git repository is the source of truth for research artifacts and
their ordinary history.

### Decision

Repository bodies, frontmatter, evidence, ledger snapshots, seal files, and
their normal Git history live **only** in the bound private repository.

Evaluchat may retain only:

- AES-256-GCM-encrypted credentials;
- numeric GitHub repository and installation IDs;
- encrypted repository display metadata;
- the managed branch and commit/blob pointers;
- cryptographic hashes;
- idempotency and reconciliation state;
- webhook delivery IDs; and
- publication references.

Evaluchat never retains artifact bodies, derived title indexes, commit
messages, raw webhook payloads, or private-content excerpts. Private content is
excluded from LangGraph Store, thread checkpoints, tracing, logs, telemetry,
analytics, backups, search indexes, queues, dead-letter records, and job
payloads. Error records use stable artifact IDs and non-content error codes.

Webhook HMAC is validated against the raw request bytes before parsing. Only
the minimum fields needed for an installation, installation-repositories, or
push event are extracted. The raw body is discarded, and `X-GitHub-Delivery`
is retained only as an idempotency key. Delivery-ID retention covers GitHub's
redelivery window: at least three days for GitHub.com and at least seven days
for GitHub Enterprise Server. An expired or unknown delivery ID triggers
reconciliation against current repository state; Evaluchat never re-applies
the event.

### Consequences

- A repository deletion or revoked grant does not leave an Evaluchat content
  archive behind.
- Private repository AI must be stateless, keep conversation in browser memory,
  and run with tracing disabled. If zero-trace behavior cannot be demonstrated,
  AI remains disabled while manual editing remains available.
- Jobs must carry IDs, pointers, and hashes and fetch authorized bytes just in
  time; content cannot be recovered from a retry queue.
- Operational debugging cannot depend on body excerpts or commit messages.

## 6. Browser-memory-only cache policy (ADR-0005)

Even without server retention, HTTP caches and browser persistence can leave
private artifacts on shared machines, CDN nodes, framework caches, service
workers, crash recovery, or future sessions.

### Decision

Every response that contains private repository content, content-derived
previews, or content-bearing errors sends:

```http
Cache-Control: no-store
```

Routes are dynamically evaluated and excluded from framework, reverse-proxy,
and CDN response caches. Repository requests must not opt into revalidation,
incremental static regeneration, or service-worker caching.

Decrypted repository content and uncommitted edits exist in browser memory
only. They are not written to `localStorage`, `sessionStorage`, IndexedDB, the
Cache API, client databases, persisted state stores, analytics buffers, or
offline drafts. Navigation and unload warn while a draft is dirty, but the
warning does not persist the draft.

Client code clears in-memory content on disconnect, sign-out, workspace
switch, authorization loss, and terminal repository state. Browser extensions,
screen capture, swap, and compromised endpoints remain outside guarantees that
a web application can enforce and are disclosed as residual risk.

User authorization and App installation are separate GitHub grants. Revocation
of the user's GitHub App authorization invalidates the associated access and
refresh tokens; the client clears in-memory content and refuses refresh, even
when refresh-token expiry would otherwise preserve uncommitted text briefly for
copy or download.

Installation removal or loss of repository access revokes the repository
grant, not the user's authorization. GitHub may reject subsequent access or
token refresh. The workspace then enters the status-model state matching the
reported condition: `blocked` with `permission_lost` for lost repository access,
or `blocked` with `installation_suspended` for an unavailable installation, and
offers the corresponding reinstall or access-restoration recovery. Only a
refresh failure caused by user-grant invalidation maps to `read_only` with
`authorization_required` and offers reauthorization. Repository-access and
installation failures are not treated as user-authorization revocation, and do
not by themselves assert that both user tokens are invalid.

### Consequences

- Reloading loses uncommitted work; the product must make "Not committed" state
  and explicit **Commit changes** behavior clear.
- Offline editing and cross-device draft recovery are intentionally unavailable
  in v1.
- Route tests must verify `no-store` on successful and error responses.

## 7. What this design does NOT do

- Does not replace the
  [research threat model](https://github.com/evaluchat/research/blob/main/governance/github-research-threat-model.en.md)
  — leak vectors, verification obligations, and rotation failure modes are
  documented there.
- Does not describe contributor local setup — see the canvas repo
  `CONTRIBUTING.md`.
- Does not ready, approve, or merge public-catalogue pull requests.

## 8. Sequencing

1. Ratify Zod schemas and fixtures in `packages/shared` (v1 repository contract).
2. Implement two-app registration, OAuth PKCE flow, and token envelope storage.
3. Enforce no-retention and `no-store` policies across server, client, and AI
   graph paths.
4. Promote to `concepts/` once v0.8 ships.
