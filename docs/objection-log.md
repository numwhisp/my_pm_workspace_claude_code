# Objection Log — PRD Pressure Test

**Date:** 2026-07-16
**Method:** Roleplayed 3 reviewers against [docs/prd.md](prd.md): Raj and Marcus per their stakeholder profiles ([stakeholders/raj.md](../stakeholders/raj.md), [stakeholders/marcus.md](../stakeholders/marcus.md)), Tom per the churned-user profile given (5 weeks in, switched to YNAB, feels guilty about money, wanted something to act on, found the dashboard static and unrewarding).

## 1. Raj

**1.** The savings-goal data model is sitting in the PRD's Open Questions as a bullet point, not scoped as its own ticket. This isn't a quick lookup — it's a schema decision. Where's the rollback plan, and is this one sprint or two? Shipped buried inside the feature ticket, this is exactly the kind of mid-sprint scope growth Raj doesn't accept.

**2.** Success Metrics has exactly one line: 30-day retention — a lagging metric. Raj has previously asked "how will we know if this is working after it ships," and a 30-day number doesn't answer that in week one. Where are the proxy metrics, and where do they get measured?

## 2. Marcus

**1.** The PRD's own Open Questions state the company's north-star metric isn't confirmed, and it's unclear whether 30-day retention is what leadership judges this against beyond this initiative. Without that confirmed, this can't be defended to the board as the number that matters.

**2.** No date appears anywhere in the document. Marcus has asked for a rollout timeline before committing to the Q3 sprint — that request is still unanswered here.

## 3. Tom (churned user, week 5, switched to YNAB)

**1.** The PRD's own Non-Goals admit "a single feature... may satisfy Priya's mode but not address Tom's." The document already acknowledges this may not work for a user like Tom, and ships anyway — why should he expect anything different from the static screen that made him leave?

**2.** Does this compare him to other people's spending again? To Tom, that's not "something to act on" — it's another way to feel judged about money, which is the opposite of what he said he needed (something that asks something of him, not something that lectures him).

## Which Objection Is Most Likely to Kill the Initiative

**Marcus's first question — the unconfirmed north-star metric — is the most dangerous if left unaddressed.** Raj's objections would delay a sprint; Tom's objection is a real product-fit risk but would only surface as a metric shortfall after launch, not before either ships. Marcus's is different in kind: he holds the authority to simply not prioritize this, and the PRD hands him the reason to do so — it admits the metric being optimized might not even be what leadership cares about. That's a credibility gap in the core premise, not a request for more detail. If confidence in "why this matters" breaks before the sprint is scheduled, no engineering or design fix downstream saves it.
