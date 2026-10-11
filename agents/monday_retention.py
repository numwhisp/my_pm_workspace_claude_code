"""
Monday Retention Digest — Nudge Engage v2

Compares this week's cohort against last week's on 3 metrics (30-day retention,
avg sessions/user, nudge open rate), identifies the biggest mover, and prints a
plain-English Slack digest.

CURRENT LIMITATION (read before relying on this): there is no live, standing
data source wired up yet (see CLAUDE.md, "Data source ground truth" — still
TBD). This script currently reads a manually-provided export file. For a real
Monday-morning cron/n8n job, DATA_PATH below must be replaced with a query
against wherever retention data actually ends up living (warehouse, dashboard
API, etc.) once that's decided — that is a real blocker to automating this,
not a detail to skip past.

Usage (manual run):
    python monday_retention.py "C:\\path\\to\\Nudge Dataset.xlsx"

If no path is given, defaults to the path used during development.
"""

import sys
import pandas as pd
import sqlite3

DEFAULT_DATA_PATH = r"C:\Users\Banke\Downloads\Nudge Dataset.xlsx"


def load_data(path):
    users = pd.read_excel(path, sheet_name='Users')
    sessions = pd.read_excel(path, sheet_name='Sessions')
    retention = pd.read_excel(path, sheet_name='Retention')
    nudges = pd.read_excel(path, sheet_name='Nudges')

    conn = sqlite3.connect(':memory:')
    users.to_sql('nudge_users', conn, index=False)
    sessions.to_sql('nudge_sessions', conn, index=False)
    retention.to_sql('nudge_retention', conn, index=False)
    nudges.to_sql('nudge_nudges', conn, index=False)
    return conn


def week_metrics(conn, week):
    """Compute the 3 tracked metrics for a single cohort_week."""
    retention_pct = pd.read_sql(f"""
        SELECT ROUND(100.0*SUM(day_30)/COUNT(*), 1) AS pct
        FROM nudge_retention WHERE cohort_week = {week}
    """, conn).iloc[0]['pct']

    avg_sessions = pd.read_sql(f"""
        SELECT COUNT(s.session_id)*1.0/COUNT(DISTINCT u.user_id) AS avg_sessions
        FROM nudge_users u LEFT JOIN nudge_sessions s ON u.user_id = s.user_id
        WHERE u.cohort_week = {week}
    """, conn).iloc[0]['avg_sessions']

    # "Push notification open rate" is approximated as pooled nudge open rate —
    # this dataset does not distinguish delivery channel (push vs. in-app vs. email)
    # per nudge. Flagged explicitly rather than silently assumed.
    nudge_open_pct = pd.read_sql(f"""
        SELECT ROUND(100.0*SUM(n.opened)/COUNT(*), 1) AS pct
        FROM nudge_nudges n JOIN nudge_users u ON n.user_id = u.user_id
        WHERE u.cohort_week = {week}
    """, conn).iloc[0]['pct']

    return {
        'retention_pct': round(float(retention_pct), 1),
        'avg_sessions': round(float(avg_sessions), 2),
        'nudge_open_pct': round(float(nudge_open_pct), 1),
    }


def biggest_mover(current, baseline):
    """Return (metric_name, current_val, baseline_val, delta) for the metric
    with the largest absolute point/unit change."""
    deltas = {
        'retention_pct': current['retention_pct'] - baseline['retention_pct'],
        'avg_sessions': current['avg_sessions'] - baseline['avg_sessions'],
        'nudge_open_pct': current['nudge_open_pct'] - baseline['nudge_open_pct'],
    }
    # Normalize sessions delta to a comparable percent-change scale so it isn't
    # dwarfed by point-based metrics — this is a rule-based heuristic, not a
    # statistical test.
    normalized = {
        'retention_pct': abs(deltas['retention_pct']),
        'avg_sessions': abs(deltas['avg_sessions']) / baseline['avg_sessions'] * 100 if baseline['avg_sessions'] else 0,
        'nudge_open_pct': abs(deltas['nudge_open_pct']),
    }
    metric = max(normalized, key=normalized.get)
    return metric, current[metric], baseline[metric], deltas[metric]


def suggested_action(metric, delta):
    """Simple rule-based suggestion — transparent, not a black box."""
    if metric == 'retention_pct':
        if delta < 0:
            return ("Retention is the biggest mover and it dropped. Start by checking "
                    "session frequency and engagement with actionable screens (savings goal, "
                    "weekly summary) for this week's cohort — that's the pattern that explained "
                    "the original decline (see data/metric-diagnosis.md).")
        return "Retention improved and is the biggest mover — check what changed this week and consider whether it's replicable."
    if metric == 'avg_sessions':
        if delta < 0:
            return "Session frequency dropped the most this week — review whether anything (a bug, a missed nudge, a platform issue) reduced return visits."
        return "Session frequency is up the most this week — worth understanding why, so it can be sustained."
    if metric == 'nudge_open_pct':
        if delta < 0:
            return ("Nudge open rate dropped the most — check relevance/targeting. A prior NPS finding "
                    "showed a user disabled notifications entirely after one irrelevant nudge "
                    "(research/nps-analysis.md, #4) — a silent-opt-out risk worth checking for.")
        return "Nudge open rate is up the most — worth identifying which nudge type is driving it."
    return "No clear standout mover this week — monitor as usual."


METRIC_LABELS = {
    'retention_pct': '30-day retention',
    'avg_sessions': 'avg sessions/user',
    'nudge_open_pct': 'nudge open rate',
}


def build_digest(current_week, baseline_week, current, baseline, mover):
    metric, cur_val, base_val, delta = mover
    label = METRIC_LABELS[metric]
    sign = '+' if delta >= 0 else ''
    unit = 'pts' if metric != 'avg_sessions' else ''

    headline = (f"📊 *30-Day Retention:* {current['retention_pct']}% "
                f"(week {current_week}) vs {baseline['retention_pct']}% (week {baseline_week}) "
                f"— {'+' if current['retention_pct']-baseline['retention_pct']>=0 else ''}"
                f"{round(current['retention_pct']-baseline['retention_pct'],1)}pts")

    signal = (f"👀 *Signal to watch:* {label} moved the most this week — "
              f"{cur_val}{unit} vs {base_val}{unit} ({sign}{round(delta,2)}{unit}).")

    action = f"✅ *Suggested action:* {suggested_action(metric, delta)}"

    return "\n\n".join([headline, signal, action])


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_PATH
    conn = load_data(path)

    weeks = pd.read_sql("SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week", conn)['cohort_week'].tolist()
    if len(weeks) < 2:
        print("Not enough cohort weeks in the data to compare week-over-week.")
        return

    current_week, baseline_week = weeks[-1], weeks[-2]
    current = week_metrics(conn, current_week)
    baseline = week_metrics(conn, baseline_week)
    mover = biggest_mover(current, baseline)

    digest = build_digest(current_week, baseline_week, current, baseline, mover)
    print("----- SLACK DIGEST OUTPUT -----")
    print(digest)
    print("-------------------------------")


if __name__ == '__main__':
    main()
