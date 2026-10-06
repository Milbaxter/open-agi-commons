from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from pick_task import select_tasks, issue_is_available
from task_contracts import load_tasks, validate_task

ROOT = Path(__file__).resolve().parents[1]


def task(name="one", priority=10, **changes):
    packet = json.loads((ROOT / "tasks/004-replicate-retrieval-example.json").read_text())
    packet.update(id=name, priority=priority, **changes)
    return packet


def choose(tasks, **options):
    settings = dict(profile="cpu", minutes=30, ram_gb=8, offline=True)
    settings.update(options)
    return select_tasks(tasks, **settings)


class TaskPickerTests(unittest.TestCase):
    def test_filters_machine_time_network_paid_and_readiness(self):
        specs = [task("good"), task("draft", status="draft"), task("gpu"),
                 task("long", budget={"minutes":31, "paid_compute":False}),
                 task("network"), task("paid", budget={"minutes":5, "paid_compute":True}), task("ram")]
        specs[2]["routing"]["profile"] = "gpu"
        specs[4]["routing"]["network"] = True
        specs[6]["routing"]["min_ram_gb"] = 32
        eligible, excluded = choose(specs)
        self.assertEqual([packet["id"] for packet in eligible], ["good"])
        self.assertEqual(len(excluded), 6)

    def test_orders_fit_tasks_by_priority_budget_and_id(self):
        specs = [task("b", priority=10), task("a", priority=10), task("c", priority=2)]
        eligible, _ = choose(specs)
        self.assertEqual([packet["id"] for packet in eligible], ["c", "a", "b"])

    def test_dependency_done_states_and_completed_task_are_respected(self):
        specs = [task("one"), task("two", dependencies=["one"])]
        eligible, _ = choose(specs)
        self.assertEqual([packet["id"] for packet in eligible], ["one"])
        eligible, _ = choose(specs, completed=["one"])
        self.assertEqual([packet["id"] for packet in eligible], ["two"])
        specs[0]["status"] = "done"
        eligible, _ = choose(specs)
        self.assertEqual([packet["id"] for packet in eligible], ["two"])

    def test_live_availability_failure_excludes_even_a_ready_local_task(self):
        eligible, excluded = choose([task()], offline=False,
                                    live_check=lambda packet: (False, "live issue check failed"))
        self.assertFalse(eligible)
        self.assertIn("live issue check failed", excluded[0]["reasons"])

    def test_actual_issue_flags_require_open_ready_unassigned(self):
        class Response:
            def __init__(self, payload): self.payload = payload
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return json.dumps(self.payload).encode()
        packet = task(issue_url="https://github.com/owner/repo/issues/1")
        payload = {"state":"open", "labels":[{"name":"ready"}], "assignees":[]}
        with patch("pick_task.urlopen", return_value=Response(payload)):
            self.assertTrue(issue_is_available(packet)[0])
        for change in ({"state":"closed"}, {"assignees":[{"login":"worker"}]},
                       {"labels":[{"name":"ready"},{"name":"claimed"}]}, {"labels":[]}):
            updated = {**payload, **change}
            with patch("pick_task.urlopen", return_value=Response(updated)):
                self.assertFalse(issue_is_available(packet)[0])

    def test_bad_budgets_and_missing_scope_are_rejected(self):
        packet = task()
        for bad_budget in (0, -1, True, "30"):
            packet["budget"]["minutes"] = bad_budget
            with self.assertRaises(ValueError): validate_task(packet)
        packet = task(scope=[])
        with self.assertRaises(ValueError): validate_task(packet)
        for key, value in (("title",123), ("module",None), ("baseline",["untyped"]), ("issue_url",4)):
            packet = task()
            packet[key] = value
            with self.assertRaises(ValueError): validate_task(packet)

    def test_dependency_cycle_unknown_dependency_and_filename_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"one.json").write_text(json.dumps(task("one", dependencies=["two"])))
            (root/"two.json").write_text(json.dumps(task("two", dependencies=["one"])))
            with self.assertRaisesRegex(ValueError, "cycle"): load_tasks(root)
            (root/"two.json").write_text(json.dumps(task("two", dependencies=["missing"])))
            with self.assertRaisesRegex(ValueError, "unknown"): load_tasks(root)
            (root/"two.json").write_text(json.dumps(task("different")))
            with self.assertRaisesRegex(ValueError, "differs"): load_tasks(root)


if __name__ == "__main__":
    unittest.main()
