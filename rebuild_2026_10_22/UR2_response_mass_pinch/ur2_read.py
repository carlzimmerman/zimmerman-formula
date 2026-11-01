#!/usr/bin/env python3
"""UR2 read of ur2_results.json, per FROZEN_CRITERIA.md. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "ur2_results.json"))); U1 = json.load(open(os.path.join(H, "..", "UR1_one_response_rule", "ur1_results.json")))["runs"]; T = ("A_c2b_refit", "B_cfg886_bg"); OUT = []
def P(s): print(s); OUT.append(s)
rows = lambda m: sorted([r for k, r in R["rows"].items() if k.startswith(m + "|")], key=lambda r: r["delta"])
def cross(ds, us):
    for i in range(len(ds) - 1, 0, -1):
        if us[i] >= 0.5: return ds[i]
        if us[i - 1] >= 0.5: return ds[i - 1] + (0.5 - us[i - 1]) / (us[i] - us[i - 1]) * (ds[i] - ds[i - 1])
    return None if us[0] < 0.5 else ds[0]
def dU(rr): return cross([r["delta"] for r in rr], [min(r["sparc"][t]["U"] for t in T) for r in rr])
for m in ("off", "blum", "gnedin"):
    P(f"\n{m}: delta U_A/U_B rms tilt_A/B groupsZ verdict LT_A/B")
    for r in rows(m):
        s = r["sparc"]; g = r["groups"]; P(f"  {r['delta']:+.2f} {s[T[0]]['U']:.2f}/{s[T[1]]['U']:.2f} {s[T[0]]['rms']:.4f} {s[T[0]]['tilt']:+.2f}/{s[T[1]]['tilt']:+.2f} {g.get('Z', g.get('z', float('nan'))):+.2f} {g.get('verdict')} {r['lt'][T[0]]:+.3f}/{r['lt'][T[1]]:+.3f}")
    d = dU(rows(m)); P(f"  delta_U {d}")
    rr = rows(m); bins = list(rr[0]["sparc"][T[0]]["bins"]); P("  delta at U 0.50 by V_flat bin (bg A): " + ", ".join(f"{b} {cross([r['delta'] for r in rr], [r['sparc'][T[0]]['bins'][b] for r in rr])}" for b in bins))
b0 = R["rows"]["blum|+0.00"]; e = U1["EM1|blum"]; k = [abs(b0["sparc"][t][q] - e["sparc"][t][q]) for t in T for q in ("U", "rms", "tilt")] + [abs(b0["lt"][t] - e["lt"][t]) for t in T]; o0 = R["rows"]["off|+0.00"]; e0 = U1["EM1|off"]; k1 = [abs(o0["sparc"][t][q] - e0["sparc"][t][q]) for t in T for q in ("U", "rms")]
P(f"\nK1 off vs UR1 (= NR1) |d| {max(k1):.1e}; K2 blum vs UR1 |d| {max(k):.1e}; groups {b0['groups']} vs {e['groups']}")
us = [r["sparc"][T[0]]["U"] for r in rows("blum")]; P(f"K3 U monotonic in delta: {all(a >= b - 1e-9 for a, b in zip(us, us[1:]))}")
mu = R["MUTATE"]; ds = sorted(float(x) for x in mu); P(f"MUTATE M_b x 2 in response: delta_U {cross(ds, [min(mu[f'{d:+.2f}']['sparc'][t]['U'] for t in T) for d in ds])}")
open(os.path.join(H, "ur2.out"), "w").write("\n".join(OUT) + "\n")
