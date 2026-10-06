# Build on work that already exists

Open AGI Commons should improve the software around open models.
That includes search, memory, plans, tools, serving, and checks.
Existing projects give us parts to study and improve.
Our contribution is a clear task, a useful patch, and evidence that survives review.

**Status:** these are upstream candidates. Selection and integration remain planned.
The source and license links below were checked for this map.
The linked commits record the source review. They are not tested integration versions.
Use [registry.json](../registry.json) for actual component status.

## A small map of useful foundations

The last column proposes work for Commons. It is not a claim about a current defect.
Choose one task with one baseline and one fixed budget.

| Part | Primary source and code license | A useful bounded task | What must be checked |
| --- | --- | --- | --- |
| Local inference | [llama.cpp](https://github.com/ggml-org/llama.cpp) · [MIT](https://github.com/ggml-org/llama.cpp/blob/5ad1c5da0ad7f6176256b823925aad19134f0263/LICENSE) | Compare one cache or quantization setting on one named machine. | Answer quality, peak memory, total time, and slow requests. Faster tokens alone do not establish better task performance. |
| Shared inference | [vLLM](https://github.com/vllm-project/vllm) · [Apache-2.0](https://github.com/vllm-project/vllm/blob/385d86a6cf6f05051899b53d83ec55c63cccb379/LICENSE) | Reproduce serving behavior for a fixed request mix. Then change one scheduling or caching setting. | Task quality, throughput, latency distribution, and failed requests on the same hardware. Serving compute needs a separate budget. |
| Search | [SQLite FTS5](https://sqlite.org/fts5.html) · [public domain](https://sqlite.org/copyright.html); [Faiss](https://github.com/facebookresearch/faiss) · [MIT](https://github.com/facebookresearch/faiss/blob/83ae8b0908312c1e40734a806a3cc435b64f9496/LICENSE) | Compare text search with vector search on a fixed, licensed document set. | Retrieval recall, source accuracy, final answer quality, index cost, and query cost. Faiss searches vectors; it does not create embeddings or check citations. |
| Persistent memory | [Letta Code](https://github.com/letta-ai/letta-code) · [Apache-2.0](https://github.com/letta-ai/letta-code/blob/4b028fab07c69edaac2ddb4f7b9a43573ff20d81/LICENSE) | Test when to write, update, retrieve, or delete one class of memory. | Later task success, stale facts, false memories, and deletion behavior. Fix the backend and memory settings. A stateful agent is a foundation to test, not proof of reliable long-term learning. |
| Program and prompt improvement | [DSPy](https://github.com/stanfordnlp/dspy) · [MIT](https://github.com/stanfordnlp/dspy/blob/bc8af7ed3d5ee0b892211e5c03274396442a413c/LICENSE) | Change one module, search policy, or prompt under a fixed call budget. | Fresh-task outcomes and the cost of all optimization attempts. Keep development examples separate from acceptance examples. More agents need a strong single-agent comparison. |
| Checked reasoning | [Lean 4](https://github.com/leanprover/lean4) · [Apache-2.0](https://github.com/leanprover/lean4/blob/0f6e0e910a2b4aaa46735c2b0dc992ef789df3a1/LICENSE) | Improve proof search for a fixed set of formal statements. | Kernel-checked proofs, the declared assumptions, and all search attempts. Reject placeholders and unapproved axioms. A proof checks the formal statement; the statement must also match the intended question. |
| Code tools | [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) · [MIT](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/LICENSE.md) | Change one tool interface or recovery rule on isolated code tasks. | Fresh tests and the final repository state. Count retries and human help. Pin the agent version and execution environment. A plausible transcript is weaker evidence than an independently checked result. |
| Agent evaluation | [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) · [MIT](https://github.com/UKGovernmentBEIS/inspect_ai/blob/5d97e38cee66d640b3c4612f9c13d7fffcbe2d3f/LICENSE) | Add a task, scorer test, or trace that exposes one failure mode. | Known pass and fail cases, repeat runs, and scorer agreement. A framework provides tools; a valid experiment still needs a fixed contract and independent review. |
| Model evaluation | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) · [MIT](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/LICENSE.md) | Reproduce a small model baseline or fix one task adapter. | Exact model, tokenizer, prompt, task version, and raw outputs. A model benchmark score does not establish agent success or general intelligence. |
| Small model adaptation | [PEFT](https://github.com/huggingface/peft) · [Apache-2.0](https://github.com/huggingface/peft/blob/e13de7e469d37e3163d93f2356ec013c7a7e1f0a/LICENSE) | Check one small adapter experiment after a runtime baseline exists. | Independent task gains, regressions, training resources, and inference cost. Training fewer parameters can reduce cost. It still needs model access, suitable hardware, and a training budget. |

## Choose the smallest system that can answer the question

Start with a fixed model interface, a local document set, a memory store, and a task runner.
Text search and simple stored records are useful baselines.
Add vector search, an agent framework, or model adaptation when the task needs it.
Each extra part adds setup, failure modes, and work for reviewers.

Check project status before each selection.
[Letta's original repo](https://github.com/letta-ai/letta) points current work to Letta Code.
[SWE-agent](https://github.com/SWE-agent/SWE-agent) recommends mini-SWE-agent for new work.
These changes are why a source map must stay separate from a tested version record.

Prefer a patch to an existing project when its scope fits.
Follow that project's contribution rules and acceptance process.
Record an upstream patch as a dependency only after a maintainer selects and tests it.
External projects in this map are separate projects, with separate maintainers.
They are not Commons components or partners.

For reliability work, test each proposed system against concrete failures.
Examples include a document that issues tool commands, stale memory, invalid tool arguments,
and an interrupted operation that an agent retries.
Check both blocked failures and useful task completion.
For research work, ask for a reproducible experiment and a supported conclusion.
An agent's own judgment of its research quality is not an acceptance test.

## Keep rights and evidence attached to the work

The code license covers the named code project.
Model weights, data, embeddings, optional dependencies, and hosted services have their own terms.
Record each artifact's source, license or terms, exact version, and content hash.
Retain the required notices when code is reused.
Check bundled files and dependencies before redistribution.

Pin versions in the experiment contract.
Then run the [verification process](verification.md).
Publishing a result requires enough method and evidence for another person to check it.
The result must state its hardware, task scope, resource budget, and limits.

Return to the [stack map](stack.md) or [contribution guide](../CONTRIBUTING.md).
