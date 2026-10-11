"""
Nudge Anomaly Diagnosis — chained off the Retention Pulse agent

Triggers only when agents/metric_pulse.py's headline retention move is >2pts
in either direction. Runs a 4-step gated loop: threshold check -> metric tree
decomposition -> hypothesis generation -> SQL + Slack post.

REAL-DATA CAVEAT: hypotheses and SQL templates below are built against the
actual schema in the Nudge dataset (nudge_users, nudge_sessions,
nudge_retention, nudge_nudges). The sample spec this was built from referenced
fields we don't actually have (a "nudge_notifications" table with a
"delivered" column, a "push opt-in rate") — those aren't real fields in this
dataset, so they are NOT used here. Every driver and SQL query below maps to
a column that actually exists. See agents/anomaly-diagnosis.md for the full
mapping and what would need to be added to track push-delivery specifically.

Usage:
    python anomaly_diagnosis.py "C:\\path\\to\\Nudge Dataset.xlsx" 2026-07-16
    python anomaly_diagnosis.py --simulate         # runs the synthetic 4pt-drop test case
"""

import sys
import pandas as pd
import sqlite3

MEANINGFUL_THRESHOLDS = {
    'day7_retention_pts': 1.5,
    'avg_sessions_pct': 10.0,      # relative % change
    'nudge_open_pts': 1.5,
    'goal_set_rate_pts': 3.0,
    'channel_retention_pts': 3.0,
    'platform_retention_pts': 3.0,
}


# ---------- Data loading (real mode) ----------

def load_conn(path):
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


def compute_real_drivers(conn, current_week, baseline_week):
    """Compute every driver in the metric tree for two cohort weeks. Returns
    a dict of driver -> (current_val, baseline_val, delta, unit)."""

    def day30(week):
        r = pd.read_sql(f"SELECT ROUND(100.0*SUM(day_30)/COUNT(*),1) v FROM nudge_retention WHERE cohort_week={week}", conn).iloc[0]['v']
        return float(r)

    def day7(week):
        r = pd.read_sql(f"SELECT ROUND(100.0*SUM(day_7)/COUNT(*),1) v FROM nudge_retention WHERE cohort_week={week}", conn).iloc[0]['v']
        return float(r)

    def avg_sessions(week):
        r = pd.read_sql(f"""
            SELECT COUNT(s.session_id)*1.0/COUNT(DISTINCT u.user_id) v
            FROM nudge_users u LEFT JOIN nudge_sessions s ON u.user_id=s.user_id
            WHERE u.cohort_week={week}""", conn).iloc[0]['v']
        return float(r)

    def nudge_open(week):
        r = pd.read_sql(f"""
            SELECT ROUND(100.0*SUM(n.opened)/COUNT(*),1) v
            FROM nudge_nudges n JOIN nudge_users u ON n.user_id=u.user_id
            WHERE u.cohort_week={week}""", conn).iloc[0]['v']
        return float(r)

    def goal_set_rate(week):
        r = pd.read_sql(f"""
            SELECT ROUND(100.0*SUM(CASE WHEN goal_set_date IS NOT NULL
                AND (julianday(goal_set_date)-julianday(signup_date))<=7 THEN 1 ELSE 0 END)/COUNT(*),1) v
            FROM nudge_users WHERE cohort_week={week}""", conn).iloc[0]['v']
        return float(r)

    def channel_retention(week, ch):
        r = pd.read_sql(f"""
            SELECT COUNT(*) n, SUM(r.day_30) ret
            FROM nudge_users u JOIN nudge_retention r ON u.user_id=r.user_id
            WHERE u.cohort_week={week} AND u.acquisition_channel='{ch}'""", conn).iloc[0]
        return round(100.0 * r['ret'] / r['n'], 1) if r['n'] else None

    def platform_retention(week, plat):
        r = pd.read_sql(f"""
            SELECT COUNT(*) n, SUM(r.day_30) ret
            FROM nudge_users u JOIN nudge_retention r ON u.user_id=r.user_id
            WHERE u.cohort_week={week} AND u.platform='{plat}'""", conn).iloc[0]
        return round(100.0 * r['ret'] / r['n'], 1) if r['n'] else None

    drivers = {}
    drivers['day7_retention'] = (day7(current_week), day7(baseline_week), 'pts')
    cur_s, base_s = avg_sessions(current_week), avg_sessions(baseline_week)
    drivers['avg_sessions'] = (cur_s, base_s, 'pct_relative')
    drivers['nudge_open_rate'] = (nudge_open(current_week), nudge_open(baseline_week), 'pts')
    drivers['goal_set_rate'] = (goal_set_rate(current_week), goal_set_rate(baseline_week), 'pts')
    for ch in ['organic', 'paid', 'referral']:
        drivers[f'{ch}_channel_retention'] = (channel_retention(current_week, ch), channel_retention(baseline_week, ch), 'pts')
    for plat in ['ios', 'android', 'web']:
        drivers[f'{plat}_platform_retention'] = (platform_retention(current_week, plat), platform_retention(baseline_week, plat), 'pts')

    return drivers


