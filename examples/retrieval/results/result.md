# Retrieval fixture result

This is a measured teaching example. It is not an independently verified model result.

Evidence state: `fixture-measured`

| Measure | Baseline | Candidate |
| --- | --- | --- |
| Correct first result | 5/12 | 12/12 |
| Regressions from baseline | — | 0 |

| Fixture | Baseline correct | Candidate correct |
| --- | --- | --- |
| whole-word-plan | no | yes |
| whole-word-cache | no | yes |
| coverage-memory | no | yes |
| coverage-sources | no | yes |
| coverage-tool | no | yes |
| plain-quantization | yes | yes |
| plain-retrieval | yes | yes |
| coverage-retention | no | yes |
| no-overlap | yes | yes |
| empty-query | yes | yes |
| case-punctuation | no | yes |
| query-punctuation | yes | yes |

| Contract gate | Pass |
| --- | --- |
| overall_accuracy | yes |
| minimum_gain | yes |
| acceptance_accuracy | yes |
| no_regressions | yes |
| empty_and_no_overlap | yes |

Both development and acceptance fixtures are public. They are not held-out evidence.
The candidate and fixtures were designed together. This tests the work process, not generalization.
An independent contributor must repeat the run before any replication credit is assigned.
Raw outputs, environment, resource use, and file hashes are in result.json.
