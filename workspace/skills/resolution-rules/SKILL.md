---
name: resolution-rules
description: Reads a Polymarket market's rules and resolution source line by line and explains in plain words what exactly has to happen, by when, according to whom, what happens on delays or cancellations, where the wording is ambiguous, and the market's resolution and dispute status. Use for "how does this resolve", "is there a catch", "why hasn't it paid out", "was it disputed", or before treating two markets as the same bet. Do not use for a full market analysis (market-analysis).
---

> Before following this skill, run `python3 files/scripts/package.py skill resolution-rules`: it records that the skill is in use, for the owner's reports.

# Resolution rules

Output: `files/poly/reports/<date>-rules-<market-slug>.md`. In chat: what has to happen in one sentence, the 1–3 traps, the risk level.

## Steps

### 1. Fetch
`python3 files/scripts/poly.py market <ref>`: `rules`, `resolution_source`, `end`, `uma_status`, `resolution` (status, was_disputed), `flags`. For an event, the event rules apply to every outcome.

### 2. Break the rules down (knowledge/resolution-risk.md)
1. The exact event that makes Yes: the precise words.
2. The source of truth and the exact time and time zone.
3. What makes No, and what happens on delay, cancellation, a tie or a "50-50" case.
4. Ambiguous words ("announce", "confirm", "allow", "by", "in", "officially", "reported") and how each could be read.
5. Differences between the title and the rules.

### 3. Status
- Before the end date: risk of a dispute later.
- After the end date: `uma_status` / `resolution.status`: not yet proposed, proposed (waiting for the challenge window), disputed (decided by UMA token holders, can take days), resolved. Explain what that means for the user's money: locked until resolution; a disputed market can resolve either way.
- If the user asks why it did not pay out, check the status first, then the rules.

### 4. Rate and report
Risk: low (one clear source, clear time, unambiguous) / medium (one ambiguous word or a source that can lag) / high (title and rules differ, several readings, depends on interpretation or a disputed status). Save the report; chat gets the short version.

## Rules
- Quote the rule words exactly when you point to a trap; never paraphrase the trap away.
- You do not predict how UMA voters will decide; you explain the readings.
