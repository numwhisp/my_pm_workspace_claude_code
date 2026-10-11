# Agent Spec — Anomaly Diagnosis Loop (chained off Retention Pulse)

**Trigger:** only runs when `agents/metric_pulse.py`'s headline 30-day retention move exceeds ±2pts. Below that, it logs and stops — no diagnostic runs, no Slack post.

**⚠️ Data caveats, same family as every other agent in this workspace:** no live retention pipeline exists yet, dataset provenance is unconfirmed (CLAUDE.md). Additionally specific to this agent: **the sample spec this was built from referenced a `nudge_notifications` table with a `delivered` column and a "push opt-in rate" — neither exists in the real Nudge dataset.** The real schema has `nudge_nudges` (nudge_type, opened, acted_on — no delivery-confirmation field). Every hypothesis and SQL query below is built against columns that actually exist; nothing here references the fictional table. If push-delivery-specific diagnosis is genuinely needed, that's a real data-tracking gap to raise with Raj, not something to paper over with an invented schema.

## 1. The Chained Agent

`agents/anomaly_diagnosis.py` — takes the headline retention comparison (real mode: computed from the dataset for the two most recent cohort weeks; simulated mode: a synthetic scenario via `--simulate`) and runs the 4-step gated loop below.

## 2. Step Conditions — What Passes, What Stops

**Step 1 — Threshold check.** Passes if `|headline delta| > 2.0pts`. If not: log the move and stop — no further steps run, nothing posted to Slack.

**Step 2 — Metric tree decomposition.** Computes every driver in the metric tree (day-7 retention, session frequency, nudge open rate, week-1 goal-set rate, retention by acquisition channel ×3, retention by platform ×3) for both weeks, and flags each as "meaningfully moved" against its own threshold (1.5pts for rate-based drivers, 3pts for channel/platform retention, 10% relative change for session frequency — thresholds chosen to be tighter than the headline's 2pt bar, since a driver needs to move more than noise before it's worth naming as a candidate cause). Passes only if **2 or more** drivers clear their threshold. If only 1 (or 0) did: flag inconclusive and stop — the spec explicitly forbids generating hypotheses from a single signal, and the code enforces that, not just the prompt.

**Step 3 — Hypothesis generation.** Each meaningfully-moved driver maps to a candidate hypothesis (see library in the script) with a transparent, rule-based confidence score: magnitude of that driver's own move, plus a bonus for co-movement with the other meaningfully-moved drivers (more drivers moving together = a more defensible shared-cause story, capped at +4). Top 3 by confidence are kept. Passes only if the #1 hypothesis scores **above 6.0/10**. If not: post the low-confidence Slack variant and stop — no SQL is generated for a hypothesis that didn't clear the bar.

**Step 4 — SQL + Slack.** Only reached if all 3 prior gates passed. Generates the SQL template mapped to the top hypothesis's driver (against real table/column names), and formats the full diagnostic for Slack.

## 3. Slack Diagnostic Format

**Full diagnostic** (all 4 steps passed):
```
🔍 *Nudge Anomaly Detected — {date}*

Trigger: 30-day retention {dropped/rose} {X}pts ({baseline}% → {current}%)

Metric tree decomposition:
  {driver}   {baseline} → {current}  ({arrow} {delta}{unit})
  ... (all computed drivers, with a note on any that didn't clear their own threshold)

Top 3 hypotheses:
  1. {hypothesis text} (confidence: {score}/10)
  2. ...
  3. ...

SQL to confirm hypothesis 1:
  {SQL against real schema}

Run this query and reply with the output. I'll interpret.
```

**Low-confidence variant** (steps 1–2 passed, step 3 failed):
```
⚠️ *Nudge Anomaly Detected — Low Confidence — {date}*

Trigger: 30-day retention {dropped/rose} {X}pts ({baseline}% → {current}%)

Best available hypothesis: {top hypothesis text} — confidence only {score}/10 (below the 6/10 bar to act on).

Not writing SQL or naming a root cause I can't defend. Needs a human look before standup — likely more data or a wider time window than one week-over-week comparison can resolve.
```

