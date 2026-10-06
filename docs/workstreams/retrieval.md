# Retrieval · make evidence reach the answer

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** give the agent the right evidence, with source spans that a checker can inspect.

Scope includes parsing, search, ranking, document versions, and citation links.
A relevant document and a correct answer are separate outcomes.
Measure both.

## Fixed baseline

Pin a corpus snapshot, parser, index, query set, and relevance labels.
Start with a simple lexical search baseline.
Fix the retrieved item count and context token budget.
Use queries from a held-out source or time period where practical.
Report retrieval recall, ranking quality, supported-answer rate,
unsupported claims, index cost, and query latency.

## Three proposed tasks

### 1. Preserve source spans through parsing

Add an adapter for one document format.
Use fixtures with headings, tables, duplicate text, and changed versions.
Return source ID, version, and byte or character offsets with each chunk.

**Verifier:** reconstruct each cited span from the original file.
**Acceptance:** every expected fixture span maps to the correct source version.
Reject missing spans, invented offsets, and silent dropped tables.
Keep expected mappings outside the worker's edit scope.
**Initial budget:** 45 minutes; CPU only; a small licensed fixture set.

### 2. Test one ranking change

Compare lexical search with one bounded candidate, such as lexical search plus re-ranking.
Keep the corpus and context size fixed.
Save ranked results for every query.

**Verifier:** recompute metrics from saved ranks and fixed labels.
Repeat the runtime run on the pinned model, if the candidate uses one.
**Acceptance:** fix the minimum ranking gain and latency limit before dispatch.
Run the answer check too. Ranking alone cannot earn an answer-quality claim.
**Initial budget:** 60 minutes for the adapter.
Re-ranking model calls need a separate call and token allowance.

### 3. Reject unsupported citations

Make a citation checker that validates source identity and quoted spans.
Use correct citations, wrong document versions, broken offsets, and fabricated quotes.
Add questions for which the corpus contains no answer.

**Verifier:** compare outputs with locked expected labels.
**Acceptance:** all known invalid spans are rejected.
All valid spans remain accepted.
Claim support beyond exact quotations requires a separate semantic review.
**Initial budget:** 30 minutes; CPU only; no model calls.

## Failure modes and dependencies

Overlapping chunks can inflate recall. Duplicate answers can leak across splits.
A correct quotation can still fail to support a conclusion.
A missing answer should produce an explicit lack of evidence.
Do not invent a source to complete an answer.
Depend on [evaluation](evaluation.md) for labels and
[reliability](reliability.md) for instructions hidden inside documents.

Fixtures prove parsing and citation mechanics.
A useful retrieval claim needs a real corpus and held-out queries.
A deployment claim also needs index updates, stale document tests,
and access checks for documents with different permissions.

## Source map

- [BEIR repository](https://github.com/beir-cellar/beir): retrieval datasets and common evaluation tools.
- [BEIR paper](https://arxiv.org/abs/2104.08663): a cross-domain retrieval benchmark.

Dataset rights can differ from the code license.
Record the chosen corpus, rights, split, and hashes in the task.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
