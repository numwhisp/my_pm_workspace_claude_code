# Metric Diagnosis — 30-Day Retention

**Date:** 2026-07-16
**Source:** Same dataset as [metric-findings.md](metric-findings.md) — `Nudge Dataset.xlsx`, queried directly via SQLite. All numbers below are freshly queried, not restated from the earlier file.

## 1. Metric Tree — What Actually Moves 30-Day Retention

```
30-Day Retention Rate
│
├── Day-7 Retention (gate, not just a correlate)
│     Day-7=1 → 32.7% reach day-30. Day-7=0 → 19.7% reach day-30.
│     Whatever happens in week 1 sets the ceiling for day 30.
│
├── Session Frequency (sessions/user)
│     Tracks the cohort decline almost linearly: 5.74 → 5.08 → 4.48 → 3.69 (weeks 1–4),
│     alongside day-30 retention 32% → 25% → 25% → 22%.
│
├── Engagement with "actionable" screens specifically (not just any session)
│     savings_goal and weekly_summary screen views fell ~47–50% weeks 1→4,
│     vs. home screen falling only ~19% over the same period.
│     Users kept opening the app; they stopped using the parts of it that ask for action.
│
├── Week-1 Goal-Setting
│     Goal set within 7 days → 35% day-30 retention. No goal → ~22%. (~13pt gap,
│     holds even excluding the week-5 experiment cohort.)
│
├── Nudge Volume & Open/Act Rate
│     Roughly flat across cohorts (open% 12.1, 11.7, 14.3, 9.4; acted% 4.2, 4.5, 6.6, 3.2 —
│     no clean trend). A weak lever for explaining the *cohort-level* decline, though still
│     relevant at the individual level and to the NPS notification-fatigue risk noted elsewhere.
│
├── Acquisition Channel Mix
│     Doesn't shift cleanly with the cohort trend (paid % bounces 31→42→32→31) — not a driver
│     of the weeks 1–4 decline, but matters within-cohort (see Section 4).
│
└── Weekly Summary Exposure (week 5 only)
      Proximate driver of the week-5 lift: summary screen views jumped from 40 (week 4)
      to 142 (week 5); summary open rate climbed 28%→56% across 4 sends.
```

## 2. What Caused the Decline in Weeks 1–4 — Specifically

Three findings, all pulled from the same dataset, point to one consistent story:

1. **Session frequency eroded steadily, cohort over cohort.** Average sessions per user: 5.74 (week 1) → 5.08 → 4.48 → 3.69 (week 4) — a 36% drop, tracking the retention curve closely.
2. **The erosion was concentrated in the screens that require the user to act, not just look.** Screen-level view counts, week 1 → week 4: `savings_goal` −47% (74→39), the old `weekly_summary` screen −50% (80→40), `notifications` −42% (81→47) — versus `home` at only −19% (184→149). Users didn't stop opening the app; they stopped engaging with anything that asked something of them.
3. **This was not a nudge-volume or nudge-quality collapse.** Nudge send volume per user was flat (~3.4–3.6/user across all 4 weeks) and open/act rates showed no consistent downward trend. Ruling this out matters: the decline isn't "we spammed people less relevantly," it's that the app itself gave users progressively less to act on as their own account aged.

**Conclusion:** the decline is a quantitative confirmation of the qualitative research (Tom, Amara) — a "nothing to act on" problem, not an acquisition-quality or nudge-targeting problem. Acquisition channel and platform mix were checked and don't track the cohort trend closely enough to be the primary driver.

## 3. What the Week-5 Split Tells Us the Summary Actually Fixed

- **It reversed the specific decay identified above.** `weekly_summary` screen views jumped from 40 (week 4) to 142 (week 5) — more than triple — directly re-engaging the exact screen category that had been eroding fastest.
- **It moved the leading indicator, not just the lagging one.** Day-7 retention (the gate identified in the metric tree) jumped to 76% for treatment vs. 46% control — a 30-point gap that shows up almost immediately, not as a slow accumulation.
- **The open-rate curve compounds rather than fatigues** (28%→52%→52%→56% across 4 sends), meaning this isn't a novelty effect that will decay by send 5 or 6 — at least not yet.
- **Important nuance:** within the treatment group itself, simply opening the summary does *not* distinguish churners from retained users (96.9% of churners opened it at least once, vs. 94.4% of retained — nearly identical). The feature's effect is real at the population level (treatment vs. control), but *what specifically separates a treatment user who stays from one who still churns* isn't "did they open it." That's the question Section 4 digs into.

## 4. Four Ranked Hypotheses for Why Some Treatment Users Still Churned

*(32 of 50 treatment users churned by day 30, despite 97% of them opening the summary at least once.)*

