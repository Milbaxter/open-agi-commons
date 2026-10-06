# Roadmap · prove the small loop first

The mission spans the full stack.
The next work improves the software around existing open models.
Do not make the first contribution depend on a new foundation-model training run.

## 1. Make contribution work tangible — available

- Ten downstream workstream guides with 30 bounded task proposals.
- A source map of existing open projects.
- Five ready task files, including offline replication and routing review.
- A read-only local picker that checks declared resource fit and readiness.
- A frozen retrieval fixture with passing and rejecting result paths.
- Evidence, review, handover, and credit rules.
- Repo checks and a daily merged-PR leaderboard.

The fixture demonstrates the work process. It does not report a model capability gain.

## 2. Repeat and challenge the process — next

Have another contributor repeat the retrieval example from a clean checkout.
Compare file hashes and per-query results. Test the task picker against misleading state.
Measure setup time, worker time, verification time, and human review.

**Gate:** a new person can select a task, reproduce its inputs, and submit a checkable result.

## 3. Prepare one fixed-model slice — planned

Select one open model, licensed document set, agent interface, and execution environment.
Prepare question answering with citations, permitted memory, and controlled local tools.
Make the checker reject known bad evidence and wrong final states before changing the agent.
Run the baseline and publish its complete resource record.
The [slice plan](runtime-slice.md) defines the artifacts and gates.

**Gate:** baseline and checker run in a clean environment within named runtime and review budgets.

## 4. Accept the first bounded runtime gain — planned

Prepare one task for retrieval, memory, inference, reasoning, or tool recovery.
Freeze the metric, gain threshold, regression bounds, and attempt budget.
Measure the candidate. Repeat it under separate control.
Check the full slice before claiming a final-task gain.
Retain useful negative and inconclusive results too.

**Gate:** independent evidence supports one stated gain at equal total resources.

## 5. Open component repos where the process works — planned

Create component repos when each has a clear scope, reproducible baseline,
working verifier, review capacity, and a short ready queue.
Record real repo URLs and tested versions in registry.json.
Build integration jobs around actual interfaces.

**Gate:** contributors can work on one component without rebuilding the whole research setup.

## 6. Automate only the parts already understood — planned

Add claim reservations and expiry, attempt ledgers, enforced resource limits,
a separate verifier queue, and durable handovers.
Add coordination after a strong single-agent baseline exists.
Add research agents after experiment limits and evidence review work reliably.

**Gate:** more useful accepted work per total resource and reviewer budget.

These stages have no fixed dates. Evidence and review capacity set the pace.
The component repos, model-assisted slice, and enforcing runner do not exist yet.
