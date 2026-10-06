import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_leaderboard as board


def pr(number, login="alice", merged=True, labels=(), kind="User"):
    return {"number": number, "user": {"login": login, "type": kind},
            "merged_at": "2026-10-06T12:00:00Z" if merged else None,
            "labels": [{"name": label} for label in labels]}


class LeaderboardTests(unittest.TestCase):
    def test_only_merged_humans_receive_credit(self):
        rows = board.aggregate([("owner/repo", [pr(1), pr(2, merged=False),
            pr(3, "robot[bot]", kind="Bot"), pr(4, "", kind="User")])])
        self.assertEqual([(r["login"], r["merged_prs"]) for r in rows], [("alice", 1)])

    def test_categories_deduplication_and_multiple_repos(self):
        rows = board.aggregate([
            ("owner/one", [pr(1, labels=("verified", "replication", "documentation")), pr(1)]),
            ("owner/two", [pr(1, "Alice", labels=("negative-result",)), pr(2, "bob")])])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["merged_prs"], 2)
        self.assertEqual([rows[0][k] for k in board.CATEGORIES.values()], [1, 1, 1, 1])
        self.assertEqual(len(rows[0]["pull_requests"]), 2)

    def test_pagination_goes_past_the_first_hundred(self):
        calls = []
        def fetch(url):
            calls.append(url)
            return [pr(i) for i in range(100)] if len(calls) == 1 else [pr(100)]
        results = list(board.fetch_closed_prs("owner/repo", None, fetch))
        self.assertEqual(len(results), 101)
        self.assertIn("page=2", calls[1])

    def test_planned_and_paused_repos_are_not_fetched(self):
        registry = {"overview": {"status": "active", "repository": "owner/main"},
                    "modules": [{"status": "planned", "repository": None},
                                {"status": "paused", "repository": "owner/paused"},
                                {"status": "active", "repository": "owner/part"},
                                {"status": "active", "repository": "OWNER/main"}]}
        self.assertEqual(board.active_repositories(registry), ["owner/main", "owner/part"])

    def test_ties_share_rank_and_empty_board_has_no_fake_scores(self):
        snapshot = {"generated_at": "2026-10-06T00:00:00Z", "repositories": ["owner/repo"],
                    "contributors": board.aggregate([("owner/repo", [pr(1, "bob"), pr(2, "alice")])])}
        rendered = board.render(snapshot)
        self.assertIn("| 1 | [alice]", rendered)
        self.assertIn("| 1 | [bob]", rendered)
        snapshot["contributors"] = []
        self.assertIn("No merged contributions yet", board.render(snapshot))
        self.assertNotIn("[alice]", board.render(snapshot))

    def test_api_failure_preserves_both_prior_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "data/leaderboard.json").write_text("previous data")
            (root / "LEADERBOARD.md").write_text("previous board")
            (root / "registry.json").write_text(json.dumps({
                "overview": {"status": "active", "repository": "owner/one"},
                "modules": [{"status": "active", "repository": "owner/two"}]}))
            with patch.object(board, "ROOT", root), patch.object(sys, "argv", ["update"]), \
                 patch.object(board, "fetch_closed_prs", side_effect=[[pr(1)], RuntimeError("rate limit")]):
                with self.assertRaises(RuntimeError):
                    board.main()
            self.assertEqual((root / "data/leaderboard.json").read_text(), "previous data")
            self.assertEqual((root / "LEADERBOARD.md").read_text(), "previous board")


if __name__ == "__main__":
    unittest.main()
