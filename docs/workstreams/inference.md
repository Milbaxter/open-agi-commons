# Inference · deliver useful work within the budget

[Workstream index](README.md) · [Full stack](../stack.md)

**Goal:** make a fixed open model cheaper or faster to use without an unacceptable loss in quality.

Scope includes caching, batching, quantization, request routing, and bounded retries.
New training methods belong elsewhere.
Change one serving choice at a time. Record model and tokenizer hashes.

## Fixed baseline

Pin one model, engine commit, machine, and request trace.
Keep prompt templates, sampling settings, output limits, and concurrency fixed.
Separate cold-cache runs from warm-cache runs.
Measure correct tasks per total cost, peak memory, time to first token,
end-to-end latency, and the 95th-percentile latency.
Count timeouts and failed requests as outcomes.

## Three proposed tasks

### 1. Detect false cache gains

Build a trace replay with shared prefixes and unique prefixes.
Compare caching on and off. Reset state between cold runs.
Keep warm runs in a separate report.

**Verifier:** replay the same trace from a fresh engine process.
Check response correctness with an independent answer fixture.
**Acceptance:** the report accounts for every request, including failures.
It must identify a deliberately warmed run as warm.
A speed claim also needs the fixed quality floor and latency rule to pass.
**Initial budget:** 45 minutes to build the CPU trace checker.
Model timing requires a separate approved runtime budget.

### 2. Check quantization at the task level

Prepare an adapter that compares two weight formats for one model revision.
Use the same unseen task set and generation settings.
Save per-task results and peak memory.

**Verifier:** load both formats independently and repeat the comparison.
Check weight origins and conversion settings.
**Acceptance:** a maintainer fixes the memory target and quality loss limit before dispatch.
Reject a memory gain if errors exceed that limit.
**Initial budget:** 60 minutes for metadata and report tooling.
Weight conversion, downloads, and GPU runs need explicit limits.

### 3. Stop runaway retry policies

Add a total token and request limit to a serving adapter.
Test a success, a timeout, a partial output, and repeated failures.
Include concurrent requests that share one budget.

**Verifier:** use a scripted engine stub and inspect the call ledger.
**Acceptance:** no accepted request exceeds the fixed allowance.
Retries count toward the total. Exhaustion returns a clear stop result.
Existing successful requests must still pass.
**Initial budget:** 30 minutes; CPU only; no model calls.

## Failure modes and dependencies

A cache can hide repeated prompts. A short output can fake a speed gain.
A mean can hide slow requests. A retry can hide the original failure.
Compare correct work at equal total budgets.
Depend on [evaluation](evaluation.md) for quality checks and
[commons](commons.md) for the resource ledger.

A stub proves control flow. It cannot prove serving performance.
A runtime claim needs the named model, hardware, workload, and repetitions.
Production work also needs cancellation, load limits, and memory recovery tests.

## Source map

- [llama.cpp](https://github.com/ggml-org/llama.cpp): an open inference engine to inspect or extend.
- [vLLM benchmark guide](https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md): client latency measurement and cache reuse pitfalls.
- [vLLM prefix cache design](https://github.com/vllm-project/vllm/blob/main/docs/design/prefix_caching.md): cache structure and isolation considerations.

These are reference projects. A task must pin the chosen revision and license.
Follow the [ready-task gate](README.md#turn-a-proposal-into-a-ready-task).
