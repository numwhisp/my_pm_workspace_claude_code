---
name: competitive-pulse-check
description: One-paste workflow that checks for genuinely new competitor moves this week, diffed against the canonical competitive matrix, with sources.
---

# Competitive Pulse Check

## Trigger Prompt

Paste exactly this to run it:

> Run the competitive pulse check workflow for Nudge Engage v2.

No additional input required — this workflow uses web search and the existing competitive matrix.

## Steps Claude Runs

1. Read `research/competitive-matrix-2026-07-16.md` (the canonical version — check `CLAUDE.md`'s "Current Canonical Documents" section in case a newer one exists) to get the current competitor list and each one's documented "Notable recent changes" as the baseline.
2. For each competitor (YNAB, Rocket Money, Copilot Money, Monarch Money, PocketGuard), run a web search for new feature updates, pricing changes, or notable news dated within the last 7–14 days.
3. **Diff against the baseline** — only report items that are not already captured in the matrix's "Notable recent changes." Do not re-report something already documented as if it were new this week.
4. Cite a source link for every new item found. If a search returns nothing genuinely new for a competitor, state that plainly rather than restating old information to fill space.
5. Flag anything that changes the two white-space gaps identified in the matrix (no competitor pushes a single ranked personalized insight unprompted; no competitor treats a savings goal as a recurring touchpoint) — if a competitor ships something that closes either gap, this is the single most important thing to surface, not just another bullet.

## Output Format

```
# Competitive Pulse Check — [date]

## YNAB
[new items with sources, or "Nothing new found this week"]

## Rocket Money
...

## Copilot Money
...

## Monarch Money
...

## PocketGuard
...

## Gap Impact
[does anything found this week close either of the 2 white-space gaps? Yes/no, with reasoning]
```

## Where It Gets Saved

`research/competitive-pulse-{YYYY-MM-DD}.md` (today's date). New file each week — if a finding is significant enough to change the canonical matrix, flag it to the user rather than editing `research/competitive-matrix-2026-07-16.md` automatically.
