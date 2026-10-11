# PM Brief — Engage v2 Prototype: Personalized Weekly Money Summary

**Date:** 2026-07-16
**Builds on:** [docs/decision-brief.md](decision-brief.md) (Marcus-approved direction)

## User

28-year-old who connected their Chase account 2 weeks ago and has not opened the app since — a near-churn reactivation target, consistent with the interview finding that users disengage well before the ~3-month mark where Nudge's real personalization value emerges (research/interview-synthesis.md).

## Job to Be Done

Understand where their money went this week, and take one action.

## Feature

Personalized weekly money summary:
- Top spending insight
- One contextual nudge
- Savings goal progress

## Constraint

Use data Nudge already has — no new integrations.

## Key Decisions (from interview)

1. **Top spending insight** is built from the user's actual 2 weeks of category-level spending, plus a comparison against a benchmark/average (e.g., "$340 on dining — 20% above average"). Deliberately not framed as deep pattern-recognition — research shows that takes ~3 months of data, which this user doesn't have yet. Avoids over-promising personalization depth the data can't support this early.
2. **Savings goal progress:** this user has no goal set, so the section becomes a prompt to set one rather than an empty state or being omitted — directly targets the NPS finding that a goal, once set, was never referenced again (research/nps-analysis.md, item #6) by making goal-setting a first-class, visible moment.
3. **Contextual nudge** is an actionable button (e.g., "Move $50 to savings," "Review dining budget") that triggers gamified, positive-reinforcement feedback on click, plus a suggested next-action CTA to sustain momentum. Directly responds to the NPS theme that users want to be told "what to do," not just shown data (research/nps-analysis.md, Theme 3).
4. **Scope includes the re-engagement trigger**, not just the in-app screen: a redesigned version of Nudge's existing weekly summary email (22% open rate today) leads into the in-app summary. Two connected views.
5. **Fidelity:** a real interactive, stateful prototype — not a static mockup.
6. **Visual style:** professional, fintech-credible, but playful/colorful/warm — full creative latitude on execution.

## Traceability to Research

- Static/repetitive experience (dominant complaint, 5/10 NPS mentions) → addressed by a screen that changes weekly based on the user's own data.
- 3-month time-to-value gap → addressed by not overclaiming insight depth for a 2-week-old connection.
- "Tell me what to do" / goal neglect → addressed by an actionable nudge button and a first-class goal-setting prompt.
- Competitive white space (no competitor pushes a single ranked insight + action, or treats a goal as a recurring touchpoint) → this prototype is a direct attempt to own that gap.
