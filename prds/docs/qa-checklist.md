# QA Checklist — Weekly Summary Feature

**Date:** 2026-07-16
**Sources:** [docs/spec-readiness.md](spec-readiness.md), [prototype/README.md](../prototype/README.md), [prototype/index.html](../prototype/index.html)

## 1. Edge Case List

### Empty states
- No transactions this week — **not implemented in the current prototype file at all** (see QA item #7 below); this is the exact scenario the acceptance criteria in spec-readiness.md require.
- No savings goal set — implemented (goal-empty prompt state exists).
- No sessions/opens in the past week (user skipped last week's summary entirely) — not modeled; unclear if next open shows "this week" only or acknowledges the gap.
- User never interacts with any nudge, across multiple weeks — no escalation/fallback content strategy defined.
- Account connected but zero activity for an extended period (fully dormant account, not just a quiet week) — not distinguished from a normal zero-transaction week.

### Edge data conditions
- Single transaction all week — insight logic (as implemented) assumes multiple categories; behavior with one transaction is untested.
- Duplicate/renamed categories mid-week (e.g., a category split or merchant re-categorized) — not addressed.
- Zero or negative amounts (refunds, reversals, chargebacks) — the comparison-bar math in the prototype is hardcoded to one specific pair of numbers ($340/$283); a zero or negative "you spent" value would need explicit handling (divide-by-zero or negative-width risk) that isn't proven out anywhere in this file.
- Savings goal target amount of $0 or negative — the goal-amount `<input type="number">` has no `min` attribute; nothing prevents a $0 or negative target, which breaks any progress-percent calculation (division by zero).
- Very large amounts (formatting/truncation, e.g., a $34,000 miscategorized transaction) — no currency formatting logic visible to evaluate.

### Multi-account scenarios
- Multiple banks connected — not represented anywhere in the prototype; no account-selector or aggregation UI exists to evaluate.
- Conflicting/duplicate data across linked accounts (e.g., a shared card double-counted) — not addressed. Notably, this is the exact class of bug flagged for competitors PocketGuard and Monarch in research/competitive-reddit.md — worth explicitly testing for, not assuming away.
- One linked account disconnected or needing re-auth mid-week — no degraded/error state modeled.

### Permission states
- Push notifications disabled — not modeled at all; the prototype only covers email + in-app. Directly relevant given NPS research: a user previously disabled notifications entirely after one irrelevant nudge (research/nps-analysis.md, item #4) — a real precedent for this exact channel.
- Background refresh disabled (stale data risk) — no "last synced" or staleness indicator anywhere in the UI.
- Email unsubscribed/marked as spam — no unsubscribe link visible in the email markup. This is a deliverability/compliance gap, not just a UX edge case, before this goes to a real inbox.

## 2. PM QA Pass — Screen by Screen

| # | What was verified | Result | Blocking? |
|---|---|---|---|
| 1 | Email subject line matches hero content (dining callout) | **Pass** | No |
| 2 | Email CTA correctly opens the in-app summary | **Pass** (verified in-browser) | No |
| 3 | Insight math is internally consistent — dining transaction breakdown ($28+$64+$97+$81+$70) sums exactly to the stated $340 | **Pass** | No |
| 4 | Comparison bars render and reflect the stated "~20% above average" ($340 vs. $283) | **Pass** (verified in-browser) | No |
| 5 | "Move $50 to savings" triggers success state, confetti, and reveals the auto-save follow-up CTA | **Pass** (verified in-browser) | No |
| 6 | Goal-creation flow (empty state → form → created state with interpolated goal name) | **Pass** (verified in-browser) | No |
| 7 | Zero-transaction / low-activity fallback state renders (insight → goal progress → goal-creation prompt) | **Fail** — no code path for this exists anywhere in the file; only the hardcoded $340-dining scenario is implemented | **Yes — blocking.** This was explicit acceptance criteria agreed with Raj (spec-readiness.md, item #4). Shipping without it contradicts sign-off criteria already committed to. |
| 8 | Bottom nav tabs (Spending / Goals / You) are functional | **Fail / cannot determine scope** — no click handlers exist on these elements; only "Home" is visually active | **Not blocking if confirmed out of prototype scope** — but must be explicitly confirmed as intentional before sign-off, not assumed. |
| 9 | Goal-amount input has basic validation (no $0/negative targets) | **Fail** — `<input type="number">` has no `min` attribute | **Not blocking for this prototype stage**, but must be a named requirement in the real ticket — flagged here so it doesn't quietly get missed later. |
| 10 | Form accessibility — inputs have associated `<label>` elements | **Fail** — goal-name and goal-amount inputs use `placeholder` only, no `<label>` | **Not blocking for prototype sign-off**, but should be tracked as a production requirement. |

**Summary: 6 pass, 1 hard blocker (#7), 3 non-blocking known issues to carry forward (#8, #9, #10).**

## 3. Draft PR Comment for Raj

> Hey — this is looking solid, the insight math and the savings/goal flows all check out end to end. One thing I want to flag before we merge, though: I don't see a rendering path anywhere for the zero-transaction / low-activity week — right now it looks like every state assumes the $340-dining scenario. Is that fallback (insight → goal progress → goal-creation prompt) coming in a follow-up PR, or did we land on handling it a different way? Want to make sure it doesn't quietly fall out of scope, since it was one of the four things we agreed sign-off required.
