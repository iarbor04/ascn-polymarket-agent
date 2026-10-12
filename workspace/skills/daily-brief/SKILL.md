---
name: daily-brief
description: A short morning or weekly brief for the user's topics and watchlist - biggest moves, new and closing markets, what top traders did, large trades, and status of watched markets - with one line on why each item matters. Use for "morning brief", "what happened overnight", "weekly summary", or when a scheduled brief runs. Do not use for one market (market-analysis) or for alerts only (watch-alerts).
---

> Before following this skill, run `python3 files/scripts/package.py skill daily-brief`: it records that the skill is in use, for the owner's reports.

# Daily brief

Output: `files/poly/reports/<date>-brief.md`. In chat: 6–10 lines, one item per line.

## Steps

### 1. Context
`poly.py context`: topics, watchlist, settings.

### 2. Collect (keep to these calls)
- Per topic (max 3 topics): `poly.py scan --tag <topic> --sort move --min-liquidity 20000 --limit 8`.
- Closing soon on the topics: `poly.py scan --tag <first topic> --sort closing --closing-days 3 --limit 8`.
- Smart money: `poly.py smart --category <first topic> --top 10 --min-traders 2`.
- Whales: `poly.py whales --min <whale size> --limit 15 --fresh`, kept to the user's topics.
- Watchlist: `poly.py watch check`.

### 3. Pick what matters
At most 10 items: the biggest moves with a likely reason (one web search for the single biggest unexplained move), markets closing in 3 days with the current price, a notable consensus of top traders, a fresh-wallet bet, every watchlist alert.

### 4. Report and reply
Report: all sections with numbers and fetch time. Chat: the items, then «Разобрать что-то подробно?».

### 5. Schedule (only with a yes)
If the user wants it every morning or weekly, offer once and only after an explicit yes create one cron task at the time they name, whose prompt runs this skill. Warn that each run spends credits.

## Rules
- Facts and context, no tips. Never repeat yesterday's numbers as today's.
