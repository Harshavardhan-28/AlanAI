# Scoring config schema

`scoring.v<N>.yaml` is validated at load time by `apps/worker/scoring` against this contract.

| Field | Type | Meaning |
|---|---|---|
| `version` | string | Config version, stored on every `Score` row. Bump on any change. |
| `categories.<key>.weight` | float | Multiplier applied to finding points in the category. |
| `categories.<key>.cap` | int | Max points a category can contribute. |
| `severity_points` | map | Base points per severity before confidence/weight. |
| `min_confidence` | float 0-1 | Findings below this contribute 0 points (hard fails unaffected). |
| `verdicts.<TIER>.max` | int | Upper risk_score bound for the tier (ordered). |
| `hard_fails[].id` | string | Rule id; a finding with `hard_fail_rule=<id>` forces `DANGEROUS`. |
| `community.quarantine_threshold` | float | Reputation-weighted report sum that triggers fast-path quarantine. |
| `community.window_hours` | int | Recency window for counted reports. |
| `community.severities_counted` | list | Which report severities count toward the threshold. |
| `judge.enabled` | bool | Whether the LLM judge/aggregator runs. |
| `judge.max_category_adjustment` | int | Max points the judge may add/remove per category. |

Finding points: `severity_points[severity] * confidence * category.weight`, floored at 0,
summed per category and capped at `category.cap`. `risk_score = min(100, round(Σ categories))`.
Verdict is the first tier whose `max` >= risk_score (order: VERIFIED_SAFE → HIGH_RISK), unless
any hard fail fired → `DANGEROUS`. `PENDING` is used only before the first completed audit.
