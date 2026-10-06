# Task queue

These tasks prepare the project for experiments or check the working overview.
All fit a CPU laptop. Two can run offline after checkout.
The issue is the source for a live claim. Task files hold the fixed work contract.

| ID | Work | Budget | Spec |
| --- | --- | --- | --- |
| 001 | Map open evaluation tools | 30 minutes | [Task](001-evaluation-map.json) |
| 002 | Draft an inference experiment contract | 30 minutes | [Task](002-inference-contract.json) |
| 003 | Draft a memory experiment contract | 30 minutes | [Task](003-memory-contract.json) |
| 004 | Repeat the retrieval example | 15 minutes | [Task](004-replicate-retrieval-example.json) |
| 005 | Challenge the task picker | 20 minutes | [Task](005-audit-task-routing.json) |

See [GitHub issues](https://github.com/Milbaxter/open-agi-commons/issues) for claims and status.
The spec records readiness at review. Issue labels record the live state.
The checks validate task structure. A human reviewer applies the acceptance rules.

```sh
make pick
python3 scripts/pick_task.py --profile cpu --minutes 20 --offline --work-type engineering
python3 scripts/pick_task.py --profile cpu --minutes 30 --work-type research --live
```

The picker explains exclusions and ranks eligible tasks by priority, budget, and ID.
It cannot reserve work, verify prerequisite claims, or enforce agent spending.
See the [routing guide](../docs/work-routing.md).

The [workstream guides](../docs/workstreams/README.md) contain 30 more task proposals.
They need prepared inputs, working commands, and fixed thresholds before dispatch.