# ---------- Simulated mode (per spec: verify loop logic with a synthetic 4pt drop) ----------

def simulated_scenario():
    """SIMULATED INPUT — not real data. Exists to verify the loop's logic end
    to end, per the request. Mirrors the sample spec's scenario shape, adapted
    to fields that actually exist in this dataset (no 'push opt-in rate' or
    'nudge_notifications.delivered' field exists — substituted with
    nudge_open_rate, our real closest equivalent)."""
    return {
        'headline': {'current': 33.0, 'baseline': 37.0},
        'drivers': {
            'day7_retention': (54.0, 58.0, 'pts'),
            'avg_sessions': (3.2, 4.1, 'pct_relative'),
            'nudge_open_rate': (11.0, 14.0, 'pts'),
            'goal_set_rate': (30.0, 31.0, 'pts'),
            'paid_channel_retention': (29.0, 33.0, 'pts'),
            'organic_channel_retention': (36.0, 37.0, 'pts'),
            'referral_channel_retention': (35.0, 36.0, 'pts'),
            'android_platform_retention': (28.0, 34.0, 'pts'),
            'ios_platform_retention': (38.0, 39.0, 'pts'),
            'web_platform_retention': (30.0, 31.0, 'pts'),
        }
    }


# ---------- Step 1: threshold check ----------

def step1_threshold_check(headline_current, headline_baseline):
    delta = round(headline_current - headline_baseline, 1)
    passed = abs(delta) > 2.0
    return passed, delta


# ---------- Step 2: metric tree decomposition ----------

def step2_decomposition(drivers):
    moved = []
    for name, (cur, base, unit) in drivers.items():
        if cur is None or base is None:
            continue
        if unit == 'pts':
            delta = round(cur - base, 1)
            key = name.split('_')[0] + '_retention_pts' if 'retention' in name and ('channel' in name or 'platform' in name) else \
                  {'day7_retention': 'day7_retention_pts', 'nudge_open_rate': 'nudge_open_pts', 'goal_set_rate': 'goal_set_rate_pts'}.get(name, 'day7_retention_pts')
            threshold = MEANINGFUL_THRESHOLDS.get(key, 2.0)
            meaningful = abs(delta) >= threshold
            moved.append({'driver': name, 'current': cur, 'baseline': base, 'delta': delta, 'unit': 'pts', 'meaningful': meaningful})
        else:  # pct_relative
            delta_pct = round((cur - base) / base * 100, 1) if base else 0
            meaningful = abs(delta_pct) >= MEANINGFUL_THRESHOLDS['avg_sessions_pct']
            moved.append({'driver': name, 'current': cur, 'baseline': base, 'delta': delta_pct, 'unit': '%', 'meaningful': meaningful})

    meaningful_movers = [m for m in moved if m['meaningful']]
    passed = len(meaningful_movers) >= 2
    return passed, moved, meaningful_movers


# ---------- Step 3: hypothesis generation ----------

HYPOTHESIS_LIBRARY = {
    'avg_sessions': {
        'text': "Session frequency {direction} is driving the retention move",
        'sql_key': 'sessions',
    },
    'nudge_open_rate': {
        'text': "Nudge engagement {direction} (open rate) is driving the retention move",
        'sql_key': 'nudges',
    },
    'paid_channel_retention': {
        'text': "New user cohort quality shift in the paid channel is driving the retention move",
        'sql_key': 'channel',
    },
    'organic_channel_retention': {
        'text': "A shift in the organic channel is driving the retention move",
        'sql_key': 'channel',
    },
    'referral_channel_retention': {
        'text': "A shift in the referral channel is driving the retention move",
        'sql_key': 'channel',
    },
    'android_platform_retention': {
        'text': "A platform-specific effect on Android is driving the retention move",
        'sql_key': 'platform_android',
    },
    'ios_platform_retention': {
        'text': "A platform-specific effect on iOS is driving the retention move",
        'sql_key': 'platform_ios',
    },
    'goal_set_rate': {
        'text': "A {direction} in week-1 goal-setting rate is driving the retention move",
        'sql_key': 'goal',
    },
    'day7_retention': {
        'text': "An early (day-7) {direction} is driving the retention move — investigate week-1 experience directly",
        'sql_key': 'day7',
    },
}

