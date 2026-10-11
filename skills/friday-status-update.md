---
name: friday-status-update
description: One-paste workflow that compiles this week's shipped/in-progress/blocked from change_log.md into calibrated updates for the team and for Marcus.
---

# Friday Status Update

## Trigger Prompt

Paste exactly this to run it:

> Run the Friday status update workflow for Nudge Engage v2.

No additional input required — this workflow is self-sufficient from `change_log.md`.

## Steps Claude Runs

1. Read `change_log.md` and identify every entry dated within the last 7 days (today back to the prior Friday).
2. Run the Accuracy Check from `skills/weekly-status.md` — before using any claim, confirm it's still accurate against the actual current file it references (a change_log entry can itself go stale if a later entry in the same window supersedes it, e.g. a memo revision). Use the most current state, not the first mention.
3. Sort the week's entries into Shipped / In Progress / Blockers, using `skills/weekly-status.md`'s sorting rules.
4. Apply `skills/weekly-status.md`'s Audience Calibration to generate two versions:
   - **Team version** — for Raj and Lena, per `stakeholders/raj.md` and `stakeholders/lena.md`.
   - **Leadership version** — for Marcus, per `stakeholders/marcus.md`.
5. For each version's Blockers section, check whether it touches any standing open item already listed in `CLAUDE.md`'s "Open decisions blocking next steps" — if so, name the connection explicitly rather than treating it as a new, isolated blocker.
6. If there is nothing to report in a section, write "None this week" — never pad or invent an item to fill a section.

## Output Format

Two updates, each following `skills/weekly-status.md`'s Shipped / In Progress / Blockers / Next Week structure, clearly labeled:

```
## Team Update — Raj & Lena
[calibrated content]

## Leadership Update — Marcus
[calibrated content]
```

## Where It Gets Saved

`meeting-notes/friday-status-{YYYY-MM-DD}.md` (today's date). New file each week — these are point-in-time snapshots, not something to edit in place.
