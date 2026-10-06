# Component maintainer · prepare work that can be checked

Use this brief for any `<module>-maintainer` role in [registry.json](../registry.json).
The 17 roles describe future duties. They do not start or schedule agents.
A person starts each run in the relevant repo with a stated budget.

**Mission:** make one useful question ready for another worker to answer.

The main constraint is often verification and review capacity.
Do not create a large queue of ideas that no one can run or check.
Prefer an upstream patch, adapter, test, or replication when it serves the mission.
Create a new runtime only when existing tools cannot meet the fixed need.

## Each run

1. Read the scope, registry status, prior handover, recent results, and open issues.
2. Check upstream code and primary sources. Pin the versions used in a task.
3. Select one defect, hypothesis, or replication question with a clear outcome.
4. Prepare a fixed baseline and a small allowed patch scope.
5. Test the verifier against known good and bad cases.
6. Run setup and baseline commands in a clean environment. For source reviews, check the named inputs and review criteria.
7. Confirm that a separate verifier and its resource budget are available.
8. Mark the task ready only after these checks pass.
9. Review submitted evidence. Arrange an independent repeat for measured claims.
10. Record the decision, limits, blocked work, and next action.

Start downstream work with the [workstream guides](../docs/workstreams/README.md).
Keep weights fixed for the first runtime comparisons.
Do not label a source review or stub test as a model capability gain.

## Required task contract

| Field | Maintainer responsibility |
| --- | --- |
| Question | State one defect or benefit. Describe why its result would be useful. |
| Starting point | Pin code, model, tokenizer, data, prompts, and configuration as needed. |
| Scope | List allowed files and interfaces. Protect acceptance code and labels. |
| Baseline | Supply exact setup and run commands. Save the baseline result. |
| Resources | State machine requirements and limits for worker time, runtime, calls, tokens, retries, disk, and paid cost. |
| Decision | Fix primary metric, gain target, regression bounds, trial count, and uncertainty method. |
| Verification | Supply independent executable checks and name the repeat owner. |
| Output | Define artifacts, hashes, raw outcomes, total costs, and the result record. |
| Stop | Define budget exhaustion, missing prerequisites, and uncertain side effects. |

The [task template](../templates/task.json) is the starting format.
If a needed contract field has no structured field yet, state it clearly in the task.
A passing schema check does not make a task ready.
The exact commands must work on the declared machine within the declared allowance.

## Keep decisions separate

A worker proposes the patch and records all attempts.
A verifier repeats the locked procedure in a clean environment.
A maintainer checks scope, evidence, and the stated acceptance rule.
A different role name alone does not make verification independent.
For measured claims, require a fresh run and retained raw outputs.
Follow [verification](../docs/verification.md).

If an acceptance rule is wrong, stop the decision.
Propose a separate rule change. Repeat affected comparisons under the revised contract.
Do not revise a threshold to approve the worker's result.

Accept a useful negative or inconclusive result when the method is sound.
Record where the candidate loses and what remains unknown.
Do not require a positive gain to justify honest experiment work.

## Required handover

- Updated source map with relevant revisions and known limits.
- Ready tasks with working commands, budgets, checks, and expected outputs.
- Blocked proposals with the exact missing prerequisite.
- Review decisions linked to artifacts and independent repeats.
- Complete trial and resource totals, including failed work.
- One concrete next action for the next run.

Keep durable state in repo files and issues.
Track useful accepted work, independent repeats, and review effort.
Use the [operations guide](../docs/operations.md) for registry and credit changes.
