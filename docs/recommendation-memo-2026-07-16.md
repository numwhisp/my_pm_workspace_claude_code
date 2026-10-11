# Results Memo — Weekly Summary (Engage v2), Week-5 Experiment

**To:** Marcus | **From:** Engage squad | **Date:** 2026-07-16 (revised)

> **Revision note (read this first):** This memo replaces the same-day version originally drafted after the pilot results came in. A statistical pressure-test run immediately afterward changed the recommendation materially — see below for exactly what changed and why. The original file is preserved, untouched, at `docs/recommendation-memo.md`.
>
> - **What the original memo said:** The pilot (+14pts day-30, +30pts day-7) was framed as a strong signal, and the ask was a light-touch extension — 2 more cohort-weeks (~200 users) — before committing to Q3 rollout.
> - **What changed it:** Running a significance test on the pilot showed the result is **not statistically significant** (p≈0.124; the 95% confidence interval runs from −3.6 to +31.6 points — it includes zero). A proper power calculation showed a real test needs **~1,160 users per arm (~2,320 total)** — roughly 23x the pilot's size — not 200 more users.
> - **Why it matters:** A 2-cohort extension would still leave us far short of a test that can actually distinguish "this works" from "we got a lucky cohort." Asking Marcus to approve an underpowered extension would just delay the same problem, not fix it.
> - **What this memo asks for instead:** approval to design and run the properly powered test, plus a scoping decision only Marcus/the team can make (see Ask) — not a quick top-up.

## Situation

We shipped the personalized weekly money summary to a 50/50 treatment/control split within cohort week 5, testing whether it recovers the 30-day retention decline (44%→37% company-wide over two quarters; 32%→22% across our own pre-launch cohort weeks 1–4).

## Evidence — and Its Real Limits

- **30-day retention: 36% treatment vs. 22% control (+14 points).** Control's 22% lands exactly on the pre-launch decline trendline, which is a good sign the comparison is fair — **but this result is not statistically significant** (p≈0.124, 95% CI: −3.6 to +31.6 points). At n=50/arm, we cannot yet rule out a true effect of zero.
- **Day-7 retention: 76% vs. 46% (+30 points).** The effect shows up immediately if real — but carries the same significance caveat as above.
- **Summary open rate climbed 28%→56% across 4 sends** while control stayed flat at 4–6% — this pattern (compounding, not fatiguing) is the most reassuring piece of evidence here, since it's a much larger relative gap and less sensitive to small-sample noise than the retention percentages.

## Recommendation

Design and run a properly powered follow-up test — **~1,160 users per variant (~2,320 total)** — before any rollout decision. Do not scale on the pilot alone.

## Ask

Two decisions needed from Marcus, not one:

1. **Approve the properly powered test design** (~2,320 users, 95% confidence, 80% power, 5-point minimum detectable effect).
2. **Decide the test's population scope** — this changes duration by more than 20 weeks and needs an explicit call: keep the pilot's new-signups-only design (≈27 weeks to run — does not fit an 8-week window) or broaden to the full active-user base (≈5 weeks — fits comfortably, but measures a related, not identical, question: ongoing engagement lift vs. new-user week-1 retention specifically).

## Risk If We Wait

Every week without a fix, retention keeps leaking on the same trendline that took us from 32% to 22% pre-launch — but scaling now on an unproven signal risks committing real roadmap and credibility to an effect that has a real statistical chance of being noise.

---

## Anticipated Hardest Questions from Marcus (updated with the real numbers)

*[Marcus]*

**1. n=50 per arm — is that actually enough to trust, or are we about to shape a quarter's roadmap off a sample the size of a coin flip?**
You were right to ask. It's not enough — the result isn't statistically significant (p≈0.124), and the confidence interval runs from a small loss to a big win. We need ~1,160 per arm to actually know, not 50.

**2. If I approve the full test, how long does that actually take, and does it fit inside a sensible window?**
Depends on one decision I need from you: if we keep the pilot's new-signups-only design, it's ~27 weeks — too long. If we broaden to the full active-user base, it's ~5 weeks — fits inside 8. I need you to pick which question we're actually answering before I can give you one number.

**3. If this holds at scale, what's the actual number I can take to the board — and when do I have a rollout date?**
Once the properly powered test completes (5–8 weeks, depending on your scope call above), I'll have a statistically defensible number, not a "positive signal." I'm asking you to set the population-scope decision now so the clock on that date can actually start.
