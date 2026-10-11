# Prototype — Personalized Weekly Money Summary (Engage v2)

**Open [`index.html`](index.html) in a browser to try it.** It's a self-contained, interactive prototype — no build step, no server required.

## Flow

1. **Email trigger** — a redesigned version of Nudge's existing weekly summary email (today's version has a 22% open rate). Click "Open your full summary" to continue.
2. **In-app weekly summary** — three sections:
   - **Top spending insight** — category breakdown of the user's actual data, compared against a benchmark average. Click "See what made up dining" to expand the underlying transactions.
   - **Contextual nudge** — "Move $50 to savings" (triggers a gamified success state + confetti + an auto-save follow-up CTA) or "Review dining budget" (expands the breakdown).
   - **Savings goal** — this user has no goal set, so it's a prompt to create one, not an empty state. Creating a goal shows a live progress ring.

Use the "1. Email trigger / 2. In-app summary" toggle at the top to jump between views directly.

## PM Brief

**User:** 28-year-old who connected their Chase account 2 weeks ago and has not opened the app since — a near-churn reactivation target.

**Job to be done:** Understand where their money went this week and take one action.

**Feature:** Personalized weekly money summary — top spending insight, one contextual nudge, savings goal progress.

**Constraint:** Use data Nudge already has — no new integrations.

## Key Decisions Made During the Interview

1. **Top spending insight** is a category breakdown of the user's actual 2 weeks of data plus a benchmark comparison (e.g., "$340 on dining — 20% above average") — not framed as deep pattern-recognition, since research shows that takes ~3 months of data this user doesn't have yet.
2. **Savings goal section** shows a prompt to set a goal (not hidden, not an empty placeholder) — this user has none set. Directly targets the NPS finding that a goal, once set, was never referenced again.
3. **Contextual nudge is actionable**, not just informational — buttons trigger gamified, positive-reinforcement feedback ("Way to go! Saving mode activated") plus a next-step CTA, responding to the NPS theme that users want to be told "what to do."
4. **Scope includes the re-engagement trigger** — the email that pulls the dormant user back in — not just the in-app screen.
5. **Fidelity:** a real interactive, stateful prototype, not a static mockup.
6. **Visual style:** professional, fintech-credible, but playful/colorful/warm.

## Traceability to Research

- Static/repetitive experience (dominant NPS complaint, 5/10 mentions) → addressed by a screen built from the user's own current-week data.
- 3-month time-to-value gap (research/interview-synthesis.md) → addressed by not overclaiming insight depth for a 2-week-old connection.
- "Tell me what to do" / goal neglect (research/nps-analysis.md) → addressed by an actionable nudge button and a first-class goal-setting prompt.
- Competitive white space (research/competitive-matrix.md) — no competitor pushes a single ranked insight + action, or treats a goal as a recurring touchpoint — this prototype is a direct attempt to own that gap.

Full PM brief also saved separately at [`../docs/pm-brief.md`](../docs/pm-brief.md).
