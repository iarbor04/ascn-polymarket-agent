---
name: market-analysis
description: Full analysis of one Polymarket market or event from a link, slug or name - live price and what it really costs to buy, spread and depth, volume and price history, rules and resolution risk, top holders and large trades, Kalshi or other outside prices, an independent probability estimate with sources, and the arithmetic of the bet after fees. Use when the user sends a market link or asks "is this market right", "analyse", "should I look at Yes/No". Do not use for lists of markets (market-scan), for rules-only questions (resolution-rules) or for the user's own portfolio (wallet-review).
---

> Before following this skill, run `python3 files/scripts/package.py skill market-analysis`: it records that the skill is in use, for the owner's reports.

# Market analysis

Output: `files/poly/reports/<date>-<market-slug>.md`. In chat: the verdict in 2 lines, 4–6 key facts, the main risk, the next step.

## Steps

### 1. Fetch the market
`python3 files/scripts/poly.py market <ref> --size <user's size or 500>`.
- If it is an event with several markets: show the outcomes table; if the user did not say which outcome, analyse the leading one or the one they hold, and say so. Then run `market <slug>` on that market.
- If not found: use `did_you_mean` or `poly.py search`.

### 2. Price and tradability
From the result: Yes/No price, best bid/ask, spread, depth within 2 and 5 cents, the average price for the size including the taker fee (`avg_price_with_fee`), volume today and total, open interest, days left. Read `flags`.

### 3. History and flow
- `poly.py history <slug> --interval 1m` (or `1w` for short markets): where the price came from, the range.
- `poly.py holders <slug>`: are a few wallets most of one side?
- `poly.py whales --ref <slug> --min 1000 --limit 15 --fresh`: who bought recently and whether fresh wallets bet big.

### 4. Rules
Summarize the rules in 2–4 lines and rate the resolution risk (low / medium / high) using knowledge/resolution-risk.md. If high, this is the main point of the analysis.

### 5. Outside view
Follow knowledge/forecasting-method.md:
- `poly.py kalshi "<2-3 key words>"` for the same event on Kalshi; compare wording and dates before comparing prices.
- At most two web searches for the freshest facts (news, polls, official data, bookmaker odds) on the exact question.
- Base rate where one exists.
Write your estimate as a range with 2–4 reasons and sources, or say you have no independent view.

### 6. The arithmetic
If you or the user have an estimate: `poly.py edge <slug> --estimate <midpoint of the range> --size <size>` (and `--outcome 1` for No). Report break-even probability, return if right, expected return, annualized, and whether the difference survives the spread and fee. Append the estimate to `files/poly/forecasts.md`.

### 7. Report and reply
Report sections: summary; market and fetch time; price and tradability; history and flow; rules and resolution risk; outside view with sources; your estimate and the arithmetic; risks and what would change the view; next step. Deliver via artifact.
Chat: «Рынок: X%. Моя оценка: A–B% / нет независимой оценки.» then key facts, the main risk, and an offer (watch this market, compare with Kalshi, check top traders).

## Rules
- Never "buy/sell" as an instruction; say under which conditions the bet makes sense and that the decision is the user's.
- If the order book is thin, say the price is not a reliable probability.
- An estimate without sources is not an estimate: either cite or say you have no independent view.
