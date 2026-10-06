# Check a claimed improvement

Each experiment needs an improvement contract.
Use the [task template](../templates/task.json) and [result record](../templates/result.md).

## Define the contract first

Record the question, allowed changes, baseline, resources, budget, and stop conditions.
Pin code, model, data, configuration, and evaluation versions.
State a primary metric, minimum gain, and allowed regressions before the run.
Define the number of runs and how uncertainty will be reported.

## Keep the comparison fair

Use equal resource budgets unless the claim is about a different budget.
Count failed attempts, training, inference, tools, verification, and human review.
Report quality as well as cost or speed.
Check for evaluation data in the training and development inputs.

Public development tests help contributors work.
Acceptance needs fresh or held-out tasks where feasible.
The contributor must not control both the change and its acceptance decision.
Test the grader with known good and bad examples.

## Repeat and review

An independent worker runs the fixed procedure in a clean environment.
Record the code commit, commands, raw outputs, resource use, and disagreements.
Confirm selected winners on fresh runs. Many attempts can produce false gains by chance.
Run an integration check when a reference system exists.

Use three clear states:

- Hypothesis: proposed benefit; not yet tested.
- Measured result: observed under stated conditions; not independently confirmed.
- Verified result: independently confirmed within the stated conditions.

Passing one test does not establish AGI or ASI.
Small-model results support claims at the tested scale.
Report a useful failure with the same care as a gain.

No model experiment has been run in this initial overview repo.
The starter tasks prepare maps and contracts for the first experiments.
