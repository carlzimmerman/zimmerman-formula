#!/usr/bin/env python3
"""CFG497 K6 diagnostic (POST-HOC, added after the main run's K6 failed; not a verdict input).
Is the 1e9-vs-1e10 self-similarity break the softening (eps = 1e-3 r_M scales as M^(1/2), lengths as M^(1/3)) or
discreteness / stream noise? Runs q = 0.1 with the core at 1e9 twice more: (a) eps rescaled to the 1e10 run's eps x 0.1^(1/3)
(exact self-similar copy), (b) a second 1e10 run with N = 19,999 (one shell fewer: a noise probe). Reuses cfg497_binding.py's
definitions (executed up to its infall banner, no side effects beyond the K3 print). Writes cfg497_k6_diag.out.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg497_binding.py")).read()
g = {"__file__": os.path.join(HERE, "cfg497_binding.py"), "__name__": "cfg497_k6"}
exec(compile(src[:src.index('P("\\n[infall]')], "cfg497_binding.py", "exec"), g)
IF, run, select, FOOTS = g["IF"], g["run"], g["select"], g["FOOTS"]
lines = []
def out(s):
    print(s, flush=True); lines.append(s)
base = run(0.1, 20000, 1e10)
direct = run(0.1, 20000, 1e9)
eps10 = IF.SOFT_FRAC * IF.r_M_kpc(1e10, "canonical")
IF.SOFT_FRAC = eps10 * 0.1 ** (1.0 / 3.0) / IF.r_M_kpc(1e9, "canonical")
scaled = run(0.1, 20000, 1e9)
IF.SOFT_FRAC = 1e-3
n1 = run(0.1, 19999, 1e10)
out("CFG497 K6 diagnostic (POST-HOC; not a verdict input). s_sel at M_b = 1e9, q = 0.1, t_d")
out(f"  z_d: base {base['z_d']:.4f}, direct {direct['z_d']:.4f}, eps-scaled {scaled['z_d']:.4f}, N-1 {n1['z_d']:.4f}")
for cand in ("A1 VIR200", "A2 VIRTH", "A3 CATCH", "A4 CORE-BOUND", "B1 Y1-FIELD", "B2 A0-FIELD", "R1 BARYON-E"):
    for f in (FOOTS if cand.startswith("B") else FOOTS[:1]):
        v = [select(r_, "td", cand, 1e9, f)[0] for r_ in (base, direct, scaled, n1)]
        out(f"  {cand:14s} {f:9s}: rescaled-1e10 {v[0]:.4f} | direct-1e9 {v[1]:.4f} | direct-1e9 eps-scaled {v[2]:.4f} | 1e10 N-1 {v[3]:.4f}")
open(os.path.join(HERE, "cfg497_k6_diag.out"), "w").write("\n".join(lines) + "\n")
