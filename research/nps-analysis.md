# NPS Feedback Analysis — Findings for Marcus

**Source:** 10 raw NPS free-text responses, provided 2026-07-16.
**Caveat:** n=10, qualitative groupings done manually — themes are interpretive clusters, not statistically derived. Item numbers below refer to the original list order.

## Themes Mentioned More Than Once (ranked by frequency)

| Rank | Theme | Frequency | Items |
|---|---|---|---|
| 1 | Static / repetitive experience — nothing new, no reason to return | 5 | #1, #2, #5, #7, #10 |
| 2 | Feels generic / not personalized — doesn't track or reference the user's own data over time | 2 | #6, #9 |
| 3 | Wants proactive, prescriptive guidance — "coach, not tracker" | 2 | #3, #8 |

**Theme 1 detail:** Users describe the home feed and overall app as unchanging after the first session or week ("same things every time," "nothing made me want to come back," "app itself has not given me a reason to open it"). This is the single largest cluster — half of all feedback touches it.

**Theme 2 detail:** Users feel Nudge doesn't build on what it already knows about them — a stated savings goal was never referenced again (#6), and one user described the content as "generic money tips I could find anywhere" despite having connected real account data (#9).

**Theme 3 detail:** Users want Nudge to tell them what to do next, not just reflect data back at them (#3), and want it to surface things they don't already know rather than confirm what they suspect (#8).

## Praise vs. Complaints

**Praise (explicit positive sentiment):**
- Initial experience/spending breakdown is genuinely valuable: "The first week was genuinely eye-opening" (#2).
- Core concept is well-liked: "Love the concept" (#5).
- The weekly email (not the app) is effective at sustaining engagement: "The weekly email is the only thing keeping me engaged" (#10) — praise for the email channel specifically, implicit criticism of the app.

**Complaints:** all 10 items contain a complaint; only #2 and #5 pair a complaint with explicit praise. No item is purely negative-with-no-redeeming-comment except #4, #6, #7, #9.

## Top 3 Actionable Issues

1. **Static, unchanging app experience (Theme 1, 5/10 mentions).** Highest-frequency issue and the one most users independently converge on. This directly supports the Engage v2 hypothesis already documented in [strategy.md](../strategy.md) — the personalized weekly summary concept under exploration is a direct response to this.

2. **Irrelevant nudges caused a user to disable notifications entirely (#4).** Only 1 mention, but flagged as top-3 despite frequency because of severity: this user didn't just ignore a nudge, they turned off the entire notification channel — permanently foreclosing a re-engagement lever for that user. Worth investigating whether nudge relevance/targeting is a broader silent problem (users may opt out quietly without leaving NPS feedback about it).

3. **No continuity or personalization on stated user intent (Theme 2, specifically #6).** A user set a savings goal and Nudge never referenced it again. This is a narrow, concretely scoped fix (surface goal progress/status) compared to the broader personalization ask in #9, and would directly address part of the Engage v2 "savings goal progress" concept already in strategy.md.

## Open Question

Themes 1 and 3 overlap conceptually — both point at the app being reactive/descriptive rather than proactive/prescriptive. Worth deciding whether Engage v2 treats these as one problem (a proactive, changing weekly insight) or two (content freshness vs. actionability of that content) when scoping the solution.
