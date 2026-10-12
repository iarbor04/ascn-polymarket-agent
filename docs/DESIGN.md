# Design decisions

- **Scope** comes from the owner-approved description in `../crypto-agents-descriptions.md` (agent 4): market picks by topic, market analysis (probability, history, book, holders), top traders and their positions, own estimate with sources, alerts, the user's wallet. Added from research (docs/research.md) because they are part of a correct analysis, not new features: resolution-rules reading and dispute status (the main trust pain, rarely covered by competitors), Kalshi comparison (named in the description as "comparison"), fees in every return number, fresh-wallet flag on large trades.
- **No trading, no wallet connection, no keys.** Positioning "analyst, not a bot": no custody risk, less regulatory risk, and the owner's approval rule. Copy-trading bots are the competitors' main paid feature; offered later only if the owner asks.
- **Data:** public read-only Polymarket Gamma, CLOB, Data API v1 (+ v2 `resolutions`, `oi`, `user-stats`) and Kalshi `/events`. All checked live on 2026-10-12. Data API v1 is being migrated to v2; if v1 endpoints stop, switch `poly.py` (leaderboard, positions, holders, trades) to the v2 equivalents listed in research.md.
- **Arithmetic in the script:** fill price for a size from the book, taker fee, edge, break-even, return, annualized (only from 3 days left), holder concentration, watch diffs.
- **Kalshi search** crawls open events (15 pages × 200) and matches all query words; ~20 s. No shared IDs exist, so the skill checks wording before comparing.
- **Alerts:** one cron task only after an explicit yes, at most hourly; the check sends nothing when nothing happened (saves credits).
- **Name** Nora is a placeholder the owner can change (IDENTITY.md, soul-intro, package.config.json greetings, rules line 9).
- **Not possible / not included:** placing bets, Polymarket comments sentiment, X/Twitter monitoring (needs paid API), bookmaker odds API (paid; the agent uses web search for odds when needed).