SQL_TEMPLATES = {
    'sessions': """SELECT u.cohort_week, COUNT(s.session_id)*1.0/COUNT(DISTINCT u.user_id) AS avg_sessions_per_user
FROM nudge_users u LEFT JOIN nudge_sessions s ON u.user_id = s.user_id
WHERE u.cohort_week IN ({current_week}, {baseline_week})
GROUP BY u.cohort_week ORDER BY u.cohort_week;""",
    'nudges': """SELECT u.cohort_week, ROUND(100.0*SUM(n.opened)/COUNT(*),1) AS open_pct, ROUND(100.0*SUM(n.acted_on)/COUNT(*),1) AS acted_pct
FROM nudge_nudges n JOIN nudge_users u ON n.user_id = u.user_id
WHERE u.cohort_week IN ({current_week}, {baseline_week})
GROUP BY u.cohort_week ORDER BY u.cohort_week;""",
    'channel': """SELECT u.cohort_week, u.acquisition_channel, COUNT(*) n_users, ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_pct
FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week IN ({current_week}, {baseline_week})
GROUP BY u.cohort_week, u.acquisition_channel ORDER BY u.cohort_week, u.acquisition_channel;""",
    'platform_android': """SELECT u.cohort_week, u.platform, COUNT(*) n_users, ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_pct
FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week IN ({current_week}, {baseline_week}) AND u.platform='android'
GROUP BY u.cohort_week ORDER BY u.cohort_week;""",
    'platform_ios': """SELECT u.cohort_week, u.platform, COUNT(*) n_users, ROUND(100.0*SUM(r.day_30)/COUNT(*),1) AS day30_pct
FROM nudge_users u JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week IN ({current_week}, {baseline_week}) AND u.platform='ios'
GROUP BY u.cohort_week ORDER BY u.cohort_week;""",
    'goal': """SELECT cohort_week,
  ROUND(100.0*SUM(CASE WHEN goal_set_date IS NOT NULL AND (julianday(goal_set_date)-julianday(signup_date))<=7 THEN 1 ELSE 0 END)/COUNT(*),1) AS goal_week1_pct
FROM nudge_users WHERE cohort_week IN ({current_week}, {baseline_week})
GROUP BY cohort_week ORDER BY cohort_week;""",
    'day7': """SELECT cohort_week, COUNT(*) n, ROUND(100.0*SUM(day_7)/COUNT(*),1) AS day7_pct
FROM nudge_retention WHERE cohort_week IN ({current_week}, {baseline_week})
GROUP BY cohort_week ORDER BY cohort_week;""",
}


def confidence_score(mover, all_meaningful_movers):
    """Rule-based, transparent: base score from movement magnitude, bonus for
    co-movement with other meaningful drivers (a plausible shared cause)."""
    if mover['unit'] == '%':
        magnitude_score = min(abs(mover['delta']) / 5.0, 5.0)  # 5% relative move ~ 1 point, capped at 5
    else:
        magnitude_score = min(abs(mover['delta']), 5.0)  # 1pt move ~ 1 point, capped at 5

    co_movement_bonus = min((len(all_meaningful_movers) - 1) * 1.0, 4.0)
    score = round(min(magnitude_score + co_movement_bonus, 10.0), 1)
    return max(score, 1.0)


def step3_hypotheses(meaningful_movers):
    ranked = []
    for m in meaningful_movers:
        lib = HYPOTHESIS_LIBRARY.get(m['driver'])
        if not lib:
            continue
        score = confidence_score(m, meaningful_movers)
        direction = "drop" if m['delta'] < 0 else "rise"
        text = lib['text'].format(direction=direction) if '{direction}' in lib['text'] else lib['text']
        ranked.append({'driver': m['driver'], 'text': text, 'sql_key': lib['sql_key'], 'confidence': score, 'delta': m['delta'], 'unit': m['unit']})

    ranked.sort(key=lambda h: h['confidence'], reverse=True)
    top3 = ranked[:3]
    passed = bool(top3) and top3[0]['confidence'] > 6.0
    return passed, top3


# ---------- Step 4: SQL + Slack ----------

def step4_sql(top_hypothesis, current_week, baseline_week):
    template = SQL_TEMPLATES[top_hypothesis['sql_key']]
    return template.format(current_week=current_week, baseline_week=baseline_week)


# ---------- Slack formatting ----------

