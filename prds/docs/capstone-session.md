# Capstone Session — Nudge Engage v2 Workspace Review

**Date:** 2026-07-16

## 1. What's Been Built

A full product-development lifecycle for one feature (personalized weekly money summary):

- **Discovery:** interview synthesis (n=3), NPS analysis (n=10), competitive matrix (5 competitors + Mint), competitive Reddit sentiment (low-confidence).
- **Strategy:** strategy.md, decision-brief.md, a learning synthesis + formal hypothesis statement.
- **Design & prototype:** a working interactive prototype, tested across 3 personas via roleplay, 2 usability rounds, a design review.
- **Spec & validation:** a pressure-tested PRD, a spec-readiness review, a QA checklist, a 3-reviewer objection log.
- **Real data analysis:** SQL-verified retention findings, a metric diagnosis, a statistical pressure-test (significance/power/sample-size/duration).
- **Leadership communication:** a recommendation memo (revised once), a 6-slide deck with speaker notes.
- **Team process:** 3 stakeholder profiles, a triad-session agenda/template, a Slack invite.
- **Reusable tooling:** 4 skill templates, 1 agent spec + working script.
- **Governance:** CLAUDE.md, a workspace audit, a continuous change log.

## 2. Confidence Per Artifact

| Artifact | Confidence | What gets it to 95% |
|---|---|---|
| Interview synthesis, NPS analysis | ~70%, capped by sample size | Larger samples (10–15+ interviews, hundreds of NPS responses) |
| Competitive matrix | ~85% on features, lower on gap claims | Hands-on trial of each competitor's product |
| Competitive Reddit sentiment | ~30–40% | Real Reddit API/scraping access |
| Prototype code | ~100% | N/A — verified working in-browser |
| Persona roleplay / usability | ~50–55% | Real usability sessions (plan now drafted: `research/usability-test-plan.md`) |
| PRD, objection log | ~70% | Real sign-off from the actual Raj/Lena/Marcus/users, not roleplay |
| Metric findings, diagnosis, experiment design | Math ~95%+, data provenance **unconfirmed** | Confirm whether `Nudge Dataset.xlsx` is real or illustrative (flagged in CLAUDE.md, not yet resolved) |
| Recommendation memo, presentation | ~85%, inherits the above | Same as above, plus real Marcus feedback |
| Skills / agent tooling | ~90% mechanics, low deployment-readiness | Live data source + Slack webhook, a few real weeks of runtime |
| CLAUDE.md / workspace-audit.md | ~95% | Keep current as things change |

## 3. Fixes Identified, and What Happened

**Fix 1 — Stakeholder profiles unverified.** Drafted: `stakeholders/profile-confirmation-request.md` — a ready-to-send message per person (Raj, Lena, Marcus) asking them to confirm or correct their working profile. Not yet sent; responses will need to be folded back into `stakeholders/*.md`.

**Fix 2 — Dataset provenance unconfirmed.** Flagged explicitly in `CLAUDE.md`'s "Data source ground truth" section as an unresolved, decision-blocking gap. **Declined to fabricate numbers to fill the gap** — asked to do so directly, and refused, because inventing data and presenting it as findings would violate this workspace's own core rule ("never invent numbers or facts") and would retroactively undermine every "verified against real data" claim made this session. The responsible fix is the flag itself, not a plausible-looking substitute.

**Fix 3 — No real usability testing.** Drafted: `research/usability-test-plan.md` — recruitment criteria matching the three original interview segments, and a session script reusing the same four questions from the persona roleplay, so real results are directly comparable to the simulated ones. Not yet run.

## 4. Prompt to Recreate This Workspace for a Different Product

Copy-paste this into a fresh session to start over with a new product:

---

> I want to set up a PM workspace for [PRODUCT NAME] using Claude Code. Before creating any files, interview me one question at a time until you have 95% confidence you understand what I need — don't batch questions, and don't proceed until I approve a summary of what you've learned. Cover at minimum: what the product is and who it's for, my role and team (who's on my triad/pod, who I report to), what problem or initiative I'm working on right now, what data sources exist (and explicitly ask if none exist yet — don't assume), and how I want documents organized.
>
> Once I approve, set up a CLAUDE.md with these hard rules baked in, non-negotiably:
> - Never invent numbers, facts, or data — every figure needs a cited source or must be explicitly flagged as TBD. If asked to fabricate data to fill a gap, refuse and explain why, don't comply.
> - Explicitly highlight assumptions — never let them blend into stated fact.
> - Accuracy and precision over polish, always.
> - Never overwrite an existing doc when asked to edit or rewrite one — save a new file with the date appended instead, except for CLAUDE.md itself and anything in a `/skills` folder, which are living config edited in place.
> - Proactively prompt me to save conversation content to a file — don't wait to be asked.
> - Before propagating any claim into a new artifact, check whether the source file it came from is stale, superseded, or contradicted elsewhere in the workspace — flag it rather than silently passing it along.
>
> Set up a folder structure organized by artifact type (not by date or project phase), and include a stakeholder-profile folder if I have a team — build each profile from what I tell you, clearly marked as "as provided, not independently verified," and don't treat roleplay based on those profiles as equivalent to real feedback from the actual people.
>
> As we work together, maintain a running change_log.md, and periodically (or when I ask) audit the workspace for staleness — especially CLAUDE.md drifting out of date as the project progresses.

---
