#!/usr/bin/env python3
"""Polymarket analyst toolkit: live market data from Polymarket's public read-only APIs (Gamma, CLOB, Data API) and
Kalshi's public API, plus the arithmetic the analysis needs. No keys, no trading. Standard library only. Prints JSON.

A market <ref> is a polymarket.com link, a market or event slug, or a condition id (0x...).

  context                                  start of a conversation: profile filled or not, watchlist, settings, recent reports
  search <query> [--limit N]               events and markets matching the words, with prices and volume
  scan [--tag SLUG] [--query TEXT] [--sort volume|liquidity|closing|move] [--min-liquidity USD] [--min-volume USD]
       [--closing-days N] [--price-min P] [--price-max P] [--limit N]
                                           ranked list of open markets by the filters (tags: crypto, politics, sports,
                                           economy, tech, geopolitics, culture, ...)
  market <ref> [--size USD]                one market or a whole event: outcomes and prices, bid/ask/spread, volume,
                                           liquidity, days left, price changes, rules, resolution source, UMA status,
                                           fees, order-book depth and the cost of buying --size dollars, open interest,
                                           resolution status and whether the outcome was disputed
  history <ref> [--interval 1d|1w|1m|max] [--outcome N]   price path: first, last, min, max, change, sampled points
  holders <ref> [--limit N]                top holders of each outcome and how concentrated they are
  leaderboard [--period day|week|month|all] [--by pnl|vol] [--category overall|politics|sports|crypto|culture|
              economics|tech|finance|weather|mentions] [--limit N]
  trader <wallet|username> [--positions N] public profile: rank and PnL, open positions, recent trades
  wallet <wallet|username>                 the user's own wallet: trader + flags (closing soon, redeemable, big losses)
  smart [--category C] [--period P] [--top N] [--min-traders K]
                                           what the top-N traders of the leaderboard hold now, grouped by market
  whales [--ref REF] [--min USD] [--limit N] [--fresh]
                                           recent large trades, on one market or across Polymarket; --fresh adds each
                                           wallet's age, trade count and realized PnL and marks fresh wallets
  kalshi <query> [--series TICKER] [--pages N]
                                           open Kalshi markets whose title contains all query words, with yes bid/ask,
                                           most traded first
  edge <ref> --estimate P [--outcome N] [--size USD]
                                           your probability vs the price: edge, expected return, break-even, return if
                                           right, annualized expected return to the end date (fees not included)
  bonds [--min-price P] [--min-days N] [--max-days N] [--min-liquidity USD] [--limit N]
                                           near-certain outcomes close to resolution: price, return if it resolves as
                                           priced, annualized, with risk flags
  watch add <ref> [--move P] [--note TEXT] | watch add-wallet <wallet> [--note TEXT] | watch list | watch remove <id>
  watch check                              compare the watchlist with the last snapshot: price moves over the threshold,
                                           closing within 48 h, resolution status changes, new large trades of watched
                                           wallets; saves a new snapshot; "alerts" is empty when nothing happened
  report-path <topic>                      the path for today's report file (files/poly/reports/<date>-<topic>.md)
"""
import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("POLY_ROOT") or Path(__file__).resolve().parents[2])
DATA = ROOT / "files" / "poly"
PROFILE = DATA / "profile" / "poly-profile.md"
SETTINGS = DATA / "settings.json"
WATCH = DATA / "watch" / "watchlist.json"
SNAP = DATA / "snapshots" / "watch-last.json"
REPORTS = DATA / "reports"

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
DATAAPI = "https://data-api.polymarket.com"
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
UA = "Mozilla/5.0 (compatible; ascn-poly/1.0)"
CATEGORIES = ["overall", "politics", "sports", "crypto", "culture", "economics", "tech", "finance", "weather", "mentions"]
PERIODS = {"day": "DAY", "week": "WEEK", "month": "MONTH", "all": "ALL"}


def out(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=1))
    sys.exit(code)


def fail(msg, **extra):
    out({"ok": False, "error": msg, **extra}, 1)


def get(url, params=None, tries=3):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 404):
                try:
                    return json.loads(e.read().decode("utf-8"))
                except Exception:
                    return None
        except Exception as e:  # network hiccup
            last = str(e)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"request failed: {url.split('?')[0]} ({last})")


def now():
    return datetime.now(timezone.utc)


def iso(ts):
    return datetime.fromtimestamp(int(ts), timezone.utc).isoformat(timespec="minutes")