def format_slack_full(headline_delta, headline_current, headline_baseline, decomposition, top3, sql, timestamp_label):
    lines = []
    lines.append(f"\U0001F50D *Nudge Anomaly Detected — {timestamp_label}*")
    lines.append("")
    direction = "dropped" if headline_delta < 0 else "rose"
    lines.append(f"Trigger: 30-day retention {direction} {abs(headline_delta)}pts ({headline_baseline}% → {headline_current}%)")
    lines.append("")
    lines.append("Metric tree decomposition:")
    for m in decomposition:
        flag = "" if m['meaningful'] else "  (below meaningful-movement threshold)"
        arrow = "↓" if m['delta'] < 0 else ("↑" if m['delta'] > 0 else "→")
        unit_label = "pts" if m['unit'] == 'pts' else "%"
        lines.append(f"  {m['driver']:<28} {m['baseline']} → {m['current']}  ({arrow} {abs(m['delta'])}{unit_label}){flag}")
    lines.append("")
    lines.append("Top 3 hypotheses:")
    for i, h in enumerate(top3, 1):
        lines.append(f"  {i}. {h['text']} (confidence: {h['confidence']}/10)")
    lines.append("")
    lines.append(f"SQL to confirm hypothesis 1:")
    lines.append(f"  {sql}")
    lines.append("")
    lines.append("Run this query and reply with the output. I'll interpret.")
    return "\n".join(lines)


def format_slack_low_confidence(headline_delta, headline_current, headline_baseline, top3, timestamp_label):
    lines = []
    lines.append(f"⚠️ *Nudge Anomaly Detected — Low Confidence — {timestamp_label}*")
    lines.append("")
    direction = "dropped" if headline_delta < 0 else "rose"
    lines.append(f"Trigger: 30-day retention {direction} {abs(headline_delta)}pts ({headline_baseline}% → {headline_current}%)")
    lines.append("")
    if top3:
        lines.append(f"Best available hypothesis: {top3[0]['text']} — confidence only {top3[0]['confidence']}/10 (below the 6/10 bar to act on).")
    else:
        lines.append("No hypothesis cleared the confidence bar.")
    lines.append("")
    lines.append("Not writing SQL or naming a root cause I can't defend. Needs a human look before standup — likely more data or a wider time window than one week-over-week comparison can resolve.")
    return "\n".join(lines)


def format_log_no_trigger(headline_delta, headline_current, headline_baseline):
    return f"[log] Retention move {headline_delta:+.1f}pts ({headline_baseline}% → {headline_current}%) — within ±2pt threshold, no anomaly diagnosis triggered."


def format_log_inconclusive(headline_delta, decomposition):
    n_meaningful = len([m for m in decomposition if m['meaningful']])
    return (f"[log] Retention moved {headline_delta:+.1f}pts (above threshold) but only {n_meaningful} driver(s) showed "
            f"meaningful movement. Flagged inconclusive — not generating hypotheses from a single signal. Stopped.")


# ---------- Orchestration ----------

def run_loop(headline_current, headline_baseline, drivers, current_week, baseline_week, timestamp_label):
    passed1, delta = step1_threshold_check(headline_current, headline_baseline)
    if not passed1:
        print(format_log_no_trigger(delta, headline_current, headline_baseline))
        return

    passed2, decomposition, meaningful_movers = step2_decomposition(drivers)
    if not passed2:
        print(format_log_inconclusive(delta, decomposition))
        return

    passed3, top3 = step3_hypotheses(meaningful_movers)
    if not passed3:
        print(format_slack_low_confidence(delta, headline_current, headline_baseline, top3, timestamp_label))
        return

    sql = step4_sql(top3[0], current_week, baseline_week)
    print(format_slack_full(delta, headline_current, headline_baseline, decomposition, top3, sql, timestamp_label))


def main():
    if '--simulate' in sys.argv:
        print("===== SIMULATED TEST — synthetic input, not real data =====\n")
        scenario = simulated_scenario()
        run_loop(scenario['headline']['current'], scenario['headline']['baseline'],
                  scenario['drivers'], current_week='SIM_CURRENT', baseline_week='SIM_BASELINE',
                  timestamp_label='Tue May 13, 8:47am (simulated)')
        return

    path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None
    date_label = sys.argv[2] if len(sys.argv) > 2 else '[date]'
    if not path:
        print("Usage: python anomaly_diagnosis.py <dataset_path> [date_label]  OR  --simulate")
        return

    conn = load_conn(path)
    weeks = pd.read_sql("SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week", conn)['cohort_week'].tolist()
    current_week, baseline_week = weeks[-1], weeks[-2]

    headline_current = pd.read_sql(f"SELECT ROUND(100.0*SUM(day_30)/COUNT(*),1) v FROM nudge_retention WHERE cohort_week={current_week}", conn).iloc[0]['v']
    headline_baseline = pd.read_sql(f"SELECT ROUND(100.0*SUM(day_30)/COUNT(*),1) v FROM nudge_retention WHERE cohort_week={baseline_week}", conn).iloc[0]['v']

    drivers = compute_real_drivers(conn, current_week, baseline_week)
    print("===== REAL DATA RUN =====\n")
    run_loop(float(headline_current), float(headline_baseline), drivers, current_week, baseline_week, date_label)


if __name__ == '__main__':
    main()
