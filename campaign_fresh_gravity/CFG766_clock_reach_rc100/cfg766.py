"""CFG766: pre-flight -- does any RC100 galaxy reach the clock-diagnostic regime (y <= 0.17) within 3 R_e?

Criteria: FROZEN_CRITERIA.md (committed alone, c1d71c3be). R_need = sqrt(G M_bar / (y_th a0)); rho = R_need / R_e.
kappa = 1/2 FITTED; not "theory closed".  Run: python3 cfg766.py   (CFG766_MUTATE=1: y_th = 1.7; exit 1 iff R1 then REACHABLE)
"""
import os, sys, csv, json, math

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402

MUT = os.environ.get("CFG766_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
YTH = 1.7 if MUT else 0.17
G, MSUN, KPC = 6.6743e-11, 1.98847e30, 3.0856775814913673e19
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv"))))
lines = [__doc__.strip(), f"\n{len(rows)} RC100 galaxies; threshold y = {YTH}"]
out = {"lane": "CFG766", "mutate": MUT, "y_threshold": YTH}
ok_all = True
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    rho = np.array([math.sqrt(G * 10 ** float(r["logMbar_Msun"]) * MSUN / (YTH * a0)) / KPC / float(r["Re_kpc"]) for r in rows])
    n3, n5 = int((rho <= 3).sum()), int((rho <= 5).sum())
    ok = n3 >= 10
    ok_all &= ok
    out[fo] = dict(rho_min=float(rho.min()), rho_median=float(np.median(rho)), rho_p16=float(np.percentile(rho, 16)), n_le3=n3, n_le5=n5,
                   R1="REACHABLE" if ok else "NOT REACHABLE")
    lines.append(f"  {fo:9s}: R_need/R_e min {rho.min():.2f}, 16th pct {np.percentile(rho, 16):.2f}, median {np.median(rho):.2f};  "
                 f"<= 3 R_e: {n3};  <= 5 R_e: {n5}  ->  {out[fo]['R1']}")
out["R1"] = "REACHABLE" if ok_all else "NOT REACHABLE"
lines.append(f"\nVERDICT: R1 {out['R1']}")
print("\n".join(lines))
open(os.path.join(HERE, f"cfg766{TAG}.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, f"cfg766_results{TAG}.json"), "w"), indent=1)
sys.exit(1 if (MUT and ok_all) else 0)
