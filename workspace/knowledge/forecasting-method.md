# Forecasting method (for your own estimate)

Use this every time you give a probability of your own. If you can't do steps 1–3 with real sources, say you have no independent view.

1. **Pin the question.** Restate exactly what makes Yes, by when, by which source (from the rules, not the title).
2. **Outside view first: the base rate.** How often did events of this kind happen? Examples: incumbents re-elected, bills passing by a deadline, a central bank moving when futures price X, an asset touching a level within N days (use its recent volatility), a favourite winning at these bookmaker odds. Name the reference class and the source.
3. **Inside view: adjust.** News, official statements, polls, schedules, data releases. Each adjustment names its source and date and moves the estimate up or down with a reason.
4. **Other markets.** Kalshi (`poly.py kalshi`), bookmakers (remove the margin: divide each implied probability by their sum), CME FedWatch for rates, poll averages. Only comparable if the wording and dates match.
5. **Give a range, not a point.** Wider when evidence is thin. Note what would move it (an event, a date, a number).
6. **Compare with the market only at the end.** If your range contains the market price, say the market looks fair. A gap matters only if it is bigger than spread + fee and your sources are solid.
7. **Record it.** One line in files/poly/forecasts.md: date, market link, market price, your range, reason.

Traps: anchoring on the market price; one vivid news story; treating a whale's bet as information; markets where the outcome depends on wording rather than events; very long-dated markets where money is locked for months (compare the return with a safe yield).
