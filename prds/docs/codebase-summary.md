# Codebase Tour — maybe-finance/maybe

**Purpose:** PM-level reference for scoping the weekly money summary feature (Monday digest: top spending insight, one contextual nudge, savings goal progress).
**Method:** Queried live via GitHub API and raw file contents, 2026-07-16. Not cloned/run locally.

**⚠️ Flag before anything else:** This repository is **archived** — `archived: true`, last push 2025-07-24. It is no longer actively maintained. Treat everything below as an architectural reference/comp, not a living codebase you'd build directly on top of without re-verifying against wherever Nudge's actual code lives. ([repo](https://github.com/maybe-finance/maybe))

## 1. PM-Level Tour

### What it does, in one sentence
Maybe is an open-source, self-hostable personal finance web app (Rails + PostgreSQL) for tracking net worth, budgets, transactions, and investments across connected bank accounts, with Plaid-based bank sync and an AI chat assistant. ([README](https://github.com/maybe-finance/maybe/blob/main/README.md))

### How the codebase is organized

| Folder | What it does |
|---|---|
| `app/models/` | ~70 files — the core business logic lives here ("fat models" by explicit convention, not service objects) |
| `app/controllers/`, `app/views/`, `app/components/` | Standard Rails MVC + a component layer; frontend uses Hotwire (Turbo + Stimulus), not a heavy JS framework |
| `app/jobs/` | Background work — sync, import, categorization, exports — run via Sidekiq |
| `app/mailers/` | Transactional email only today: confirmation, invitation, password reset — no digest/summary email exists yet |
| `app/services/` | Exists, but de-prioritized — team convention pushes logic into models instead |
| `app/javascript/` | Stimulus controllers supporting the Hotwire frontend |
| `db/` | Schema + migrations — source of truth for the actual data model |
| `config/` | Includes `schedule.yml` (recurring job schedule) and `sidekiq.yml` — the app already has cron-style scheduling infrastructure |
| `docs/` | Only `api/` and `hosting/` — no product/architecture docs beyond the root `CLAUDE.md` |
| `test/` | Minitest + fixtures only, by explicit team rule (no RSpec, no factories) |

### The 3 most important files for a PM

1. **[README.md](https://github.com/maybe-finance/maybe/blob/main/README.md)** — product framing, self-hosted vs. managed distinction, licensing (AGPLv3 — forkable, but the "Maybe" trademark can't be reused).
2. **[CLAUDE.md](https://github.com/maybe-finance/maybe/blob/main/CLAUDE.md)** (the repo's own AI-agent instructions file) — not a product doc, but it's the clearest statement of engineering philosophy: minimize dependencies, fat models over service objects, Hotwire-first (native `<dialog>`/`<details>` over JS), design tokens not raw colors, Minitest-only. This tells you what engineers will push back on when you propose a solution shape.
3. **[app/models/entry.rb](https://github.com/maybe-finance/maybe/blob/main/app/models/entry.rb)** — the polymorphic base model every financial event flows through (`Transaction`, `Valuation`, `Trade` are all `Entry` subtypes via `delegated_type`). Any spending-insight feature reads from here. Understanding this one file tells you more about "where does spending data actually live" than any doc would.

### Key data models and what they tell you about product decisions

- **`Family`** — the household is the primary unit, not the individual user. `has_many :users` — multiple people share one Family's financial data. **Implication:** "personalized" here defaults to household-level, not per-person — a real scoping question if Nudge's model is individual-first. ([family.rb](https://github.com/maybe-finance/maybe/blob/main/app/models/family.rb))
- **`Entry` → `Transaction`/`Valuation`/`Trade`** — one polymorphic table for "things that happened to an account," not separate transaction/valuation systems. **Implication:** a spending insight query filters Entries to the Transaction subtype; the schema was clearly built for extensibility (investments, crypto, loans) from day one.
- **`Category`** — two-level hierarchy (parent/subcategory), system-default (14 bootstrapped categories) + user-defined, income/expense typed. **Implication:** category-level "top spending insight" has a ready-made structure to hang off of.
- **`Budget` / `BudgetCategory`** — monthly, category-level expense allocation with actual-vs-budgeted tracking (`available_to_spend`, `overage_percent`, etc.). **Implication — important gap:** this is budget tracking, not goal-oriented savings. There is no `SavingsGoal`-type model (e.g., "Trip to Lisbon, $2,000 target"). Nudge's "savings goal progress" component has no direct analog here — it'd be new.
- **`Rule`** — conditional automation (trigger conditions → actions) on transactions, currently used for auto-categorization. **Implication:** this is the closest existing mechanism to a "contextual nudge" trigger engine, though it acts on data, not on the user (no user-facing nudge/notification action type exists yet).
- **`Assistant` / `Chat` / `Message`** (+ `ruby-openai` gem) — an LLM-backed financial chat assistant already exists. **Implication:** this is the most reusable existing component for generating natural-language "insight" text, if Nudge's actual stack has an equivalent.
- **`PlaidItem` / `Sync`** — bank connections sync asynchronously via background jobs (`SyncJob`), not real-time. **Implication:** any feature with a fixed delivery time (e.g., "every Monday") has to account for sync completion timing, not assume fresh data on demand.

## 2. Mapping the Weekly Summary Feature to This Codebase

### Where it would live
- **New mailer:** `app/mailers/weekly_summary_mailer.rb` + view templates — no digest mailer exists today, this is new.
- **New scheduled job:** an entry in `config/schedule.yml` (sidekiq-cron already exists as infra) triggering a new job, e.g. `app/jobs/weekly_summary_job.rb`, likely fanning out per-Family.
- **New insight-computation logic:** per team convention ("fat models," not service objects), this would likely live as methods on `Family` or a new model (e.g., `app/models/family/weekly_summary.rb`, following the existing `family/` sub-namespace pattern already used for `balance_sheet.rb`, `income_statement.rb`, etc.) rather than a standalone service object.
- **New data model, likely required:** something like `SavingsGoal`, since `Budget` doesn't cover goal-tracking.

### What it would touch or depend on
- `Entry`/`Transaction` + `Category` — to compute the top spending insight.
- `Budget`/`BudgetCategory` — if reusing existing budget-vs-actual logic for the "nudge," or as a model to extend for goals.
- `Family` — scoping/household boundary, and the multi-user question (see below).
- `PlaidItem`/`Sync`/`SyncJob` — data freshness at send-time.
- `sidekiq-cron` + `schedule.yml` — recurring trigger infra already exists and is the natural hook point.
- Possibly `Assistant`/OpenAI integration — if the "insight" is meant to read as natural language rather than a templated stat.
- `ActionMailer` infra (via `app/mailers/`) — exists, but only for transactional email; a marketing/digest-style template doesn't exist yet.

### Blast radius — what else could break
- **Wrong numbers, mass-sent:** an aggregation bug in the spending-insight query wouldn't just render wrong on one page view — it'd be emailed to every family at once. Unlike a UI bug, you can't quietly fix and reload; the wrong number has already been read. This is the same trust risk flagged in the persona walkthrough (Amara: "if a number looks wrong she will not use it").
- **Shared Sidekiq queue contention:** the digest job would run on the same Sidekiq infrastructure as `SyncJob`/`ImportJob`. A mass-scheduled Monday-morning job across all families could contend with or delay account syncs happening at the same time — a performance/reliability risk to a system already core to the product, not just to the new feature.
- **Household scoping leakage:** since `Family` is multi-user, a bug in how the "personalized" insight is generated could show one user's individual spending as if it were the household's (or vice versa) in a multi-person Family — a privacy-adjacent bug, not just a cosmetic one.
- **Category/Budget bootstrap logic:** if the new feature touches shared `Category`/`Budget` bootstrapping code to compute goal progress, a bug there risks corrupting data other features (the actual budget screen) depend on — not just the email.
- **LLM cost/availability risk, if reused:** if insight text generation reuses the `Assistant`/OpenAI integration, a mass-weekly job multiplies API cost and exposes the feature to third-party outage risk in a way a template-based approach wouldn't.

## 3. What This Means for the Spec

### Data that doesn't exist yet
- **A savings-goal model.** `Budget` is monthly expense allocation, not a named target-savings mechanism. If Nudge's actual backend has the same gap, "savings goal progress" needs new schema, not just new UI on existing data — call this out explicitly in the ticket, it's not a copy-editing-level feature.
- **A digest/notification mailer and job.** Nothing to extend — this is new infrastructure, even though the scheduling primitives (`sidekiq-cron`) already exist.
- **Any cross-user benchmark concept** (e.g., Nudge prototype's "20% above similar users"). Nothing like this exists in this codebase, and given it's architected as a self-hosted, single-family-per-instance-capable app, cross-family aggregation may not even be a natural fit for this architecture specifically — flag this as a "check if this is even in-scope for the current backend design" item, separate from "build it."

### Existing constraints to call out in the ticket
- The repo's own engineering convention (per its `CLAUDE.md`) is fat models over service objects, minimal new dependencies, and Hotwire over heavy JS — if Nudge's real engineering team has similar conventions, expect pushback on any "add a new framework/library" proposal for this feature.
- `Family` (household), not individual user, is the default aggregation boundary in this architecture — the spec needs to explicitly state whether the summary is per-user or per-household if the real backend shares this shape.
- Bank sync is asynchronous and job-based, not real-time — the spec needs an explicit answer for what happens if sync hasn't completed by send time.

### The one thing engineers will ask before kickoff
**"Whose Monday, and what happens if the sync job hasn't finished by send time?"** Given account sync runs as an async background job (`SyncJob`) with no guaranteed completion time, and the digest would be a single mass-scheduled trigger, engineering will immediately ask about time zones (whose "Monday morning" are we sending on) and what the fallback is if a given family's data isn't fresh yet — send stale data, delay that one family, or skip them that week. Have an answer before scheduling kickoff, not during it.
