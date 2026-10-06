#!/usr/bin/env python3
"""Select bounded work from reviewed local task files; never run an agent or claim a task."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

from task_contracts import load_tasks, PROFILE_ORDER, WORK_TYPES

ROOT = Path(__file__).resolve().parents[1]


def issue_is_available(task):
    match = re.fullmatch(r"https://github.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/issues/([0-9]+)", task.get("issue_url") or "")
    if not match:
        return False, "no published task issue"
    owner, repo, number = match.groups()
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "open-agi-commons-picker",
               "X-GitHub-Api-Version": "2026-03-10"}
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urlopen(Request(f"https://api.github.com/repos/{owner}/{repo}/issues/{number}", headers=headers), timeout=20) as response:
            issue = json.load(response)
    except (URLError, OSError):
        return False, "live issue check failed; availability is unknown"
    labels = {label["name"] for label in issue.get("labels", [])}
    available = issue.get("state") == "open" and "ready" in labels \
        and not labels & {"claimed", "blocked", "needs-verification"} and not issue.get("assignees")
    return available, "issue is closed, assigned, or not ready" if not available else "live issue is ready"


def select_tasks(tasks, profile, minutes, ram_gb, offline, work_type=None, module=None,
                 completed=(), allow_paid=False, live_check=None):
    done = set(completed) | {task["id"] for task in tasks if task["status"] == "done"}
    eligible, excluded = [], []
    for task in tasks:
        reasons = []
        routing, budget = task["routing"], task["budget"]
        if task["status"] != "ready":
            reasons.append("task is not ready")
        if task["id"] in done:
            reasons.append("task is already complete")
        if PROFILE_ORDER[routing["profile"]] > PROFILE_ORDER[profile]:
            reasons.append("requires a GPU profile")
        if routing["min_ram_gb"] > ram_gb:
            reasons.append("requires more RAM")
        if budget["minutes"] > minutes:
            reasons.append("exceeds the time budget")
        if offline and routing["network"]:
            reasons.append("needs network access")
        if budget["paid_compute"] and not allow_paid:
            reasons.append("needs explicit paid-compute permission")
        if work_type and work_type != routing["work_type"]:
            reasons.append("different work type")
        if module and module != task["module"]:
            reasons.append("different stack part")
        missing = set(task["dependencies"]) - done
        if missing:
            reasons.append("unfinished dependencies: " + ", ".join(sorted(missing)))
        if live_check and not reasons:
            available, reason = live_check(task)
            if not available:
                reasons.append(reason)
        if reasons:
            excluded.append({"id": task["id"], "reasons": reasons})
        else:
            eligible.append(task)
    eligible.sort(key=lambda task: (task["priority"], task["budget"]["minutes"], task["id"]))
    return eligible, excluded


def positive_integer(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("Use a positive integer.")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_ORDER, default="cpu")
    parser.add_argument("--minutes", type=positive_integer, default=30)
    parser.add_argument("--ram-gb", type=positive_integer, default=8)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--work-type", choices=sorted(WORK_TYPES))
    parser.add_argument("--module")
    parser.add_argument("--completed", action="append", default=[], help="Task ID already accepted; can repeat.")
    parser.add_argument("--allow-paid", action="store_true", help="Selection only; does not start or authorize a paid job.")
    parser.add_argument("--live", action="store_true", help="Read GitHub issue labels and assignees before recommending.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.live and args.offline:
        parser.error("--live needs network access; do not combine it with --offline.")
    tasks = load_tasks(ROOT / "tasks")
    if not set(args.completed) <= {task["id"] for task in tasks}:
        parser.error("--completed contains an unknown task ID.")
    eligible, excluded = select_tasks(tasks, args.profile, args.minutes, args.ram_gb,
                                     args.offline, args.work_type, args.module, args.completed,
                                     args.allow_paid, issue_is_available if args.live else None)
    selected = eligible[0] if eligible else None
    snapshot = {"selected": selected, "eligible_ids": [task["id"] for task in eligible], "excluded": excluded,
                "availability": "live snapshot; claim still needs confirmation" if args.live else "local files only; live claims not checked",
                "selection_rule": "Ready tasks that fit declared resources and dependencies; lowest priority number, then budget, then ID.",
                "task_sha256": hashlib.sha256((ROOT / "tasks" / (selected["id"] + ".json")).read_bytes()).hexdigest() if selected else None}
    if args.json:
        print(json.dumps(snapshot, indent=2))
    else:
        print(f"Availability: {snapshot['availability']}.")
        if selected:
            print(f"Selected: {selected['id']} — {selected['title']}")
            print(f"Why: ready; {selected['budget']['minutes']} minutes; {selected['routing']['profile']}; dependencies satisfied.")
            print(f"Contract: tasks/{selected['id']}.json")
            print(f"Task SHA-256: {snapshot['task_sha256']}")
            print("Next: read the task and AGENTS.md; follow the claim process; work in a new branch.")
        else:
            print("No ready task fits. Increase a budget only if you choose, or ask for a smaller task.")
        for task in excluded:
            print(f"Excluded {task['id']}: {'; '.join(task['reasons'])}.")
    return 0 if selected else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as error:
        print(f"Task selection failed: {error}", file=sys.stderr)
        sys.exit(1)
