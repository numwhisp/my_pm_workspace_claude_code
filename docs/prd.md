# PRD — Nudge Personalized Weekly Summary

**Audience:** Raj (Eng), Lena (Design) | **Date:** 2026-07-16

## Problem Statement

30-day retention dropped from 44% to 37% over two quarters (docs/decision-brief.md). The dominant cause: users go passive after the initial spending breakdown because nothing afterward changes or asks anything of them — the single largest NPS theme, 5 of 10 responses (research/nps-analysis.md), echoed directly by Tom ("The app just showed me the same dashboard every time") and Amara ("nothing has changed since the first day") in research/interview-synthesis.md. The retention mechanism that does work — personalized pattern recognition — takes roughly 3 months to emerge (Priya: "it took about three months to get there"), but users churn well before that (Tom at week 5; Amara stalling at day 10). No competitor currently pushes a single ranked personalized insight + action, or treats a stated goal as a recurring touchpoint (research/competitive-matrix.md) — this is real market white space, not just an internal gap.

## User & Job to Be Done

A newly-connected user in their first weeks — before the 3-month pattern-recognition payoff — at risk of following Amara's trajectory (still checking at day 10, seeing nothing new) toward Tom's outcome (churned by week 5). Job to be done: understand where their money went this week and take one action.

## Goals

- Give users a weekly reason to return that is personal, timely, and actionable — directly targeting NPS Theme 1 (static/repetitive experience) and Theme 3 ("tell me what to do," research/nps-analysis.md).
- Treat a stated savings goal as a recurring, referenced touchpoint — closing the exact gap a user named: "I set a savings goal but Nudge has never once mentioned it since. It is like it forgot" (research/nps-analysis.md, #6).
- Sequence goal-continuity as the fastest validated win, per the approved recommendation (docs/decision-brief.md).

## Non-Goals

- Not attempting to accelerate or fake Priya's real ~3-month pattern-recognition insight. V1's insight is a current-week category breakdown + benchmark comparison, not personal-pattern discovery (research/interview-synthesis.md).
- Not resolving the Priya-vs-Tom engagement-mode tension in v1: "Priya describes a passive ritual... Tom wants the app to actively ask something of him. A single feature... may satisfy Priya's mode but not address Tom's" (research/interview-synthesis.md, Contradictions). Tracked as an open question below, not solved here.
- Not building debt-context-aware nudge logic in v1 unless data availability is confirmed (open question below, per stakeholders/lena.md).

## Success Metrics

Primary: 30-day retention rate — the feature's committed outcome measure (docs/hypothesis.md: "We believe that the personalized weekly money summary will deliver a reason for users to return and act... as measured by 30-day retention rate").

## User Stories

1. As a user with limited transaction history, I see a spending insight built from my actual current-week data (category + benchmark), not a claim of deep personalization the data can't support yet (research/interview-synthesis.md).
2. As a user without a savings goal, I get a first-class prompt to set one — not an empty or hidden state — because a previously-set goal being ignored is a named complaint (research/nps-analysis.md, #6).
3. As a user, I get one clear actionable nudge, not just data, because "waiting for the next step" is what both Tom and Amara described before disengaging (research/interview-synthesis.md).
4. As a user who opens off-cadence (not Monday), I see current, non-repeated content — never a stale repeat of an earlier insight.
5. As a user with no new transactions in a given week, I still receive real content (goal progress or a goal-creation prompt) — the app must never go silent, since silence recreates the exact "nothing changes" complaint this feature exists to fix (research/nps-analysis.md, Theme 1).

## Open Questions

- **Savings-goal data model does not yet exist** — Raj's own open item is "waiting on data model clarification for the savings goal field" (stakeholders/raj.md). Needs resolution before build.
- **Engagement-mode tension (Priya vs. Tom) is unresolved.** A single passive weekly format may not serve both a progress-motivated user and a user who wants to be actively pushed (research/interview-synthesis.md, Contradictions).
- **Debt-context awareness for the nudge is unconfirmed.** Lena's open item is to revisit the goal-progress design pending whether debt/balance data is actually available (stakeholders/lena.md) — a data-availability question, not yet a design answer.
- **Competitive white-space gaps are not independently confirmed.** research/competitive-reddit.md could not directly validate or contradict the two matrix gaps due to tooling limitations — recommend a manual spot-check before treating them as proven.
- **Bank-sync/notification reliability is competitors' top friction theme** (research/competitive-reddit.md) — worth confirming Nudge doesn't share this risk, independent of this feature.
- **Company-wide north-star metric is still unconfirmed** (docs/hypothesis.md) — unclear whether 30-day retention is what leadership ultimately judges this against beyond this initiative.
- **Whether the narrower goal-continuity-only scope would have sufficed** on its own vs. the fuller build now planned was never tested head-to-head (docs/decision-brief.md, docs/hypothesis.md).
