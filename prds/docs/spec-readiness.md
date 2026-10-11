# Spec Readiness Review — Weekly Summary Feature (Raj Walkthrough)

**Date:** 2026-07-16
**Method:** Roleplayed Raj (per [stakeholders/raj.md](../stakeholders/raj.md)) reviewing [docs/decision-brief.md](decision-brief.md), [docs/pm-brief.md](pm-brief.md), and related docs, then working through open questions in dialogue with the PM.

## 1. Spec Readiness Summary

**What was solid:**
- The problem framing and "why now" (decision-brief.md) — Raj didn't push back on this at all; it wasn't in question.
- The feature's core shape (insight + nudge + goal progress) and the deliberate choice not to overclaim personalization depth for low-data users.
- The constraint that this uses existing data only, no new integrations — confirmed accurate: the Chase account connection already exists from a prior session, so transactions/transfers occurring in real time don't violate that constraint.

**What needed work (all resolved during this session):**
1. **Undisclosed scope: schema design was bundled into the feature ticket.** The savings-goal data model doesn't exist yet, and the original spec treated "build the feature" as one ticket without flagging that a new, hard-to-reverse data model decision was embedded inside it.
2. **Ambiguous mechanism: does "move to savings" move real money?** The prototype's gamified copy ("saving mode activated") implied a real transfer without the spec confirming it. Resolved: yes, real transfer, using the existing Chase connection — no new integration required.
3. **Scope creep via example, not by decision:** the multi-goal "unlock" mechanic was included as an illustrative example in conversation but functions as a whole new engagement-gating feature (streak/return-visit logic, unlock state) — not a detail of the goal model. Resolved: explicitly cut to phase 2.
4. **Missing edge case: zero-transaction weeks.** The spec didn't define what happens for a user with no activity — ironic, since the brief's own example user is exactly this case. Resolved: a content-priority fallback waterfall (insight → goal progress → goal-creation prompt → never fabricate).
5. **Missing success definition:** no specific metric or measurement location was tied to shipping the feature. Resolved: 30-day retention is the committed outcome metric (hypothesis.md), with five proxy metrics for real-time build signal; the warehouse/instrumentation location remains a genuinely open item (per CLAUDE.md), now named rather than hidden.

**Bottom line:** the spec was directionally right but under-scoped — it read as one feature when it was actually two tickets plus a deferred phase-2 idea, with two real edge cases (no-data state, success measurement) left undefined.

## 2. Rewritten Sections

### Original (implied) scope statement
> Build the personalized weekly money summary: top spending insight, one contextual nudge, savings goal progress.

### Rewritten
> **Ticket 1 — SavingsGoal data model.** Design and migrate a new `SavingsGoal` model (fields: name, target amount, target date [optional], current progress). Progress is derived automatically from transactions/transfers tagged to the goal — not manually entered. One goal per user for v1 (multi-goal unlock is explicitly out of scope — see Phase 2 below). Include a rollback plan before this ships, given schema changes are hard to reverse once real user data exists in them.
>
> **Ticket 2 — Weekly summary feature.** Build the Monday digest (email trigger → in-app summary) covering: top spending insight (category breakdown + benchmark comparison, not deep pattern-recognition, for users with limited history), one contextual nudge with a real "move to savings" action (uses the existing Chase connection — no new integration), and savings-goal progress (or a goal-creation prompt if none exists). Depends on Ticket 1 shipping first.
>
> **Explicitly out of scope (Phase 2):** multi-goal unlock mechanic gated by engagement/return-visit frequency. This requires new streak/unlock-state tracking and is a distinct feature, not a detail of the goal model.

### Original (missing) edge case
> *(not previously specified)*

### Rewritten
> **Zero-activity state:** if a user has no new transactions in the weekly window, the summary must still send — do not silently skip, as that reinforces the "static/nothing changes" complaint that's the dominant reason this feature exists. Content priority waterfall:
> 1. Real top-spending insight, if transaction volume supports it.
> 2. Savings-goal progress, if a goal exists.
> 3. Goal-creation prompt, if no goal exists.
> 4. Never fabricate an insight from insufficient data.

### Original (missing) success metric
> *(not previously specified)*

### Rewritten
> **Success metric:** committed outcome metric is 30-day retention rate (per docs/hypothesis.md). Since this is a lagging, cohort-level signal, ship-time proxy metrics are: digest open rate, click-through to in-app summary, % of users taking the one contextual action, goal-creation rate among previously goal-less users, and week-over-week return-open rate. **Open item, named not hidden:** the data warehouse/instrumentation location for these metrics is still TBD per CLAUDE.md — needs a named owner and a deadline before this ships, not after.

## 3. Async Slack Message — Scope Confirmation Before Kickoff

> Hey Raj — writing up the ticket split we landed on, want your quick confirm before I finalize for kickoff:
>
> 1. Two tickets: **SavingsGoal schema + migration** (with rollback plan) and **the weekly summary feature** (depends on #1).
> 2. Multi-goal unlock mechanic → cut to Phase 2, not in this sprint.
> 3. Zero-transaction weeks handled via fallback waterfall: insight → goal progress → goal-creation prompt, never fabricated.
> 4. Metrics: 30-day retention is the outcome measure; 5 proxy metrics (open rate, click-through, action-taken, goal-created, return-open) instrumented at ship. Warehouse location is still TBD — need to name an owner + deadline for that before we call this sprint-ready.
>
> If this matches what you need to commit to sprint scope, thumbs-up and I'll finalize the tickets. If not, flag what's missing and I'll fix it before kickoff, not during.
