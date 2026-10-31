#!/usr/bin/env python3
"""ZN1 read-out after the frozen grade: BA1's joint chi^2 on each graded job (reported, BA1's criteria don't list ZN1), and Argon's predictions on record scored. Changes no class. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []; HH = ("h0672", "h0686")
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(HERE, "zn1_results.json"))); BA = json.load(open(os.path.join(RB, "BA1_joint_shear_statistic", "ba1_results.json"))); SH = json.load(open(os.path.join(HERE, "zn1_shapes.json")))
def joint(cells, RJ, h, Rk="R_boot"):
    ks = RJ[h]["keys"]; R = np.array(RJ[h][Rk]); d = np.array([cells[h][k]["meas"] - cells[h][k]["pred"] for k in ks]); s = np.array([cells[h][k]["s"] for k in ks]); w, V = np.linalg.eigh(R); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ (d / s); c2 = float((z * z / w[ok]).sum()); dof = int(ok.sum()); return c2, dof, float(chi2.sf(c2, dof))
P("ZN1 score: BA1's joint chi^2 on each job, worse h; Argon's predictions on record; kappa = 1/2 FITTED; not theory closed"); RES = {}
for lab, r in J["runs"].items():
    RJ = BA["R_orig"] if "eRASS1" in lab else BA["R_gas"]; v = {h: joint(r["cells"], RJ, h) for h in HH}; w = {h: joint(r["cells"], RJ, h, "R_jack") for h in HH}; hw = min(HH, key=lambda q: v[q][2]); RES[lab] = dict(chi2=v[hw][0], dof=v[hw][1], p=v[hw][2], jack_p=w[hw][2]); lb = "JOINT PASS" if v[hw][2] >= 0.05 else "JOINT FAIL" if v[hw][2] < 0.01 else "JOINT MARGINAL"; P(f"  {lab}: chi^2 {v[hw][0]:.1f} / {v[hw][1]}, p {v[hw][2]:.2e} {lb}; jackknife p {w[hw][2]:.2e}")
r = J["runs"]["f* 0.034, X-COP's gas"]; c = r["cells"]["h0672"]; x = r["xcop"]
def rng(v, lo, hi): return "HIT" if lo <= v <= hi else "MISS"
P("Argon, f* 0.034, h 0.672, one template, X-COP's gas:")
P(f"  X-COP mean predicted +0.022: measured {x['mean']:+.3f}; rms predicted 0.082: measured {x['rms']:.3f}; passes G4: {'yes' if abs(x['mean']) <= 0.05 and x['rms'] <= 0.10 else 'no'}")
P(f"  G-OUT-M3 predicted +2.85 [+2.35, +3.40]: measured {c['G-OUT-M3']['Z']:+.2f}: {rng(c['G-OUT-M3']['Z'], 2.35, 3.40)}; predicted model about 1.06: measured {c['G-OUT-M3']['pred']:.3f}")
P(f"  G-OUT-Mall predicted +1.75 [+1.35, +2.15]: measured {c['G-OUT-Mall']['Z']:+.2f}: {rng(c['G-OUT-Mall']['Z'], 1.35, 2.15)}")
P(f"  G-IN-Mall predicted -1.65 [-2.05, -1.35]: measured {c['G-IN-Mall']['Z']:+.2f}: {rng(c['G-IN-Mall']['Z'], -2.05, -1.35)}")
P(f"  class predicted X-COP ONLY [MASS-DEFINITION-DEPENDENT]: measured {J['verdict']}{J['tags']}")
b = J["runs"].get("f* 0.034, X-COP's gas, MA1's budget M200"); 
if b: bm = b["cells"]["h0672"]["G-OUT-M3"]["Z"]; P(f"  Argon's drop condition: FAILS BOTH, or G-OUT-M3 above +3.0 on both fair-share and budget M200: fair share {c['G-OUT-M3']['Z']:+.2f}, budget {bm:+.2f}: {'MET' if (J['verdict'] == 'FAILS BOTH' or (c['G-OUT-M3']['Z'] > 3 and bm > 3)) else 'not met'}")
for M in ("1e13", "1e14"):
    q = SH[M]["0.00"]["seeds"]; cc = [s["c_nfw"] for s in q if s["c_nfw"] is not None]; P(f"  c_nfw at z = 0 (X48's fit over r_vir), M {M}: median {np.median(cc):.2f}, n {len(cc)}; Argon's c200 about 7.25 (fit definitions differ)")
json.dump(dict(joint=RES), open(os.path.join(HERE, "zn1_score.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "zn1_score.out"), "w").write("\n".join(OUT) + "\n")
