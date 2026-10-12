# Resolution risk: how to read Polymarket rules

How resolution works (Polymarket docs, checked 2026-10-12): after the end, someone proposes the outcome with a bond; there is a challenge window; if challenged, the question can be re-proposed and then goes to a vote of UMA token holders, which can take days. Money stays locked until it resolves. `poly.py market` shows `uma_status` and, after the end or when disputed, `resolution` (status, was_disputed).

## Checklist
1. **Exact trigger.** Which words make Yes? "announces" vs "completes"; "by" (inclusive?) vs "in"; "officially"; "according to".
2. **Source of truth.** One named source (a site, an exchange candle, an official body) is safer than "credible reporting" or "consensus of media".
3. **Time and time zone.** ET vs UTC, a specific candle or close, a date that falls on a weekend or holiday.
4. **Edge cases.** Postponement, cancellation, tie, partial event, a source that stops publishing; is there a "resolves 50-50" or "resolves No" clause?
5. **Title vs rules.** If they differ, the rules win; say so loudly.
6. **Clarifications.** Rules can carry "additional context" added later; mention if present.
7. **Who benefits from a fight.** Large holders on one side and an ambiguous word mean a higher chance of a dispute.

## Risk levels
- **Low:** one clear trigger, one named source, exact time.
- **Medium:** one ambiguous word, or a source that can lag or be revised.
- **High:** title and rules differ, several fair readings, "credible reporting" with a contested event, or a market already disputed.

Real cases that hurt traders (2025–2026): ambiguous verbs ("allow" in a Fort Knox market), a large UMA holder in a disputed market about a minerals deal, retroactive "clarification" of a market about a company's bitcoin. Sources: theblock.co (UMA governance attack), docs.polymarket.com (disputes).
