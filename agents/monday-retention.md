# Agent Spec — Monday Retention Digest

**Purpose:** Runs before Monday standup. Checks Nudge 30-day retention against last week's baseline, compares session counts and nudge open rates, and posts a plain-English digest to Slack.

**Status:** Manual-run script today (`agents/monday_retention.py`), designed to become a scheduled job (cron / n8n / timer) once the blockers below are resolved. Not automated yet — see Limitations.

## ⚠️ Limitations to Resolve Before This Can Actually Run on a Timer

1. **No live data source.** Per `CLAUDE.md` ("Data source ground truth"), where retention data lives on an ongoing basis (warehouse, dashboard API, recurring export) is still undecided. The script currently reads a manually-provided `Nudge Dataset.xlsx` export — that's a real blocker to automation, not a detail to paper over. A cron/n8n version needs a real query target.
2. **"Push notification open rate" is approximated.** The dataset doesn't distinguish delivery channel (push vs. in-app vs. email) per nudge — the script uses the pooled nudge open rate across all nudge types as the closest available proxy. If push-specific tracking exists elsewhere, swap it in.
3. **Retention numbers blend variants once an experiment is running.** Cohort week 5 mixes treatment and control (see `data/metric-findings.md`) — the digest currently reports the blended number. Once an experiment is live, decide whether the digest should split by variant or report blended (and flag which, so nobody misreads a blended number as the treatment effect).
4. **No Slack webhook is wired up.** The script prints the digest to console. Posting it to Slack requires a webhook URL and an HTTP POST — see "Wiring to Slack" below for the shape of that step.

## 1. The Agent Script

`agents/monday_retention.py` — reads the dataset, computes 3 metrics for the two most recent cohort weeks (30-day retention, avg sessions/user, nudge open rate), identifies whichever moved the most (a simple rule-based heuristic, not a statistical test), and prints a formatted Slack digest.

Logic summary:
- Load `Users`, `Sessions`, `Retention`, `Nudges` sheets into SQLite.
- For the current and prior cohort week: compute day-30 retention %, avg sessions/user, pooled nudge open %.
- Biggest mover = whichever metric has the largest normalized change (sessions normalized to % change so it's comparable to point-based metrics).
- Suggested action is rule-based and transparent (see the `suggested_action()` function) — e.g., a retention drop points to checking actionable-screen engagement (per `data/metric-diagnosis.md`); a nudge-open-rate drop points to checking relevance/targeting (per the notification opt-out precedent in `research/nps-analysis.md`, #4).

## 2. How to Run It Manually (verify output before trusting it)

```bash
python agents/monday_retention.py "C:\path\to\Nudge Dataset.xlsx"
```

If no path is given, it defaults to the path used during development. On Windows terminals, set `PYTHONIOENCODING=utf-8` first if emoji characters throw a `UnicodeEncodeError` in console output — this is a Windows console display quirk only; it doesn't affect the emoji rendering fine once posted to Slack.

**Verified real output** (run 2026-07-16, against the actual uploaded dataset, comparing cohort week 5 vs. week 4):

```
📊 *30-Day Retention:* 29.0% (week 5) vs 22.0% (week 4) — +7.0pts

👀 *Signal to watch:* avg sessions/user moved the most this week — 4.48 vs 3.69 (+0.79).

✅ *Suggested action:* Session frequency is up the most this week — worth understanding why, so it can be sustained.
```

This confirms the script runs end-to-end against real data and produces the required 3-part format (headline / signal / action) with no invented numbers.

## 3. Slack Message Template

```
:bar_chart: *Nudge Retention — Monday Digest*

*30-Day Retention:* {current_pct}% (week {current_week}) vs {baseline_pct}% (week {baseline_week}) — {sign}{delta}pts

:eyes: *Signal to watch:* {metric_label} moved the most this week — {current_val} vs {baseline_val} ({sign}{delta}).

:white_check_mark: *Suggested action:* {suggested_action_text}

_Auto-generated ahead of Monday standup. Source: agents/monday_retention.py._
```

The script's `build_digest()` function already produces text in this shape — swapping `:bar_chart:` colon-emoji for the Unicode emoji it prints is a cosmetic choice depending on how the webhook renders it.

## 4. Wiring to Slack (future step, not done yet)

Once a webhook URL exists (Slack app → Incoming Webhooks), the script's `main()` function would `POST` the digest string as `{"text": digest}` to that URL instead of (or in addition to) printing it. Left undone here deliberately — no webhook exists yet, and wiring one up is a real infrastructure step, not a documentation exercise.

## 5. Where This Runs From, in the Real World

Cron job, n8n workflow, or a scheduled Python task — triggered Monday early morning, ahead of standup. Not implemented as a live schedule in this workspace; this spec and the manually-runnable script are the design artifact for that future step.
