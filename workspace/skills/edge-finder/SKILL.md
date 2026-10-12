---
name: edge-finder
description: Looks for Polymarket prices that may be wrong - gaps against Kalshi for the same event, outcome sets whose prices don't add up, sharp moves without news, long shots and favourites priced against base rates - and near-certain outcomes close to resolution ("bonds") with their real return after fees and the risk behind it. Use for "where is the price wrong", "find undervalued markets", "safe bets that close soon", "compare with Kalshi". Do not use for one known market (market-analysis) or for following traders (top-traders).
---

> Before following this skill, run `python3 files/scripts/package.py skill edge-finder`: it records that the skill is in use, for the owner's reports.

# Edge finder

Output: `files/poly/reports/<date>-edges-<topic>.md`. In chat: 3–5 candidates, each with the gap, why it may exist, the main risk.

## Steps

### 1. Choose the hunt from the request
- **Cross-venue:** `poly.py scan --tag <topic> --min-liquidity 20000 --limit 20`, then for the top events `poly.py kalshi "<key words>"`. A candidate needs the same question, the same date and comparable sources. Gap = Polymarket buy price (with fee) vs Kalshi yes ask.
- **Outcome sets:** `poly.py market <event>`; for exclusive outcomes (`exclusive_outcomes: true`) a Yes sum far from 1 is worth a note; for ladders (price thresholds) check that higher thresholds are not priced above lower ones.
- **Moves without news:** `poly.py scan --sort move --min-liquidity 20000`; for the top movers, one web search for news. A big move with no news and one large wallet behind it (`poly.py whales --ref <slug> --fresh`) is a candidate either way: the market may know something, or one player pushed it.
- **Near-certain ("bonds"):** `poly.py bonds --min-price <settings or 0.95> --min-days 3 --max-days 30 --limit 20`. Read each candidate's rules (resolution-rules, short form): a near-certain price with a messy rule is a trap, not a yield.

### 2. Check each candidate
`poly.py market <slug>` for the real buy price, depth and flags. Drop candidates where the gap is smaller than spread plus fee, or where the depth for 500 dollars moves the price past the gap.

### 3. Rank
By size of the gap after costs, quality of the outside price (same rules, deep market), days to resolution and resolution risk. For each kept candidate run `poly.py edge <slug> --estimate <outside probability>` and report break-even, return if right and annualized.

### 4. Report and reply
Report: method, every candidate checked with numbers and why it was kept or dropped, the ranked list, risks. Chat: the top 3–5 in one line each plus «Разобрать какой-то подробно или поставить на отслеживание?».

## Rules
- A gap is a hypothesis to check, never "free money" or "arbitrage" unless both legs are the same event under the same rules and the user understands both venues' access limits.
- Near-certain bets: always say that one surprise loses the whole stake, and that annualized numbers on a few days mislead.
- Do not present Kalshi as an option for users where it is not available; it is a reference price.
