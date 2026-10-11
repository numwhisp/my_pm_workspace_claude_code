# Experiment Design — Weekly Summary Full Test

**Date:** 2026-07-16
**Purpose:** Pressure-test the week-5 pilot before Marcus commits to full rollout, and design a properly powered follow-up test.
**Source:** Same dataset as [metric-findings.md](metric-findings.md) and [metric-diagnosis.md](metric-diagnosis.md).

## 1. Statistical Significance of the Pilot

**Concept:** Statistical significance tells you whether a result is large enough, given your sample size, to be unlikely to have occurred by chance — the difference between "a nice-looking number" and "real evidence."

**Result:** Treatment 18/50 (36%) vs. control 11/50 (22%).

| Metric | Value |
|---|---|
| Difference | +14 points |
| z-score | 1.54 |
| p-value (two-tailed) | ≈0.124 |
| 95% CI on the difference | −3.6 to +31.6 points |

**Not statistically significant at 95% confidence** (requires p < 0.05; actual p ≈ 0.124).

**Plain-English meaning:** The confidence interval spans from a small loss to a large win — the pilot cannot yet distinguish "this feature drives a real 14-point lift" from "this cohort got lucky and the true effect is near zero." n=50/arm is too small to trust as a rollout basis on its own.

## 2. Minimum Detectable Effect (MDE)

**Concept:** MDE is the smallest effect size worth caring about, fixed *before* the test runs — set afterward, it becomes a way to rationalize a result you already like rather than an honest design parameter.

**Set for this test:** 5 percentage points — a deliberately lower bar than the pilot's 14-point signal, so a real but more modest win isn't missed.

## 3. Required Sample Size

**Concept:** Statistical power is the probability the test detects a real effect of the MDE size, if one exists. Too little power risks a **false negative** — discarding a feature that actually works because the test was too small to see it.

**Inputs:** baseline 22%, MDE +5pts (→ 27% treatment), 95% confidence, 80% power.

**Result: ≈1,160 users per variant (≈2,320 total)** — roughly 23x the pilot's size, which is exactly why the pilot alone couldn't reach significance.

## 4. Test Duration

**Unresolved design question, flagged rather than assumed:** does the full test stay scoped to new signups only (matching the pilot's cohort design), or expand to the broader active-user base (85,000 WAU)? The answer changes the duration by more than 20 weeks.

| Scope | Weekly enrollment capacity | Time to reach 1,160/arm | + 30-day observation lag | Total | Fits in 8 weeks? |
|---|---|---|---|---|---|
| New signups only (pilot design) | ~50/arm (100/week total, per pilot cohort size) | ~23 weeks | +4.3 weeks | **~27 weeks** | **No — overshoots by 3x+** |
| Broader WAU pool (85,000/week) | ~42,500/arm | <1 week | +4.3 weeks | **~5 weeks** | **Yes, comfortably** |

**This must be decided explicitly before scheduling the test** — it is a scoping decision (what population and what outcome we're actually measuring), not a statistics detail.

## 5. Decision

**Recommendation: wait for a properly powered test. Do not recommend scaling on the pilot alone.**

The pilot's result is not statistically distinguishable from zero effect (p≈0.124, CI crosses zero) — recommending full rollout on it risks committing a quarter's roadmap to a signal that could plausibly be noise.

- **Risk of waiting for the full test:** continued retention leakage for the ~5–8 week test window on a feature we're fairly confident helps but haven't yet proven.
- **Risk of scaling now instead:** committing engineering, design, and organizational credibility to an effect with a real chance of being noise — costing more trust later than the delay costs now if it doesn't hold up.

## 6. Leading Indicators to Monitor Weekly

| Indicator | What would make us nervous | Why |
|---|---|---|
| Day-7 retention gap (treatment vs. control) | The pilot's +30pt gap narrows substantially week over week | Day-7 is the strongest early gate on day-30 (day7=1 → 32.7% reach day-30 vs. day7=0 → 19.7%, per metric-diagnosis.md) — a fading gap here predicts a fading day-30 result |
| Weekly summary open rate (treatment, by send number) | Open rate declines send-over-send instead of holding/compounding as the pilot showed (28%→56%) | Declining open rate is the signature of a novelty spike, not a durable habit — would predict the effect won't hold at full test length |
| iOS vs. Android retention split (treatment only) | The ~20pt platform gap from the pilot widens, or Android stays flat/low | Diagnosis flagged this as the top actionable churn hypothesis — a real platform gap would mean part of the true effect is masked by a fixable delivery problem, changing both the result's interpretation and the rollout plan |

## Implication for the Recommendation Memo

**This changes [docs/recommendation-memo.md](../docs/recommendation-memo.md).** That memo's ask ("approve a 2-cohort extension, set a Q3 go/no-go date") is now underscoped — 2 more cohort-weeks (~200 users) is nowhere near the ~2,320 needed for a properly powered test. The memo should be revised to ask for the full test design above (with the population-scope decision surfaced explicitly), not a short informal extension. Flagging this rather than silently editing the memo — recommend revisiting it together before it goes to Marcus.
