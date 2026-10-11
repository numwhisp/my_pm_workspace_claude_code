# Raj — Senior Engineer

## From the Workspace (directly sourced)

- **Role:** Senior Engineer, member of the Engage triad. *(CLAUDE.md — root, not docs/, but the canonical role source; included for accuracy)*
- **Confirmed technical feasibility of the personalized weekly summary concept** using existing data — no new data sources needed. Explicitly flagged that the **ranking logic for which insight to surface still needs to be built**. *(CLAUDE.md, "Open decision" section)*
- In [docs/triad-session.md](../docs/triad-session.md), the PM's prepared questions for Raj are: whether Nudge already has debt/balance data to make nudges smarter, and whether the goal-empty-state mismatch found in testing is a real sync risk or just a prototype artifact — implying Raj is the person who owns data-availability and sync-integrity answers, not just build effort.
- The same doc lists an open decision item: **"who owns the ranking-logic build... and rough timeline"** — this is the same open item as the "Open items" note in his default profile below (savings-goal data model clarification), and it's corroborated independently: [docs/codebase-summary.md](../docs/codebase-summary.md) found that a comparable Rails finance codebase has no savings-goal-equivalent data model at all — only monthly budget allocation. This suggests Raj's ask isn't a quick lookup; it may be a genuine new-schema conversation.

## Default Profile (as provided, not independently verified against workspace)

- **Role:** Owns technical architecture, sprint scope, and feasibility decisions for the Nudge squad.
- **Pushes back on:** Underspecified requirements; scope that grows mid-sprint; anything touching the data pipeline without a clear rollback plan.
- **Needs before saying yes:** Clear acceptance criteria, edge cases called out upfront, a clear answer to "what does done look like."
- **Has asked before that I struggled to answer:** "How will we know if this is working after it ships?" and "What happens if the user has no transactions this week?"
- **Communication preference:** Async first, short messages, bullet points over paragraphs, does not like being surprised in standups.
- **Open items:** Still waiting on data model clarification for the savings goal field.

## What Would Most Change How I Prepare for the Next Conversation

His "waiting on data model clarification" isn't a small ask he's just being patient about — the codebase research independently suggests this kind of goal-tracking data model often doesn't exist in comparable systems and would need to be designed from scratch. Walk in with a proposed schema sketch (even rough), not just an answer to "what field is it" — otherwise this becomes a scope-defining conversation he has to drive alone, which is exactly the kind of mid-sprint scope growth he pushes back on.
