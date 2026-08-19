---
type: Concept
id: finding-authoring-ux
title: Evidence Ledger workspace and light Finding authoring
description: "Design plan: Evidence Ledger as a workspace item with a template-rendered filter canvas, immutable source-linked snapshot, GitHub publication, and a deliberately light Finding starter that cites published ledgers."
lang: en
origin: native
status: draft
tags: [design, evidence-ledger, workspace, canvas, findings, research, github, ai-assistance, human-review, okf]
applies_to: 0.5.9
timestamp: 2026-08-19T09:14:38Z
generated: { by: codex/gpt-5, at: 2026-08-19T09:14:38Z }
sources:
  - id: finding-authoring
    resource: https://github.com/evaluchat/knowledge/blob/main/designs/finding-authoring.en.md
    title: Finding authoring — evidence ledgers and human-controlled claims
  - id: evidence-publishing
    resource: https://github.com/evaluchat/knowledge/blob/main/designs/evidence-publishing.en.md
    title: Evidence publishing mechanics — the workspace Evidence action
  - id: review-protocol
    resource: https://github.com/evaluchat/research/blob/main/governance/review-protocol.en.md
    title: Claim governance — review protocol for findings
  - id: github-protected-branches
    resource: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
    title: Managing protected branches — GitHub Docs
  - id: github-pr-reviews
    resource: https://docs.github.com/en/pull-requests/reference/pull-request-reviews
    title: Pull request reviews — GitHub Docs
---

# Evidence Ledger workspace and light Finding authoring

> Proposed V1 product specification (2026-08-18; draft). This is a
> concreteisation of the [finding-authoring decision record](finding-authoring.en.md).
> It keeps the product Markdown-native: versioned evidence templates define the
> available facts, a deterministic resolver creates ledgers, and GitHub stores
> the published artifacts. It does not describe a shipped feature or establish a
> research finding.

## 1. V1 decisions

The Evidence Ledger—not a Finding editor—is the first research synthesis
surface to build. It makes a declared slice of already public, accepted evidence
inspectable and citable without becoming a data-mining system or an AI verdict.

| Decision | V1 product behaviour |
| --- | --- |
| Entry point | **Create workspace item** offers existing **Templates** and **Methods**, plus new **Evidence Ledger**. The new item opens a ledger-configuration Canvas, not a blank document. |
| Method selection | The first required choice is one published **Method version** that has an evidence template and at least one accepted contribution. The method card exposes its linked questions, template version, and accepted-evidence count. One method version per ledger keeps V1's schema and comparability boundary clear. |
| Ledger boundary | An Evidence Ledger tabulates contributions from exactly one Method version and its one resolved evidence-template version. Its published frontmatter records both identities. A ledger also selects exactly one research question linked by that Method version. |
| Schema source | The resolved `evidence-template.en.md` versions declare the small set of typed, factual fields that can be used as ledger dimensions. No separate query language or warehouse schema is introduced. |
| Filter UI | Declared enumerations render as multi-select controls; declared numbers and dates render as inclusive min/max controls (a slider may be used as a convenience, but exact endpoints are always visible). |
| Scope | After method selection, a linked research question is required and locked once the configuration is generated. The default is all accepted evidence for that exact method version and question; filters can only narrow that set by declared facts. There is no prose, keyword, outcome, sentiment, or “supporting evidence” filter. |
| AI in configuration | The assistant can explain a field, clarify its `unknown` value, compare safe filter options, and describe the resulting preview. It cannot write filters, generate a ledger, or publish; every filter change is an explicit human action. |
| Generate | **Generate ledger** deterministically creates a new, read-only Ledger Snapshot Canvas context. The configuration remains editable; the snapshot never is. |
| AI in snapshot | The assistant can navigate and describe the sealed ledger with source citations, surface counterevidence and gaps, and explain why a comparison may be invalid. It cannot amend the snapshot, choose a finding claim, or publish. |
| Publish | A human GitHub collaborator explicitly publishes a selected snapshot through a PR to public `evaluchat/research`. On merge, it is a citable, immutable `Evidence Ledger` at `evidence-ledgers/<ledger-id>.en.md`. |
| Finding V1 | A normal Canvas **Finding starter** is a recommended Markdown template plus OKF/Research validation. It must declare one or more research questions and cite one or more *published* ledgers. It does not yet introduce a separate Finding workbench, claim-authoring AI, tier workflow, or reviewer-management UI. |

