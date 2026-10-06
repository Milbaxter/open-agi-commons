# A small contribution loop you can run

This example makes the work process concrete.
It compares a frozen baseline with a teaching candidate, checks a fixed contract,
and writes enough evidence for another contributor to repeat the run.
It uses public, hand-written English text. There are no model calls or training runs.

## Run it

From the repo root:

```sh
make demo
make demo-reject
```

The passing run writes `work/retrieval-demo/result.json` and `result.md`.
The rejection run writes `work/retrieval-rejected/result.json` and `result.md`.
Local output is ignored by Git. Submit links or a small reviewed result record in a PR.

## What changes

The [baseline](baseline.py) counts query substrings in each document.
Repeated terms and partial-word matches can outrank a document with better term coverage.
The [candidate](candidate.py) matches complete words and counts distinct query terms.
Both break ties by document ID and return no result when their own matching method finds nothing.

| Fixture outcome | Baseline | Candidate |
| --- | --- | --- |
| Correct first result | 5 / 12 | 12 / 12 |
| Regression from a correct baseline result | — | 0 |
| Correct rejection for empty or absent query terms | 2 / 2 | 2 / 2 |

The [corpus](corpus.json) and [queries](queries.json) make every case inspectable.
The public queries have development and acceptance labels to illustrate the workflow.
Both sets are visible to the author. Neither is held out.

## What decides acceptance

[contract.json](contract.json) pins the baseline, corpus, queries, and grader with SHA-256 hashes.
The fixed candidate must meet all gates:

- Correct first result on all 12 fixtures.
- At least three more correct cases than the baseline.
- Correct first result on all eight acceptance fixtures.
- No regression on a case the baseline gets right.
- No invented result for empty or no-overlap queries.

The grader rejects changed frozen artifacts, unknown or duplicate document IDs,
and output that changes on an immediate repeat.
It copies input records so one ranker cannot change the other's corpus.
It compiles captured source bytes directly and rejects changed artifacts after the run.
The recorded hashes identify those captured inputs, rather than cached bytecode.

`make demo-reject` uses the unchanged baseline as the candidate.
It correctly fails the gain and accuracy gates. A valid result record is still useful.

## Read the evidence

The [committed example output](results/result.md) and [raw source record](results/result.json)
show one author-run measurement. The record includes each query, gate, source hash,
checkout state, environment, model-call count, and local runtime.
Wall time is descriptive. It is not an accepted speed claim.

Evidence state is `fixture-measured` or `fixture-rejected`.
Independent verification is always `false` in this runner.
A separate contributor must supply their own repeat record and review verdict.
Use [task 004](../../tasks/004-replicate-retrieval-example.json) for that work.

The candidate and fixtures were designed together.
Passing this example establishes behavior on these cases.
It does not establish retrieval quality on a real corpus, final-answer quality,
generalization, model capability, AGI, or production readiness.

## Try a reviewed alternative

```sh
python3 scripts/run_retrieval_demo.py --candidate path/to/reviewed_ranker.py
```

The file must define `rank(query, documents)` and return an ordered list of known document IDs.
This command executes Python in your local process.
Use reviewed files and an environment suited to their permissions.
A separate clone does not provide process or network isolation.
The runner does not enforce CPU time, memory, network, or spend limits.

For model experiments, add a real licensed corpus, independent acceptance tasks,
a fixed model interface, token accounting, and a final-answer check.
Use the [retrieval guide](../../docs/workstreams/retrieval.md)
and [verification method](../../docs/verification.md) to prepare that next contract.