def parse_dt(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00").replace(" ", "T"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def days_left(end):
    dt = parse_dt(end)
    return None if not dt else round((dt - now()).total_seconds() / 86400, 2)


def jl(v):
    if isinstance(v, list):
        return v
    try:
        return json.loads(v or "[]")
    except Exception:
        return []


def num(v, nd=4):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return round(f, nd) if math.isfinite(f) else None


def money(v):
    return None if v is None else round(float(v), 2)


def short(text, n=1500):
    text = (text or "").strip()
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def read_json(p, default):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def settings():
    s = {"language": "ru", "min_liquidity": 5000, "move_alert": 0.05, "whale_min_usd": 10000, "bonds_min_price": 0.95}
    s.update(read_json(SETTINGS, {}))
    return s


# ---------- resolving a market reference ----------

def slug_from(ref):
    ref = ref.strip()
    if ref.startswith("http"):
        path = [p for p in urllib.parse.urlparse(ref).path.split("/") if p]
        if "event" in path:
            rest = path[path.index("event") + 1:]
            return rest[-1] if rest else None, rest[0] if rest else None
        if "market" in path:
            rest = path[path.index("market") + 1:]
            return (rest[0] if rest else None), None
        return path[-1] if path else None, None
    return ref, None


def resolve(ref):
    """Returns (event or None, [markets]) for a link, slug or condition id."""
    ref = ref.strip()
    if re.fullmatch(r"0x[0-9a-fA-F]{64}", ref):
        ms = get(f"{GAMMA}/markets", {"condition_ids": ref}) or get(f"{GAMMA}/markets", {"condition_ids": ref, "closed": "true"}) or []
        return None, ms
    slug, event_slug = slug_from(ref)
    if not slug:
        fail("could not read a market from the reference", ref=ref)
    ms = get(f"{GAMMA}/markets", {"slug": slug}) or get(f"{GAMMA}/markets", {"slug": slug, "closed": "true"}) or []
    if ms:
        return None, ms
    evs = get(f"{GAMMA}/events", {"slug": event_slug or slug}) or get(f"{GAMMA}/events", {"slug": event_slug or slug, "closed": "true"}) or []
    if evs:
        return evs[0], evs[0].get("markets") or []
    found = get(f"{GAMMA}/public-search", {"q": slug.replace("-", " "), "limit_per_type": 3}) or {}
    cands = [e.get("slug") for e in found.get("events") or []]
    fail("market not found", ref=ref, did_you_mean=cands)


def market_row(m, brief=True):
    outs, prices = jl(m.get("outcomes")), jl(m.get("outcomePrices"))
    row = {
        "question": m.get("question"),
        "slug": m.get("slug"),
        "url": f"https://polymarket.com/market/{m.get('slug')}",
        "outcomes": [{"name": o, "price": num(p)} for o, p in zip(outs, prices)],
        "best_bid": num(m.get("bestBid")),
        "best_ask": num(m.get("bestAsk")),
        "spread": num(m.get("spread")),
        "last": num(m.get("lastTradePrice")),
        "volume_24h": money(m.get("volume24hr")),
        "volume_total": money(m.get("volumeNum") or m.get("volume")),
        "liquidity": money(m.get("liquidityNum") or m.get("liquidity")),
        "end": m.get("endDate"),
        "days_left": days_left(m.get("endDate")),
        "change_1d": num(m.get("oneDayPriceChange")),
        "change_1w": num(m.get("oneWeekPriceChange")),
        "accepting_orders": m.get("acceptingOrders"),
    }
    if not brief:
        row.update({
            "condition_id": m.get("conditionId"),
            "token_ids": jl(m.get("clobTokenIds")),
            "change_1h": num(m.get("oneHourPriceChange")),
            "change_1m": num(m.get("oneMonthPriceChange")),
            "rules": short(m.get("description"), 2500),
            "resolution_source": m.get("resolutionSource") or None,
            "uma_status": m.get("umaResolutionStatus") or None,
            "uma_statuses": jl(m.get("umaResolutionStatuses")),
            "closed": m.get("closed"),
            "neg_risk": m.get("negRisk"),
            "fees_enabled": m.get("feesEnabled"),
            "taker_fee_bps": m.get("takerBaseFee"),
            "fee_schedule": m.get("feeSchedule"),
            "min_order": m.get("orderMinSize"),
            "tick": m.get("orderPriceMinTickSize"),
            "rewards": {"min_size": m.get("rewardsMinSize"), "max_spread": m.get("rewardsMaxSpread")}
            if m.get("rewardsMinSize") else None,
        })
    return row


def fee_rate(m):
    """Taker fee rate from the market's fee schedule (fee = shares x rate x p x (1 - p)); 0 when fees are off."""
    if not m or not m.get("feesEnabled"):
        return 0.0
    fs = m.get("feeSchedule") or {}
    try:
        return float(fs.get("rate") or 0)
    except (TypeError, ValueError):
        return 0.0


def book_stats(token, size_usd, rate=0.0):
    b = get(f"{CLOB}/book", {"token_id": token})
    if not b or "bids" not in b:
        return {"available": False}
    bids = sorted(((float(x["price"]), float(x["size"])) for x in b.get("bids", [])), reverse=True)
    asks = sorted((float(x["price"]), float(x["size"])) for x in b.get("asks", []))
    res = {"available": True, "best_bid": bids[0][0] if bids else None, "best_ask": asks[0][0] if asks else None}
    if bids and asks:
        mid = (bids[0][0] + asks[0][0]) / 2
        res["mid"] = round(mid, 4)
        for c in (0.02, 0.05):
            res[f"bid_depth_usd_within_{int(c * 100)}c"] = round(sum(p * s for p, s in bids if p >= mid - c), 2)
            res[f"ask_depth_usd_within_{int(c * 100)}c"] = round(sum(p * s for p, s in asks if p <= mid + c), 2)
    if size_usd and asks:
        left, shares, cost = size_usd, 0.0, 0.0
        for p, s in asks:
            take = min(left, p * s)
            shares += take / p
            cost += take
            left -= take
            if left <= 1e-9:
                break
        res["buy"] = {"usd": size_usd, "filled_usd": round(cost, 2), "shares": round(shares, 2),
                      "avg_price": round(cost / shares, 4) if shares else None,
                      "slippage_vs_best": round(cost / shares - asks[0][0], 4) if shares else None,
                      "fully_filled": left <= 1e-6}
        if rate and shares:
            avg = cost / shares
            fee = shares * rate * avg * (1 - avg)
            res["buy"].update({"taker_fee_usd": round(fee, 2), "avg_price_with_fee": round((cost + fee) / shares, 4)})
    return res


# ---------- commands ----------

def cmd_context(a):
    prof = PROFILE.read_text(encoding="utf-8") if PROFILE.exists() else ""
    filled = [l for l in prof.splitlines() if ":" in l and not l.strip().startswith("#")
              and l.split(":", 1)[1].strip() and not l.split(":", 1)[1].strip().startswith("(")
              and not l.startswith("Updated")]
    wl = read_json(WATCH, {"markets": [], "wallets": []})
    reps = sorted(REPORTS.glob("*.md"), reverse=True)[:5] if REPORTS.exists() else []
    out({"ok": True, "profile_filled": bool(filled), "profile": prof.strip() if filled else "",
         "watch": {"markets": len(wl.get("markets", [])), "wallets": len(wl.get("wallets", []))},
         "settings": settings(), "recent_reports": [str(p.relative_to(ROOT)) for p in reps],
         "today_utc": now().date().isoformat()})


def cmd_search(a):
    r = get(f"{GAMMA}/public-search", {"q": a.query, "limit_per_type": a.limit, "events_status": "active"}) or {}
    events = []
    for e in r.get("events") or []:
        ms = [market_row(m) for m in (e.get("markets") or []) if not m.get("closed")]
        ms.sort(key=lambda x: -(x["volume_24h"] or 0))
        events.append({"title": e.get("title"), "slug": e.get("slug"), "url": f"https://polymarket.com/event/{e.get('slug')}",
                       "end": e.get("endDate"), "volume_24h": money(e.get("volume24hr")),
                       "markets": len(ms), "top_markets": ms[:5]})
    out({"ok": True, "query": a.query, "events": events})


def open_markets(a, limit):
    rows = []
    if a.query:
        r = get(f"{GAMMA}/public-search", {"q": a.query, "limit_per_type": 20, "events_status": "active"}) or {}
        for e in r.get("events") or []:
            rows += [m for m in e.get("markets") or [] if not m.get("closed")]
    elif a.tag:
        for off in (0, 100):
            evs = get(f"{GAMMA}/events", {"tag_slug": a.tag, "active": "true", "closed": "false", "limit": 100,
                                          "offset": off, "order": "volume24hr", "ascending": "false"}) or []
            for e in evs:
                rows += [m for m in e.get("markets") or [] if not m.get("closed")]
            if len(evs) < 100:
                break
    else:
        order = {"liquidity": "liquidityNum", "closing": "endDate"}.get(a.sort, "volume24hr")
        params = {"active": "true", "closed": "false", "limit": max(limit, 200), "order": order,
                  "ascending": "true" if a.sort == "closing" else "false"}
        if a.min_liquidity:
            params["liquidity_num_min"] = a.min_liquidity
        if a.closing_days:
            params["end_date_min"] = now().isoformat(timespec="seconds").replace("+00:00", "Z")
            params["end_date_max"] = datetime.fromtimestamp(time.time() + a.closing_days * 86400, timezone.utc) \
                .isoformat(timespec="seconds").replace("+00:00", "Z")
        rows = get(f"{GAMMA}/markets", params) or []
    return rows


def cmd_scan(a):
    rows = [market_row(m) for m in open_markets(a, a.limit) if m.get("acceptingOrders", True)]
    keep = []
    for r in rows:
        yes = r["outcomes"][0]["price"] if r["outcomes"] else None
        if a.min_liquidity and (r["liquidity"] or 0) < a.min_liquidity:
            continue
        if a.min_volume and (r["volume_24h"] or 0) < a.min_volume:
            continue
        if a.closing_days and (r["days_left"] is None or r["days_left"] < 0 or r["days_left"] > a.closing_days):
            continue
        if a.price_min is not None and (yes is None or yes < a.price_min):
            continue
        if a.price_max is not None and (yes is None or yes > a.price_max):
            continue
        keep.append(r)
    seen, uniq = set(), []
    for r in keep:
        if r["slug"] not in seen:
            seen.add(r["slug"])
            uniq.append(r)
    key = {"liquidity": lambda r: -(r["liquidity"] or 0), "closing": lambda r: (r["days_left"] if r["days_left"] is not None else 1e9),
           "move": lambda r: -abs(r["change_1d"] or 0)}.get(a.sort, lambda r: -(r["volume_24h"] or 0))
    uniq.sort(key=key)
    out({"ok": True, "filters": {k: v for k, v in vars(a).items() if k not in ("func", "cmd") and v not in (None, False)},
         "count": len(uniq), "markets": uniq[:a.limit]})


def cmd_market(a):
    ev, ms = resolve(a.ref)
    if not ms:
        fail("no markets in this event", ref=a.ref)
    if ev and len(ms) > 1:
        rows = [market_row(m) for m in ms if not m.get("closed")]
        rows.sort(key=lambda r: -((r["outcomes"][0]["price"] or 0) if r["outcomes"] else 0))
        exclusive = bool(ev.get("negRisk") or ev.get("enableNegRisk"))
        yes_sum = round(sum((r["outcomes"][0]["price"] or 0) for r in rows if r["outcomes"]), 4) if exclusive else None
        out({"ok": True, "type": "event", "title": ev.get("title"), "url": f"https://polymarket.com/event/{ev.get('slug')}",
             "end": ev.get("endDate"), "days_left": days_left(ev.get("endDate")), "volume_24h": money(ev.get("volume24hr")),
             "volume_total": money(ev.get("volume")), "neg_risk": ev.get("negRisk"),
             "rules": short(ev.get("description"), 2500), "resolution_source": ev.get("resolutionSource") or None,
             "yes_prices_sum": yes_sum,
             "exclusive_outcomes": exclusive,
             "note": "Exclusive outcomes (only one can win): the Yes prices should add up to about 1, and a sum far from 1 "
                     "means a thin book. Not exclusive (for example price ladders): each market is a separate bet."
                     if exclusive else "Outcomes are not exclusive: each market is a separate bet; do not add the prices.",
             "markets": rows, "next": "Run market <slug> on one outcome for its order book and rules."})
    m = ms[0]
    row = market_row(m, brief=False)
    toks = row["token_ids"]
    rate = fee_rate(m)
    row["order_book"] = {o["name"]: book_stats(t, a.size, rate) for o, t in zip(row["outcomes"], toks)} if toks else {}
    if ev:
        row["event"] = {"title": ev.get("title"), "url": f"https://polymarket.com/event/{ev.get('slug')}"}
    flags = []
    if row["spread"] is not None and row["spread"] >= 0.05:
        flags.append("wide spread: the displayed price is far from what you can trade at")
    if (row["liquidity"] or 0) < settings()["min_liquidity"]:
        flags.append("thin liquidity: a few traders can move the price")
    if row["days_left"] is not None and row["days_left"] < 0:
        flags.append("end date passed: waiting for resolution")
    if row["uma_status"] and row["uma_status"] not in ("resolved",):
        flags.append(f"resolution status: {row['uma_status']}")
    if not row["resolution_source"]:
        flags.append("no single resolution source named: read the rules text")
    if row["fees_enabled"]:
        flags.append(f"taker fee on this market: shares x {fee_rate(m)} x p x (1 - p); 'avg_price_with_fee' includes it")
    try:
        rs = (get(f"{DATAAPI}/v2/resolutions", {"condition": row["condition_id"]}) or {}).get("data") or []
        ended = row["days_left"] is not None and row["days_left"] < 0
        if rs and (ended or row["uma_status"] or rs[0].get("was_disputed")):
            row["resolution"] = {k: rs[0].get(k) for k in ("status", "was_disputed", "extended_review", "proposed_price")}
            if rs[0].get("was_disputed"):
                flags.append("the proposed outcome was disputed: expect delay and read the rules closely")
        oi = (get(f"{DATAAPI}/v2/oi", {"condition": row["condition_id"]}) or {}).get("data") or []
        row["open_interest"] = money(oi[0].get("value")) if oi else None
    except RuntimeError:
        row["resolution"] = None
    row["flags"] = flags
    row["fetched_at"] = now().isoformat(timespec="seconds")
    out({"ok": True, "type": "market", **row})


def pick_token(ref, outcome):
    ev, ms = resolve(ref)
    if ev and len(ms) > 1:
        fail("this is an event with several markets: pass one market slug", markets=[m.get("slug") for m in ms][:30])
    m = ms[0]
    toks, outs = jl(m.get("clobTokenIds")), jl(m.get("outcomes"))
    if outcome >= len(toks):
        fail("no such outcome", outcomes=outs)
    return m, toks[outcome], outs[outcome]


def cmd_history(a):
    m, tok, name = pick_token(a.ref, a.outcome)
    fid = {"1d": 10, "1w": 60, "1m": 360, "max": 1440}.get(a.interval, 60)
    h = (get(f"{CLOB}/prices-history", {"market": tok, "interval": a.interval, "fidelity": fid}) or {}).get("history") or []
    if not h:
        out({"ok": True, "question": m.get("question"), "outcome": name, "points": 0, "note": "no price history"})
    ps = [x["p"] for x in h]
    step = max(1, len(h) // 24)
    out({"ok": True, "question": m.get("question"), "outcome": name, "interval": a.interval, "points": len(h),
         "first": {"t": iso(h[0]["t"]), "p": ps[0]}, "last": {"t": iso(h[-1]["t"]), "p": ps[-1]},
         "min": min(ps), "max": max(ps), "change": round(ps[-1] - ps[0], 4),
         "sample": [{"t": iso(x["t"]), "p": x["p"]} for x in h[::step]]})


def cmd_holders(a):
    ev, ms = resolve(a.ref)
    if ev and len(ms) > 1:
        fail("this is an event with several markets: pass one market slug", markets=[m.get("slug") for m in ms][:30])
    m = ms[0]
    outs = jl(m.get("outcomes"))
    r = get(f"{DATAAPI}/holders", {"market": m.get("conditionId"), "limit": a.limit}) or []
    res = []
    for grp in r:
        hs = grp.get("holders") or []
        idx = hs[0].get("outcomeIndex", 0) if hs else 0
        amounts = [float(h.get("amount") or 0) for h in hs]
        tot = sum(amounts) or 1
        res.append({"outcome": outs[idx] if idx < len(outs) else idx,
                    "listed_shares": round(sum(amounts), 2),
                    "top1_share_of_listed": round(amounts[0] / tot, 3) if amounts else None,
                    "top5_share_of_listed": round(sum(amounts[:5]) / tot, 3) if amounts else None,
                    "holders": [{"name": h.get("name") or h.get("pseudonym"), "wallet": h.get("proxyWallet"),
                                 "shares": round(float(h.get("amount") or 0), 2)} for h in hs]})
    out({"ok": True, "question": m.get("question"), "note": "Shares are counted among the listed top holders only.",
         "outcomes": res})


def lb(period="month", by="pnl", category="overall", limit=20, user=None):
    p = {"timePeriod": PERIODS.get(period, "MONTH"), "orderBy": by.upper(), "limit": limit}
    if category and category != "overall":
        p["category"] = category.upper()
    if user:
        p["user"] = user
    return get(f"{DATAAPI}/v1/leaderboard", p) or []


def cmd_leaderboard(a):
    rows = lb(a.period, a.by, a.category, a.limit)
    out({"ok": True, "period": a.period, "by": a.by, "category": a.category,
         "traders": [{"rank": r.get("rank"), "name": r.get("userName"), "x": r.get("xUsername") or None,
                      "wallet": r.get("proxyWallet"), "pnl": money(r.get("pnl")), "volume": money(r.get("vol")),
                      "profile": f"https://polymarket.com/profile/{r.get('proxyWallet')}"} for r in rows]})


def wallet_of(who):
    who = who.strip()
    if re.fullmatch(r"0x[0-9a-fA-F]{40}", who):
        return who.lower(), None
    r = get(f"{GAMMA}/public-search", {"q": who.lstrip("@"), "search_profiles": "true", "limit_per_type": 5}) or {}
    profs = r.get("profiles") or []
    exact = [p for p in profs if (p.get("name") or "").lower() == who.lstrip("@").lower()]
    p = (exact or profs or [None])[0]
    if not p:
        fail("no Polymarket profile with this name", who=who)
    return p["proxyWallet"].lower(), p.get("name")


def trader_data(who, npos=15):
    w, name = wallet_of(who)
    pos = get(f"{DATAAPI}/positions", {"user": w, "limit": 200, "sortBy": "CURRENT", "sortDirection": "DESC",
                                       "sizeThreshold": 1}) or []
    value = get(f"{DATAAPI}/value", {"user": w}) or []
    act = get(f"{DATAAPI}/activity", {"user": w, "limit": 15, "type": "TRADE"}) or []
    ranks = {}
    for per in ("month", "all"):
        r = lb(per, "pnl", "overall", 1, user=w)
        if r:
            ranks[per] = {"rank": r[0].get("rank"), "pnl": money(r[0].get("pnl")), "volume": money(r[0].get("vol"))}
            name = name or r[0].get("userName")
    positions = [{"title": p.get("title"), "slug": p.get("slug"), "outcome": p.get("outcome"),
                  "shares": round(p.get("size") or 0, 2), "avg_price": num(p.get("avgPrice")), "price_now": num(p.get("curPrice")),
                  "value": money(p.get("currentValue")), "pnl": money(p.get("cashPnl")), "pnl_pct": num(p.get("percentPnl"), 1),
                  "end": p.get("endDate"), "days_left": days_left(p.get("endDate")), "redeemable": p.get("redeemable")}
                 for p in pos]
    for p in positions:
        if p["price_now"] in (0, 0.0) and (p["redeemable"] or (p["days_left"] or 0) < 0):
            p["status"] = "resolved: lost"
        elif p["redeemable"] and (p["price_now"] or 0) >= 0.99:
            p["status"] = "resolved: won, claim in the Polymarket app"
        elif (p["days_left"] or 0) < 0:
            p["status"] = "ended, waiting for resolution"
        else:
            p["status"] = "open"
    lost = [p for p in positions if p["status"] == "resolved: lost"]
    positions = [p for p in positions if p not in lost]
    return w, name, value, ranks, positions, act, lost, len(pos) >= 200


def cmd_trader(a, mine=False):
    w, name, value, ranks, positions, act, lost, capped = trader_data(a.who)
    res = {"ok": True, "wallet": w, "name": name, "profile": f"https://polymarket.com/profile/{w}",
           "portfolio_value": money(value[0]["value"]) if value else None, "leaderboard": ranks,
           "open_positions": sum(1 for p in positions if p["status"] == "open"), "open_pnl_total": money(sum(p["pnl"] or 0 for p in positions)),
           "lost_positions_not_shown": len(lost),
           "note": "Only the 200 largest positions were loaded; totals cover those." if capped else None,
           "positions": positions[:getattr(a, "positions", 15)],
           "recent_trades": [{"time": iso(x["timestamp"]), "side": x.get("side"), "outcome": x.get("outcome"),
                              "price": num(x.get("price")), "usd": money(x.get("usdcSize")), "title": x.get("title")}
                             for x in act]}
    if mine:
        res["flags"] = {
            "to_claim": [p for p in positions if p["status"].startswith("resolved: won")],
            "closing_7d": [p for p in positions if p["status"] == "open" and p["days_left"] is not None and 0 <= p["days_left"] <= 7],
            "big_losses": [p for p in positions if p["status"] == "open" and (p["pnl_pct"] or 0) <= -40 and (p["value"] or 0) >= 10],
            "lost_resolved": lost,
        }
        res["positions"] = positions
    out(res)


def cmd_smart(a):
    top = lb(a.period, "pnl", a.category, a.top)
    agg = {}
    for t in top:
        w = t.get("proxyWallet")
        for p in get(f"{DATAAPI}/positions", {"user": w, "limit": 100, "sortBy": "CURRENT", "sortDirection": "DESC",
                                              "sizeThreshold": 1}) or []:
            if p.get("redeemable") or (p.get("curPrice") or 0) in (0, 1):
                continue
            if (days_left(p.get("endDate")) or 99) < 1:
                continue  # minute and hourly markets say nothing about a view
            k = (p.get("slug"), p.get("outcome"))
            g = agg.setdefault(k, {"title": p.get("title"), "slug": p.get("slug"), "outcome": p.get("outcome"),
                                   "traders": [], "value": 0.0, "price_now": num(p.get("curPrice")),
                                   "end": p.get("endDate")})
            g["traders"].append({"name": t.get("userName"), "rank": t.get("rank"), "avg_price": num(p.get("avgPrice")),
                                 "value": money(p.get("currentValue"))})
            g["value"] += p.get("currentValue") or 0
    rows = [g for g in agg.values() if len(g["traders"]) >= a.min_traders]
    for g in rows:
        g["value"] = money(g["value"])
        g["n_traders"] = len(g["traders"])
        g["days_left"] = days_left(g["end"])
    rows.sort(key=lambda g: (-g["n_traders"], -g["value"]))
    out({"ok": True, "top_traders": len(top), "period": a.period, "category": a.category,
         "note": "Positions of top PnL traders right now; a trader may hedge elsewhere, and past profit says nothing "
                 "certain about this bet.", "markets": rows[:40]})


def cmd_whales(a):
    p = {"limit": a.limit, "filterType": "CASH", "filterAmount": a.min, "takerOnly": "true"}
    title = None
    if a.ref:
        ev, ms = resolve(a.ref)
        p["market"] = ",".join(m.get("conditionId") for m in ms[:20])
        title = ev.get("title") if ev else ms[0].get("question")
    tr = get(f"{DATAAPI}/trades", p) or []
    stats = {}
    if a.fresh:
        for w in list(dict.fromkeys(x.get("proxyWallet") for x in tr))[:15]:
            d = (get(f"{DATAAPI}/v2/user-stats", {"user": w}) or {}).get("data") or {}
            if d:
                age = (time.time() - d["join_date"]) / 86400 if d.get("join_date") else None
                pnl = (d.get("all_time_pnl") or {}).get("realized_pnl")
                stats[w] = {"days_on_polymarket": round(age) if age is not None else None, "trades_total": d.get("trades"),
                            "realized_pnl": money(pnl),
                            "fresh_wallet": bool((age is not None and age <= 30) or (d.get("trades") or 0) <= 10)}
    out({"ok": True, "market": title, "min_usd": a.min,
         "note": "A fresh wallet with a large bet can mean inside knowledge, a whale's new account or just a new user: "
                 "a reason to look closer, never proof." if a.fresh else None,
         "trades": [{"wallet_stats": stats.get(x.get("proxyWallet")),"time": iso(x["timestamp"]), "name": x.get("name") or x.get("pseudonym"), "wallet": x.get("proxyWallet"),
                     "side": x.get("side"), "outcome": x.get("outcome"), "price": num(x.get("price")),
                     "usd": money((x.get("size") or 0) * (x.get("price") or 0)), "title": x.get("title"),
                     "slug": x.get("slug")} for x in tr]})


def cmd_kalshi(a):
    words = [w for w in re.findall(r"\w+", a.query.lower()) if len(w) > 1]
    found, cursor = [], None
    for _ in range(a.pages):
        r = get(f"{KALSHI}/events", {"limit": 200, "status": "open", "with_nested_markets": "true", "cursor": cursor,
                                     "series_ticker": a.series, "mve_filter": "exclude"}) or {}
        for e in r.get("events") or []:
            for m in e.get("markets") or []:
                text = " ".join(str(x or "") for x in (e.get("title"), e.get("sub_title"), m.get("title"),
                                                        m.get("yes_sub_title"))).lower()
                if all(w in text for w in words):
                    found.append({"event": e.get("title"), "market": m.get("title"), "option": m.get("yes_sub_title"),
                                  "ticker": m.get("ticker"), "yes_bid": num(m.get("yes_bid_dollars")),
                                  "yes_ask": num(m.get("yes_ask_dollars")), "last": num(m.get("last_price_dollars")),
                                  "volume": m.get("volume_fp") or m.get("volume"), "close": m.get("close_time"),
                                  "url": f"https://kalshi.com/markets/{(e.get('series_ticker') or '').lower()}"})
        cursor = r.get("cursor")
        if not cursor:
            break
    def vol(m):
        try:
            return -float(m["volume"] or 0)
        except (TypeError, ValueError):
            return 0
    found.sort(key=vol)
    out({"ok": True, "query": a.query, "series": a.series, "count": len(found), "markets": found[:40],
         "note": "Kalshi rules and resolution sources can differ from Polymarket's: compare the wording before "
                 "treating two markets as the same bet. Pages searched are limited; no match is not proof of absence."})


def cmd_edge(a):
    if not 0 < a.estimate < 1:
        fail("estimate must be a probability between 0 and 1")
    m, tok, name = pick_token(a.ref, a.outcome)
    rate = fee_rate(m)
    bk = book_stats(tok, a.size or 100, rate)
    ask = (bk.get("buy") or {}).get("avg_price") or bk.get("best_ask")
    if not ask:
        prices = jl(m.get("outcomePrices"))
        ask = float(prices[a.outcome]) if a.outcome < len(prices) else None
    if not ask or ask >= 1:
        fail("no price to buy at", book=bk)
    if rate:
        ask = ask + rate * ask * (1 - ask)
    d = days_left(m.get("endDate"))
    exp = a.estimate / ask - 1
    res = {"ok": True, "question": m.get("question"), "outcome": name, "your_estimate": a.estimate,
           "buy_price": round(ask, 4), "price_source": "order book" if bk.get("available") else "last displayed price",
           "edge_points": round(a.estimate - ask, 4), "break_even_probability": round(ask, 4),
           "return_if_right": round(1 / ask - 1, 4), "expected_return": round(exp, 4),
           "days_left": d, "taker_fee_rate": rate,
           "note": "Buy price includes the taker fee when the market charges one; a limit order that rests in the book "
                   "pays no fee. Expected return assumes your estimate is right and the market resolves as the rules say."}
    if d and d > 0 and exp > -1:
        res["annualized_expected_return"] = round((1 + exp) ** (365 / max(d, 1)) - 1, 4) if d >= 1 else None
    if a.size:
        res["size_usd"] = a.size
        res["fill"] = bk.get("buy")
    out(res)


def cmd_bonds(a):
    params = {"active": "true", "closed": "false", "limit": 500, "order": "endDate", "ascending": "true",
              "end_date_min": datetime.fromtimestamp(time.time() + a.min_days * 86400, timezone.utc)
              .isoformat(timespec="seconds").replace("+00:00", "Z"),
              "end_date_max": datetime.fromtimestamp(time.time() + a.max_days * 86400, timezone.utc)
              .isoformat(timespec="seconds").replace("+00:00", "Z"),
              "liquidity_num_min": a.min_liquidity}
    rows = []
    for m in get(f"{GAMMA}/markets", params) or []:
        if not m.get("acceptingOrders", True):
            continue
        if (days_left(m.get("endDate")) or 0) < a.min_days:
            continue
        start = parse_dt(m.get("gameStartTime"))
        if start and start <= now():
            continue  # a game already in play: prices move by the minute
        outs, prices = jl(m.get("outcomes")), jl(m.get("outcomePrices"))
        ask_yes, bid_yes = num(m.get("bestAsk")), num(m.get("bestBid"))
        for i, (o, p) in enumerate(zip(outs, prices)):
            p = num(p)
            if p is None or not (a.min_price <= p < 0.995):
                continue
            buy = ask_yes if i == 0 else (round(1 - bid_yes, 4) if bid_yes else None)
            buy = buy if buy and buy < 1 else p
            d = days_left(m.get("endDate"))
            rate = fee_rate(m)
            if rate:
                buy = round(buy + rate * buy * (1 - buy), 4)
            r = 1 / buy - 1
            flags = []
            if (m.get("spread") or 0) >= 0.03:
                flags.append("wide spread")
            if m.get("umaResolutionStatus") and m.get("umaResolutionStatus") != "resolved":
                flags.append(f"resolution status: {m.get('umaResolutionStatus')}")
            if not m.get("resolutionSource"):
                flags.append("no single resolution source: read the rules")
            if rate:
                flags.append("taker fee included")
            rows.append({"question": m.get("question"), "slug": m.get("slug"), "outcome": o, "price": p, "buy_at": buy,
                         "return_if_resolves_as_priced": round(r, 4),
                         "annualized": round((1 + r) ** (365 / d) - 1, 2) if d and d >= 3 else None,
                         "days_left": d, "liquidity": money(m.get("liquidityNum")), "flags": flags})
    rows.sort(key=lambda r: (-(r["annualized"] or 0), -r["return_if_resolves_as_priced"]))
    out({"ok": True, "count": len(rows), "markets": rows[:a.limit],
         "note": "The missing few cents are the price of the risk that the outcome does not happen or the rules are read "
                 "differently. One surprise loses the whole stake. Annualized only from 3 days left; games already in play are skipped."})


def cmd_watch(a):
    wl = read_json(WATCH, {"markets": [], "wallets": []})
    if a.action == "list":
        out({"ok": True, **wl})
    if a.action == "remove":
        before = len(wl["markets"]) + len(wl["wallets"])
        t = a.target.strip().lower()
        hit = lambda x: t in (str(x.get("id")).lower(), str(x.get("name") or "").lower())
        wl["markets"] = [x for x in wl["markets"] if not hit(x)]
        wl["wallets"] = [x for x in wl["wallets"] if not hit(x)]
        write_json(WATCH, wl)
        out({"ok": True, "removed": before - len(wl["markets"]) - len(wl["wallets"])})
    if a.action == "add":
        ev, ms = resolve(a.target)
        added = []
        for m in ms[:30]:
            if m.get("closed"):
                continue
            item = {"id": m.get("slug"), "question": m.get("question"), "condition_id": m.get("conditionId"),
                    "move": a.move or settings()["move_alert"], "note": a.note, "added": now().date().isoformat()}
            wl["markets"] = [x for x in wl["markets"] if x["id"] != item["id"]] + [item]
            added.append(item["id"])
        write_json(WATCH, wl)
        out({"ok": True, "added": added, "total": len(wl["markets"])})
    if a.action == "add-wallet":
        w, name = wallet_of(a.target)
        item = {"id": w, "name": name, "note": a.note, "added": now().date().isoformat()}
        wl["wallets"] = [x for x in wl["wallets"] if x["id"] != w] + [item]
        write_json(WATCH, wl)
        out({"ok": True, "added": w, "name": name})
    if a.action == "check":
        snap = read_json(SNAP, {"markets": {}, "wallets": {}, "at": None})
        new = {"markets": {}, "wallets": {}, "at": now().isoformat(timespec="seconds")}
        alerts = []
        whale_min = settings()["whale_min_usd"]
        for item in wl["markets"]:
            ms = get(f"{GAMMA}/markets", {"slug": item["id"]}) or []
            if not ms:
                continue
            m = ms[0]
            row = market_row(m, brief=False)
            price = row["outcomes"][0]["price"] if row["outcomes"] else None
            new["markets"][item["id"]] = {"price": price, "uma": row["uma_status"], "closed": row["closed"]}
            old = snap["markets"].get(item["id"])
            if old and price is not None and old.get("price") is not None and abs(price - old["price"]) >= item["move"]:
                alerts.append({"type": "move", "question": row["question"], "from": old["price"], "to": price,
                               "url": row["url"]})
            if old and row["uma_status"] != old.get("uma"):
                alerts.append({"type": "resolution", "question": row["question"], "status": row["uma_status"],
                               "url": row["url"]})
            if row["days_left"] is not None and 0 <= row["days_left"] <= 2 and not (old or {}).get("closing_alerted"):
                alerts.append({"type": "closing", "question": row["question"], "days_left": row["days_left"],
                               "url": row["url"]})
                new["markets"][item["id"]]["closing_alerted"] = True
            elif (old or {}).get("closing_alerted"):
                new["markets"][item["id"]]["closing_alerted"] = True
        for item in wl["wallets"]:
            act = get(f"{DATAAPI}/activity", {"user": item["id"], "limit": 30, "type": "TRADE"}) or []
            last_seen = (snap["wallets"].get(item["id"]) or {}).get("last_ts", 0)
            new["wallets"][item["id"]] = {"last_ts": max([x["timestamp"] for x in act] + [last_seen])}
            if snap.get("at") is None:
                continue
            for x in act:
                if x["timestamp"] > last_seen and (x.get("usdcSize") or 0) >= whale_min:
                    alerts.append({"type": "wallet_trade", "who": item.get("name") or item["id"], "side": x.get("side"),
                                   "outcome": x.get("outcome"), "price": num(x.get("price")), "usd": money(x.get("usdcSize")),
                                   "title": x.get("title"), "time": iso(x["timestamp"])})
        write_json(SNAP, new)
        out({"ok": True, "checked": {"markets": len(wl["markets"]), "wallets": len(wl["wallets"])},
             "first_run": snap.get("at") is None, "since": snap.get("at"), "alerts": alerts})


def cmd_report_path(a):
    topic = re.sub(r"[^\w-]+", "-", a.topic.lower()).strip("-")[:60] or "report"
    REPORTS.mkdir(parents=True, exist_ok=True)
    out({"ok": True, "path": str((REPORTS / f"{now().date().isoformat()}-{topic}.md").relative_to(ROOT))})


def main():
    ap = argparse.ArgumentParser(description="Polymarket analyst toolkit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("context").set_defaults(func=cmd_context)
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--limit", type=int, default=8); p.set_defaults(func=cmd_search)
    p = sub.add_parser("scan")
    p.add_argument("--tag"); p.add_argument("--query")
    p.add_argument("--sort", choices=["volume", "liquidity", "closing", "move"], default="volume")
    p.add_argument("--min-liquidity", type=float); p.add_argument("--min-volume", type=float)
    p.add_argument("--closing-days", type=float); p.add_argument("--price-min", type=float); p.add_argument("--price-max", type=float)
    p.add_argument("--limit", type=int, default=20); p.set_defaults(func=cmd_scan)
    p = sub.add_parser("market"); p.add_argument("ref"); p.add_argument("--size", type=float, default=500); p.set_defaults(func=cmd_market)
    p = sub.add_parser("history"); p.add_argument("ref"); p.add_argument("--interval", choices=["1d", "1w", "1m", "max"], default="1w")
    p.add_argument("--outcome", type=int, default=0); p.set_defaults(func=cmd_history)
    p = sub.add_parser("holders"); p.add_argument("ref"); p.add_argument("--limit", type=int, default=20); p.set_defaults(func=cmd_holders)
    p = sub.add_parser("leaderboard"); p.add_argument("--period", choices=list(PERIODS), default="month")
    p.add_argument("--by", choices=["pnl", "vol"], default="pnl"); p.add_argument("--category", choices=CATEGORIES, default="overall")
    p.add_argument("--limit", type=int, default=20); p.set_defaults(func=cmd_leaderboard)
    p = sub.add_parser("trader"); p.add_argument("who"); p.add_argument("--positions", type=int, default=15); p.set_defaults(func=cmd_trader)
    p = sub.add_parser("wallet"); p.add_argument("who"); p.set_defaults(func=lambda a: cmd_trader(a, mine=True))
    p = sub.add_parser("smart"); p.add_argument("--category", choices=CATEGORIES, default="overall")
    p.add_argument("--period", choices=list(PERIODS), default="month"); p.add_argument("--top", type=int, default=15)
    p.add_argument("--min-traders", type=int, default=2); p.set_defaults(func=cmd_smart)
    p = sub.add_parser("whales"); p.add_argument("--ref"); p.add_argument("--min", type=float, default=10000)
    p.add_argument("--fresh", action="store_true", help="check each wallet's age, trade count and realized PnL")
    p.add_argument("--limit", type=int, default=25); p.set_defaults(func=cmd_whales)
    p = sub.add_parser("kalshi"); p.add_argument("query"); p.add_argument("--pages", type=int, default=15)
    p.add_argument("--series", help="a Kalshi series ticker, e.g. KXBTCD, to search one series only"); p.set_defaults(func=cmd_kalshi)
    p = sub.add_parser("edge"); p.add_argument("ref"); p.add_argument("--estimate", type=float, required=True)
    p.add_argument("--outcome", type=int, default=0); p.add_argument("--size", type=float); p.set_defaults(func=cmd_edge)
    p = sub.add_parser("bonds"); p.add_argument("--min-price", type=float, default=0.95); p.add_argument("--max-days", type=float, default=14)
    p.add_argument("--min-days", type=float, default=1)
    p.add_argument("--min-liquidity", type=float, default=5000); p.add_argument("--limit", type=int, default=20); p.set_defaults(func=cmd_bonds)
    p = sub.add_parser("watch"); p.add_argument("action", choices=["add", "add-wallet", "list", "remove", "check"])
    p.add_argument("target", nargs="?"); p.add_argument("--move", type=float); p.add_argument("--note")
    p.set_defaults(func=cmd_watch)
    p = sub.add_parser("report-path"); p.add_argument("topic"); p.set_defaults(func=cmd_report_path)
    a = ap.parse_args()
    if a.cmd == "watch" and a.action in ("add", "add-wallet", "remove") and not a.target:
        fail(f"watch {a.action} needs a target")
    if a.cmd == "smart":
        a.top = min(a.top, 25)
    try:
        a.func(a)
    except RuntimeError as e:
        fail(str(e), hint="Polymarket or Kalshi did not answer; try again in a minute. Never fill the gap with guesses.")


if __name__ == "__main__":
    main()
