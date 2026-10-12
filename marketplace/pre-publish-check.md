# Pre-publish check

1. `python3 files/scripts/package.py check` → `clean: true`.
2. `files/poly/` has no test data (profile, watchlist, snapshots, reports) in the publishing workspace, or run `python3 files/scripts/package.py prepublish`.
3. No cron job for the watchlist or the brief in the publishing workspace (`cron list`).
4. Soul field deployed from `marketplace/soul-intro.md` (name Nora).
5. Start prompt from `marketplace/startup-task.md`; exclude paths from `marketplace/publish-exclude.txt` (with `workspace/` prefix in the form).
6. Secrets: none required. All data comes from public read-only Polymarket and Kalshi endpoints.
7. One probe from the publishing workspace: `python3 files/scripts/poly.py scan --limit 3` returns markets (the sandbox can reach polymarket.com).
