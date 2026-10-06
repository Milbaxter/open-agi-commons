.PHONY: check leaderboard

check:
	python3 scripts/check_repo.py
	python3 -m unittest discover -s tests -v

leaderboard:
	python3 scripts/update_leaderboard.py
