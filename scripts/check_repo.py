#!/usr/bin/env python3
"""Check registry, task contracts, generated credit, and local Markdown links."""

import json
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote

from update_leaderboard import active_repositories, render
from task_contracts import load_tasks, require

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    registry = json.loads((root / "registry.json").read_text())
    assert registry["schema_version"] == 1, "Unsupported registry schema"
    repos = active_repositories(registry)
    ids = {entry["id"] for entry in registry["modules"]}
    assert len(ids) == len(registry["modules"]), "Duplicate module IDs"
    assert registry["overview"]["status"] == "active", "Overview must be active"
    for entry in registry["modules"]:
        assert entry["status"] in {"planned", "active", "paused"}, "Unknown module status"
        assert set(entry["dependencies"]) <= ids - {entry["id"]}, "Invalid module dependencies"
        assert all(entry.get(key) for key in ("title", "scope", "verification", "maintainer_role")), "Incomplete module"
        if entry["status"] == "planned":
            assert entry["repository"] is None and entry["tested_commit"] is None, "Planned module has a false pin"
        if entry["tested_commit"] is not None:
            assert entry["repository"], "Tested commit needs a repository"
            assert re.fullmatch(r"[0-9a-f]{40}", entry["tested_commit"]), "Use a full commit SHA"

    tasks = load_tasks(root / "tasks")
    task_ids = {task["id"] for task in tasks}
    for task in tasks:
        assert task["module"] in ids | {"overview"}, "Unknown task module"
        if task.get("verification"):
            spec = task["verification"]
            require((root / spec["contract"]).is_file(), f"{task['id']}: missing contract")
            for artifact in spec["baseline_artifacts"]:
                path = root / artifact["path"]
                require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"],
                        f"{task['id']}: baseline artifact changed: {artifact['path']}")

    contract = json.loads((root / "examples/retrieval/contract.json").read_text())
    for artifact in contract["frozen_artifacts"]:
        path = root / artifact["path"]
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"],
                f"Demo contract artifact changed: {artifact['path']}")

    snapshot = json.loads((root / "data/leaderboard.json").read_text())
    assert snapshot["schema_version"] == 1, "Unsupported leaderboard schema"
    assert snapshot["repositories"] == repos, "Leaderboard scope does not match registry; refresh it"
    assert (root / "LEADERBOARD.md").read_text() == render(snapshot), "Leaderboard differs from source data"

    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            assert (path.parent / target).exists(), f"Broken local link in {path.name}: {target}"
    print(f"Repo checks passed: {len(ids)} modules, {len(task_ids)} tasks, and local links.")


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, KeyError, ValueError, OSError) as error:
        print(f"Repo check failed: {error}", file=sys.stderr)
        sys.exit(1)
