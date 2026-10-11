"""
Nudge Weekly Insight Report — Friday 4pm

Pulls from 3 real sources:
  1. Retention metrics (data/ folder, via the actual dataset)
  2. Sprint completions this week (change_log.md)
  3. Top NPS theme this week (research/nps-analysis.md)

Outputs a 3-2-1 report: Done this week (3) / Changed this week (2) / Watch next week (1).
Saves to reports/YYYY-MM-DD.md and prints the Slack-ready 3-2-1 summary.

DATA CAVEAT: same as agents/monday-retention.md and agents/metric-pulse.md —
no live retention pipeline exists yet, dataset provenance is unconfirmed, and
"week over week" here means the two most recent cohort weeks in the dataset,
not a live rolling calculation. change_log.md parsing takes the most recent
dated section as "this week" — in a workspace with real weekly cadence, this
would filter to entries from the last 7 days instead.

Usage:
    python weekly_insight.py "C:\\path\\to\\Nudge Dataset.xlsx"
"""

import sys
import re
import os
from datetime import date
import pandas as pd
import sqlite3

DEFAULT_DATA_PATH = r"C:\Users\Banke\Downloads\Nudge Dataset.xlsx"
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGE_LOG_PATH = os.path.join(WORKSPACE_ROOT, "change_log.md")
NPS_PATH = os.path.join(WORKSPACE_ROOT, "research", "nps-analysis.md")
CLAUDE_MD_PATH = os.path.join(WORKSPACE_ROOT, "CLAUDE.md")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")


# ---------- Source 1: Retention metrics ----------

def get_retention_signals(data_path):
    users = pd.read_excel(data_path, sheet_name='Users')
    retention = pd.read_excel(data_path, sheet_name='Retention')
    conn = sqlite3.connect(':memory:')
    users.to_sql('nudge_users', conn, index=False)
    retention.to_sql('nudge_retention', conn, index=False)

    weeks = pd.read_sql("SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week", conn)['cohort_week'].tolist()
    current_week, baseline_week = weeks[-1], weeks[-2]

    def retention_for(week, channel=None):
        where = f"AND u.acquisition_channel = '{channel}'" if channel else ""
        row = pd.read_sql(f"""
            SELECT COUNT(*) n, SUM(r.day_30) retained
            FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
            WHERE u.cohort_week = {week} {where}
        """, conn).iloc[0]
        return round(100.0 * row['retained'] / row['n'], 1) if row['n'] else None

    headline_cur = retention_for(current_week)
    headline_base = retention_for(baseline_week)
    headline_delta = round(headline_cur - headline_base, 1)

    channel_deltas = {}
    for ch in ['organic', 'paid', 'referral']:
        cur = retention_for(current_week, ch)
        base = retention_for(baseline_week, ch)
        if cur is not None and base is not None:
            channel_deltas[ch] = round(cur - base, 1)

    biggest_channel = max(channel_deltas, key=lambda k: abs(channel_deltas[k])) if channel_deltas else None

    signals = []
    signals.append(f"30-day retention: {headline_cur}% ({'+' if headline_delta>=0 else ''}{headline_delta}pts vs cohort week {baseline_week}, week {current_week} data)")
    if biggest_channel:
        d = channel_deltas[biggest_channel]
        signals.append(f"{biggest_channel.capitalize()} channel retention moved most: {'+' if d>=0 else ''}{d}pts week-over-week")
    return signals, (current_week, baseline_week)


# ---------- Source 2: Sprint completions from change_log.md ----------

def get_done_this_week(n=3):
    with open(CHANGE_LOG_PATH, encoding='utf-8') as f:
        text = f.read()

    # Most recent dated section = "this week" stand-in (see caveat above)
    sections = re.split(r'\n## ', text)
    last_section = sections[-1]
    lines = [l.strip('- ').strip() for l in last_section.split('\n')
             if l.strip().startswith('- ') and not l.strip().startswith('- **Open items carried forward')]

    # Most recent N bullets (last in the section = most recently logged),
    # trimmed to a clean length without cutting mid-sentence.
    def clean_trim(line, max_len=160):
        if len(line) <= max_len:
            return line
        cut = line[:max_len].rsplit(' ', 1)[0]
        return cut.rstrip('.,;:—-') + '...'

    recent = lines[-n:] if len(lines) >= n else lines
    return [clean_trim(l) for l in recent]


# ---------- Source 3: Top NPS theme from research/nps-analysis.md ----------

def get_top_nps_theme():
    with open(NPS_PATH, encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'\|\s*1\s*\|(.+?)\|(.+?)\|(.+?)\|', text)
    if not match:
        return "No NPS theme table found this week."
    theme, freq = match.group(1).strip(), match.group(2).strip()
    return f"Top NPS theme: {theme} ({freq} mentions)"


# ---------- Source 4 (for "watch next week"): CLAUDE.md open decisions ----------

def get_top_watch_item():
    with open(CLAUDE_MD_PATH, encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'\*\*Open decisions blocking next steps:\*\*\n((?:- .+\n?)+)', text)
    if not match:
        return "No open decisions found in CLAUDE.md."
    first_item = match.group(1).split('\n')[0].strip('- ').strip()
    return first_item


# ---------- Assemble ----------

def build_report(done, changed, watch, nps_line, report_date):
    lines = []
    lines.append(f"# Nudge Weekly Insight — {report_date.strftime('%a %b %-d' if os.name != 'nt' else '%a %b %#d')}")
    lines.append("")
    lines.append("## Done this week")
    for d in done:
        lines.append(f"- {d}")
    lines.append("")
    lines.append("## Changed this week")
    for c in changed:
        lines.append(f"- {c}")
    lines.append(f"- {nps_line}")
    lines.append("")
    lines.append("## Watch next week")
    lines.append(f"- {watch}")
    return "\n".join(lines)


def build_slack_summary(done, changed, watch, report_date, saved_path):
    lines = []
    lines.append(f"\U0001F4CB *Nudge Weekly Insight — {report_date.strftime('%a %b %-d' if os.name != 'nt' else '%a %b %#d')}*")
    lines.append("")
    lines.append("Done this week:")
    for d in done:
        lines.append(f"• {d}")
    lines.append("")
    lines.append("Changed this week:")
    for c in changed:
        lines.append(f"• {c}")
    lines.append("")
    lines.append("Watch next week:")
    lines.append(f"• {watch}")
    lines.append("")
    lines.append(f"Saved to {saved_path}")
    return "\n".join(lines)


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_PATH
    # NOTE: the real system clock and this workspace's fictional "current date"
    # (2026-07-16, used throughout change_log.md etc.) don't match. Pass a date
    # explicitly as the 2nd argument (YYYY-MM-DD) to keep report dates consistent
    # with the rest of the workspace; defaults to the real system date otherwise.
    if len(sys.argv) > 2:
        report_date = date.fromisoformat(sys.argv[2])
    else:
        report_date = date.today()

    retention_signals, weeks = get_retention_signals(data_path)
    done = get_done_this_week(n=3)
    nps_line = get_top_nps_theme()
    watch = get_top_watch_item()

    report_md = build_report(done, retention_signals, watch, nps_line, report_date)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"{report_date.isoformat()}.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    rel_path = f"reports/{report_date.isoformat()}.md"
    slack_summary = build_slack_summary(done, retention_signals, watch, report_date, rel_path)

    print("----- FULL REPORT (saved to file) -----")
    print(report_md)
    print("\n----- SLACK 3-2-1 SUMMARY -----")
    print(slack_summary)


if __name__ == '__main__':
    main()
