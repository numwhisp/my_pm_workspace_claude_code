# Nudge PM Agent Stack — 6-Month Roadmap

**Starting point:** 3 agents built (Metric Pulse, Weekly Insight, Anomaly-to-Hypothesis), not yet live-scheduled, with one known connection gap (Anomaly → Weekly Insight, see `agents/registry.md`). This roadmap adds one new agent per month, prioritized so each month also closes a real connection gap from the prior month rather than just adding an isolated new capability.

## Month 1 — Foundation Hardening + Competitive Pulse Agent

- **Close the existing gap first:** wire Anomaly Agent's output to a durable log (`reports/anomaly-log/YYYY-MM-DD.md`) so Weekly Insight can read it back — closes the one connection gap already flagged.
- **New agent:** automate `skills/competitive-pulse-check.md` into a real scheduled agent (weekly, diffs against `research/competitive-matrix-2026-07-16.md`, flags anything that closes either white-space gap).
- **New connection:** Weekly Insight Report gains a 4th source — competitive moves worth knowing about land in "Watch next week" when relevant.

## Month 2 — NPS/Feedback Ingestion Agent

- Automates `skills/weekly-research-synthesis.md` — but only becomes a *real* agent (not a manual paste-and-run) once a live feedback source exists (support tickets, in-app NPS), which is still an open item per CLAUDE.md.
- **New connection:** Weekly Insight's "top NPS theme" bullet stops being a static read of one old file and starts reflecting genuinely new signal each week.

## Month 3 — Sprint/Ticket Sync Agent

- Replaces `change_log.md` text-parsing (a real limitation flagged in `agents/weekly-insight.md`) with a direct pull from an actual ticket tracker (Jira/Linear/whatever Nudge uses), once one is connected.
- **New connection:** "Done this week" in Weekly Insight becomes accurate and automatic instead of inferred from log entries that may or may not map cleanly to a calendar week.

## Month 4 — Stakeholder Digest Router

- Takes Metric Pulse + Weekly Insight output and automatically generates the calibrated per-person versions using `skills/friday-status-update.md`'s existing audience-calibration logic — Raj, Lena, and Marcus each get their version without a manual trigger.
- **New connection:** the 3 existing agents' output becomes the *input* to a 4th, rather than each agent's output being a dead end that a person has to manually reformat and redistribute.

## Month 5 — Experiment Monitor Agent

- Once the properly-powered test from `data/experiment-design.md` is actually running, this agent tracks real-time progress toward the required ~2,320-user sample, flags if significance is reached early, and applies the Anomaly Agent's diagnostic logic specifically to the live experiment (not just general retention).
- **New connection:** directly extends the Anomaly Agent's confidence-scored hypothesis engine into a live-experiment context, rather than building a separate one from scratch.

## Month 6 — Decision Memory Agent

- The connective-tissue agent: reads every other agent's output plus `CLAUDE.md` and `change_log.md`, and produces a monthly "state of Engage v2" strategic memo — automating what `docs/recommendation-memo-2026-07-16.md` and `docs/presentation.md` did manually.
- **New connection:** this is the point where the stack becomes genuinely "fully connected" — every agent's output is both human-readable on its own *and* an input to this synthesis agent, closing the loop from raw metric movement all the way to a leadership-ready narrative, without a person manually re-deriving it each time.

## What "Fully Connected" Means by Month 6

Not 6 independent tools that each post to Slack — a pipeline where: Pulse detects → Anomaly diagnoses → Weekly Insight narrates → the Stakeholder Router distributes it calibrated per person → the Experiment Monitor applies the same rigor to whatever's live → the Decision Memory Agent rolls all of it into the monthly narrative Marcus actually reads. Each month's agent is scoped specifically to close the connection gap the previous month's agent left open, not just to add a new isolated capability.
