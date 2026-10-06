# Operate the overview

## What runs now

`make check` validates the registry, task fields, generated leaderboard, and local links.
Unit tests check merged-only credit, bot exclusion, pagination, categories,
multiple repos, tied ranks, and preservation of prior data after an API failure.
They also test resource routing, dependencies, claims, malformed tasks,
fixture acceptance and rejection, ranker determinism, and source identity.
GitHub Actions runs these checks on pushes and pull requests.

`make pick` runs the local task picker. `make demo` runs the public retrieval fixture.
`make demo-reject` confirms that the unchanged baseline fails the improvement rule.
See [work routing](work-routing.md) and the [example](../examples/retrieval/README.md).
These commands do not start a model or agent.

The leaderboard job runs daily at 03:23 UTC and can be started manually.
It also runs when its script, workflow, or the registry changes on main.
It reads all closed PR pages for active repos, selects merged PRs, and writes a snapshot.
It commits only LEADERBOARD.md and data/leaderboard.json.
GitHub can delay scheduled runs. The board shows its last complete update time.

The update job runs trusted main-branch code. It does not run code from submitted PRs.
The PR check job uses read-only repository permission and does not keep checkout credentials.
The leaderboard job needs contents write permission to commit its generated files.
If branch rules later block that commit, change this job to submit a snapshot PR.

## Repo registry

registry.json has one active overview entry and 17 component entries.
Each component records scope, verification, status, repository, tested commit,
dependencies, and its maintainer role.
The `current_focus` list names the ten downstream workstreams.
Their `guide` paths point to the detailed work and evidence plans.

- `planned`: no repo or tested commit yet.
- `active`: a real repo is accepting work and is included in the leaderboard.
- `paused`: work is on hold; it is excluded from the current leaderboard scope.

Use `owner/repo` for repository names and a full 40-character commit for tested versions.
An active repo can have an empty tested commit until integration is checked.
The registry is an inventory. This version does not fetch components or run integration tests.
Dependencies are empty until actual interfaces establish them.

To activate a component, create its repo, verify its setup, update the registry,
and refresh the leaderboard before submitting the change.
Use public repos for this first version. The overview token can read their public PR metadata.
Private repos would need separate access and a reviewed change to this process.

## Tasks and maintainer state

tasks/*.json contains versioned task contracts.
Each contract gives a question, baseline, scope, resources, budget, acceptance,
checks, evidence, stop conditions, deliverable, and issue URL.
Routing fields add priority, task dependencies, machine profile, network need,
minimum RAM, work type, and public artifact access.
Runnable tasks can link a verification contract and baseline artifact hashes.
The picker filters these declared fields. It does not inspect the machine automatically.
Use templates/task.json for new work. A maintainer checks readiness before publication.
Planning tasks use document inputs and manual acceptance criteria.
Experiment tasks must also have working baseline and verification commands.

Issue labels track live state: `proposal`, `ready`, `claimed`, `needs-verification`,
and `blocked`. Close the issue when its work is accepted.
An assignee and a maintainer-confirmed UTC expiry record an active claim.
This version has a read-only local picker. It has no task reservation service or agent runner.
The component maintainer brief is in roles/component-maintainer.md.

## Leaderboard rules

Count one merged PR for its GitHub author in each active registered repo.
Combine counts across repos. Exclude bots and accounts with no usable public username.
Equal totals share a rank. Sort tied names alphabetically.
PR authors receive the count; coauthors and reviewers can be credited in the PR text.
Dedicated credit for those roles is a future improvement.

Show reviewed categories separately: `verified`, `replication`, `negative-result`,
and `documentation`. Categories can overlap. A label is a maintainer record;
the evidence must remain linked in the PR. It is not an automatic scientific check.

Use merged count as a simple first measure. Do not treat it as proof of research value.
Do not split one change for points. Useful tests and honest negative results deserve review.
The raw JSON links each counted PR so people can inspect and correct the score.

The first commit is a direct repo setup. It is not a PR and gives no leaderboard points.
The first accepted contributor PR starts the board.

Use a verified label only when a separate contributor's run and verdict are linked.
The fixture runner always records `independent_verification: false`.
A green fixture or CI check must not automatically add the label.

## Manual refresh

From the repo root:

```sh
make leaderboard
make check
```

Public access works without a token, subject to GitHub rate limits.
For a larger registry, set GH_TOKEN or GITHUB_TOKEN through your normal local credential method.
Do not commit a token. The Actions job uses its built-in token.
If any repo fetch fails, the script exits before writing either output.
The last complete snapshot remains available. Check the workflow logs and access.

## Sources

These official docs informed the small set of tool integrations. Checked 6 October 2026.

- [OpenAI: project instructions in AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- [Claude Code: project memory and shared instruction imports](https://code.claude.com/docs/en/memory).
- [GitHub: pull-request API and pagination](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests).
- [GitHub: workflow token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).

Provider plans and usage rules can change. Contributors use supported tools under their own accounts.
This repo makes no promise about a plan's remaining capacity or a provider's reset times.
