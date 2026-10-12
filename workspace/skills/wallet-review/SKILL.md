---
name: wallet-review
description: Reviews the user's own Polymarket positions from their public wallet address or username - value, profit and loss, positions closing soon, winnings waiting to be claimed, big losers, and for each important position whether anything changed since entry (price, news, rules status). Use for "check my portfolio", "what's in my wallet", "what should I look at". Do not use for other traders (top-traders). Never ask for a private key or seed phrase.
---

> Before following this skill, run `python3 files/scripts/package.py skill wallet-review`: it records that the skill is in use, for the owner's reports.

# Wallet review

Output: `files/poly/reports/<date>-wallet-review.md`. In chat: value and open PnL, what needs attention now (claims, closing soon, big moves), the next step.

## Steps

### 1. Wallet
Take the address or username from the request or the profile. If missing, ask for the public address or username (one line; never a key). Save it to the profile.

### 2. Fetch
`python3 files/scripts/poly.py wallet <address or username>`: value, ranks, positions, recent trades, flags (`redeemable`, `closing_7d`, `big_losses`).

### 3. Look closer where it matters
For the 3–5 largest positions and every `closing_7d` one: `poly.py market <slug>` (price now vs entry, spread, rules flags, resolution status). One web search only if a position moved a lot and the reason is unclear.

### 4. Write it up
- **Claim:** winnings ready to be claimed (redeemable): remind that they are collected in the Polymarket app.
- **Closing soon:** what has to happen, the current price, the resolution risk.
- **Big moves and losses:** what changed; the options (hold, reduce, exit) with the facts behind each, not an instruction.
- **Concentration:** share of the portfolio in the top position and in one topic.

### 5. Report and reply
Save the report; offer to put the closing-soon markets on the watchlist.

## Rules
- Options with facts, never "sell" or "buy more" as advice; the decision is the user's.
- Only 200 largest positions are loaded: say so when the note appears.
