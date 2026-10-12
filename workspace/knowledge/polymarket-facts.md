# Polymarket facts (checked 2026-10-12; re-check official docs if a question depends on something newer)

- **Prices:** each share pays 1 dollar if its outcome wins, 0 if not. Price = what the market pays for that, not a guaranteed probability.
- **Taker fee (since 2026-03-30):** shares × rate × p × (1 − p), only for orders that take liquidity. Rates by category: crypto 0.07; sports, economics, culture, weather, other 0.05; politics, finance, tech, mentions 0.04; geopolitics 0. Limit orders that rest in the book pay no fee and can earn a maker rebate. The market's own `fee_schedule` in `poly.py market` is the authority. Source: docs.polymarket.com/trading/fees.
- **Rewards:** liquidity rewards for limit orders near the middle on some markets (`rewards` in `poly.py market`); holding rewards (about 4% a year) on some long-dated markets.
- **Resolution:** UMA optimistic oracle; disputes go to a UMA holder vote; see knowledge/resolution-risk.md.
- **Access:** not available in every country. A US version runs under a CFTC-regulated entity with its own app and fees; availability by state changes. Never state what is allowed for a user; tell them to check where they live. Never help get around restrictions.
- **Data used by this agent:** Polymarket Gamma (markets, events, search), CLOB (order book, price history) and Data API (positions, trades, holders, leaderboard, resolutions, open interest), all public and read-only; Kalshi public market data for comparison.
