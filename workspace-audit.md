# Workspace Audit — Nudge Engage v2

**Date:** 2026-07-16
**Scope:** Full folder review (30 files across prds/, research/, docs/, prototype/, meeting-notes/, stakeholders/, data/, skills/, plus root).

## 1. What's Missing (would make Claude more useful next session)

- **CLAUDE.md's folder structure was badly out of date.** It listed `/roadmap` and `/retention-analysis`, neither of which was ever created, and didn't mention `docs/`, `prototype/`, `stakeholders/`, `data/`, or `skills/` — five folders now in active, heavy use. A session starting cold would have no idea these exist. **Fixed in this update.**
- **CLAUDE.md's "Current initiative" section was stuck at the very beginning of the project** — "not yet decided, Marcus wants problem alignment before solutioning." In reality: discovery is complete, a prototype has been built and tested across three personas, a pilot shipped and was analyzed, the pilot was found *not* statistically significant, and a properly powered follow-up test is now being scoped. Anyone reading CLAUDE.md alone would be weeks behind actual state. **Fixed in this update.**
- **No "canonical vs. superseded" tracking.** There are now two pairs of dated/original files — `docs/recommendation-memo.md` (superseded) vs. `docs/recommendation-memo-2026-07-16.md` (current), and `research/competitive-matrix.md` (original) vs. `research/competitive-matrix-2026-07-16.md` (current, with Mint added). This already caused a real problem this session — a task was scoped to read the original memo, which would have put a statistically-unsupported claim in front of Marcus if it hadn't been caught. Nothing in the workspace flags the old file as superseded to someone opening it cold. **Partially fixed** — CLAUDE.md now points to the current versions, but the old files themselves still carry no in-file pointer forward. Recommend adding a one-line "superseded by X" note at the top of a file whenever a dated replacement is created going forward.
- **No single "current state" summary.** `change_log.md` has the full history, but it's a chronological log, not a status snapshot — getting oriented requires reading a long file top to bottom. CLAUDE.md now carries a short current-state section so a new session doesn't have to reconstruct it.
- **The skills/ exemption to the editing rule was never written down.** Mid-session, `skills/weekly-status.md` was treated as edited-in-place (like CLAUDE.md) rather than versioned like a team-facing doc — a reasonable call, but it was never actually added to the editing rule itself, so nothing would tell a future session that convention exists. **Fixed in this update.**

## 2. Reorganization Suggestions (not made automatically — these are recommendations)

- **`/prds` holds only the original dated skeleton PRD.** The actual completed, pressure-tested PRD (`docs/prd.md`) lives in `docs/` instead. Worth deciding explicitly: either route future PRDs to `/prds` for consistency, or accept `docs/` as the real home for finished deliverables and stop treating `/prds` as a distinct category. Not changed — this is your call, not an obvious fix.
- **`/roadmap` and `/retention-analysis` were declared in CLAUDE.md but never created or used.** `data/` has effectively become what `/retention-analysis` was meant to be (metric findings, diagnosis, experiment design). Recommend dropping both unused folder names from CLAUDE.md rather than creating empty folders to match a plan that changed — done in this update, but flagging so you know it was a deliberate removal, not an oversight.
- **`docs/` is now the largest, most heterogeneous folder** — 15 files spanning strategy docs, review docs, QA checklists, and presentation materials. Not urgent, but if it keeps growing, subfolders (e.g., `docs/reviews/`, `docs/presentations/`) would reduce scroll-and-scan friction. Flagging to watch, not acting on it now.

## 3. CLAUDE.md Update

CLAUDE.md has been rewritten in place (per its own standing exemption from the never-overwrite rule) to reflect:
- The actual current folder structure (all 8 active folders).
- The actual current project state (discovery → prototype → pilot → analysis → properly-powered test being scoped), replacing the stale "not yet decided" framing.
- A new "Current Canonical Documents" section pointing to the up-to-date version of anything that has a superseded predecessor.
- The skills/ exemption formally added to the editing rule.
- The data source section updated to reflect that a real dataset (`Nudge Dataset.xlsx`) has now been used for analysis, while the standing warehouse/dashboard question remains open.
