#!/usr/bin/env python3
"""Run a fixed retrieval fixture contract. This is not an independent model evaluation."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/retrieval"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_ranker(path, source=None):
    # A local candidate is executable code. Run only reviewed files in an isolated clone.
    # Compile the recorded bytes directly; timestamp-valid .pyc files can be stale.
    source = path.read_bytes() if source is None else source
    module = ModuleType("retrieval_candidate")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    if not callable(getattr(module, "rank", None)):
        raise ValueError("Ranker file must define a callable rank(query, documents).")
    return module.rank


def checked_ranking(rank, query, documents):
    document_ids = {doc["id"] for doc in documents}

    def snapshot():
        ranked = rank(query, deepcopy(documents))
        if not isinstance(ranked, list) or any(not isinstance(item, str) for item in ranked):
            raise ValueError("Ranker must return a list of document IDs.")
        frozen = tuple(ranked)
        if len(frozen) != len(set(frozen)) or not set(frozen) <= document_ids:
            raise ValueError("Ranker returned duplicate or unknown document IDs.")
        return frozen

    first = snapshot()
    if snapshot() != first:
        raise ValueError("Deterministic fixture ranker changed its output on repetition.")
    return first[0] if first else None


def judge(rows, thresholds):
    total = len(rows)
    if not total:
        raise ValueError("An empty evaluation cannot pass.")
    acceptance_rows = [row for row in rows if row["split"] == "acceptance"]
    if not acceptance_rows:
        raise ValueError("Acceptance fixtures are missing.")
    baseline_correct = sum(row["baseline_correct"] for row in rows)
    candidate_correct = sum(row["candidate_correct"] for row in rows)
    regressions = [row["id"] for row in rows if row["baseline_correct"] and not row["candidate_correct"]]
    guard_failures = [row["id"] for row in rows if row["expected_top1"] is None and row["candidate_top1"] is not None]
    gates = {
        "overall_accuracy": candidate_correct / total >= thresholds["minimum_accuracy"],
        "minimum_gain": candidate_correct - baseline_correct >= thresholds["minimum_extra_correct"],
        "acceptance_accuracy": sum(row["candidate_correct"] for row in acceptance_rows) / len(acceptance_rows)
            >= thresholds["minimum_acceptance_accuracy"],
        "no_regressions": len(regressions) <= thresholds["maximum_regressions"],
        "empty_and_no_overlap": not guard_failures,
    }
    return {"baseline_correct": baseline_correct, "candidate_correct": candidate_correct,
            "total": total, "baseline_accuracy": baseline_correct / total,
            "candidate_accuracy": candidate_correct / total,
            "acceptance_correct": sum(row["candidate_correct"] for row in acceptance_rows),
            "acceptance_total": len(acceptance_rows), "regressions": regressions,
            "guard_failures": guard_failures, "gates": gates, "passed": all(gates.values())}


def run(candidate):
    candidate = candidate.resolve()
    inputs = [EXAMPLE / "contract.json", EXAMPLE / "baseline.py", EXAMPLE / "corpus.json",
              EXAMPLE / "queries.json", Path(__file__).resolve(), candidate]
    contents = {path: path.read_bytes() for path in inputs}
    contract = json.loads(contents[EXAMPLE / "contract.json"])
    for artifact in contract["frozen_artifacts"]:
        path = ROOT / artifact["path"]
        if path not in contents:
            contents[path] = path.read_bytes()
        if hashlib.sha256(contents[path]).hexdigest() != artifact["sha256"]:
            raise ValueError(f"Frozen artifact changed: {artifact['path']}. Propose a separate contract update.")
    documents = json.loads(contents[EXAMPLE / "corpus.json"])
    queries = json.loads(contents[EXAMPLE / "queries.json"])
    if len({doc["id"] for doc in documents}) != len(documents):
        raise ValueError("Duplicate document IDs.")
    if len({query["id"] for query in queries}) != len(queries):
        raise ValueError("Duplicate query IDs.")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    rankers = {"baseline": load_ranker(EXAMPLE / "baseline.py", contents[EXAMPLE / "baseline.py"]),
               "candidate": load_ranker(candidate, contents[candidate])}
    rows = []
    started = time.perf_counter()
    for query in queries:
        row = {"id": query["id"], "split": query["split"], "expected_top1": query["expected_top1"]}
        for label, rank in rankers.items():
            first = checked_ranking(rank, query["query"], documents)
            row[f"{label}_top1"] = first
            row[f"{label}_correct"] = first == query["expected_top1"]
        rows.append(row)
    summary = judge(rows, contract["thresholds"])
    for path, source in contents.items():
        if path.read_bytes() != source:
            raise ValueError(f"Artifact changed during the run: {path.name}. No result can be accepted.")
    return {"schema_version": 1, "contract_id": contract["id"],
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "evidence_state": "fixture-measured" if summary["passed"] else "fixture-rejected",
            "independent_verification": False,
            "scope": "Deterministic public English lexical fixtures only. No model calls or capability claim.",
            "environment": {"python": platform.python_version(), "platform": platform.platform()},
            "checkout": {"commit": commit.stdout.strip() if commit.returncode == 0 else None,
                         "working_tree_dirty": bool(status.stdout.strip()) if status.returncode == 0 else None},
            "resources": {"model_calls": 0, "training_runs": 0, "paid_compute": False,
                          "candidate_attempts_this_run": 1, "ranker_calls": len(queries) * 4,
                          "ranking_seconds": time.perf_counter() - started,
                          "note": "Wall time is descriptive, not an acceptance metric. Prior attempts must be recorded separately."},
            "artifacts": [{"path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                           "sha256": hashlib.sha256(contents[path]).hexdigest()} for path in inputs],
            "summary": summary, "queries": rows}


def markdown(result):
    summary = result["summary"]
    lines = ["# Retrieval fixture result", "",
             "This is a measured teaching example. It is not an independently verified model result.", "",
             f"Evidence state: `{result['evidence_state']}`", "",
             "| Measure | Baseline | Candidate |", "| --- | --- | --- |",
             f"| Correct first result | {summary['baseline_correct']}/{summary['total']} | {summary['candidate_correct']}/{summary['total']} |",
             f"| Regressions from baseline | — | {len(summary['regressions'])} |", "",
             "| Fixture | Baseline correct | Candidate correct |",
             "| --- | --- | --- |"]
    for row in result["queries"]:
        lines.append(f"| {row['id']} | {'yes' if row['baseline_correct'] else 'no'} | {'yes' if row['candidate_correct'] else 'no'} |")
    lines += ["", "| Contract gate | Pass |", "| --- | --- |"]
    lines += [f"| {name} | {'yes' if passed else 'no'} |" for name, passed in summary["gates"].items()]
    lines += ["", "Both development and acceptance fixtures are public. They are not held-out evidence.",
              "The candidate and fixtures were designed together. This tests the work process, not generalization.",
              "An independent contributor must repeat the run before any replication credit is assigned.",
              "Raw outputs, environment, resource use, and file hashes are in result.json.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=EXAMPLE / "candidate.py",
                        help="Reviewed Python ranker; this executes local code.")
    parser.add_argument("--output", type=Path, default=ROOT / "work/retrieval-demo")
    args = parser.parse_args()
    result = run(args.candidate.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.output / "result.md").write_text(markdown(result))
    summary = result["summary"]
    print(f"Baseline: {summary['baseline_correct']}/{summary['total']}; candidate: "
          f"{summary['candidate_correct']}/{summary['total']}; contract: {'PASS' if summary['passed'] else 'FAIL'}.")
    print(f"Evidence: {result['evidence_state']}. Independent verification: no.")
    print(f"Result files: {args.output}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print(f"Demo failed: {error}", file=sys.stderr)
        sys.exit(1)
