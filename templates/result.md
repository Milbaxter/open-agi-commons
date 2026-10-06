# Result record

Use one record for one bounded claim. Attach it to the PR.
Mark missing evidence as `missing`. Mark an unused field `not applicable`, with a reason.
Label estimates. Preserve raw outputs and failed attempts.

## Claim and ownership

- Task ID, contract version, issue, and PR:
- Work type: research / replication / engineering
- Author and coding tool, if used:
- Claim in one sentence:
- Evidence state: hypothesis / measured result / verified result
- Fixture state, if used: fixture-measured / fixture-rejected
- Integration state: passed / failed / pending / not applicable
- Tested task set, scale, budget, and environment:
- What this result does not establish:

## Frozen contract and inputs

- Contract path, commit, and SHA-256:
- Allowed change scope:
- Baseline code commit and command:
- Candidate code commit and command:
- Model revision, configuration, and license, if used:
- Input data sources, release, split, license, and SHA-256 hashes:
- Grader path or revision, SHA-256, and command:
- Primary metric, unit, direction, threshold, and fixed pass rule:
- Regression limits:
- Public development set:
- Acceptance set owner, hash, access policy, and release plan:
- Known or possible exposure to acceptance data:
- Fixed candidate limit and acceptance submission limit:
- Planned repeats, task count, seeds, run order, and uncertainty method:
- Fixed stop rules and resource limits:

## Environment and baseline check

- Operating system, runtime, and pinned dependencies:
- CPU, GPU if used, available RAM, and drivers if relevant:
- Network and tool permissions:
- Baseline command, date and time in UTC, exit code, and output:
- Baseline artifacts and hashes matched: yes / no
- Environment differences from the contract:

## Attempts and results

List every candidate and retry. Include failed setup, timeout, and rejected output.
Add rows as needed. Link the raw output for each attempt.

| Attempt | Candidate commit | Development or acceptance | Command / output link | Result | Resources | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |

- Primary result, with baseline and candidate values:
- All repeats and task-level results:
- Uncertainty interval, confidence level, and calculation method:
- Multiple tested claims and how selection was accounted for:
- Regression results and failure cases:
- Raw output location and SHA-256 hashes:
- Contract changed after work started: yes / no; link separate review if yes
- Final outcome: gain / no gain / regression / inconclusive
- Limitations and exact next step:

## Total resources

Record development, final acceptance, and verification separately.
For hosted tools with unavailable usage counts, write `unknown`.

| Phase | Wall time | Compute / hardware time | Model calls / tokens | Tool calls | Paid cost | Human review time |
| --- | --- | --- | --- | --- | --- | --- |
| Development, including failures | | | | | | |
| Final acceptance | | | | | | |
| Independent verification | | | | | | |

- Budget limits passed: yes / no
- Unrecorded usage or estimates, with reason and method:

## Independent verification

Leave this section `pending` until a separate verifier supplies their own evidence.
A second agent in the author's session is local review.
An automated fixture checker does not create an independent verifier identity.

- Verifier identity and link to their review:
- Relationship to the author, conflicts, and author help:
- Frozen candidate commit checked:
- Verifier's environment and hardware:
- Date and time in UTC:
- Baseline and acceptance commands:
- Verifier's raw outputs and SHA-256 hashes:
- Contract and inputs matched: yes / no
- Primary rule, regression limits, and budget passed: yes / no for each
- Verdict: confirmed / rejected / inconclusive
- Disagreements and their resolution:

## Integration and review

- Reference agent commit, component versions, and regression set:
- Integration commands and raw outputs:
- Final outcome and resource comparison at the fixed budget:
- Interface compatibility and rollback path:
- If pending or not applicable, reason:
- Reviewer, decision, and evidence label:
- Superseded or disputed result links, if any:

An honest negative result is a valid deliverable.
Keep the claim within the evidence. A merged PR alone does not verify it.
