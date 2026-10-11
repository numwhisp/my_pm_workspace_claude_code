"""
Nudge Retention Pulse — Monday Morning Slack Digest

Monitors 30-day retention week-over-week, broken down by acquisition channel
(organic, paid, referral), and flags an alert if the headline metric moves
2+ percentage points.

DATA CAVEAT (see agents/metric-pulse.md for full detail): there is no live,
standing retention pipeline (CLAUDE.md, "Data source ground truth" — still
open, provenance of the underlying dataset also unconfirmed). This script
reads a manually-provided export and treats consecutive cohort_week values as
"week over week" — it is not a live daily/rolling retention feed. Swap
DATA_PATH and the query layer for a real source before trusting this for a
real rollout decision.

Usage:
    python metric_pulse.py "C:\\path\\to\\Nudge Dataset.xlsx"
"""

import sys
import pandas as pd
import sqlite3

DEFAULT_DATA_PATH = r"C:\Users\Banke\Downloads\Nudge Dataset.xlsx"
ALERT_THRESHOLD_PTS = 2.0
CHANNELS = ["organic", "paid", "referral"]


def load_data(path):
    users = pd.read_excel(path, sheet_name='Users')
    retention = pd.read_excel(path, sheet_name='Retention')

    conn = sqlite3.connect(':memory:')
    users.to_sql('nudge_users', conn, index=False)
    retention.to_sql('nudge_retention', conn, index=False)
    return conn


def retention_for_week(conn, week, channel=None):
    where_channel = f"AND u.acquisition_channel = '{channel}'" if channel else ""
    q = f"""
        SELECT COUNT(*) AS n, SUM(r.day_30) AS retained
        FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
        WHERE u.cohort_week = {week} {where_channel}
    """
    row = pd.read_sql(q, conn).iloc[0]
    if row['n'] == 0:
        return None
    return round(100.0 * row['retained'] / row['n'], 1)


def arrow(delta):
    if delta is None:
        return "→", "flat"
    if delta > 0.05:
        return "↑", f"{abs(round(delta,1))}pt{'s' if abs(round(delta,1))!=1 else ''}"
    if delta < -0.05:
        return "↓", f"{abs(round(delta,1))}pt{'s' if abs(round(delta,1))!=1 else ''}"
    return "→", "flat"


def build_digest(current_week, baseline_week, headline_cur, headline_base, channel_results, digest_date_label):
    headline_delta = round(headline_cur - headline_base, 1)
    arr, mag = arrow(headline_delta)
    alert = " ⚠️ ALERT" if abs(headline_delta) >= ALERT_THRESHOLD_PTS else ""

    lines = []
    lines.append(f"\U0001F4CA *Nudge Retention Pulse — {digest_date_label}*")
    lines.append("")
    lines.append(f"30-day retention: *{headline_cur}%* ({arr} {mag} vs last week){alert}")
    lines.append("")
    lines.append("By channel:")

    # find the channel with the biggest absolute move for "watch this" + top signal
    biggest = None
    for ch, (cur, base) in channel_results.items():
        if cur is None or base is None:
            continue
        d = round(cur - base, 1)
        if biggest is None or abs(d) > abs(biggest[1]):
            biggest = (ch, d)

    for ch in CHANNELS:
        cur, base = channel_results.get(ch, (None, None))
        if cur is None:
            lines.append(f"  {ch.capitalize():<9} no data this week")
            continue
        d = round(cur - (base if base is not None else cur), 1)
        a, m = arrow(d if base is not None else None)
        watch = "  ← watch this" if biggest and ch == biggest[0] and abs(d) >= ALERT_THRESHOLD_PTS else ""
        lines.append(f"  {ch.capitalize():<9} {cur}% ({a} {m}){watch}")

    lines.append("")
    if biggest and abs(biggest[1]) >= ALERT_THRESHOLD_PTS:
        direction = "dropping" if biggest[1] < 0 else "rising"
        lines.append(f"Top signal: {biggest[0].capitalize()} channel {direction} the fastest "
                      f"({biggest[1]:+.1f}pts). Check what changed there last week.")
    else:
        lines.append("Top signal: no channel moved enough to flag this week.")

    lines.append("")
    lines.append("Next: run anomaly diagnosis? Reply YES to trigger.")

    return "\n".join(lines)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_PATH
    conn = load_data(path)

    weeks = pd.read_sql("SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week", conn)['cohort_week'].tolist()
    if len(weeks) < 2:
        print("Not enough cohort weeks to compare week-over-week.")
        return

    current_week, baseline_week = weeks[-1], weeks[-2]

    headline_cur = retention_for_week(conn, current_week)
    headline_base = retention_for_week(conn, baseline_week)

    channel_results = {}
    for ch in CHANNELS:
        cur = retention_for_week(conn, current_week, ch)
        base = retention_for_week(conn, baseline_week, ch)
        channel_results[ch] = (cur, base)

    digest = build_digest(current_week, baseline_week, headline_cur, headline_base,
                           channel_results, digest_date_label="[Monday date]")
    print("----- SLACK DIGEST OUTPUT -----")
    print(digest)
    print("-------------------------------")


if __name__ == '__main__':
    main()
