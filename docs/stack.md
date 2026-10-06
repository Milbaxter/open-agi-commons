# Stack map

Each row is a planned workstream. Component repos do not exist yet.
The registry is the source for repo status and tested versions.

| Part | Scope | Evidence of improvement |
| --- | --- | --- |
| `compute` — Hardware and distributed compute | Scheduling, hardware use, storage, and fault recovery. | Run the same checked workload with less time, cost, or energy. Count retries and failures. |
| `kernels` — Compilers and numerical software | Compilers, kernels, memory layouts, and numerical precision. | Pass reference correctness tests. Show speed or memory gains on real workloads and named hardware. |
| `data` — Training data | Data collection, cleaning, labels, coverage, and data origins. | Improve unseen-task results at equal training compute. Check data rights and test contamination. |
| `environments` — Environments and curricula | Simulators, task generators, learning order, and rewards. | Check rewards for exploits. Show learning transfers to separately made tasks. |
| `architectures` — Model structures | Attention, recurrence, expert routing, representations, and world models. | Compare capability at equal training and inference budgets. State the tested model sizes. |
| `pretraining` — Pretraining and optimization | Training objectives, optimizers, schedules, and stability. | Reach a fixed capability with fewer resources. Include failed runs and repeat measurements. |
| `posttraining` — Post-training | Instruction tuning, reinforcement learning, feedback, and reward models. | Improve independent task results. Evaluate with a method separate from the training reward. |
| `inference` — Inference and serving | Quantization, caching, batching, and adaptive compute. | Measure quality, cost, memory, and latency on fixed workloads. Include slow requests. |
| `retrieval` — Knowledge access | Search, document parsing, retrieval, citations, and grounding. | Check retrieved evidence and final answers on unseen information. Report each result separately. |
| `memory` — Memory and continual learning | Persistent memory, feedback, adaptation, and retention. | Improve long task sequences. Measure forgetting, false memory, and poisoned input. |
| `reasoning` — Reasoning and planning | Search, plans, program generation, and proof construction. | Check executable solutions, proofs, or final outcomes. Count all attempts within a fixed budget. |
| `tools` — Tool use and action | Software tools, browsers, computer use, and robot interfaces. | Check final outcomes, recovery, and permissions in varied environments. A transcript alone is insufficient. |
| `agent-coordination` — Agent coordination | Delegation, routing, shared state, and cooperation in the system under study. | Compare with a strong single-agent baseline. Count communication, extra calls, and human help. |
| `research` — Autonomous research | Hypotheses, experiment design, implementation, and result analysis. | Reproduce useful findings independently. Measure accepted outcomes per total resource budget. |
| `evaluation` — Evaluation and verification | Benchmarks, graders, statistics, and contamination checks. | Detect known defects. Reproduce results. Test whether scores predict success on independent tasks. |
| `reliability` — Reliability, alignment, and security | Constraint following, uncertainty, prompt injection, containment, and interpretability. | Reduce measured failures while retaining useful capability. Make testable claims with clear limits. |
| `commons` — Project tools and reproducibility | Task formats, contribution tools, result records, and integration. | Let another person reproduce the result. Reduce the work needed to review and integrate useful changes. |


## How the parts fit

Compute, kernels, and data support training.
Environments provide tasks and learning signals.
Architecture, pretraining, and post-training produce models.
Inference serves them. Retrieval, memory, reasoning, and tools support useful action.
Agent coordination and research connect these parts into longer work.
Evaluation, reliability, and reproducibility apply across the stack.

This overview coordinates project development.
The `agent-coordination` workstream studies coordination in the AI system itself.

## First practical slice

Start with evaluation, inference, and memory.
Select an open model and a small reference agent.
Fix the task set and resource budget before testing changes.
Accept the first capability claim only after an independent run confirms it.

Each future repo needs a scope, setup commands, one checked baseline,
an improvement contract, and at least one ready task.
Use the [maintainer role](../roles/component-maintainer.md) to prepare it.
