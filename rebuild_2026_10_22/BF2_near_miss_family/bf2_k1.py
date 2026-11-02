#!/usr/bin/env python3
"""BF2 K1, K2: RQ3 through this lane's loader against RQ3's own law.json; generated H = 1 against it. Then the table. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
R = os.path.dirname(os.path.abspath(__file__)); Q = os.path.join(R, "..", "RQ3_acceptance_v2", "results", "law.json"); ref = json.load(open(Q))
def cmp(a, b, tol=1e-9):
    bad = []
    for f in ref["footings"]:
        x, y = a["footings"][f]["rows"], b["footings"][f]["rows"]
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y: bad.append((f, k, "missing")); continue
            if x[k].get("label") != y[k].get("label"): bad.append((f, k, x[k].get("label"), y[k].get("label")))
            for q in ("value", "Z"):
                u, v = x[k].get(q), y[k].get(q)
                if isinstance(u, (int, float)) and isinstance(v, (int, float)) and abs(u - v) > tol * max(1, abs(u)): bad.append((f, k, q, u, v))
    return bad
ok = True
for n in ("law", "Hone"):
    b = cmp(json.load(open(os.path.join(R, "results", f"{n}.json"))), ref); print(n, "differences from RQ3 law.json:", len(b), b[:12]); ok &= not b
K = ["A1", "A2", "A3", "A4", "A9", "B23", "B24"]; KS = None
for n in ("law", "P1", "P2", "P3", "P4"):
    o = json.load(open(os.path.join(R, "results", f"{n}.json")))
    for f in ("canonical", "alt"):
        F = o["footings"][f]; r = F["rows"]; c = F["summary"]["counts"]; keys = [k for k in r if k[0] == "B" and ":" in k]; kp = sum(r[k]["label"] == "PASS" for k in keys); kf = [(k.split(":")[1], round(r[k]["Z"], 2)) for k in keys if r[k]["label"] == "FAIL"]
        print(f"\n{n} {f}: {F['summary']['overall']} {c} computed {F['summary']['computed']}; keys {kp}/15 fail {kf}; p_joint {F['summary']['joint']['p_joint']} worst {F['summary']['joint']['min_block']}; no solar next: {sorted(F['summary']['joint']['block_p'].items(), key=lambda t: t[1])[:3]}")
        print("  " + "; ".join(f"{k} {r[k]['label']} v {r[k].get('value') if not isinstance(r[k].get('value'), float) else round(r[k]['value'], 4)} Z {round(r[k].get('Z', float('nan')), 2)}" for k in K))
        fails = {k.split(':')[0]: round(r[k].get("Z", float("nan")), 2) for k in r if r[k]["label"] == "FAIL"}; print("  FAIL:", fails); print("  PASS:", sorted(k.split(":")[0] for k in r if r[k]["label"] == "PASS")); print("  B28", {x: r["B28"].get(x) for x in ("label", "M300", "dkappa", "peak", "ZM", "old")}); print("  C1 Z", r["C1"].get("Z"), r["C1"].get("label")); print("  A12", {k: round(v["Z"], 1) for k, v in r["A12"].get("classes", {}).items()}, "| A18", r["A18"].get("value"), r["A18"].get("label"), "| B1", r["B1"].get("label"), r["B1"].get("why", ""), "| A17", r["A17"].get("label"), r["A17"].get("why", ""))
sys.exit(0 if ok else 1)
