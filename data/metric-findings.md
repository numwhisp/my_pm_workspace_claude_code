# Metric Findings — Weekly Summary Experiment (Cohort Week 5)

**Date:** 2026-07-16
**Source:** `Nudge Dataset.xlsx` (uploaded directly — the linked Google Sheet's other 4 tabs weren't reachable via public export; this file has all 5: Users, Sessions, Retention, Nudges, Weekly_Summary_Sends). Queried via SQLite loaded from the raw sheet data — no numbers below are estimated or carried over from the original prompt; all were independently derived and happen to match the story as given, which cross-validates the dataset.

## Q1 — 30-Day Retention by Cohort Week

```sql
SELECT cohort_week,
       COUNT(*) AS n_users,
       SUM(day_30) AS retained_day30,
       ROUND(100.0*SUM(day_30)/COUNT(*),1) AS day30_retention_pct
FROM nudge_retention
GROUP BY cohort_week
ORDER BY cohort_week;
```

| cohort_week | n_users | retained_day30 | day30_retention_pct |
|---|---|---|---|
| 1 | 100 | 32 | 32.0% |
| 2 | 100 | 25 | 25.0% |
| 3 | 100 | 25 | 25.0% |
| 4 | 100 | 22 | 22.0% |
| 5 | 100 | 29 | 29.0% (blended — see Q3 for the treatment/control split) |

**Plain English:** For each of the 500 users, count how many were still active on day 30, grouped by which weekly cohort they signed up in.

**What it means:** The pre-launch decline is real and steady — 32% → 25% → 25% → 22% across weeks 1–4, a 10-point erosion before the weekly summary ever shipped. This is the exact leak the whole Engage v2 initiative was built to address. Week 5's blended 29% sits *above* the week-4 low point, but that number mixes both variants together — it's not yet evidence the feature worked; Q3 unpacks that.

## Q2 — Does Setting a Savings Goal in Week 1 Predict Retention?

```sql
SELECT
  CASE WHEN u.goal_set_date IS NOT NULL
            AND (julianday(u.goal_set_date) - julianday(u.signup_date)) <= 7
       THEN 'goal_set_week1' ELSE 'no_goal_week1' END AS segment,
  COUNT(*) AS n_users,
  SUM(r.day_30) AS retained_day30,
  ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_retention_pct
FROM nudge_users u
JOIN nudge_retention r ON u.user_id = r.user_id
GROUP BY segment;
```

| segment | n_users | retained_day30 | day30_retention_pct |
|---|---|---|---|
| goal_set_week1 | 165 | 60 | 36.4% |
| no_goal_week1 | 335 | 73 | 21.8% |

Restricted to pre-launch cohorts only (weeks 1–4, to rule out the week-5 experiment as a confound):

| segment | n_users | retained_day30 | day30_retention_pct |
|---|---|---|---|
| goal_set_week1 | 132 | 46 | 34.8% |
| no_goal_week1 | 268 | 58 | 21.6% |

**Plain English:** Flag each user as having set a savings goal within 7 days of signing up or not, then compare their day-30 retention rates. Checked twice — once across all users, once excluding week-5 entirely — to make sure the week-5 experiment isn't skewing the comparison.

**What it means:** Users who set a goal in week 1 retain at roughly **35%, vs. ~22%** for those who don't — a consistent ~13-point gap, holding up even with the experiment cohort excluded. This is correlational, not causal (users motivated enough to set a goal in week 1 may simply be more engaged generally), but it independently corroborates the original hypothesis: goal-setting in week 1 is a strong retention signal, which is exactly what the whole Engage v2 feature was built around.

## Q3 — Week 5 Only: Treatment vs. Control, Day-7 and Day-30

```sql
SELECT u.variant,
       COUNT(*) AS n_users,
       ROUND(100.0*SUM(r.day_7)/COUNT(*),1) AS day7_retention_pct,
       ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_retention_pct
FROM nudge_users u
JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week = 5
GROUP BY u.variant;
```

| variant | n_users | day7_retention_pct | day30_retention_pct |
|---|---|---|---|
| control | 50 | 46.0% | 22.0% |
| summary_v1 | 50 | 76.0% | 36.0% |

**Plain English:** Within the week-5 cohort only, split users by which arm of the 50/50 experiment they were in, and compare day-7 and day-30 retention between the two groups.

**What it means:** This is the core result. Treatment users retained at **36% by day 30 vs. 22% for control** — a 14-point lift, and control's 22% is exactly in line with the pre-launch decline trendline from Q1 (i.e., control looks like "what would have happened anyway"). The day-7 gap is even starker — 76% vs. 46%, a 30-point difference — meaning the effect shows up almost immediately, not just as a slow burn. With n=50 per arm, this is a small sample for a single week of data; directionally strong, but worth continuing to monitor before treating the magnitude as fully stable.

## Q4 — Did the Weekly Summary Open Rate Improve Across the 4 Sends?

```sql
SELECT variant, week_number,
       COUNT(*) AS n_sends,
       SUM(opened) AS n_opened,
       ROUND(100.0*SUM(opened)/COUNT(*),1) AS open_rate_pct
FROM nudge_weekly_summary_sends
GROUP BY variant, week_number
ORDER BY variant, week_number;
```

| variant | week_number | n_sends | n_opened | open_rate_pct |
|---|---|---|---|---|
| control | 1 | 50 | 2 | 4.0% |
| control | 2 | 50 | 2 | 4.0% |
| control | 3 | 50 | 2 | 4.0% |
| control | 4 | 50 | 3 | 6.0% |
| summary_v1 | 1 | 50 | 14 | 28.0% |
| summary_v1 | 2 | 50 | 26 | 52.0% |
| summary_v1 | 3 | 50 | 26 | 52.0% |
| summary_v1 | 4 | 50 | 28 | 56.0% |

**Plain English:** For each of the 4 weekly sends, count what fraction of recipients opened it, split by variant.

**What it means:** Control's open rate is flat and low (~4–6%) across all 4 weeks — it never builds a habit. Treatment's open rate climbs sharply from 28% (send 1) to 52% (send 2) and holds around 52–56% through send 4 — a 7–14x gap over control that *compounds* rather than decaying, which is the opposite of the fatigue pattern you'd worry about with a repeated weekly touchpoint. This is the behavioral mechanism underneath the Q3 retention lift: users are actually building a habit of opening the thing, not just getting lucky once.

## Decision: Did the Weekly Summary Work?

**Yes, on every metric queried, in the same direction, at a scale that matters:**

- 14-point day-30 retention lift (36% vs. 22%) and 30-point day-7 lift (76% vs. 46%) in a clean 50/50 split.
- The mechanism is visible and consistent: open rate climbs and holds (not fatigues) across all 4 sends, control stays flat near-zero.
- It corroborates a pre-existing, independently-verified signal (Q2): goal-setting in week 1 already predicted better retention before this feature existed — the weekly summary's goal-progress component is very plausibly acting on the same lever.

**Caveat before scaling company-wide:** this is one week-5 cohort, n=50 per arm. Directionally strong and internally consistent across 4 independent queries, but a single cohort-week of data is not yet the same as a proven, durable effect — the recommendation is to scale with continued monitoring, not to treat this one week as the final word.
