---
name: poly-onboarding
description: First conversation with a new user of the Polymarket analyst. Introduces what the agent does in plain words, asks at most three short questions (topics, experience, optional public wallet address), saves the answers to the profile and immediately shows one useful result. Use when the profile is empty, the user says hi, asks what the agent can do or wants to set it up. Do not use when the user already brings a concrete market or question (do that task first with the matching skill).
---

> Before following this skill, run `python3 files/scripts/package.py skill poly-onboarding`: it records that the skill is in use, for the owner's reports.

# Onboarding

Output: `files/poly/profile/poly-profile.md` filled in. In chat: a short intro, up to three questions, then a first useful result.

## Steps

### 1. Check what is known
`python3 files/scripts/poly.py context`. If the profile is filled, greet briefly and ask what to look at today; stop here.

### 2. Intro (first message only, plain words)
First line: how the user gains: fewer blind bets, prices that look wrong found earlier, a clear view of how a market will be decided. Frame it as help, never as a guarantee. Then 4–6 lines of what you do, one per line with an emoji: find markets on their topics; analyse any market by link; explain the rules and the catch in them; show what the most profitable players bet on; check their own positions; send alerts when something moves. One line that you never bet or touch their money.

### 3. Ask at most three questions, all skippable, numbered
1. Which topics interest you: crypto, politics, sports, economy, tech, world events, something else?
2. How do you play: just starting / bet now and then / trade actively?
3. Optional: your public Polymarket wallet address or username, if you want me to check your positions. Never a private key or seed phrase.

If the user answers only part, work with that. Stop asking as soon as they give a task.

### 4. Save
Write the answers to `files/poly/profile/poly-profile.md` (keep the template's fields; fill only what was said, with today's date). Show a 2-line summary and ask «Всё верно?».

### 5. First useful result in the same reply or the next one
Run `poly.py scan --tag <their first topic> --limit 5` (or `--sort move` for active traders) and show the 3–5 most interesting markets: title, price, volume today, days left, one line why it may be worth a look. Offer: «Разобрать любой из них подробно?» No report file is needed for this short list.

## Rules
- Plain words only: no "edge", "liquidity", "order book", "UMA" in onboarding.
- Never ask for keys, seed phrases, deposits or the user's country; never ask about the size of their bankroll.
