# Triad Working Session — Engage v2 Prototype Review

**Attendees:** Raj (Eng), Lena (Design), [PM] | **Duration:** 30 min

## Session Agenda

### 1. Context recap (3 min)
- Quick reminder of the approved direction from [decision-brief.md](decision-brief.md): ship the personalized weekly summary, goal-continuity first as the fastest win.
- This session is about moving from prototype → build scope, not re-debating the problem.

### 2. Live walkthrough of the prototype (8 min)
Show, don't just describe — click through `prototype/index.html` live:
- Email trigger (with the action-teaser fix from round 1 testing)
- In-app summary: spending insight + benchmark comparison
- Contextual nudge → gamified "move to savings" interaction
- Savings goal empty state → goal-creation flow

### 3. What testing surfaced — walk through the open issues (10 min)
Present these as decisions to make, not just FYI:

- **Benchmark framing tension:** peer comparison ("20% above similar users") motivated one tested persona (Priya) but read as being lectured/judged to another (Tom) — our highest churn-risk profile. *Question for the room: should this be optional, reframed, or shipped as-is for v1?*
- **Debt-context blind spot:** the "move $50 to savings" nudge ignores whether a user is carrying debt (Amara's reaction) — a generic suggestion undermined her trust. *Question for Raj: do we have debt/balance data from connected accounts already, or is this a v2 problem?*
- **Data-trust gap:** the goal-empty state can contradict a user who already has a goal in a different context (Priya's reaction) — a "the app forgot me" moment. *Question for Raj: is this a real state-sync bug risk, or purely a prototype artifact?*
- **Benchmark-cohort clarity:** "similar users" is undefined — testers want to know who they're being compared to. *Question for Lena: design direction for showing cohort context without adding clutter.*

### 4. Decisions to walk out with (7 min)
- [ ] v1 build scope: goal-continuity only, or goal-continuity + ranked insight together?
- [ ] How we handle the benchmark-framing tension for v1 (ship as-is / reframe copy / make optional)
- [ ] Whether debt-context awareness is in v1 scope or explicitly deferred
- [ ] Who owns the ranking-logic build (Raj's original open item from the initial scoping) and rough timeline
- [ ] Date for the next prototype iteration / next triad checkpoint

---

## Post-Session Alignment Doc Template

*(Fill this in during/immediately after the session — capture decisions in the room, not from memory afterward.)*

# Triad Alignment — Engage v2 [Date]

**Attendees:**
**Duration:**

## Decisions Made

1.
2.
3.

## Open Questions / Parking Lot

*(Real open items surfaced but not resolved this session — carry forward, don't let them silently drop.)*

-

## Action Items

| Owner | Action | Due |
|---|---|---|
| | | |
| | | |

## Scope Confirmed for Next Build

-

## Next Checkpoint

**Date:**
**Purpose:**