The public repository is the only V1 destination. A connected GitHub account
with current collaborator/write access is required for the platform's ledger or
finding publication flow; invitation and revocation remain GitHub operations.
This gates the platform workflow, not unsolicited fork PRs made outside it.

## 2. The workspace journey

```text
Create workspace item
        │
        ▼
Select Method version → linked research question
        │
        ▼
Evidence Ledger configuration Canvas  (editable, human-controlled)
        │  Generate ledger
        ▼
Ledger Snapshot Canvas context       (read-only, source-linked)
        │  Publish selected snapshot
        ▼
GitHub PR → merged Evidence Ledger   (immutable, citable source)
        │
        ▼
Finding starter links published ledger(s) (human-authored, light V1)
```

### 2.1 Select a ledger-ready Method version and question

The user selects **Evidence Ledger** in **Create workspace item**. The opening
Canvas first shows **Select a Method**. It lists only published Method versions
that have a resolved `evidence-template.en.md`, at least one linked research
question, and accepted evidence. A card displays:

| Card field | Purpose |
| --- | --- |
| Method title, ID, and exact version | The fixed intervention/evidence contract for this ledger |
| Linked research questions | The questions available in the next selector |
| Evidence-template ID and version | The schema that will render the filter controls |
| Accepted-evidence count | The current number of ledger candidates before question and fact filters |
| Status | **Ledger ready** or a mechanical reason it cannot be selected |

The version is an explicit selector, not an implicit “latest”. Choosing a
Method version narrows the question selector to the questions linked by that
version. If it has one question, the Canvas preselects it but still displays the
canonical link. If it has several, the user must choose one. The chosen method
version and question form the baseline scope; changing either clears downstream
filters and preview, while prior generated snapshots remain unchanged.

V1 creates a ledger for exactly one Method version and its resolved evidence
template version. A researcher wanting to inspect two Methods creates two
ledgers, each with its own template semantics, then compares them as separate
sources in a later Finding. A cross-method ledger is deferred until the platform
can define compatible fields, missingness treatment, and comparability rules
explicitly rather than pretending different templates are one schema.

The Canvas then renders the structured configuration in this order:

1. **Selected Method version and research question** — fixed, canonical links
   with the exact evidence-template version that provides the dimensions.
2. **All accepted evidence for this Method version and question** — an
   uneditable baseline count. This makes the initial scope visible before any
   narrowing filter is applied.
3. **Filter by declared facts** — generated controls grouped as Context,
   Intervention profile, and Collection date. A field unavailable in historical
   evidence remains visible as `unavailable`, not silently inferred.
4. **Scope preview** — server-calculated included count, excluded count by
   mechanical reason, count missing each chosen dimension, and the exact
   predicate that will be sealed.
5. **Generate ledger** — the only action that creates a snapshot.

If the catalog has no ledger-ready Methods, the empty state says **No Methods
with accepted evidence yet** and links to the relevant Method's Evidence action.
If a published Method has a missing template, unlinked question, or no accepted
evidence, it is shown only in an unavailable section with that mechanical reason
and no **Select** action. The user cannot bypass this by pasting a Method ID.

The initial Canvas is a workspace item like existing form-aware threads: it is
owned through existing workspace ownership metadata and keeps its configuration
in the Canvas. It is neither a Finding nor a repository artifact, and it is not
listed as evidence in the Research catalog.

### 2.2 Template-declared dimensions

An evidence template opts a field into ledger filtering. Only factual Context,
method, or collection fields may opt in; owner judgements, Results, narrative
observations, reflections, limitations, and model-generated classifications may
not. The template also fixes the field's ID, type, allowed values, and missing
semantics for its version.

```yaml
fields:
  education_level:
    type: select
    options: [k12, tertiary, adult, other, unknown]
    ledger_dimension:
      role: context
      control: multi-select
  country_code:
    type: select
    options: [US, ZA, GB, other, unknown]
    ledger_dimension:
      role: context
      control: multi-select
  collection_date:
    type: date
    ledger_dimension:
      role: collection
      control: range
```

The platform catalog generator mirrors this metadata with the selected evidence
template version, as it does the template itself. The client renders the
metadata; the server remains the sole resolver and validates that a requested
predicate uses only fields and values declared by that fixed template version.

For a selected filter, `unknown` is a real recorded value. Evidence whose
template predates the field is separately `unavailable`. Neither state may be
mapped to a guessed value, discarded from the baseline, or rewritten by an AI.

### 2.3 Filter behaviour and safe assistance

The configuration Canvas uses controls rather than a general-purpose query
builder:

