# 15-Minute Live Onboarding Demo — Script

**Goal:** by minute 15, your teammate has run the AI interview themselves, for their own product, in their own folder — not watched you do it.
**Prep before starting:** have this workspace open, and confirm `meeting-notes/product-engage-slack-thread.md` exists (it's the raw Slack thread that originally kicked off this project — used in minutes 2–7 below).

---

## Minutes 0–2 — Open the Workspace, Show What Claude Already Knows

1. Open the Nudge workspace folder and run `claude` to start a session.
2. Point out: nothing was asked yet, and Claude already has context. Say out loud: "Claude just read `CLAUDE.md` automatically before I typed anything."
3. Ask Claude a simple question that only makes sense with prior context loaded, e.g. **"Who's on my triad and what's the status of Engage v2?"** It should answer correctly — the product, the team (Raj/Lena/Marcus), and the current project state — without you explaining any of it.
4. Say the point out loud: **"That answer came entirely from a text file, not from Claude remembering our past conversations. That's the whole model."**

## Minutes 2–7 — Run the AI Interview, Show Plan Mode

1. Open `meeting-notes/product-engage-slack-thread.md` — this is the real Slack thread that started this whole project. Paste it into the chat and ask Claude to turn it into a PRD skeleton (Problem Statement, Goals, Non-Goals, Success Metrics), telling it not to invent details not in the thread.
2. Watch it come back with a skeleton that flags unknowns as TBD instead of guessing — point out that this is the "never invent facts" rule from CLAUDE.md in action, not a coincidence.
3. Now demonstrate the interview pattern on a bigger ask: tell Claude you want to prototype a new feature, and watch it ask clarifying questions one at a time instead of just building something. Answer 2–3 of them live.
4. **If you have plan mode available, trigger it here** on a multi-step build (e.g., "build the prototype") — show your teammate that Claude lays out its approach before touching any files, and you approve or redirect before it starts. Say out loud: "This is the point where I catch a wrong assumption *before* it becomes wasted work, not after."

## Minutes 7–12 — Run the Weekly Status Skill, Then Hand Over the Keyboard

1. Trigger the reusable status-update workflow: paste the trigger line from `skills/friday-status-update.md` (or `skills/weekly-status.md` for the simpler single-audience version) along with a couple of made-up example status notes.
2. Show the output — point out it's using the *same* stakeholder profiles (`stakeholders/raj.md`, `lena.md`, `marcus.md`) from earlier in the workspace to calibrate tone automatically, without you re-explaining who Raj and Marcus are.
3. **Hand over the keyboard.** Have your teammate write 3–4 quick, real bullet notes about something they actually worked on this week (their own project, unrelated to Nudge is fine), paste the same trigger line, and run it themselves.
4. Let them see the output land — this is their first "I made Claude do something useful" moment.

## Minutes 12–15 — Their Turn: New Product, New Folder

1. Have them create a brand-new empty folder for their own product/project.
2. Open `docs/capstone-session.md` in this workspace, section 4 — the reusable onboarding prompt.
3. Have them copy that prompt, open a `claude` session in their new folder, and paste it themselves.
4. **The session ends here, with them mid-interview, answering Claude's first question about their own product.** Don't finish the interview for them — the goal is that they leave already in motion, not having watched a demo.

---

**Closing line to say out loud:** "Everything you just watched came from files, not from me explaining things to Claude live. Your new folder starts empty — what you put in `CLAUDE.md` over the next few sessions is what makes Claude useful to you specifically."
