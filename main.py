"""Forecast GTA VI launch-day Twitch viewers, hours 2-24, from comparables.

Deterministic and offline. For each case, learn the median post-hour-1 viewer
trajectory from past big console launches (midnight-local unlock) supplied in
the case's `comparables`, scale it to the case's hour-1 print, and emit honest
quantiles with an empirical log-residual spread.
"""
import json, math, os, statistics
from datetime import datetime

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
Z = [-1.645, -0.674, 0.0, 0.674, 1.645]


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def hourly_by_hour(comp, start):
    out = {}
    for row in comp.get("hourly", []):
        t = parse_ts(row["from"])
        h = int(round((t - start).total_seconds() / 3600.0)) + 1
        if 1 <= h <= 24:
            out[h] = max(float(row.get("viewers") or 0), 0.0)
    return out


def is_gta_like(comp, hb):
    name = (comp.get("name") or "").lower()
    if "grand theft auto vi category before release" in name:
        return False
    unlock = (comp.get("unlock") or "").lower()
    midnight = ("midnight local" in unlock) or ("rolling" in unlock and "midnight" in unlock)
    p1 = hb.get(1, 0.0)
    peak = max(hb.values()) if hb else 0.0
    return midnight and p1 > 1000 and peak > 50000


def learn_curve(comparables, exclude_name):
    ratios = {h: [] for h in range(2, 25)}
    for comp in comparables:
        name = comp.get("name", "")
        if exclude_name and exclude_name.lower() in name.lower():
            continue
        start = parse_ts(comp["day_start"])
        hb = hourly_by_hour(comp, start)
        if not is_gta_like(comp, hb):
            continue
        p1 = hb[1]
        for h in range(2, 25):
            v = hb.get(h, 0.0)
            if v > 0:
                ratios[h].append(math.log(v / p1))
    med, sd = {}, {}
    for h, vals in ratios.items():
        if len(vals) >= 4:
            m = statistics.median(vals)
            med[h] = m
            sd[h] = statistics.pstdev(vals)
    # fallbacks if a thin case
    default_med = 0.0
    default_sd = 0.30
    return med, sd, default_med, default_sd


def forecast(case):
    p1 = max(float(case["known"][0]["viewers"]), 1.0)
    med, sd, dm, ds = learn_curve(case.get("comparables", []), case.get("game", {}).get("name", ""))
    rows = []
    for row in case.get("forecast", []):
        h = int(row["hour"])
        m = med.get(h, dm)
        s = max(sd.get(h, ds), 0.05)
        qs = [round(p1 * math.exp(m + z * s), 2) for z in Z]
        qs = [min(max(q, 0.01), 1_000_000_000.0) for q in qs]
        for i in range(1, 5):
            qs[i] = max(qs[i], qs[i - 1])
        rows.append({"hour": h, "q": qs})
    return {"hours": rows}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fn in sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in")):
        cid = fn[:-3]
        with open(os.path.join(INPUT_DIR, fn), encoding="utf-8") as fh:
            case = json.load(fh)
        out = forecast(case)
        with open(os.path.join(OUTPUT_DIR, cid + ".out"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, separators=(",", ":"))


if __name__ == "__main__":
    main()
