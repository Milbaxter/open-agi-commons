#!/usr/bin/env python3
"""Build public credit from merged PR metadata. Uses only the Python standard library."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO_PATTERN = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
LOGIN_PATTERN = re.compile(r"[A-Za-z0-9-]+\Z")
CATEGORIES = {"verified": "verified", "replication": "replications",
              "negative-result": "negative_results", "documentation": "documentation"}


def active_repositories(registry):
    entries = [registry["overview"], *registry["modules"]]
    repos = []
    for entry in entries:
        if entry["status"] != "active":
            continue
        repo = entry.get("repository")
        if not isinstance(repo, str) or not REPO_PATTERN.fullmatch(repo):
            raise ValueError("Each active entry needs a valid owner/repo name.")
        if repo.casefold() not in {r.casefold() for r in repos}:
            repos.append(repo)
    return repos


def fetch_closed_prs(repository, token, fetch=None):
    """Fetch all closed PR pages. A failure aborts the whole update."""
    if not REPO_PATTERN.fullmatch(repository):
        raise ValueError("Invalid repository name.")
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "open-agi-commons-leaderboard",
               "X-GitHub-Api-Version": "2026-03-10"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    def get_page(url):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            # Do not print headers or response bodies that could contain sensitive data.
            raise RuntimeError(f"GitHub returned HTTP {error.code} for {repository}. "
                               "Check access and rate limits; the prior snapshot is unchanged.") from None

    get_page = fetch or get_page
    page = 1
    while True:
        url = (f"https://api.github.com/repos/{repository}/pulls"
               f"?state=closed&per_page=100&sort=created&direction=asc&page={page}")
        batch = get_page(url)
        if not isinstance(batch, list):
            raise ValueError("GitHub PR response must be a list.")
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def aggregate(repo_prs):
    people = {}
    seen = set()
    for repository, prs in repo_prs:
        for pr in prs:
            if not pr.get("merged_at"):
                continue
            key = (repository.casefold(), pr["number"])
            if key in seen:
                continue
            seen.add(key)
            author = pr.get("user") or {}
            login = author.get("login", "")
            if author.get("type") == "Bot" or login.endswith("[bot]"):
                continue
            if not LOGIN_PATTERN.fullmatch(login):
                continue  # Deleted accounts have no attributable public username.
            person = people.setdefault(login.casefold(), {
                "login": login, "merged_prs": 0,
                **{name: 0 for name in CATEGORIES.values()}, "pull_requests": [],
            })
            person["merged_prs"] += 1
            labels = {label["name"] for label in pr.get("labels", [])}
            for label, field in CATEGORIES.items():
                person[field] += int(label in labels)
            person["pull_requests"].append({
                "repository": repository, "number": pr["number"],
                "url": f"https://github.com/{repository}/pull/{pr['number']}",
                "merged_at": pr["merged_at"], "labels": sorted(labels & CATEGORIES.keys()),
            })
    for person in people.values():
        person["pull_requests"].sort(key=lambda pr: (pr["repository"].casefold(), pr["number"]))
    return sorted(people.values(), key=lambda row: (-row["merged_prs"], row["login"].casefold()))


def render(snapshot):
    lines = ["# Contributor leaderboard", "",
             "People receive credit for useful work accepted through a merged pull request.",
             "Rank uses merged PR count. Equal counts share a rank; names sort alphabetically.", "",
             f"Last complete update: {snapshot['generated_at']}", "",
             "Tracked repos: " + ", ".join(f"`{r}`" for r in snapshot["repositories"]), "",
             "| Rank | Contributor | Merged PRs | Verified | Replications | Negative results | Docs |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    last_count = None
    rank = 0
    for index, person in enumerate(snapshot["contributors"], 1):
        if person["merged_prs"] != last_count:
            rank = index
            last_count = person["merged_prs"]
        login = person["login"]
        lines.append(f"| {rank} | [{login}](https://github.com/{login}) | "
                     f"{person['merged_prs']} | {person['verified']} | {person['replications']} | "
                     f"{person['negative_results']} | {person['documentation']} |")
    if not snapshot["contributors"]:
        lines += ["", "No merged contributions yet. The first accepted PR will start the board."]
    lines += ["", "Categories can overlap. Maintainers set the labels after evidence review.",
              "Bots, deleted accounts, and closed PRs that were not merged are excluded.",
              "Credit goes to the PR author. Coauthor and reviewer credit is a future task.",
              "PR count is a contribution count, not a measure of research value.", "",
              "See [credit rules and update steps](docs/operations.md) and "
              "[the complete source records](data/leaderboard.json).", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=ROOT / "registry.json")
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    repos = active_repositories(registry)
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    # Fetch every repo before writing either output. Do not publish a partial score.
    contributors = aggregate([(repo, list(fetch_closed_prs(repo, token))) for repo in repos])
    snapshot = {"schema_version": 1,
                "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "repositories": repos, "contributors": contributors}
    markdown = render(snapshot)
    payload = json.dumps(snapshot, indent=2) + "\n"
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/leaderboard.json").write_text(payload, encoding="utf-8")
    (ROOT / "LEADERBOARD.md").write_text(markdown, encoding="utf-8")
    print(f"Updated leaderboard: {len(contributors)} people across {len(repos)} repos.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        print(f"Leaderboard update failed: {error}", file=sys.stderr)
        sys.exit(1)
