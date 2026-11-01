#!/usr/bin/env python3
"""PG1 read, per FROZEN_CRITERIA.md. eps FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "pg1_results.json"))); E = json.load(open(os.path.join(H, "..", "ER1_energy_to_undo", "er1_results.json"))); A, B = "A_c2b_refit", "B_cfg886_bg"; OUT = []
def P(s): print(s); OUT.append(s)
ok = []; 
for e in (.01, .03, .1, .2, .285, .46, .7, 1.0, 1000.0, 1e-12):
    r = R[f"SN_e{e}"]; L = r["sparc"][A]["line"] and r["sparc"][B]["line"]; T = abs(r["tilt"]) <= .15; ok += [e] if L and T and 1e-12 < e < 1000 else []
    P(f"eps {e:<7} U {r['sparc'][A]['U_median']:.2f}/{r['sparc'][B]['U_median']:.2f} rms {r['sparc'][A]['rms']:.4f} tilt {r['tilt']:+.2f} line {L} bins " + " ".join(f"{v['U']:.2f}" for v in r["bins3"].values()) + f" groups {r['groups'].get('verdict')}")
F = R["SN_e0.285"]["pg1F"]
for l, h in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)): P(f"factor {l}-{h}: median {np.median([x['F'] for x in F.values() if x['ok'] and l <= x['vf'] < h]):.3f}")
d = lambda a, b: max(abs(a["sparc"][t][k] - b["sparc"][t][k]) for t in (A, B) for k in ("U_median", "rms")); k1 = d(R["SN_e1e-12"], E["f0.872"]) <= 1e-3; k2 = d(R["SN_e1000.0"], E["f0"]) <= 1e-3; v = [x["F"] for x in F.values()]; k3 = 0 < min(v) and max(v) <= 1; km = d(R["MUT_e0.285"], R["SN_e0.285"]) > 0
P(f"K1 {k1}; K2 {k2}; K3 {k3}; MUTATE moved {km}, toward f 0.872: U {R['MUT_e0.285']['sparc'][A]['U_median']:.2f}\n=== LABEL: {'SHAPE CORRECTED ' + str(ok) if ok else 'WRONG SHAPE'}")
open(os.path.join(H, "pg1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 and k2 and k3 and km else 1)
