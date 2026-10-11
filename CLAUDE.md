# Workspace Context

Personal PM workspace. Files and artifacts produced here are shared with the team — write for that audience, not just for the owner.

## Who this is for

- **Owner:** PM at Nudge, owns the Engage squad (home feed, weekly money summaries, savings nudges, push notifications).
- **Triad:** Raj (Senior Engineer), Lena (Product Designer), Owner (PM). Full profiles: `stakeholders/raj.md`, `stakeholders/lena.md`.
- **Reports to:** Marcus, Head of Product. Full profile: `stakeholders/marcus.md`.
- **Audience for docs/artifacts:** the team above, plus other PMs at Nudge.

## Company & product

- **Nudge** — consumer personal finance app. Users connect bank accounts, see a spending breakdown, set savings goals, and get nudges to stay on track.
- Launched 4 years ago. Series B, $42M raised.
- 2.1M registered users, 340K MAU, growing 28% YoY on MAU.
- Core acquisition funnel (signup → connect account → spending breakdown) works well. The problem is what happens after: users go passive post-aha-moment.
- 30-day retention (% still active 30 days after connecting first account) dropped from 44% to 37% over the last two quarters.
- **Core company/north-star metric: TBD, not yet confirmed.** 30-day retention is the metric specific to the Engage v2 initiative — do not assume it's the company-wide north star until confirmed.

## Key tension

Nudge's top-of-funnel is healthy and growing (28% YoY MAU growth, 2.1M registered users) — signup → connect account → spending breakdown converts reliably. That growth is masking an activation-to-habit gap: once the initial "aha moment" passes, the app gives users no personal, timely, or actionable reason to return, and 30-day retention has fallen from 44% to 37% over two quarters.

## Current initiative: Engage v2 — Status as of 2026-07-16

Hypothesis: users go passive because the app stops feeling relevant after week 1. Feature concept: a personalized weekly money summary (top spending insight, one actionable nudge, savings-goal progress).

**Progress so far:**
- Discovery complete: user interviews, NPS analysis, competitive research (5 competitors + Mint historical context), competitive Reddit sentiment pass (inconclusive — tooling-limited).
- Prototype built and tested across 3 personas (Priya/Tom/Amara), through 2 usability rounds plus a design review with Lena.
- PRD written and pressure-tested against Raj/Marcus/Tom objections.
- A 50/50 pilot shipped in cohort week 5. Results: +14pt day-30 retention, +30pt day-7, compounding open-rate — **but not statistically significant at n=50/arm** (p≈0.124, 95% CI includes zero).
- A properly powered follow-up test has been designed (~1,160 users/variant). Test duration depends on an **undecided scope call**: new-signups-only (~27 weeks, doesn't fit) vs. broader active-user base (~5 weeks, fits) — this is the single biggest open blocker right now.
- A quarterly-review deck for Marcus is built, asking him to approve the powered test and make that scope call.

**Open decisions blocking next steps:**
- Test population scope (new-signups-only vs. broader WAU) — needed before the test can be scheduled.
- Savings-goal data model doesn't exist yet — needs its own ticket with a rollback plan, separate from the feature ticket (Raj's standing open item).
- Ranking logic for insight selection still needs to be built.
- Q3 rollout timeline — Marcus's standing ask, still unanswered.
- **Dataset provenance unconfirmed** — see "Data source ground truth" below. Blocks treating any `/data` finding as decision-grade for a real rollout.
- **Stakeholder profiles unverified** — `stakeholders/profile-confirmation-request.md` is drafted and ready to send to the real Raj, Lena, and Marcus; their responses haven't come back yet.
- **No real usability testing has happened** — `research/usability-test-plan.md` is drafted (recruitment + session script); not yet run.

**Capstone review completed 2026-07-16** — full workspace audit against build quality and handoff-readiness. See `docs/capstone-session.md` for the confidence assessment per artifact and the reasoning behind the three open items above.

## Agent Stack

