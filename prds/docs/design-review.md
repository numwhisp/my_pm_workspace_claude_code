# Design Review — Weekly Summary Prototype (Prep for Lena)

**Date:** 2026-07-16
**Method:** Reviewed [prototype/index.html](../prototype/index.html) against [research/interview-synthesis.md](../research/interview-synthesis.md), then roleplayed Lena (per [stakeholders/lena.md](../stakeholders/lena.md)) raising her 3 hardest questions.

## What the Prototype Addresses Well (cited)

1. **"Give me something to act on."** The nudge buttons directly answer Tom: *"I kept waiting for it to give me something to act on and it never really did"* and Amara: *"I have been waiting for Nudge to tell me the next step."*
2. **"Nothing ever changes."** Content is generated from the current week's real data, answering Tom: *"The app just showed me the same dashboard every time"* and Amara: *"I check it occasionally but nothing has changed since the first day."*
3. **Not overclaiming personalization depth.** The insight is a 2-week category breakdown + benchmark, not framed as deep pattern-recognition — deliberately not faking Priya's real timeline: *"it took about three months to get there."*

## What's Not Yet Addressed (cited)

1. **Priya's actual retention driver is still missing.** Her hook was personal-pattern discovery — *"it started surfacing patterns I had not consciously registered."* The current benchmark is a peer comparison, not a discovery about the user's own recurring behavior, and there's no visible design path toward that as data accumulates.
2. **Tom's "asking something of me" feeling is untested over multiple weeks.** One nudge in one week's screen isn't evidence of sustained accountability — we don't yet know if this fades back into the "static" complaint after a few cycles.
3. **The doc's own flagged contradiction is still open:** *"Priya describes a passive ritual... Tom wants the app to actively ask something of him... A single feature may satisfy Priya's mode but not address Tom's."* One static format doesn't resolve this by itself.

## Lena's 3 Hardest Questions — and the Answers That Closed Them

**1. What does the user do after they read this?**
"Move to savings" is a real transfer (existing Chase connection, confirmed with Raj), with a second CTA converting it into standing auto-save — so the mechanism doesn't depend on the user reopening the app weekly to keep accumulating progress. Return-open rate and action-taken rate are already committed metrics (docs/hypothesis.md, docs/spec-readiness.md) — if this is just a one-time dopamine hit, weeks 3–4 will show it, and that's the trigger to revisit, not a guess made now.

**2. Why would someone open this on a Tuesday, not Monday?**
By design, the insight describes "this week," not "the moment the email sent" — still accurate mid-week. The in-app screen always reflects current state; the email is only the trigger. Off-cadence opens with nothing new fall to the zero/low-activity waterfall (goal progress → goal-creation prompt) already scoped with Raj — never a stale repeat.

**3. Who is this actually designed for?**
V1 is built for Priya's progress-motivated mode — a named decision, not a blind spot. The Tom-vs-Priya tension (confirmed again in research/persona-roleplay-walkthrough.md — the same benchmark mechanic that motivates Priya reads as being lectured to Tom) is already a tracked open item. The scoped fix: a tone-variant system — same insight/nudge, comparative framing for progress-motivated users, non-comparative framing for users showing skepticism signals. Scoped next step for Lena to own, not an unresolved question blocking this review.

## Single Highest-Impact Change for Week-1 Retention

**Guarantee every single open — not just Monday's — shows a real, current, actionable next step, never a repeat of what the user already saw.** This is the direct implementation of interview-synthesis.md's own stated conclusion: the job isn't to accelerate Priya's real 3-month payoff, it's to manufacture a credible next step that bridges day 1 to month 3 — and the doc names Amara specifically as "the person this needs to reach before she becomes Tom." The zero/low-activity fallback waterfall (insight → goal progress → goal-creation prompt) is the mechanism that makes this true on *every* visit, not just the one week the design currently shows — making it the highest-leverage piece relative to the research's own stated priority.

## Product Decision vs. What Lena Should Own

**Product decisions (PM/Marcus-level):**
- Which metric defines success — 30-day retention + the 5 proxy metrics (open rate, click-through, action-taken, goal-created, return-open).
- Which persona mode gets built first — Priya's progress-motivated mode for v1, Tom's skeptical mode as a named next step, not a v1 blocker.
- Scope sequencing — SavingsGoal schema ticket before the feature ticket; multi-goal unlock explicitly cut to Phase 2.
- Whether the peer-benchmark mechanic is core to v1 at all — a business bet on this specific mechanic, not a design choice.

**Lena's decisions:**
- The visual/interaction design of the fallback states (goal-prompt, low-activity state).
- How "similar users" cohort context is displayed without adding clutter.
- Designing the tone-variant system for skeptical/guilt-prone users (the actual execution of the Tom-mode fix).
- Information hierarchy across the insight, nudge, and goal cards.
- The goal-creation flow and empty-state design.
