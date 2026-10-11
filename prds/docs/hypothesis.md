# Learning Synthesis & Hypothesis — Engage v2

**Date:** 2026-07-16
**Sources:** [change_log.md](../change_log.md), [decision-brief.md](decision-brief.md)

## What We Know

- 30-day retention dropped from 44% to 37% over the last two quarters (Marcus, #product-engage thread, 2026-07-13).
- A static, unchanging experience is the dominant complaint — 5 of 10 NPS responses and 2 of 3 interviews name it directly.
- The mechanism that demonstrably drives long-term retention (personalized pattern recognition) takes ~3 months to surface — but users churn well before that (week 5, day 10 disengagement signals).
- Users explicitly ask for prescriptive guidance ("tell me what to do") and goal continuity (a stated savings goal was never referenced again).
- None of 5 major competitors (YNAB, Rocket Money, Copilot Money, Monarch Money, PocketGuard) push a single ranked personalized insight unprompted, or treat a stated goal as a recurring touchpoint — this is real competitive white space, not just an internal blind spot.
- In the first prototype usability round, both screens were understood correctly at a glance, and the in-app screen rated "High" impact on actual spending behavior.
- The persona roleplay walkthrough surfaced that the peer-benchmark comparison mechanic is polarizing: motivating for a progress-driven user (Priya), but read as being lectured/judged by a guilt-prone, skeptical user (Tom) — and a generic nudge that ignores debt context undermines trust for a detail-oriented user (Amara).

## What We Assume

- That fixing post-week-1 relevance is *sufficient* to close the 7-point retention gap — not tested against alternative causes (pricing, competitor switching, unrelated app-quality issues). *(flagged in strategy.md)*
- That the interview sample (n=3) and NPS sample (n=10) generalize to the broader user base — both are directional, not statistically validated.
- That the competitive white-space gaps hold up — they're inferred from public feature descriptions and reviews, not hands-on competitive testing.
- That the personas' roleplayed reactions predict real user reactions — Tom's negative response to benchmarking is a synthetic inference, not confirmed by an actual skeptical user yet.
- That closing the day-1-to-month-3 gap with a manufactured insight will actually retain users long enough for real personalization to take over — this causal link is the core bet of the whole initiative and is untested.

## What We Still Do Not Know

- Whether Nudge has bank-sync or notification-reliability issues similar to competitors — flagged as an open risk, not yet investigated.
- Where retention/engagement data actually lives (dashboard, warehouse, or manual) — still TBD per CLAUDE.md.
- The company's core/north-star metric — still unconfirmed, so it's unclear whether 30-day retention is the metric leadership will ultimately judge this initiative against, beyond this specific effort.
- Whether peer-benchmark framing should be optional or personalized by user skepticism level — a new open question raised by the persona walkthrough, not yet resolved.
- Real user sentiment on competitors — current Reddit-adjacent research is low-confidence, secondary-source only.
- Whether the narrower goal-continuity-only option (Option 2 in the decision brief) would have been sufficient on its own, versus the fuller build now in progress — not tested head-to-head.
- No real usability testing has happened yet with actual users resembling Priya, Tom, or Amara — only synthetic roleplay so far.

## Hypothesis Statement

We believe that **the personalized weekly money summary** (a benchmarked spending insight, one actionable nudge, and continuous savings-goal progress) will **deliver a reason for users to return and take action before they would otherwise go passive — bridging the gap between the initial spending breakdown and the ~3-month point where deeper personalization takes over** for Nudge users in their first 30 days, as measured by 30-day retention rate.
