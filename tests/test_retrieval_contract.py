from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import py_compile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_retrieval_demo as demo


class RetrievalContractTests(unittest.TestCase):
    def test_candidate_meets_contract_and_unchanged_baseline_fails(self):
        improved = demo.run(demo.EXAMPLE / "candidate.py")
        unchanged = demo.run(demo.EXAMPLE / "baseline.py")
        self.assertTrue(improved["summary"]["passed"])
        self.assertEqual(improved["summary"]["candidate_correct"], 12)
        self.assertFalse(improved["independent_verification"])
        self.assertEqual(improved["resources"]["model_calls"], 0)
        self.assertFalse(unchanged["summary"]["passed"])
        self.assertEqual(unchanged["evidence_state"], "fixture-rejected")

    def test_frozen_baseline_or_grader_tampering_aborts(self):
        altered = json.loads((demo.EXAMPLE/"contract.json").read_text())
        altered["frozen_artifacts"][0]["sha256"] = "0"*64
        original = Path.read_bytes
        def read(path):
            if path == demo.EXAMPLE/"contract.json":
                return json.dumps(altered).encode()
            return original(path)
        with patch.object(Path, "read_bytes", read):
            with self.assertRaisesRegex(ValueError, "Frozen artifact changed"):
                demo.run(demo.EXAMPLE / "candidate.py")

    def test_unknown_duplicate_and_invalid_ranking_ids_are_rejected(self):
        docs = [{"id":"one", "text":"one"}]
        for output in (["invented"], ["one","one"], "one", [None]):
            with self.assertRaises(ValueError):
                demo.checked_ranking(lambda q, d: output, "one", docs)

    def test_mutating_ranker_cannot_change_the_shared_corpus(self):
        docs = [{"id":"one", "text":"one"}]
        before = deepcopy(docs)
        def mutate(query, documents):
            documents[0]["text"] = "changed"
            return ["one"]
        self.assertEqual(demo.checked_ranking(mutate, "one", docs), "one")
        self.assertEqual(docs, before)

    def test_nondeterministic_ranker_is_rejected(self):
        answers = iter([["one"], []])
        with self.assertRaisesRegex(ValueError, "changed its output"):
            demo.checked_ranking(lambda q, d: next(answers), "one", [{"id":"one","text":"one"}])

    def test_reused_mutable_output_cannot_hide_a_changed_ranking(self):
        shared = []
        calls = 0
        def alias(query, documents):
            nonlocal calls
            calls += 1
            shared[:] = ["one"] if calls == 1 else ["two"]
            return shared
        docs = [{"id":"one","text":"one"}, {"id":"two","text":"two"}]
        with self.assertRaisesRegex(ValueError, "changed its output"):
            demo.checked_ranking(alias, "one", docs)

    def test_second_ranking_is_validated_independently(self):
        answers = iter([["one"], ["invented"]])
        with self.assertRaisesRegex(ValueError, "unknown"):
            demo.checked_ranking(lambda q, d: next(answers), "one", [{"id":"one","text":"one"}])

    def test_recorded_source_wins_over_stale_timestamp_valid_bytecode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"cached.py"
            path.write_text("def rank(query, docs): return ['one']\n")
            os.utime(path, (1000000000,1000000000))
            py_compile.compile(str(path), doraise=True)
            path.write_text("def rank(query, docs): return ['two']\n")
            os.utime(path, (1000000000,1000000000))
            self.assertEqual(demo.load_ranker(path)("", []), ["two"])

    def test_candidate_rewriting_itself_cannot_pass_with_wrong_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"self_changing.py"
            path.write_text((demo.EXAMPLE/"candidate.py").read_text() + '\n'
                            + "from pathlib import Path\n"
                            + "Path(__file__).write_text(\"def rank(query, docs): return []\\n\")\n")
            with self.assertRaisesRegex(ValueError, "Artifact changed during the run"):
                demo.run(path)

    def test_empty_eval_regression_and_abstention_failure_cannot_pass(self):
        thresholds = json.loads((demo.EXAMPLE/"contract.json").read_text())["thresholds"]
        with self.assertRaises(ValueError): demo.judge([], thresholds)
        rows = [{"id":"no-overlap", "split":"acceptance", "expected_top1":None,
                 "baseline_top1":None,"candidate_top1":"one",
                 "baseline_correct":True,"candidate_correct":False}]
        verdict = demo.judge(rows, thresholds)
        self.assertFalse(verdict["passed"])
        self.assertEqual(verdict["regressions"], ["no-overlap"])
        self.assertEqual(verdict["guard_failures"], ["no-overlap"])


if __name__ == "__main__":
    unittest.main()
