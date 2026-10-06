.PHONY: check leaderboard demo demo-reject pick

check:
	python3 scripts/check_repo.py
	python3 -m unittest discover -s tests -v

leaderboard:
	python3 scripts/update_leaderboard.py

pick:
	python3 scripts/pick_task.py --profile cpu --minutes 30 --offline --work-type replication

demo:
	python3 scripts/run_retrieval_demo.py

demo-reject:
	@python3 scripts/run_retrieval_demo.py --candidate examples/retrieval/baseline.py --output work/retrieval-rejected; result=$$?; if [ $$result -ne 1 ]; then echo 'Expected a contract rejection with exit 1.'; exit 1; fi
	@python3 -c 'import json; r=json.load(open("work/retrieval-rejected/result.json")); assert r["evidence_state"] == "fixture-rejected" and not r["summary"]["passed"]; print("Unchanged baseline correctly rejected.")'
