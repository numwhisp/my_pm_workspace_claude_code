---
name: weekly-status
description: Turn raw bullet-point notes into one or more formatted status updates (Shipped, In Progress, Blockers, Next Week), calibrated per audience using stakeholder profiles.
---

# Weekly Status Update

## Input

- Raw bullet-point notes — unformatted, in any order, any level of detail.
- Optionally, one or more audiences to generate for (e.g., "team update for Raj and Lena," "leadership update for Marcus"). If audiences are named and `stakeholders/*.md` files exist for them, read those profiles and calibrate tone/format/detail per person before writing.

## Accuracy Check (run before formatting anything)

Before sorting notes into sections, cross-check each claim against the actual workspace files it references (e.g., a note claiming a doc is "70% done" or a finding is "confirmed" — verify against the real file). If a note conflicts with what's actually documented, do not silently propagate the inaccurate version. Flag the discrepancy to the user and use the accurate status in the output. This applies even under time pressure — a status update that reaches Raj, Lena, or Marcus with a wrong claim is worse than a slightly awkward correction.

## Audience Calibration

When more than one audience is requested, generate a separate update per audience rather than one generic version. Use each person's profile (`stakeholders/<name>.md`) to calibrate:

- **Format:** bullet-heavy and short for someone who prefers async/bullets over paragraphs; narrative/first-sentence-recommendation for someone who wants the bottom line up front.
- **Length:** match their stated tolerance (e.g., "anything requiring more than one page" is a hard no for some readers).
- **What to foreground:** surface the specific category of thing each person cares about — e.g., blockers with scope/estimate for an engineer who dislikes surprises in standups; business-outcome framing and a clear ask-with-deadline for a leadership reader; a pointer to look at an artifact directly, not a prose description of it, for someone who prefers seeing over reading.
- **What to omit:** don't include research-methodology or implementation-level detail a leadership reader doesn't need to feel informed; don't compress away the specific edge cases/estimates an engineering reader needs.
- **Open items:** if a person has a known standing open item (per their stakeholder profile), and this week's update touches it, name it explicitly rather than letting it sit implicit.

## Output

A leadership-ready update with exactly these four sections, in this order:

1. **Shipped**
2. **In Progress**
3. **Blockers**
4. **Next Week**

## Rules

- Keep each section tight — prioritize the highest-impact items over completeness. Default cap is 3 bullets per section; relax it only when the audience's own profile calls for more detail (e.g., an engineering team update), and tighten it when the audience caps length (e.g., a leadership reader who rejects anything over one page). Don't compress multiple items into one bullet just to hit a count.
- Plain, declarative language. No jargon, no filler adjectives ("robust," "seamless," "exciting"), no hedging.
- One line per bullet. State what happened or what's planned — not why it matters or how it was done, unless that's the point of the item.
- If a section has nothing to report, write "None this week" rather than omitting the section or padding it with a weak item.
- Never invent items not in the input notes. If a note's status is ambiguous (unclear which section it belongs to), ask rather than guess.

## Process

1. Read the raw notes.
2. Run the Accuracy Check above against any claim that references a workspace file or finding.
3. Sort each note into Shipped / In Progress / Blockers / Next Week based on its actual status. Infer from context/verb tense: "finished," "launched," "shipped" → Shipped; "working on," "in review" → In Progress; "waiting on," "stuck," "blocked by" → Blockers; "planning to," "starting," "next up" → Next Week.
4. Rewrite each note as one plain, declarative sentence.
5. If multiple audiences were requested, read each named person's `stakeholders/<name>.md` and apply Audience Calibration — produce one distinct update per audience, not one generic version reused.
6. Trim each section per the length rule above, keeping the highest-impact items.
7. Output using the template below, once per audience.

## Output Template

```
## Shipped
- ...

## In Progress
- ...

## Blockers
- ...

## Next Week
- ...
```
