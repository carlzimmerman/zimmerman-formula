#!/usr/bin/env python3
"""CFG418: R_c = x * r_ta * f_ret / r_M from CFG413's KiDS truncation profile (free two-halo).  Frozen: FROZEN_CRITERIA.md.  CFG418_MUTATE=1 -> x = 1."""
import os, sys, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(R, "campaign_fresh_gravity", "CFG100_kids_mass_rederivation")); os.environ.setdefault("ZF_REPO", R)
import cfg100_lib as Lb
MUT = os.environ.get("CFG418_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
d = json.load(open(os.path.join(R, "campaign_fresh_gravity", "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
G = 4.30091e-9; L, OUT = [], {}
def P(s=""): print(s); L.append(s)
for foot in ("canonical", "alt"):
    xs = np.array(d["xs"]); c2 = np.array([d["primary"][foot][f"{x:g}" if f"{x:g}" in d["primary"][foot] else str(x)]["free"]["chi2"] for x in xs])
    # parabola in log x through the 3 points around the minimum -> best x and the Delta chi2 <= 1 range
    i = int(np.argmin(c2)); j = slice(max(i - 1, 0), max(i - 1, 0) + 3); lx = np.log(xs[j]); a, b, cc = np.polyfit(lx, c2[j], 2)
    lb = -b / (2 * a); half = math.sqrt(1 / a) if a > 0 else 0.3
    xb, xlo, xhi = math.exp(lb), math.exp(lb - half), math.exp(lb + half)
    if MUT: xb = xlo = xhi = 1.0
    rows = []
    for lMb in (10.5, 10.8, 11.0):
        Mb = 10 ** lMb; a0 = Lb.A0[foot]; rM = math.sqrt(G * Mb / a0); rta = Lb.r_ta_law(Mb, a0, 0.0)
        for fr in (0.07, 0.10):
            rows.append((lMb, fr, xlo * rta * fr / rM, xb * rta * fr / rM, xhi * rta * fr / rM))
    lo = min(r[2] for r in rows); hi = max(r[4] for r in rows); mid = [r[3] for r in rows if r[0] == 10.8]
    v = "CONSISTENT" if lo <= 5.364 <= hi else ("HIGH" if lo > 5.364 else "LOW")
    OUT[foot] = dict(x_best=xb, x_range=[xlo, xhi], Rc_rows=rows, Rc_range=[lo, hi], Rc_central_10p8=mid, verdict=v)
    P(f"  {foot:9s}: KiDS x_best {xb:.2f} (Delta chi2<=1: {xlo:.2f}-{xhi:.2f}); inferred R_c over log M_b 10.5-11, f_ret 0.07-0.10: {lo:.1f} - {hi:.1f} "
      f"(central, log M_b 10.8: {mid[0]:.1f} / {mid[1]:.1f}); CMB 5.364 -> {v}")
P(f"\n{'MUTATE ' if MUT else ''}reading: the supply-edge picture's lensing-inferred cold-to-baryon ratio vs the CMB")
open(os.path.join(HERE, f"cfg418_rc{SUF}.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, f"cfg418_rc{SUF}.json"), "w"), indent=1)
