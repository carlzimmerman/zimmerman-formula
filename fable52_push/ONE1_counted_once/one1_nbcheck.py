#!/usr/bin/env python3
"""ONE1 reported check (post hoc, not graded; written after one1_kids.out showed the neighbours' term in R_s): why the point-mass
neighbours (E8's form) move R_s by less than the lead's scaling of E8's outer amplitude. Splits the term into its outer and inner
windows, k = 1, primary X, host-free 'all' at 1.0 and 1.6 R_h, point masses inside R_h (E8's set) and extended halos (lambda = 1).
Runs one1_kids.py's set-up read-only (up to its grid of readings).   python3 one1_nbcheck.py -> one1_nbcheck.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "one1_kids.py")).read()
pre = src[:src.index("# =================================================================== 8. the grid of readings")]
ns = {"__file__": os.path.join(HERE, "one1_kids.py"), "__name__": "one1_kids_lib"}; exec(compile(pre, "one1_kids_prefix", "exec"), ns)
np, math, P0 = ns["np"], ns["math"], ns["P"]; L = []
def P(s): print(s, flush=True); L.append(s)
for f in ns["FOOT"]:
    X = ns["XP"][f]; C1 = ns["cells"](ns["A0"][f], 1.0, X)
    Tr, Ts, npr = ns["neighbours"](X, [1.0 * math.sqrt(ns["A0C"] / ns["A0"][f])], ns["Htab_of"](X)); NBE = (Tr - Ts[2])[0]
    for F in (1.0, 1.6):
        mk = ("KO1", F, "all"); m = ns["MASKS"][mk]; S1 = ns["psum"](ns["WW1"] * C1, m); a1 = ns["amps"](mk, f, S1)
        for lab, T in (("point masses (E8's form, inside R_h)", ns["NB_POINT"] * (1 + X)), ("extended halos (this reading)", NBE)):
            a2 = ns["amps"](mk, f, S1 + ns["psum"](ns["WW1"] * T, m))
            P(f"[{f}] {F} R_h, {lab}: A_out {a1['out']:.3f} -> {a2['out']:.3f} ({a2['out'] - a1['out']:+.3f}); A_in {a1['in_']:.3f} -> {a2['in_']:.3f} ({a2['in_'] - a1['in_']:+.3f}); "
              f"R_s {a1['out'] / a1['in_']:.3f} -> {a2['out'] / a2['in_']:.3f} ({a2['out'] / a2['in_'] - a1['out'] / a1['in_']:+.3f})")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "one1_nbcheck.out"), "w").write("\n".join(L) + "\n")