| Dimension type | Canvas control | Canonical predicate |
| --- | --- | --- |
| `select` | multi-select dropdown | `in: [k12]` |
| `date` / `number` | inclusive minimum and maximum inputs; optional paired slider | `gte: …`, `lte: …` |
| declared intervention profile | multi-select dropdown | `in: [profile-id]` |
| unavailable, narrative, outcome, or AI-derived value | no filter control | not expressible |

For example, a K–12 US extract is persisted as an exact fact predicate, not a
natural-language label:

```yaml
filters:
  context.education_level: { in: [k12] }
  context.country_code: { in: [US] }
```

The configuration assistant can answer questions such as “What does `unknown`
mean here?”, “Which countries have evidence?”, or “How would this filter change
the count?” It receives the template schema and server-produced aggregate
preview only. If it suggests a predicate, it presents it as text plus the
anticipated count; the human must select the values through the Canvas controls.
There is no assistant edit, Apply, save, generate, commit, or publish tool.

The scope preview always shows the all-eligible baseline for the selected Method
version and question, plus an accounting table:

| Bucket | Meaning |
| --- | --- |
| Included | Matches every declared predicate |
| Outside declared scope | Has a known value that does not match a predicate |
| Unknown | Has the selected field but recorded `unknown` |
| Unavailable | Uses a template version that does not contain the selected field |
| Resolver exclusion | Unlinked question, invalid provenance, inaccessible, or not accepted |

This distinguishes a fact-based slice from cherry-picking. It also gives a
critic or an AI agent enough information to identify what the slice cannot say.

### 2.4 Generate a read-only Ledger Snapshot

**Generate ledger** is enabled only after the question resolves and the preview
is current. It stores a canonical, sorted manifest and creates a new read-only
Canvas context named **Ledger Snapshot**. The configuration item remains open
for changes; any changed question, filter, source commit, template version, or
input hash creates another snapshot rather than altering the prior one.

The snapshot header displays its ledger ID, Method and question versions,
canonical predicate, source commit, template/resolver/render versions, input
fingerprint, creation time, and every bucket count. Its content has five
read-only views:

| View | Required material |
| --- | --- |
| **Scope** | baseline, predicate, inclusion/exclusion accounting, and unavailable/unknown counts |
| **Evidence** | every included contribution with source link, hash, method/version, and declared context values |
| **Descriptive views** | only deterministic distributions of versioned structured fields, retaining `not-applicable` and `insufficient-information` |
| **Comparability** | method/version, resolved levers, contributor/context clustering, and explicit comparison warnings |
| **Counterevidence and gaps** | negative responses, contradictions, open challenges, alternative explanations, missingness, and questions the record cannot answer |

Counterevidence and gaps is always visible in the snapshot navigation and has a
badge when non-empty. The renderer may not add a conclusion, confidence score,
claim, or positive-pattern summary.

The snapshot assistant sees only this sealed manifest, rendered values, and
manifest-linked source records. It may explain a source, locate a distribution,
identify a gap, or test whether a proposed *fact description* matches the
snapshot. Every factual answer cites ledger source IDs and is labelled
**descriptive**, **challenge**, **insufficient evidence**, or **human decision
required**. It cannot write to the snapshot or use unbounded repository/web
search.

### 2.5 Publish a snapshot

The snapshot's **Publish** action is distinct from Generate. It first checks
that the GitHub account connected to the workspace still has collaborator/write
access to `evaluchat/research`; otherwise it reports the missing access and
creates no branch or PR.

For an eligible user, Publish presents a read-only diff containing one file:

```text
evidence-ledgers/<ledger-id>.en.md
```

It reapplies consent and anonymisation validation before any public write. The
human confirms destination, source commit, fingerprint, public-data declaration,
and file contents. The platform then creates a draft PR under the connected
user's GitHub identity. A snapshot is **published** only once that PR merges;
until then it is an unpublished workspace artifact and cannot be selected as a
Finding source.

The published file contains the immutable scope and provenance needed to
reconstruct its extract:

```yaml
---
type: Evidence Ledger
id: <ledger-slug>
lang: en
origin: native
status: stable
title: <human-readable scope title>
description: Source-linked descriptive ledger for one question and declared evidence scope.
question:
  resource: <canonical Research-question URL and version>
method:
  id: <Method ID>
  version: <Method version>
evidence_template:
  id: <evidence-template ID>
  version: <evidence-template version>
scope: <canonical predicate>
source_commit: <Research repository SHA>
input_fingerprint: sha256:<canonical-manifest hash>
render_hash: sha256:<rendered-ledger hash>
resolver_version: <semver>
generated: { by: evaluchat-ledger-service/<version>, at: <ISO timestamp> }
---
```

