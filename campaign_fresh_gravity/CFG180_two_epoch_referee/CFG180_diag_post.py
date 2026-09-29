#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180 POST-COMPARISON diagnostic (written AFTER my main, MUTATE, attack and mock runs were saved; reads CFG170's committed
results json / firstrun json.  Not part of any frozen result).  Compares my numbers with CFG170's row by row.
"""
import os
import json
import math

import numpy as np

import CFG180_lib as L
M = L.M

J = os.path.join(L.REPO, "campaign_fresh_gravity")
j = json.load(open(os.path.join(J, "CFG170_two_epoch_gas_ratio_results.json")))["numbers"]
j0 = json.load(open(os.path.join(J, "CFG170_two_epoch_gas_ratio_firstrun_results.json")))["numbers"]
tab = j["table"]
Su = L.get_kurvs("inc_star_deg")
Sk = L.get_kross()
AS = L.get_anchor()


def rel(a, b):
    if a is None or b is None:
        return None
    return abs(a - b) / abs(b)


def cmp(conv):
    worst = {"centre": 0.0, "edge": 0.0, "R": 0.0, "Redge": 0.0}
    rows = []
    for s in (0.0, 1.00, 1.42, 1.62, 1.69, 3.00):
        r = L.solve_pair(Sk, Su, AS, s, conv=conv)
        for law, nm in (("flat", "flat"), ("H", "rival")):
            t = tab[f"{s:.2f}|{nm}"]
            for smp, key in (("U", "kurvs"), ("K", "kross")):
                b = r[law][smp]
                th = t[key]
                for val, tv, kind in ((b["mu"], th[0], "centre"), (b["mu_lo"], th[1], "edge"), (b["mu_hi"], th[2], "edge")):
                    if val is None and tv is None:
                        continue
                    if (val is None) != (tv is None):
                        rows.append((s, nm, smp, kind, val, tv, "presence differs"))
                        continue
                    d = rel(val, tv)
                    worst[kind] = max(worst[kind], d)
                    if d > 0.02:
                        rows.append((s, nm, smp, kind, round(val, 4), round(tv, 4), f"{d:.3f}"))
            rl = r[law]["R"]
            if (rl is None) != (t["R"] is None):
                rows.append((s, nm, "R", "presence", None if rl is None else rl["R"], t["R"], "differs"))
            elif rl is not None:
                worst["R"] = max(worst["R"], rel(rl["R"], t["R"]))
                worst["Redge"] = max(worst["Redge"], rel(rl["lo"], t["R_lo"]))
                if math.isfinite(rl["hi"]) and t["R_hi"] is not None and math.isfinite(t["R_hi"]):
                    worst["Redge"] = max(worst["Redge"], rel(rl["hi"], t["R_hi"]))
                elif math.isfinite(rl["hi"]) != (t["R_hi"] is not None and math.isfinite(t["R_hi"])):
                    rows.append((s, nm, "R_hi open flag differs", rl["hi"], t["R_hi"]))
    return worst, rows


print("=" * 100)
print("CFG180 post-comparison with CFG170 (results json); repo=<repo>")
print("=" * 100)
for conv in ("A", "B"):
    w, rows = cmp(conv)
    print(f"\nconvention {conv}: worst relative differences  centre {w['centre']:.4f}  edge {w['edge']:.4f}  R {w['R']:.4f}  R-edge {w['Redge']:.4f}")
    for r in rows:
        print("   ", r)

print("\ncalibration scatter rows (centre only) CFG170 vs mine")
for sc in (0.6, 1.4):
    r = L.solve_pair(Sk, Su, AS, sc)
    for law, nm in (("flat", "flat"), ("H", "rival")):
        t = j["table"][f"{sc:.2f}|{nm}"]
        print(f"   s={sc} {nm}: CFG170 R {t['R']} KURVS {t['kurvs'][0]} KROSS {t['kross'][0]} | mine R {None if r[law]['R'] is None else round(r[law]['R']['R'], 4)} KURVS {r[law]['U']['mu']} KROSS {r[law]['K']['mu']}")

print("\nR_obs numbers: CFG170 vs mine")
ro = L.robs(float(np.median(Su.z)), float(np.median(Sk.z)), float(np.median(Su.logM)), float(np.median(Sk.logM)))
rj = j["R_obs"]
print(f"   in-repo {rj['in_repo']:.4f} vs {ro['Rin']:.4f}; bracket {rj['in_repo_2sigma']} vs {ro['inrep'](2.0)}; lit {rj['literature_abstract_level']:.4f} vs {ro['Rlit']:.4f}; {rj['literature_bracket']} vs {ro['litb'](0.2)}")

print("\nmatrix flags: CFG170 vs mine (conservative interval)")
diff = 0
for s in (1.00, 1.42, 1.62, 1.69, 3.00):
    r = L.solve_pair(Sk, Su, AS, s)
    for law, nm in (("flat", "flat"), ("H", "rival")):
        rl = r[law]["R"]
        for key, br in (("in_repo", ro["inrep"](2.0)), ("literature", ro["litb"](0.2))):
            mine = "disfavoured" if L.disfav_overlap(rl, br) else "not disfavoured"
            theirs = j["matrix"][f"{s:.2f}|{nm}"][key]
            if mine != theirs:
                diff += 1
                print("   DIFF", s, nm, key, mine, theirs)
print(f"   flag differences: {diff}")

print("\nfirst-run json vs final json: rows that differ")
for k in j["table"]:
    a, b = j0["table"][k], j["table"][k]
    if (a["R"] is None) != (b["R"] is None):
        print("   ", k, "firstrun R", a["R"], "final R", b["R"], "final interval", b.get("R_lo"), b.get("R_hi"))
for k in j["matrix"]:
    if j0["matrix"][k]["in_repo"] != j["matrix"][k]["in_repo"] or j0["matrix"][k]["literature"] != j["matrix"][k]["literature"]:
        print("    matrix", k, j0["matrix"][k], "->", j["matrix"][k])

print("\nsummary strings: CFG170:", j["summary"])
print("\nCFG170's own MUTATE controls: evaluator-only. M1 sets R_obs := R_flat (in-repo relative width), M2 sets R_obs := 10 R_flat; neither touches Delta', the break-even, or the interval code.")
