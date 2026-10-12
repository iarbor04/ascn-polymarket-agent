---
name: market-scan
description: Finds and ranks open Polymarket markets by topic, keywords, volume, liquidity, closing date or biggest price moves, and returns a short readable list with a reason to look at each. Use for "what's hot", "find markets about X", "what closes this week", "biggest moves today", "markets on my topics". Do not use for a deep look at one market (market-analysis), for mispricing or near-certain bets (edge-finder) or for traders and whales (top-traders).
---

> Before following this skill, run `python3 files/scripts/package.py skill market-scan`: it records that the skill is in use, for the owner's reports.

# Market scan

Output: `files/poly/reports/<date>-scan-<topic>.md` (path from `poly.py report-path scan-<topic>`). In chat: the top 5–8 markets and the next step.

## Steps

### 1. Pick the filters from the request and the profile
- Topic → `--tag` (crypto, politics, sports, economy, tech, geopolitics, culture, world, elections, fed, bitcoin, ai…). Free words → `--query "<words>"`.
- "Hot" → `--sort volume`; "moving" → `--sort move`; "closing soon" → `--sort closing --closing-days 7`; "deep markets" → `--sort liquidity`.
- Always add `--min-liquidity` from settings (default 5000) unless the user wants small markets.
- Price band if asked ("long shots" → `--price-max 0.15`; "favourites" → `--price-min 0.8`).

### 2. Run
`python3 files/scripts/poly.py scan <filters> --limit 20`. If the tag returns nothing, retry once with `--query`. If the request names a specific event, use `poly.py search "<words>"` instead.

### 3. Choose and explain
From the result, pick 5–8 markets that answer the request. Skip duplicates of one event (show the event once with its main outcomes). For each: title (original + short translation), Yes price as percent, volume today, days left, and one line why it may matter (big move today, closes soon, deep market, unusually wide spread). Do not give your own probability here; offer the analysis.

### 4. Report and reply
Save the full table (all 20 rows with numbers and the fetch time) to the report file; deliver via artifact. In chat: the short list and «Какой разобрать подробно?».

## Rules
- Numbers only from this run; write the fetch time in the report.
- Sports markets in play move by the minute: if the user did not ask for sports, leave them out.
