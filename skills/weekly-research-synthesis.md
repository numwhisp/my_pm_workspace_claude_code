---
name: weekly-research-synthesis
description: One-paste workflow that synthesizes new user feedback/NPS/support signal since the last run — pasted inline, or pulled from anything new in research/ if nothing is pasted.
---

# Weekly Research Synthesis

## Trigger Prompt

Paste this, optionally followed by any raw feedback/NPS comments/support ticket notes you have on hand:

> Run the weekly research synthesis workflow for Nudge Engage v2.
> [optional: paste raw feedback, NPS comments, or support ticket notes below this line]

No further input required after pasting — if you don't have raw notes to paste, the workflow still runs using whatever new material already exists in the workspace.

## Steps Claude Runs

1. Check `change_log.md` for the date of the most recent "weekly research synthesis" entry — this defines the review window (today back to that date, or back to project start if none exists yet).
2. **If raw feedback was pasted below the trigger:** treat that as the primary input. Extract themes mentioned more than once, cite verbatim quotes, note total item count (n), and flag praise vs. complaints — same rigor as `research/nps-analysis.md`.
3. **If nothing was pasted:** scan `research/` (and `data/` if relevant) for any file created or modified since the review-window start date. Synthesize only what's genuinely new — do not re-summarize material already covered in an existing synthesis doc.
4. **If neither of the above produces anything new:** say so explicitly — output "No new research input found this week" rather than fabricating themes or padding with old material re-labeled as new.
5. Cross-check any theme against the existing findings in `research/nps-analysis.md` and `research/interview-synthesis.md` — note explicitly whether this week's signal reinforces, contradicts, or adds something not seen before.
6. Never invent a source, a quote, or a frequency count. If a claim's origin is unclear, flag it as unsourced rather than attributing it.

## Output Format

```
# Weekly Research Synthesis — [date range]

## Input Source
[pasted feedback | new files found in research/ (list them) | none found]

## Themes (mentioned more than once)
[ranked by frequency, cited quotes, n]

## Praise vs. Complaints

## Relationship to Existing Findings
[reinforces / contradicts / new, vs. nps-analysis.md and interview-synthesis.md]

## Open Questions
```

If no new input exists, output just:
```
# Weekly Research Synthesis — [date range]
No new research input found this week (no raw notes pasted, no new files in research/ since [last synthesis date]).
```

## Where It Gets Saved

`research/weekly-synthesis-{YYYY-MM-DD}.md` (today's date). New file each run.