Its Markdown body contains the rendered source-linked views and a canonical
manifest or link to one. A refresh always has a new ID and path; Git history and
the fingerprint preserve the old scope exactly. A ledger can be published before
any Finding exists and can be cited by more than one Finding.

## 3. Light Finding authoring

V1 deliberately does not build another specialised authoring application. A
human starts from a **Finding starter** in the normal Templates workflow and
writes in an ordinary Markdown Canvas. The starter supplies a recommended body
shape and the Research fields that existing validation needs; it does not offer
claim suggestion, tier recommendation, or AI document editing.

```yaml
---
type: Finding
id: <finding-slug>
lang: en
origin: native
status: provisional
title: <human-written English title>
description: <human-written English summary>
authors:
  - name: <human author>
claim: <human-written falsifiable claim>
confidence: low
research_questions:
  - resource: <canonical Research-question URL and version>
evidence_ledgers:
  - id: <published-ledger-slug>
    path: /evidence-ledgers/<published-ledger-slug>.en.md
    question: <canonical Research-question URL and version>
    source_commit: <Research repository SHA>
    input_fingerprint: sha256:<canonical-manifest hash>
---
```

```markdown
# <human-written title>

## Claim

## Research questions

## Evidence ledgers

## Declared scope

## Interpretation

## Counterevidence and alternative explanations

## Limitations
```

The ledger picker resolves only merged artifacts in `evidence-ledgers/`. A
Finding must add at least one ledger; it may add more than one, including
ledgers from different Methods. Each selected ledger inserts a read-only
reference card and an `evidence_ledgers` entry; it does not write the claim or
interpretation. The picker adds the ledger's research question to
`research_questions` if it is not already declared.

The user may still edit all human-authored Finding content. A later Finding PR
runs existing OKF and claim checks plus linked-ledger validation:

1. `research_questions` and `evidence_ledgers` are non-empty lists;
2. every ledger path resolves to a merged `type: Evidence Ledger` artifact;
3. its source commit and input fingerprint match the entry in the Finding;
4. each ledger's one Method and evidence-template identities are present and
   internally consistent; and
5. every ledger question appears in `research_questions`, and every declared
   research question has at least one cited ledger.

This allows a human to make a Finding across multiple Methods without allowing a
ledger itself to conceal a cross-method schema merge.

The public GitHub PR remains the human-review surface. The existing deterministic
claim checker reports form and routing only; a `checks-pass` label must never be
shown as human approval. Any required approver cohort, quorum, independence rule,
or `CODEOWNERS` configuration remains an explicit Research governance decision,
not a platform role.

## 4. Verification by critics and agents

A published ledger is an inexpensive verification surface: a critic or bounded
AI agent can read one immutable Markdown artifact, inspect its canonical scope,
and follow its source links. It can also generate a new fact-based extract from
the same source commit when it needs to test a different scope.

The verifier must state which of these it did:

| Mode | Permitted conclusion |
| --- | --- |
| **Exact-ledger verification** | Whether the Finding's linked ledger exists, is unmodified, and contains the stated descriptive fact/citation |
| **Alternative-scope extract** | What a different, declared fact predicate contains; it is not confirmation or refutation of the Finding's original scope |
| **Insufficient data** | A field is unknown/unavailable, the source commit is unavailable, or the requested question cannot be answered from the ledger |

The verifier must not infer missing classifications, invoke unlisted sources,
hide counterevidence, or decide whether the human claim is true. This makes
partial-data checks fast while preserving the distinction between an extract and
a research judgement.

## 5. Minimal components and contracts

| Component | Responsibility | Deliberately absent |
| --- | --- | --- |
| Evidence-template catalog | publishes `ledger_dimension` metadata with each versioned template | universal data schema |
| Ledger configuration renderer | turns those fields into Canvas controls and previews the exact scope | free-form search/query language |
| Deterministic resolver | reads public accepted evidence, creates sorted manifest, counts buckets, and hashes the result | weighting, ranking, statistical/causal inference |
| Ledger snapshot renderer | builds read-only, source-linked Markdown/Canvas views | finding, verdict, confidence, or AI prose synthesis |
| Bounded ledger assistant | schema navigation and source-cited descriptive/challenge help | canvas write, PR, publish, tier, or review tools |
| GitHub publish service | validates public-safety preconditions and creates human-confirmed ledger PRs | private repository destinations, auto-merge, or bot approval |
| Finding starter | supplies Markdown and validated fields, selecting published ledger references | a second specialised Finding editor |

