# Leadership Deck — Engage v2 Quarterly Review

**Audience:** Marcus + leadership review | **Date:** 2026-07-16
**Note on sourcing:** Built from CLAUDE.md, docs/decision-brief.md, data/metric-findings.md, research/interview-synthesis.md, stakeholders/marcus.md — plus data/experiment-design.md for the significance finding, since presenting the pilot without it would misrepresent the result to leadership. No numbers invented; see [presentation-notes.md](presentation-notes.md) for full sourcing per slide.

---

## Slide 1 — The Problem

**One number:** 30-day retention dropped from 44% to 37% over the last two quarters. *(CLAUDE.md)*

**One insight:** Users go passive after the initial spending breakdown because the app gives them nothing afterward that's personal, timely, or actionable. *(CLAUDE.md, "Current initiative: Engage v2")*

---

## Slide 2 — Why Now

**What changed:** Completed discovery — user interviews and competitive research independently converged on the same specific gap. No competitor currently owns a single ranked personalized insight tied to a savings goal. *(docs/decision-brief.md, "Why Now" / Key Finding 4)*

**What we learned:** The real, durable personalization payoff takes roughly 3 months to build — but users churn well before that. Waiting costs real users on the same decline trendline already observed. *(research/interview-synthesis.md; docs/decision-brief.md)*

---

## Slide 3 — The Proposal

**What it is:** A personalized weekly money summary — current-week spending insight with a benchmark comparison, one actionable nudge, and savings-goal progress — delivered via an email trigger into an in-app screen. Sequenced with goal-continuity first as the fastest validated win. *(docs/decision-brief.md, Recommended Action)*

**What it isn't:** Not a claim of deep, 3-month-style personalization for new users. Not a company-wide rollout decision today — this review asks for approval to run a properly powered test, not to scale immediately.

---

## Slide 4 — Evidence

- **Prototype:** built and tested across 3 personas grounded in the actual interview subjects.
- **User quotes** *(research/interview-synthesis.md)*:
  - Tom: "The app just showed me the same dashboard every time." / "I switched to YNAB because... it feels like it is asking something of me."
  - Amara: "I have been waiting for Nudge to tell me the next step." / "nothing has changed since the first day."
  - Priya: "it started surfacing patterns I had not consciously registered... I feel like Nudge actually knows my financial habits now."
- **Pilot data** *(data/metric-findings.md)*: 36% vs. 22% day-30 retention (+14pts); 76% vs. 46% day-7 (+30pts); summary open rate climbed 28%→56% across 4 sends vs. flat 4–6% control.
- **The caveat that shapes the ask:** this result is **not yet statistically significant** at n=50/arm (p≈0.124; 95% CI −3.6 to +31.6 points). Promising, not yet proof. *(data/experiment-design.md)*

---

## Slide 5 — The Plan

**Milestones:**
1. Finalize test design — requires a scope decision (see Risks).
2. Run a properly powered test: ~1,160 users per variant (~2,320 total).
3. 5–8 week test window, depending on scope.
4. Go/no-go decision on company-wide rollout.

**Risks:**
- The test's population scope (new-signups-only vs. broader active-user base) swings duration by ~22 weeks and is undecided.
- Ranking logic for insight selection still needs to be built. *(CLAUDE.md, "Open decision")*
- Company-wide north-star metric is still unconfirmed — not yet certain 30-day retention is what leadership ultimately judges this against beyond this initiative. *(CLAUDE.md)*

---

## Slide 6 — The Ask

Approve running the properly powered test — not a company-wide rollout — and make the population-scope call needed before scheduling can start.
