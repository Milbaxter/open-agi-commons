#!/usr/bin/env python3
"""Check registry, task contracts, generated credit, and local Markdown links."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

from update_leaderboard import active_repositories, render

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

    task_ids = set()
    for path in sorted((root / "tasks").glob("*.json")):
        task = json.loads(path.read_text())
        assert task["id"] == path.stem and task["id"] not in task_ids, "Invalid task ID"
        task_ids.add(task["id"])
        assert task["module"] in ids | {"overview"}, "Unknown task module"
        assert task["status"] in {"draft", "ready", "done"}, "Invalid task readiness"
        for key in ("title", "question", "baseline", "scope", "resources", "acceptance", "checks", "evidence", "stop_conditions", "deliverable"):
            assert task.get(key), f"{path.name}: missing {key}"
        assert isinstance(task["budget"]["minutes"], int) and task["budget"]["minutes"] > 0, "Invalid time budget"
        assert isinstance(task["budget"]["paid_compute"], bool), "Paid compute must be explicit"

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
