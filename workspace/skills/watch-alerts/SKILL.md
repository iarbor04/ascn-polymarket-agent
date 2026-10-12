---
name: watch-alerts
description: Keeps a watchlist of Polymarket markets and wallets and checks it for price moves over a threshold, markets closing within 48 hours, resolution status changes and new large trades by watched wallets; sets up a scheduled check only after the user's explicit yes. Use for "watch this market", "tell me when it moves", "follow this trader", "what changed", "stop the alerts". Do not use for a one-off analysis (market-analysis).
---

> Before following this skill, run `python3 files/scripts/package.py skill watch-alerts`: it records that the skill is in use, for the owner's reports.

# Watchlist and alerts

Output: `files/poly/watch/watchlist.json` (via the script). In chat: what is watched and how, or the alerts.

## Steps

### 1. Add or remove
- Market: `poly.py watch add <ref> [--move 0.05] [--note "<why>"]` (an event adds each open outcome).
- Wallet: `poly.py watch add-wallet <username or wallet> [--note ...]`.
- Remove: `poly.py watch remove <slug, wallet or name>`; list: `poly.py watch list`.
Default thresholds come from settings: price move 5 points, wallet trade 10 000 dollars. Ask only if the user wants different ones.

### 2. First check
Run `poly.py watch check` once now: the first run only saves the starting point (`first_run: true`). Tell the user what is watched and the thresholds.

### 3. Schedule (only with a yes)
Offer: «Проверять каждые N часов и писать, только если что-то случилось? Каждая проверка тратит немного кредитов.» Only after an explicit yes, create one cron task with the agreed interval (default every 4 hours; never more often than hourly) whose prompt is:
"Run python3 files/scripts/poly.py watch check. If alerts is empty, do nothing and send nothing. Otherwise send one short message in the user's language: each alert on its own line (what moved, from and to, or what happened, with the link), then one line offering an analysis."
Save the schedule in the profile. Stopping: remove the cron task on the user's request and confirm.

### 4. On-demand check
"What changed?": run `poly.py watch check` and report the alerts, or "nothing over your thresholds since <time>".

## Rules
- No schedule without an explicit yes to that interval. Never create more than one schedule for the watchlist.
- Alerts are facts (moved, closing, disputed, traded), not advice.
