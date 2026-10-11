# Real Usability Test Plan — Weekly Summary Prototype

**Why this exists:** every user-reaction artifact so far (persona roleplay, design review, objection log) is Claude simulating Priya, Tom, and Amara — not real users. This plan replaces/supplements that with actual sessions, using the same four questions already validated in the roleplay format (research/persona-roleplay-walkthrough.md) so results are directly comparable.

## Recruitment Criteria (3 segments, matching the original interview subjects)

Recruit real users who plausibly match each profile — not the exact people interviewed, but the same segment:

1. **Progress-motivated, established user** — has used a budgeting/finance app for 6+ months, has an active savings goal, checks it roughly weekly. (Matches Priya.)
2. **Skeptical/churned-risk user** — has tried and abandoned at least one budgeting app before, describes feeling guilty rather than empowered about money, wants to avoid being "lectured." (Matches Tom.)
3. **New, still-active user** — connected a finance app within the last 2 weeks, has viewed an initial spending breakdown, hasn't taken further action since. (Matches Amara.)

Target: 5 sessions minimum (aim for 1–2 per segment), 30 minutes each.

## Session Script

Use the prototype (`prototype/index.html`) live. Ask these four questions in order, same as the roleplay walkthrough, so answers are directly comparable to the simulated version:

1. **What do you think this does?** (Show the email view first, then the in-app screen. Let them react before explaining anything.)
2. **How would you arrive at this experience?** (Do they expect email, push notification, or just opening the app? Don't lead them.)
3. **Would you change your spending based on this?** Why or why not — push for specifics, not just yes/no.
4. **If you had a magic wand, what would you change?**

After all four: ask directly whether the peer-benchmark comparison ("20% above similar users") felt motivating or judgmental — this is the specific, still-unresolved tension flagged in research/interview-synthesis.md and research/persona-roleplay-walkthrough.md, and real data on it is the single most valuable thing this test can produce.

## What to Do With Results

1. Compare each real session against the roleplay walkthrough for the matching persona (research/persona-roleplay-walkthrough.md) — note where real reactions confirm, contradict, or surprise relative to the simulation.
2. Update the confidence table in docs/capstone-session.md once sessions are complete.
3. If the benchmark-framing tension resolves clearly one way or another with real users, update docs/design-review.md's open item accordingly — that's the highest-value single finding this test can deliver.
