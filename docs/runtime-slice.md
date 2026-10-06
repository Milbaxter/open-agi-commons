# The first fixed-model slice

**Question:** can one component change help an agent answer questions from a fixed document set?

This is the next proposed experiment. It has not been run.
The offline retrieval fixture is a smaller demonstration of its work process.
Select the model, data, commands, and thresholds before this slice becomes ready.

## Use a small, complete task

Give an agent a question and a local document collection.
It can search documents, inspect source spans, read permitted memory, and use local tools.
It must return an answer with evidence, or state that the documents do not support an answer.
The checker inspects evidence and any changed final state.

Start with one agent. Use the same model revision, prompt, tool set, and budget
for the baseline and candidate, except for the component named in the task.
Change one component at a time.

## Build the parts in this order

| Step | Artifact to prepare | Gate before the next step |
| --- | --- | --- |
| 1. Inputs | A licensed corpus, source versions, questions, and answer evidence spans. | Data rights, hashes, and source labels can be inspected. |
| 2. Checker | A result schema and graders for source identity, spans, task outcome, and permissions. | Known valid and invalid outputs receive the expected verdicts. |
| 3. Baseline | One open model interface, lexical search, a simple memory store, and local tools. | A clean checkout reproduces baseline results within the declared budget. |
| 4. Work packet | One allowed patch, primary metric, regression limits, repeats, and verifier owner. | Setup and acceptance commands work before the task is marked ready. |
| 5. Candidate | A change to one component, plus a complete attempt ledger. | Measured results meet the fixed rule and relevant failure checks. |
| 6. Separate repeat | A clean run controlled by another contributor. | Raw outputs confirm or dispute the claim. |
| 7. Integration | The candidate in the full slice with all component settings pinned. | Final outcomes improve within the same total resource limits. |

## Measure the final outcome

Primary outcome: correctly supported answers, including justified abstention.
Also measure unsupported claims, correct source spans, permission failures,
stale memory, task completion, total model tokens and calls, tool calls,
retries, peak memory, and runtime.

Set the gain threshold and regression limits before the candidate run.
Do not use the candidate agent to approve its own answer quality.
Exact span checks can be executable. Semantic support needs a separate labeled test
or a calibrated review method with measured grader errors.

## Give each worker one small change

- **Retrieval worker:** improve ranking while holding context size and the model fixed.
- **Memory worker:** fix stale facts or deletion while holding retrieval and the prompt fixed.
- **Tool worker:** improve retry or timeout handling while holding the planner fixed.
- **Reasoning worker:** change search or stopping rules under the same total call budget.
- **Inference worker:** change serving settings while preserving task-quality limits.
- **Evaluation worker:** add grader tests in a separately reviewed acceptance change.
- **Reliability worker:** prepare paired normal and failure tasks before candidate evaluation.

Each result records component scores and the final answer outcome.
A ranking gain alone supports a retrieval claim.
It supports a final-answer claim only if that check passes too.

## Minimum failure set

Include no-answer questions, misleading repeated keywords, stale documents,
contradictory records, deleted memory, cross-user records, tool timeouts,
interrupted writes, duplicate retries, and instructions hidden in documents.
Add fresh task variants for independent acceptance where feasible.

## Resource boundary

Coding-agent work, open-model runtime, separate verification, and review are separate budgets.
The local picker does not enforce them.
The experiment runner must count calls and stop jobs at the declared limits
before it can run unsupervised.
Do not mark this slice ready until its runtime and verification costs are known.

Use the [upstream map](research-landscape.md) to select existing parts,
the [workstream guides](workstreams/README.md) to prepare bounded changes,
and the [verification method](verification.md) to decide what the evidence supports.
