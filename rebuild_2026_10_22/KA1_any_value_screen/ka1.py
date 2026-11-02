#!/usr/bin/env python3
"""KA1 Stage A: mechanical screen of the kappa register at any value. See FROZEN_CRITERIA.md."""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "../../campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_attempts_register.csv")
MUTATE = os.environ.get("KA1_MUTATE") == "1"
WIN = {"rho_DE": (0.227, 0.607), "rho_crit": (0.189, 0.501)}
if MUTATE:
    WIN = {"rho_DE": (100.0, 101.0), "rho_crit": (100.0, 101.0)}
DEAD = ["VOID", "EXCLUDED", "TAUTOLOG", "CIRCULAR", "CLOSURE", "TRADE", "WITHDRAWN", "ALGEBRA ERROR", "FAILS",
        "not forced", "unforced", "not integrable"]
DEAD_RE = re.compile("|".join(re.escape(w) for w in DEAD), re.I)


def determinate(r):
    try:
        float(r["kappa"])
    except (TypeError, ValueError):
        return False
    return r["cls"] in ("odd", "any", "cont")


def in_window(r):
    k = float(r["kappa"])
    return [f for f, (a, b) in WIN.items() if a <= k <= b]


def screen(rows):
    det = [r for r in rows if determinate(r)]
    win = [r for r in det if in_window(r)]
    dead, live = [], []
    for r in win:
        m = DEAD_RE.search(r["verdict"])
        (dead if m else live).append((r, m.group(0) if m else ""))
    return det, win, dead, live


def self_test():
    base = {"kid": "T", "kappa": "0.46", "cls": "odd"}
    _, _, _, live = screen([dict(base, verdict="DATA-LEVEL landing")])
    _, _, dead, _ = screen([dict(base, verdict="VOID: planted")])
    if MUTATE:
        return True
    return len(live) == 1 and len(dead) == 1


rows = list(csv.DictReader(open(REG, newline="")))
ok = self_test()
det, win, dead, live = screen(rows)
print(f"rows {len(rows)}; determinate {len(det)}; in window {len(win)}; dead {len(dead)}; live {len(live)}; planted self-test {'PASS' if ok else 'FAIL'}")
for f, (a, b) in WIN.items():
    print(f"in window {f} [{a}, {b}]: {sum(f in in_window(r) for r in det)}")
print("\nREMOVED AT STEP 3")
for r, w in dead:
    print(f"{r['kid']} {r['src']} k={r['kappa']} [{w}] {r['mechanism'][:70]} | {r['verdict'][:80]}")
print("\nDistinct values removed:", sorted({float(r['kappa']) for r, _ in dead}))
print("\nSTAGE A SURVIVORS")
for r, _ in live:
    print(f"{r['kid']} {r['src']} k={r['kappa']} cls={r['cls']} win={in_window(r)} path={r['path']}\n   {r['mechanism']}\n   {r['verdict']}")
out = "ka1_MUTATE.json" if MUTATE else "ka1.json"
json.dump({"n_rows": len(rows), "n_det": len(det), "n_win": len(win), "n_dead": len(dead), "n_live": len(live),
           "live": [r["kid"] for r, _ in live], "windows": WIN, "self_test": ok}, open(os.path.join(HERE, out), "w"), indent=1)
if MUTATE:
    print("MUTATE bites" if not win else "MUTATE FAILED")
    sys.exit(1)
sys.exit(0 if ok else 2)
