# Agent Spec — Nudge Weekly Insight Report

**Sources:** retention metrics (`data/`), sprint completions (`change_log.md`), top NPS theme (`research/nps-analysis.md`) | **Output:** 3 done / 2 changed / 1 watch | **Delivery:** save to `reports/YYYY-MM-DD.md` + post 3-2-1 summary to Slack | **Schedule:** nightly compute, Friday 4pm delivery

**⚠️ Same data caveats as `agents/monday-retention.md` and `agents/metric-pulse.md`, plus two new ones found while building this:**
- No live retention pipeline exists yet; dataset provenance is unconfirmed (CLAUDE.md).
- **"This week" in `change_log.md` is approximated as the most recent dated section.** In this workspace, the entire project so far is logged under one date (2026-07-16), so the first test run pulled from the whole project's history, not a real week — see Section 5. In a workspace with genuine weekly cadence, this would filter to entries from the last 7 days instead.
- **The real system clock and this workspace's fictional "current date" don't match** — the sandbox's actual date differs from the 2026-07-16 used consistently throughout `change_log.md` and every other file. The script defaults to the real system date but accepts an explicit date override as a second argument to stay consistent with the rest of the workspace. Flagging this because it's exactly the kind of silent inconsistency this workspace's rules exist to catch — a report dated "Jul 23" sitting next to everything else dated "Jul 16" would look wrong to anyone reading it.

## 1. The Agent Script

`agents/weekly_insight.py` — pulls from all 3 sources:
- **Retention (data/):** queries the actual dataset for the two most recent cohort weeks, computes headline retention movement and the single biggest-moving acquisition channel (same logic as `agents/metric_pulse.py`).
- **Sprint completions (change_log.md):** parses the most recent dated section, takes the last 3 bullets (most recently logged), trims cleanly without cutting mid-sentence.
- **Top NPS theme (research/nps-analysis.md):** parses the theme-frequency table, pulls the rank-1 row.
- **Watch item:** pulled from `CLAUDE.md`'s "Open decisions blocking next steps" — the first-listed item, since CLAUDE.md already documents that as the current biggest blocker.

## 2. Output Format

Saved report (`reports/YYYY-MM-DD.md`):
```
# Nudge Weekly Insight — {date}

## Done this week
- {bullet 1}
- {bullet 2}
- {bullet 3}

## Changed this week
- {retention headline signal}
- {biggest-mover channel signal}
- {top NPS theme}

## Watch next week
- {top open decision from CLAUDE.md}
```

Slack summary (posted separately): same content, condensed with `•` bullets and a "Saved to {path}" footer — see the real run in Section 5 for exact formatting.

## 3. How to Run It Manually

```bash
python agents/weekly_insight.py "C:\path\to\Nudge Dataset.xlsx" 2026-07-16
```

Second argument (date, `YYYY-MM-DD`) is optional — include it to keep the report consistent with the workspace's established date, given the system-clock mismatch noted above. On Windows, set `PYTHONIOENCODING=utf-8` first if console emoji throw an encoding error.

## 4. How This Would Be Wired in the Real World

Same three options as `agents/metric-pulse.md`, applied here:
- **Python + cron:** nightly compute job, Friday-4pm delivery job posts to a Slack webhook — once a real data source and a real weekly `change_log`/sprint-tracking cadence exist.
- **n8n:** scheduled trigger → data-source query + change-log/ticket-system query + NPS-source query → format → Slack node. A better fit here specifically because this agent pulls from 3 different source types (metrics, dev log, qualitative feedback) — a visual workflow tool makes that fan-in easier to maintain than a single script as sources multiply.
- **Developer ticket:** needed once `change_log.md` and `research/nps-analysis.md` are replaced by real systems (a ticket tracker, a live NPS feed) — the parsing logic in this script is a placeholder for real API calls at that point, not something to keep scraping markdown files in production.

## 5. Test Run — Real Output, Nudge Workspace Snapshot

**First attempt caught its own bugs** — worth showing, since "run it manually to verify" only means something if verification can actually fail. The first run grabbed the *oldest* 3 change_log entries instead of the most recent, truncated one bullet mid-sentence, and dated the report "Jul 23" (real system date) while everything else in the workspace says "Jul 16." All three fixed before treating this as verified.

**Verified output**, run 2026-07-16 (explicit date argument), against the real uploaded dataset and the real current `change_log.md`/`research/nps-analysis.md`:

```
📋 Nudge Weekly Insight — Thu Jul 16

Done this week:
• Ran a full capstone review of the workspace — saved docs/capstone-session.md. Inventoried everything built (discovery through statistically-validated pilot...
• Built onboarding materials for a new-to-Claude-Code teammate — saved docs/onboarding-guide.md (5-minute read: what Claude Code is, first-session...
• Built the Nudge Retention Pulse agent (30-day retention, ±2pt alert threshold, channel breakdown by organic/paid/referral, Monday 8am Slack digest) — saved...

Changed this week:
• 30-day retention: 29.0% (+7.0pts vs cohort week 4, week 5 data)
• Organic channel retention moved most: +11.0pts week-over-week

Watch next week:
• Test population scope (new-signups-only vs. broader WAU) — needed before the test can be scheduled.

Saved to reports/2026-07-16.md
```

Note the same experiment-cohort caveat as `agents/metric-pulse.md`: the +7.0pt retention move is the live pilot cohort (blended treatment/control), not organic week-over-week movement — see `data/metric-findings.md` for the real variant split (36% vs. 22%). A production version running on non-experiment weeks won't have this confound.
