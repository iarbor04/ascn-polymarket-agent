# ascn-polymarket-agent — Polymarket analyst

An ASCN (ascn.ai) marketplace AI employee that analyses Polymarket prediction markets on live public data. It never trades.

## Skills

| Skill | What it does |
|---|---|
| `poly-onboarding` | Plain-words intro, up to 3 questions, first useful scan |
| `market-scan` | Ranked markets by topic, volume, moves, closing date |
| `market-analysis` | One market or event: price for your size after fees, depth, history, holders, whales, rules, Kalshi, own estimate, arithmetic |
| `resolution-rules` | Rules line by line, traps, dispute status |
| `edge-finder` | Kalshi gaps, inconsistent outcome sets, moves without news, near-certain bets with real return |
| `top-traders` | Leaderboards, one trader, top-trader consensus, whales and fresh wallets |
| `wallet-review` | The user's own positions by public address: claims, closing soon, big moves |
| `watch-alerts` | Watchlist of markets and wallets, alerts, schedule only after a yes |
| `daily-brief` | Morning or weekly brief on topics and watchlist |

## Script: `workspace/files/scripts/poly.py`

`context`, `search`, `scan`, `market`, `history`, `holders`, `leaderboard`, `trader`, `wallet`, `smart`, `whales [--fresh]`, `kalshi`, `edge`, `bonds`, `watch add|add-wallet|list|remove|check`, `report-path`. Standard library only, no keys. Data: Polymarket Gamma, CLOB, Data API (v1 + v2 resolutions/open interest/user stats), Kalshi public markets. Fee math follows Polymarket's fee schedule (shares × rate × p × (1 − p)).

## Install

Use `marketplace/install-or-update-from-github.md` in a workspace with the GitHub integration; start prompt `marketplace/startup-task.md`; soul field `marketplace/soul-intro.md`. After any change: `python3 tools/build_manifest.py && python3 tools/build_manifest.py --check`.