The derived index may be a small build-time or resolver-time map of declared
dimension values from public Markdown evidence. It is not a new analytics
database: its only rows are evidence ID/path, template version, declared
filterable field values, and source hash. Markdown evidence remains the source
of truth.

## 6. Acceptance criteria

| Scenario | Required result |
| --- | --- |
| User creates Evidence Ledger item | Canvas first lists ledger-ready Method versions, then exposes only their linked questions, all-eligible baseline, and dimensions declared by the selected template version. |
| No ledger-ready Method exists | Canvas shows the mechanical absence reason and the Evidence-collection path; it never offers a blank or manually entered Method scope. |
| User selects K–12 and US | Preview shows an exact predicate, included count, outside-scope count, `unknown`, `unavailable`, and resolver exclusions. |
| User tries prose/outcome filtering | No control or API predicate exists; server rejects a forged request. |
| Assistant suggests a scope | It supplies explanation/text only; values change only through an explicit human Canvas action. |
| User changes configuration after Generate | Prior snapshot stays readable and hashed; a new snapshot is created. |
| Snapshot contains contradictory evidence | It appears in Counterevidence and gaps and is available to the snapshot assistant. |
| GitHub access is lost | Publish is denied before branch/PR creation; private workspace snapshot remains unchanged. |
| Ledger PR merges | Artifact is selectable by the Finding starter and exposes its immutable path, commit, and fingerprint. |
| Ledger PR has not merged | It cannot be selected as a Finding source. |
| Finding has no question or no ledger | Validation fails before a PR can be created. |
| Finding cites one or more ledgers | Validator resolves every entry and rejects a missing, wrong-type, wrong-question, wrong-Method/template, wrong-commit, or wrong-fingerprint target. |
| Finding declares a question without a ledger | Validation fails; every declared question needs at least one cited ledger, and every cited ledger question must be declared. |
| Critic asks for a different slice | System produces a separately labelled, reproducible extract; it does not claim to verify the original Finding scope. |

## 7. Delivery sequence

1. **Method availability and template contract** — derive ledger-ready Method
   versions from published Method/question/template/evidence links; add and
   validate `ledger_dimension` metadata, taxonomy values,
   `unknown`/`unavailable` semantics, and version compatibility using synthetic
   evidence templates.
2. **Workspace item** — add **Evidence Ledger** to Create workspace item,
   render the Method-version and linked-question selectors, then render the
   editable configuration Canvas with deterministic preview counts.
3. **Snapshots** — implement manifest hashing, immutable read-only Ledger
   Snapshot contexts, source-linked views, configuration history, and bounded
   assistant access.
4. **Ledger publication** — define `evidence-ledgers/` in Research, create the
   GitHub collaborator-gated publish PR, and validate public consent/privacy,
   OKF fields, one-Method/template identity, source commit, and hashes.
5. **Light Finding starter** — add the template, published-ledger picker, and
   one-or-more question/ledger and linked-ledger checks to the existing Research
   validation path.
6. **Review governance** — separately decide the GitHub reviewer cohort, quorum,
   branch rule, and relationship to provisional/tentative auto-routing before
   requiring approvals for Finding PRs.
7. **Controlled pilot** — use synthetic, contradictory, incomplete, and
   cross-template fixtures before any classroom evidence; monitor resolver,
   publication, and validation failures, never “positive findings”.

## 8. Out of scope

- an arbitrary data-mining or SQL-like query platform;
- filtering evidence by apparent conclusion, free-text narrative, or AI-created
  classifications;
- editing an immutable snapshot or reusing a fingerprint after inputs change;
- raw student work, raw transcripts, private analytics, or unpublished evidence;
- AI-authored Findings, automatic claim selection, tier choice, approval, or
  merge; and
- a private-repository destination, reviewer roster, or `CODEOWNERS` policy.

# Citations

[1] [Finding authoring — evidence ledgers and human-controlled claims](finding-authoring.en.md)

[2] [Evidence publishing mechanics](evidence-publishing.en.md)

[3] [Claim governance — review protocol for findings](https://github.com/evaluchat/research/blob/main/governance/review-protocol.en.md)

[4] [Managing protected branches — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

[5] [Pull request reviews — GitHub Docs](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)