Three agents are built (specced + working scripts, not yet live-scheduled — see each spec's caveats on data source and deployment):

- **Metric Pulse Agent** — nightly, monitors 30-day retention (±2pt alert threshold, channel breakdown), delivers Monday 8am to Slack `#pm-nudge-engage`. `agents/metric-pulse.md`.
- **Weekly Insight Report** — Friday 4pm, pulls retention data + change_log.md sprint completions + top NPS theme, saves `reports/YYYY-MM-DD.md` + posts a 3-2-1 Slack summary. `agents/weekly-insight.md`.
- **Anomaly-to-Hypothesis Agent** — event-driven, fires only when Pulse Agent detects a >2pt move; runs a 4-step gated diagnostic (threshold → metric-tree decomposition → ranked hypotheses → SQL), or posts a low-confidence variant if nothing clears a 6/10 confidence bar. `agents/anomaly-diagnosis.md`.

Full registry (data sources, output formats, owners, connection plan): `agents/registry.md`. **Known gap:** Anomaly Agent's output doesn't yet feed back into Weekly Insight Report — flagged in the registry's Connection Plan, not yet closed.

## Current Canonical Documents

Where a file has a dated successor, treat the dated version as current and the original as historical context only:

- **Recommendation memo:** `docs/recommendation-memo-2026-07-16.md` is current (accounts for the significance finding). `docs/recommendation-memo.md` is superseded — do not use it as a source of the current ask.
- **Competitive matrix:** `research/competitive-matrix-2026-07-16.md` is current (adds Mint historical context). `research/competitive-matrix.md` is the original, still accurate on the 5 live competitors, just without that addition.
- **PRD:** `docs/prd.md` is the real, completed PRD. `prds/prd-engage-v2-2026-07-16.md` is the early skeleton draft — historical only.
- When in doubt about which version of anything is current, check `change_log.md` for the most recent entry touching that file before treating it as ground truth.

## Constraints

No standing constraints defined yet (deadlines, engineering limits, resourcing) beyond the open decisions listed above. If any surface during work that should apply to every session, flag them here for the user to decide whether to add.

## Folder structure

- `/prds` — early-stage PRD drafts/skeletons. The finished, current PRD lives in `/docs` instead (`docs/prd.md`) — this split hasn't been reconciled, see `workspace-audit.md`.
- `/meeting-notes` — notes from meetings, Slack thread writeups, invites.
- `/research` — user research, NPS analysis, competitive research, persona work.
- `/docs` — the primary home for finished deliverables: decision briefs, the PRD, design/spec reviews, QA, recommendation memos, presentations.
- `/prototype` — the working interactive prototype (`index.html`) and its README.
- `/stakeholders` — profiles for Raj, Lena, Marcus — used to calibrate tone/format/content per audience and for objection-testing roleplay.
- `/data` — real dataset analysis: metric findings, metric diagnosis, experiment design.
- `/skills` — reusable prompt/instruction templates (e.g., `weekly-status.md`). Treated as living config, edited in place (see Editing rule).
- `/agents` — specs (and, where they exist, runnable scripts) for automated/scheduled workflows, e.g. `monday-retention.md` + `monday_retention.py`, `metric-pulse.md` + `metric_pulse.py`, `weekly-insight.md` + `weekly_insight.py`. Not live schedules — design artifacts for a future cron/n8n/timer step.
- `/reports` — dated output from the weekly insight agent (`reports/YYYY-MM-DD.md`). Generated files, not hand-written.
- Root — `project.md`, `strategy.md`, `change_log.md`, `workspace-audit.md`, and other cross-cutting files stay at root.

## Writing rules (hard rules — apply to every doc/artifact)

- Concise and data-driven. Cut fluff. Don't bury key information in dense paragraphs — use structure (headers, bullets, short lines).
- **Never invent numbers or facts.** Every figure needs a cited source, or must be explicitly flagged as `TBD`.
- **Explicitly highlight assumptions** whenever one is made — don't let them blend into stated fact.
- Accuracy and precision over polish. This is a Nudge cultural norm, not just a personal preference. If a task's source files are stale or superseded, flag it before propagating a claim you know is outdated — this has already come up more than once.

## Editing rule

**Never overwrite an existing doc.** When asked to edit or rewrite a file, save a new file: original filename + date appended, e.g. `prd-engage-v2-2026-07-16.md`. The old version stays untouched.

**Exceptions — edited in place, never versioned/dated:**
- `CLAUDE.md` itself.
- Files in `/skills` — these are reusable tool/process config, not team-facing artifacts.

The "always save as new dated file" rule applies to team-facing docs/artifacts only.

## Session behavior

Proactively prompt the user when conversation content looks worth saving to a file — whether an existing tracked file (`project.md`, `strategy.md`, `change_log.md`, etc.) or a new one. Don't wait to be asked; flag it, name the file, and let the user confirm.

## Data source ground truth

A dataset (`Nudge Dataset.xlsx`, uploaded directly) was used for the week-5 pilot analysis, queried via SQLite — this is the current source for anything in `/data`. **⚠️ Provenance unconfirmed:** whether this file is real production data or an illustrative/generated dataset built for this exercise has never been established. Every downstream statistical claim (metric-findings.md, metric-diagnosis.md, experiment-design.md, the recommendation memo, the presentation deck) inherits this uncertainty. Confirm the actual source before treating any of those numbers as decision-grade for a real rollout call. **Also still open:** where retention/engagement data lives on an ongoing basis (dashboard, warehouse, recurring export) has not been defined. Don't assume a standing pipeline exists — ask, or flag figures as unsourced/TBD, until both of these are confirmed.
