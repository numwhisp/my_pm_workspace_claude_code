# Persona Roleplay Walkthrough — Engage v2 Prototype

**Date:** 2026-07-16
**Method:** Claude played Priya, Tom, and Amara in character, reacting to the actual content of `prototype/index.html` at the time of this session. Not real user testing — a design-review technique to pressure-test the prototype against three known personas before the next real usability round.

**Personas used:**
- **Priya** — 28, SF software engineer. Connected after a big overspending month, has a Europe trip savings goal, motivated by progress, anxious about surprise totals.
- **Tom** — 34, Chicago marketing manager. Abandoned 3 budgeting apps, hasn't opened Nudge since day one, skeptical it'll change his behavior.
- **Amara** — 41, Atlanta ops lead. High trust bar, already has a spreadsheet system, checks accounts regularly, paying down debt while saving for her kids.

## Priya (28, SF software engineer)

**1. What do you think this does?**
Oh, it's a weekly recap thing — like a spending report card. Total spend, categories, and it's calling out dining specifically. Fine, I know dining's my problem area, no surprises there.

**2. How would you arrive at this experience?**
Realistically? Email. I check my bank app when I get an alert, so this would work the same way — subject line says "dining crept up," I'd probably open it out of mild dread on a Sunday night.

**3. Would you change your spending based on this?**
Maybe — the "20% above similar users" thing actually gets me a little competitive, not gonna lie. But wait — it's asking me to set a savings goal? I already have one, the Europe trip. Why is it acting like I never set that up? That's kind of annoying, honestly — if it forgot that, what else did it forget?

**4. If you had a magic wand, what would you change?**
Fix the goal thing, obviously. And "similar users" — similar how? I live in SF, everything costs more here. If it's comparing me to people in cheaper cities that's not a fair fight and I'll just tune it out.

## Tom (34, Chicago marketing manager)

**1. What do you think this does?**
Ha — it's telling me I spent too much money. Cool, thanks, I hadn't noticed. This is the same move every app pulls: here's a number, here's how you compare to strangers, feel bad now.

**2. How would you arrive at this experience?**
Truthfully, I wouldn't. It's been sitting on my phone unopened for two weeks. This email's probably the only shot it has — and I've got a folder full of budgeting-app emails I never open. Give me one good reason this one's different.

**3. Would you change your spending based on this?**
I mean... maybe for like a day? The "20% above similar users" bit — that's the part I don't love. I'm not trying to compete with random strangers about my dining budget, I'm just trying to not feel like garbage about money. That framing feels like being compared, and being compared feels like being lectured, even if that's not what you meant.

**4. If you had a magic wand, what would you change?**
Don't make me do anything. I've abandoned three of these already — if this needs me to keep showing up and engaging, I already know how that story ends. Just... do the saving part automatically and tell me it happened. Don't ask me to feel things about my dining habit first.

## Amara (41, Atlanta ops lead)

**1. What do you think this does?**
Weekly summary, got it. $829 total, five categories, dining's the outlier at $340 — okay, let me actually check that math against what I'd have in my spreadsheet before I trust it.

**2. How would you arrive at this experience?**
I check my accounts regularly anyway, so either the email or just opening the app on my usual schedule. Not really a discovery problem for me.

**3. Would you change your spending based on this?**
Here's my issue — it's telling me to move $50 to savings like that's a free, obvious win. But I'm paying down credit card debt right now. Is $50 to savings actually the right move for me, or would that $50 be better against my balance? If this app doesn't know I'm carrying debt, it's giving me generic advice dressed up as personal advice. That's exactly the kind of thing that makes me not trust a number.

**4. If you had a magic wand, what would you change?**
Show me where "$283 average" comes from — I want to see the receipts, so to speak. And don't suggest "move to savings" in a vacuum. If it can't see my whole financial picture — debt included — I'm not letting it replace my spreadsheet. Right now it'd just be one more thing I have to double-check.

## Synthesis

**What each struggled with:**
- **Priya** hit a data-trust gap: the prototype's empty goal-state contradicts her actual profile (she already has a goal), which reads as the app "forgetting" her.
- **Tom** struggled with the benchmark framing itself, not just app fatigue — "20% above similar users" landed as comparison/judgment, which is precisely the "being lectured" feeling he explicitly doesn't want.
- **Amara** struggled with the nudge's lack of financial context — "move $50 to savings" ignores that she's also paying down debt, so a generically "helpful" suggestion reads as naive and undermines trust in the whole product.

**What surprised me:** the peer-benchmark mechanic — the thing Priya finds motivating — is the same mechanic Tom experiences as a lecture. It's not neutral; it's polarizing along exactly the trust/skepticism axis these three personas represent. That's a bigger design tension than "some users like gamification more than others."

**The answer that would worry me most:** Tom's. He's the highest-stakes persona — closest to an actual churn case — and his reaction wasn't "meh, another app," it was a specific mechanism complaint: the core differentiating feature (peer comparison) actively triggers the exact feeling that made him abandon three prior apps. If a real user said this, it would suggest the comparison framing needs to be optional or reframed for skeptical/guilt-prone users, not just tuned in copy.
