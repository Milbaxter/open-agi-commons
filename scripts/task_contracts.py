"""Shared validation for small local work packets. Does not execute task commands."""

import json
from pathlib import Path
import re

PROFILE_ORDER = {"cpu": 0, "gpu": 1}
WORK_TYPES = {"research", "replication", "engineering"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_task(task, filename=None):
    name = task.get("id", "unknown")
    require(isinstance(name, str) and bool(re.fullmatch(r"[a-z0-9-]+", name)), "Invalid task ID")
    if filename:
        require(name == filename, f"Task ID differs from file: {filename}")
    require(task.get("status") in {"draft", "ready", "done"}, f"{name}: invalid status")
    require(isinstance(task.get("module"), str) and bool(re.fullmatch(r"[a-z0-9-]+", task["module"])),
            f"{name}: invalid module ID")
    for key in ("title", "question", "baseline", "scope", "resources", "acceptance", "checks", "evidence", "stop_conditions", "deliverable"):
        require(bool(task.get(key)), f"{name}: missing {key}")
    for key in ("title", "question", "baseline", "resources", "deliverable"):
        require(isinstance(task[key], str) and bool(task[key].strip()), f"{name}: {key} must be text")
    require(task.get("issue_url") is None or isinstance(task["issue_url"], str), f"{name}: invalid issue URL")
    for key in ("scope", "acceptance", "checks", "evidence", "stop_conditions"):
        require(isinstance(task[key], list) and all(isinstance(item, str) and item.strip() for item in task[key]),
                f"{name}: {key} must contain nonempty strings")
    budget = task["budget"]
    require(type(budget["minutes"]) is int and budget["minutes"] > 0, f"{name}: invalid time budget")
    require(type(budget["paid_compute"]) is bool, f"{name}: paid compute must be explicit")
    require(type(task.get("priority")) is int and task["priority"] >= 0, f"{name}: invalid priority")
    require(isinstance(task.get("dependencies"), list), f"{name}: missing dependencies")
    require(all(isinstance(item, str) for item in task["dependencies"]), f"{name}: dependencies must be task IDs")
    routing = task["routing"]
    require(routing["profile"] in PROFILE_ORDER, f"{name}: invalid machine profile")
    require(type(routing["network"]) is bool, f"{name}: network need must be explicit")
    require(type(routing["min_ram_gb"]) is int and routing["min_ram_gb"] > 0, f"{name}: invalid RAM need")
    require(routing["work_type"] in WORK_TYPES, f"{name}: invalid work type")
    require(routing["artifact_access"] == "public", f"{name}: this picker supports public artifacts only")
    if task.get("verification"):
        spec = task["verification"]
        require(spec["expected_state"] == "fixture-measured", f"{name}: unsupported evidence state")
        require(spec["independent_required"] is True, f"{name}: independent review is required")
        require(bool(spec["contract"] and spec["command"] and spec["baseline_artifacts"]), f"{name}: incomplete verification")
        for artifact in spec["baseline_artifacts"]:
            require(bool(artifact["path"]) and bool(re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"])),
                    f"{name}: invalid artifact hash")


def load_tasks(directory):
    tasks = []
    for path in sorted(Path(directory).glob("*.json")):
        task = json.loads(path.read_text())
        require(isinstance(task, dict), f"{path.name}: expected a task object")
        validate_task(task, path.stem)
        tasks.append(task)
    ids = set()
    for task in tasks:
        require(task["id"] not in ids, "Duplicate task IDs")
        ids.add(task["id"])
    lookup = {task["id"]: task for task in tasks}
    for task in tasks:
        dependencies = task["dependencies"]
        require(set(dependencies) <= ids - {task["id"]}, f"{task['id']}: unknown or self dependency")
        require(len(dependencies) == len(set(dependencies)), f"{task['id']}: duplicate dependencies")
    visiting, visited = set(), set()

    def visit(name):
        require(name not in visiting, f"Task dependency cycle at {name}")
        if name in visited:
            return
        visiting.add(name)
        for dependency in lookup[name]["dependencies"]:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in lookup:
        visit(name)
    return tasks
