# Nudge PM Agent Registry

**Last updated:** 2026-07-16
**Note on the template:** the requested template listed `data/retention-metrics.md` as a data source — that file doesn't exist. The real source, as actually built and verified in `agents/metric_pulse.py`, `agents/weekly_insight.py`, and `agents/anomaly_diagnosis.py`, is the uploaded `Nudge Dataset.xlsx`, queried directly via SQLite. Corrected below rather than left as-is. **Owner** is left as a placeholder — fill in your name; not something I can fill in for you.

## Metric Pulse Agent

- **Trigger:** nightly compute (cron or n8n in production)
- **Data source:** `Nudge Dataset.xlsx` (Users + Retention sheets), queried via SQLite — see `agents/metric-pulse.md`. Provenance of this dataset is unconfirmed (real vs. illustrative) — flagged in CLAUDE.md.
- **Alert threshold:** ±2pts week over week (headline 30-day retention)
- **Breakdown:** acquisition channel (organic, paid, referral)
- **Output format:** headline metric + channel breakdown + alert flag + top signal (see `agents/metric-pulse.md` Section 2)
- **Delivery channel:** Slack `#pm-nudge-engage`
- **Schedule:** nightly compute, delivers Monday 8am
- **Owner:** [your name]
- **Spec:** `agents/metric-pulse.md` | **Script:** `agents/metric_pulse.py`

## Weekly Insight Report

- **Trigger:** Friday 4pm (cron or n8n in production)
- **Data sources:** `Nudge Dataset.xlsx` (retention), `change_log.md` (sprint completions), `research/nps-analysis.md` (top NPS theme)
- **Output format:** 3 done / 2 changed / 1 watch — see `agents/weekly-insight.md` Section 2
- **Delivery channel:** `reports/YYYY-MM-DD.md` (versioned file) + Slack `#pm-nudge-engage` (3-2-1 summary)
- **Schedule:** weekly, Friday 4pm
- **Owner:** [your name]
- **Spec:** `agents/weekly-insight.md` | **Script:** `agents/weekly_insight.py`

## Anomaly-to-Hypothesis Agent

- **Trigger:** fired by Metric Pulse Agent when the headline retention move exceeds ±2pts (see Connection Plan below)
- **Data source:** inherits the headline delta from Pulse Agent's output; independently queries `Nudge Dataset.xlsx` for the full metric-tree decomposition (day-7 retention, session frequency, nudge open rate, goal-set rate, channel × platform retention)
- **Output format:** 4-step gated diagnostic (threshold check → decomposition → ranked hypotheses with confidence scores → SQL) or a low-confidence variant if no hypothesis clears 6/10 — see `agents/anomaly-diagnosis.md` Section 3
- **Delivery channel:** Slack `#pm-nudge-engage`, diagnostic thread
- **Schedule:** event-driven — only fires when Pulse Agent detects an alert
- **Owner:** [your name]
- **Spec:** `agents/anomaly-diagnosis.md` | **Script:** `agents/anomaly_diagnosis.py`

## Connection Plan

**Pulse → Anomaly:** Metric Pulse Agent computes the headline retention delta every night. When `|delta| > 2pts`, that delta (plus the two cohort weeks being compared) becomes the direct input to the Anomaly Agent's Step 1 — today this is two independent scripts each re-querying the dataset; in production wiring, one nightly query result feeds both, and the Anomaly Agent's `run_loop()` is called directly with Pulse's output rather than recomputing it. Below the 2pt threshold, Pulse still delivers its Monday digest, but Anomaly never runs — no diagnostic, no Slack post from that agent.

**Anomaly → Weekly Insight:** **not yet built — this is a design gap, flagged rather than glossed over.** `agents/weekly_insight.py` currently computes its own "Changed this week" retention signal independently (same dataset, same query pattern as Pulse) — it does not currently ingest anything from the Anomaly Agent's output. The intended connection: when an anomaly diagnostic ran that week (full or low-confidence), its top hypothesis (or the low-confidence flag itself) should replace or augment Weekly Insight's raw "Changed this week" bullet — so a Friday report reads "retention rose 7pts, likely driven by day-7 improvement (confidence 9/10, per Tuesday's anomaly diagnosis)" instead of just restating the number with no attributed cause. This requires Weekly Insight to read the week's anomaly diagnostic output (e.g., a saved log/file from the Anomaly Agent) as a 4th data source, which doesn't exist yet.

## What Would Need to Be Built to Close the Gap

The Anomaly Agent needs to write its output somewhere durable (today it only prints to console/Slack) — e.g., `reports/anomaly-log/YYYY-MM-DD.md` — so Weekly Insight Report can read it back on Friday. Until that exists, Weekly Insight's "Changed this week" section will keep restating raw numbers without the attributed cause, even in weeks when Anomaly already diagnosed one.
