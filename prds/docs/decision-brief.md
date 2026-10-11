# Decision Brief — Engage v2

**For:** Marcus (Head of Product) | **From:** Engage squad | **Date:** 2026-07-16

## Situation

30-day retention has dropped from 44% to 37% over the last two quarters — users go passive after the first week because the app gives them nothing personal, timely, or actionable once the initial spending breakdown is seen. This pattern is independently corroborated by user interviews, NPS feedback, and competitive research (sources below).

## Key Findings

1. **A static, unchanging experience is the dominant complaint** — 5 of 10 NPS responses and 2 of 3 interviews name it directly ("nothing has changed since the first day"). *(research/nps-analysis.md, research/interview-synthesis.md)*
2. **The one mechanism that demonstrably drives retention — personalized pattern recognition — takes ~3 months to surface, but users churn well before that.** Our power-user interview took 3 months to hook; our churned user left at week 5; our newest user is already stalling at day 10. The real payoff arrives too late to save week-1 users on its own. *(research/interview-synthesis.md)*
3. **Users are explicitly asking for prescriptive guidance and goal continuity** — "I need it to tell me what to do," and a user whose stated savings goal was never referenced again, "It is like it forgot." *(research/nps-analysis.md)*
4. **Competitive research confirms this is real white space, not just an internal blind spot.** None of 5 major competitors (YNAB, Rocket Money, Copilot Money, Monarch Money, PocketGuard) push a single ranked personalized insight unprompted, or treat a stated goal as a recurring re-engagement touchpoint. *(research/competitive-matrix.md)*
5. **Reddit sentiment neither confirms nor contradicts these two gaps** — available research skewed toward competitors' reliability/billing complaints (e.g., PocketGuard and Monarch bank-sync failures, Rocket Money billing traps) rather than feature-gap complaints, likely because direct Reddit access wasn't available to this research pass. One adjacent risk did surface worth a quick internal check: bank-sync reliability is competitors' top friction theme — confirm Nudge doesn't share it. *(research/competitive-reddit.md — flagged as lower-confidence, secondary-source data)*

## Options Considered

1. **Ship the personalized weekly summary** (top insight + one actionable nudge + savings-goal progress) — the concept already scoped with Lena (design) and Raj (feasibility confirmed on existing data, ranking logic still to be built).
2. **Ship goal-continuity alone, first** — a narrower, faster fix: surface/reference a user's stated savings goal on a recurring cadence. Addresses finding #3 directly without the full ranking-logic build.
3. **Hold on new features; investigate reliability risk first** — check whether Nudge has bank-sync or notification-relevance issues (per finding #5 and the NPS notification opt-out incident) before investing in new engagement mechanics that a reliability problem could undermine anyway.

## Recommended Action

Commit to Option 1 (the personalized weekly summary), sequenced to ship the goal-continuity piece first as the fastest validated win, while Option 3's reliability check runs in parallel — not as a blocker.

## Why Now

Three independent sources — user interviews, NPS feedback, and competitive research — triangulate on the same specific gap, retention is actively declining quarter over quarter, and no competitor currently owns this mechanic; waiting risks losing more users to the 3-month gap between first breakdown and real personalization ever arriving.

---
*Caveats: interview sample is n=3, NPS sample is n=10 — both directional, not statistically validated. Competitive white-space gaps are inferred from public feature research, not hands-on testing. See individual source docs for full detail.*