### Rank 1 — Acquisition channel quality, independent of the feature

**Prediction:** Treatment users acquired organically retain at a meaningfully higher rate than treatment users acquired via paid or referral channels, because channel quality reflects underlying intent that the feature doesn't change.

**Confidence: 6/10** — Retention within treatment by channel: organic 43.3% (13/30), paid 28.6% (4/14), referral 16.7% (1/6) — a real, monotonic, 26-point spread. Scored a 6, not higher, because referral's n=6 is too small to trust on its own, and this may just be restating a pre-existing acquisition-quality effect rather than something the feature can influence.

**Would confirm it:** The same organic > paid > referral ordering, with a similar or larger gap, replicates in the next treatment cohort at higher n.
**Would rule it out:** The gap collapses to <5 points or reverses once sample size increases — indicating this cohort's spread was noise.

### Rank 2 — Platform-driven engagement gap (iOS vs. Android)

**Prediction:** Treatment users on iOS retain at a higher rate than treatment users on Android, because of a platform-specific difference in how reliably the summary notification reaches and re-engages the user.

**Confidence: 5/10** — Retention within treatment by platform: iOS 47.8% (11/23), Android 27.3% (6/22), web 20% (1/5) — a 20-point iOS-vs-Android gap. Scored a 5: the gap is real-sized, but web's n=5 is negligible, and this could as easily be confounded with device tier or channel as reflect an actual platform delivery problem.

**Would confirm it:** A notification-delivery audit shows Android open rates for the summary are mechanically lower than iOS's, and the ~20-point gap replicates next cohort.
**Would rule it out:** Android and iOS notification delivery/open rates are statistically equal, and the gap shrinks toward zero at higher n.

### Rank 3 — Goal-setting does *not* meaningfully explain who churns within treatment (testing the example hypothesis directly)

**Prediction:** Among treatment users who opened the summary, those without a savings goal set churn at a similar rate to those with one — meaning the goal-progress component is not the primary mechanism carrying the treatment's effect, contrary to the intuitive version of this hypothesis.

**Confidence: 4/10** — Among openers, has-goal retention is 38.1% (n=21) vs. no-goal 33.3% (n=27) — only a 4.8-point gap, much smaller than the 13-point gap seen population-wide in Section 1. Scored a 4 (not lower) because the gap is small but not zero, and n=21/27 is genuinely too small to confidently rule the effect out entirely — it may simply be underpowered here, not actually absent.

**Would confirm it:** A larger treatment cohort continues to show a has-goal/no-goal gap under ~5 points — well below the population-wide baseline — holding as n increases.
**Would rule it out:** A larger cohort shows the gap widen back toward or past the 13-point population-wide baseline — meaning this cohort's near-zero gap was just sampling noise.

### Rank 4 — Reactive over-engagement: churners act on the nudge *more*, not less (a genuine reversal worth flagging, not dismissing)

**Prediction:** Treatment users who eventually churn are *more* likely to act on the summary's nudge (e.g., "move to savings") than users who retain — consistent with financially-stressed users engaging reactively with a single feature without it changing their broader trajectory, rather than the feature failing to prompt action.

**Confidence: 3/10** — Observed: 62.5% of churners (20/32) acted on the summary at least once, vs. 50% of retained users (9/18) — the opposite direction of the intuitive hypothesis. Scored a 3, the lowest of the four, specifically because n=32/18 is small enough that this reversal could easily be noise — but it's flagged rather than discarded because a reversal signal is more interesting than a null one, and dismissing it without checking would risk misreading "acted_on" as a straightforwardly positive leading indicator when it may not be.

**Would confirm it:** A qualitative follow-up with churned users who acted on the nudge surfaces financial-stress language or one-off reactive framing, distinct from retained users' framing.
**Would rule it out:** A larger sample flips the direction — retained users showing a higher acted-on rate than churners, as the naive hypothesis would predict — indicating this cohort's reversal was noise.

## 5. Which Hypothesis to Test First

**Test Rank 2 (platform/Android engagement gap) first.**

Not because it's the highest-confidence finding — Rank 1 (acquisition channel) has a slightly larger and cleaner spread. The reason is actionability: acquisition channel quality is a growth-team lever the Engage squad doesn't control this sprint, whereas a platform-specific notification/engagement gap is something Raj's team can directly audit and fix (delivery reliability, notification permissions, rendering issues) within a sprint. It's also the hypothesis with the clearest mechanical next step — a notification-delivery audit — rather than requiring another full cohort-week of data collection before anything can be done. If confirmed, it's a fixable engineering problem with a direct line to retention; if ruled out, it's a fast, cheap check that clears the way to focus on Rank 1 or Rank 3 next.
