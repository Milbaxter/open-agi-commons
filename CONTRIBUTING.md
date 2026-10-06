# Contribute

Use your own coding tool, account, and machine.
Choose a task that fits your budget. Direct human work is welcome too.

## Select and claim a task

1. Check open issues with the `ready` label and their linked files in `tasks/`.
2. Read the scope, budget, checks, and acceptance rules.
3. Comment with the task ID, your planned work, and an expiry time in UTC.
4. A maintainer confirms the claim, assigns the issue, and changes `ready` to `claimed`.

An unconfirmed comment is not an exclusive claim.
You can inspect the task and prepare a local draft while you wait.
A maintainer can release an expired claim. Save partial results so others can continue.
Task files define the work. Issue labels and assignees track current claims.

## Do the work

Fork this repo if you do not have write access. Create a branch for one task.
Read AGENTS.md. Use your supported coding-tool session.
Set a time budget and keep control of any paid compute.
Save work and stop when the budget or a task stop condition is reached.

Change only what the task permits. Ask in the issue if the scope must change.
Record commands, versions, results, total resources, and limitations.
Keep large data and weights outside Git. Record retrieval instructions and hashes.
Use data and code with known rights and licenses.

## Submit a pull request

Run `make check`. Use the PR template.
Link the task issue and state the result in plain words.
For a performance claim, include a filled [result record](templates/result.md).
For a docs change, include sources and the manual checks used to review it.
State which tool helped, if any. The GitHub author receives leaderboard credit.

A useful negative result can be accepted if its method and evidence are sound.
Do not change an acceptance rule to make your own result pass.
Propose a rule change separately, with reasons and review.

## Review and credit

Automated checks validate repo structure and leaderboard behavior.
They do not verify scientific claims.
A maintainer checks scope and evidence before merge.
A capability or performance claim needs an independent run under the fixed contract.

After review, a maintainer can add:

- `verified`: the claim has independent evidence linked in the PR.
- `replication`: the work repeats and checks a prior result.
- `negative-result`: a useful finding that a tested change did not help.
- `documentation`: useful docs or research maps.

Only merged PRs enter the leaderboard. Closed, unmerged PRs do not count.
Category labels are review records. They are not proof by themselves.
Corrections to credit go through an issue and a maintainer review.