Two other outcomes never reach Slack at all — they log and stop: **no-trigger** (move ≤2pts) and **inconclusive** (only 1 driver moved).

## 4. Test Results — All 4 Branches Verified

**Full diagnostic, simulated 4pt drop** (synthetic input, clearly labeled — not real data, exists to verify loop logic end to end per the request):
```
🔍 Nudge Anomaly Detected — Tue May 13, 8:47am (simulated)

Trigger: 30-day retention dropped 4.0pts (37.0% → 33.0%)

Metric tree decomposition:
  day7_retention               58.0 → 54.0  (↓ 4.0pts)
  avg_sessions                 4.1 → 3.2  (↓ 22.0%)
  nudge_open_rate              14.0 → 11.0  (↓ 3.0pts)
  goal_set_rate                31.0 → 30.0  (↓ 1.0pts)  (below meaningful-movement threshold)
  paid_channel_retention       33.0 → 29.0  (↓ 4.0pts)
  organic_channel_retention    37.0 → 36.0  (↓ 1.0pts)  (below meaningful-movement threshold)
  referral_channel_retention   36.0 → 35.0  (↓ 1.0pts)  (below meaningful-movement threshold)
  android_platform_retention   34.0 → 28.0  (↓ 6.0pts)
  ios_platform_retention       39.0 → 38.0  (↓ 1.0pts)  (below meaningful-movement threshold)
  web_platform_retention       31.0 → 30.0  (↓ 1.0pts)  (below meaningful-movement threshold)

Top 3 hypotheses:
  1. A platform-specific effect on Android is driving the retention move (confidence: 9.0/10)
  2. Session frequency drop is driving the retention move (confidence: 8.4/10)
  3. An early (day-7) drop is driving the retention move — investigate week-1 experience directly (confidence: 8.0/10)

SQL to confirm hypothesis 1:
  SELECT u.cohort_week, u.platform, COUNT(*) n_users, ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_pct
FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week IN (SIM_CURRENT, SIM_BASELINE) AND u.platform='android'
GROUP BY u.cohort_week ORDER BY u.cohort_week;

Run this query and reply with the output. I'll interpret.
```
(`SIM_CURRENT`/`SIM_BASELINE` are intentional placeholders, not real cohort week numbers — this run exists to test logic, not to be executed.)

**Also run and verified against real data** (cohort week 5 vs. 4 — same experiment-cohort caveat as every other agent: this blends the live pilot's treatment/control, real variant split is in `data/metric-findings.md`): correctly triggered on the real +7.0pt move, correctly ranked day-7 retention, goal-set rate, and organic channel as the top 3 (all real, all above the confidence bar), and generated real, runnable SQL.

**Also verified independently, the 3 non-full-diagnostic branches:**
- **No trigger** (+1.0pt move): logged and stopped, nothing posted.
- **Inconclusive** (move above threshold, only 1 driver moved): logged and stopped, no hypotheses generated.
- **Low confidence** (move above threshold, 2 drivers moved but both weak/isolated): posted the low-confidence Slack variant, correctly declined to generate SQL.

**Two real bugs found and fixed during testing**, worth noting since "verify before scheduling" only means something if it can catch something: an early version had hardcoded "drop" language even when the real data showed a *rise* (the sample spec's scenario was a drop, and that language leaked into the general case); and the first low-confidence test case used a headline delta of exactly −2.0pts, which doesn't clear the strict `>2.0` trigger condition — the test itself caught its own mistake.

## 5. Chaining to the Existing Pulse Agent

`agents/metric_pulse.py` computes the headline retention move already (see `agents/metric-pulse.md`). In the real-world wiring (cron/n8n/Python), the pulse agent's headline delta becomes the direct input to Step 1 here — this script's `run_loop()` function is called with that value rather than recomputing it. Today, both scripts independently query the dataset for the same two cohort weeks; wiring them together in production means one query, feeding both the Monday pulse digest and (conditionally) this diagnostic.
