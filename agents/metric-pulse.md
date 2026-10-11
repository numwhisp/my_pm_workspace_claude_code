# Agent Spec — Nudge Retention Pulse

**Metric:** 30-day retention rate | **Baseline:** 37% (company quarterly baseline, CLAUDE.md) | **Alert threshold:** ±2pts week-over-week | **Breakdown:** acquisition channel (organic, paid, referral) | **Delivery:** Monday 8am Slack digest | **Schedule:** nightly compute, Monday delivery

**⚠️ Same data caveats as `agents/monday-retention.md`, read before trusting output for a real decision:** no live retention pipeline exists yet (CLAUDE.md, "Data source ground truth" — still open), and the underlying dataset's provenance (real vs. illustrative) is unconfirmed. "Week over week" here means consecutive cohort weeks in the current dataset, not a live rolling daily calculation. The current test cohort (week 5) blends the live pilot's treatment and control users together in the headline number — see the test run in Section 5 for what that does to the numbers.

## 1. The Agent Script

`agents/metric_pulse.py` — loads `Users` and `Retention`, computes day-30 retention for the two most recent cohort weeks, both overall and split by `acquisition_channel`, and builds a Slack-formatted digest. Alert fires if the headline metric moves ≥2 points; a channel gets the "← watch this" flag if it's the biggest mover *and* its own move is ≥2 points.

## 2. Slack Message Template

```
📊 *Nudge Retention Pulse — {date_label}*

30-day retention: *{headline_pct}%* ({arrow} {magnitude} vs last week){alert_flag}

By channel:
  Organic   {organic_pct}% ({arrow} {magnitude}){watch_flag}
  Paid      {paid_pct}% ({arrow} {magnitude}){watch_flag}
  Referral  {referral_pct}% ({arrow} {magnitude}){watch_flag}

Top signal: {top_signal_text}

Next: run anomaly diagnosis? Reply YES to trigger.
```

`{alert_flag}` = " ⚠️ ALERT" if the headline move is ≥2pts, else empty. `{watch_flag}` = "  ← watch this" on whichever channel is both the biggest mover and itself ≥2pts. Arrows: ↑ up, ↓ down, → flat (movement under 0.05pt treated as flat to avoid noisy false movement on tiny samples).

## 3. How to Run It Manually (verify before scheduling)

```bash
python agents/metric_pulse.py "C:\path\to\Nudge Dataset.xlsx"
```

Defaults to the development dataset path if no argument is given. On Windows, set `PYTHONIOENCODING=utf-8` first if console emoji throw an encoding error — cosmetic only, doesn't affect real Slack delivery.

## 4. How This Would Be Wired in the Real World

Three options, in order of how this workspace would actually get there:

- **Python + cron:** simplest path once a real data source exists — a nightly cron job runs `metric_pulse.py` against a live query (not a manual file), and a Monday-8am job posts the output to a Slack webhook. Good fit if the team already has a place to run scheduled scripts.
- **n8n (or similar workflow tool):** a scheduled trigger node → a database/warehouse query node → a formatting step → a Slack node. Better fit if this needs to live outside engineering's deploy pipeline, e.g. owned by the PM team directly.
- **Developer ticket:** if this needs to plug into Nudge's actual production analytics stack (not a manually uploaded export), this becomes a real engineering ticket — the retention-pipeline decision is still open (CLAUDE.md), so the ticket would need to specify where day-30 retention and acquisition channel actually live once that's decided, plus the alert-threshold logic and the Slack webhook integration.

None of these are wired up yet — this spec and the manually-runnable script are the design artifact for that future step, same status as `agents/monday-retention.md`.

## 5. Test Run — Real Output, Nudge Dataset Snapshot

Run 2026-07-16 against the actual uploaded dataset, comparing cohort week 5 (current) vs. week 4 (baseline):

```
📊 Nudge Retention Pulse — [Monday date]

30-day retention: 29.0% (↑ 7.0pts vs last week) ⚠️ ALERT

By channel:
  Organic   37.0% (↑ 11.0pts)  ← watch this
  Paid      15.6% (↓ 0.5pts)
  Referral  28.6% (↑ 7.5pts)

Top signal: Organic channel rising the fastest (+11.0pts). Check what changed there last week.

Next: run anomaly diagnosis? Reply YES to trigger.
```

**Read before trusting this number:** the +7.0pt jump is expected and explainable — cohort week 5 is the live pilot cohort, and this test run blends treatment and control together rather than splitting by variant (see `data/metric-findings.md` for the variant-split version: 36% treatment vs. 22% control). A real Monday digest running on non-experiment weeks won't have this confound; while an experiment is live, the digest should either split by variant explicitly or note that the headline number includes an active experiment — not treat it as organic week-over-week movement. This is the same nuance already flagged in `agents/monday-retention.md`.

This confirms the script runs end-to-end against real data, matches the requested output format exactly, and correctly fires the alert flag and channel "watch" flag using real numbers — not fabricated ones.
