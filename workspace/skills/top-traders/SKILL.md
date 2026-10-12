---
name: top-traders
description: Shows who makes money on Polymarket and what they hold - leaderboards by period and category, one trader's record and positions, what the top traders hold together right now, recent large trades and fresh wallets betting big - always with the limits of such signals. Use for "who are the best players", "what do top traders bet on", a trader's username or wallet, "whales", "insiders", "who bought this". Do not use for the user's own wallet (wallet-review).
---

> Before following this skill, run `python3 files/scripts/package.py skill top-traders`: it records that the skill is in use, for the owner's reports.

# Top traders and whales

Output: `files/poly/reports/<date>-traders-<topic>.md`. In chat: the main finding, 3–6 lines of evidence, the caveat, the next step.

## Steps

### 1. Pick the view
- Leaderboard: `poly.py leaderboard --period <day|week|month|all> --category <topic> --limit 20`.
- One trader: `poly.py trader <username or wallet>`: ranks, PnL, portfolio value, largest open positions, recent trades.
- Consensus of the best: `poly.py smart --category <topic> --period month --top 15 --min-traders 2`.
- Whales: `poly.py whales --min <settings whale size> --limit 25 --fresh` (or `--ref <market>` for one market).

### 2. Read it right
- PnL over a month can be one lucky bet: check volume and number of positions before calling someone skilled.
- Several top traders on the same side is more meaningful than one whale; say how many and at what average price versus now.
- A position bought far below today's price is already in profit: the trader may be selling, not adding.
- Fresh wallet + large bet: "worth a closer look", list the facts (age, trades, PnL), never "insider".

### 3. Add context for the markets that stand out
For 1–3 markets in the finding, `poly.py market <slug>` (price now, days left, rules risk flag).

### 4. Report and reply
Report: the tables with numbers and fetch time, the reading, the caveats. Chat: the finding and «Поставить этого трейдера или рынок на отслеживание?».

## Rules
- Never "copy this trader". Always add: a big position can be a hedge, a mistake or a push on the price; past profit does not make this bet right.
- Names and wallets are public Polymarket data; do not try to find out who the person is in real life.
