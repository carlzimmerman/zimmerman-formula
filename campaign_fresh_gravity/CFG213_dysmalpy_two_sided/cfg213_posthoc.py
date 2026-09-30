#!/usr/bin/env python3
"""CFG213 POST HOC diagnostics (written AFTER the main run's numbers were seen; reported only, never a verdict).
Why: in the z ~ 5 bin the rival is DISFAVOURED-under on the fit route (n = 12) but CONSISTENT on the SED + gas route (n = 9).
  (a) Is the flip the SAMPLE (12 -> 9) or the MASS SWAP?  The fit route recomputed on exactly the route's 9 galaxies.
  (b) Leave-one-out on the fit route (n = 12): the range of the median delta and whether any single galaxy carries it.
  (c) The per-galaxy route factor M_ind / M_fit (SED + dust gas over the fitted M_bary) for the 9.
Imports the lane's main script read-only (its functions and data), with MUTATE forced off.
Run: python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_posthoc.py
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg213_two_sided.py")).read()
cut = src.index("BINS = {")
ns = {"__file__": os.path.join(LANE, "cfg213_two_sided.py"), "__name__": "cfg213"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "cfg213", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
galaxy_rows, deltas, K, A0F, E, med_ci, verdict, cr, EXCL = (ns[k] for k in ("galaxy_rows", "deltas", "K", "A0F", "E", "med_ci", "verdict",
                                                                               "cr", "EXCL"))
out = []
P = lambda s="": (print(s), out.append(s))
P(__doc__.split("Run:")[0].strip())
prim = [g for g in cr if g["id"] not in EXCL]
route_rows = galaxy_rows("Z5", prim, route=True)
ids9 = {r["id"] for r in route_rows}
same9 = [g for g in prim if g["id"] in ids9]
P(f"\n(a) the route's 9: {sorted(ids9)}")
for kname in ("nu_mono", "P2"):
    nu = ns["KER"][kname]
    for foot in ("canonical", "alt"):
        for law in ("flat", "rival"):
            fit9 = galaxy_rows("Z5", same9)
            m1, l1, h1 = med_ci(deltas(fit9, law, foot, nu), ("ph9", kname, foot, law))
            m2, l2, h2 = med_ci(deltas(route_rows, law, foot, nu), ("phr", kname, foot, law))
            P(f"  {kname:7s} {foot:9s} {law:5s}: FIT route on the 9: {m1:+.3f} [{l1:+.3f}, {h1:+.3f}] {verdict(l1, h1):17s} | "
              f"SED+gas route on the 9: {m2:+.3f} [{l2:+.3f}, {h2:+.3f}] {verdict(l2, h2)}")
P("\n(b) leave-one-out, fit route, n = 12 -> 11, nu_mono canonical, alpha 3.36:")
for law in ("flat", "rival"):
    meds = []
    for drop in prim:
        rows = galaxy_rows("Z5", [g for g in prim if g is not drop])
        meds.append((drop["id"], float(np.median(deltas(rows, law, "canonical", K.nu_mono)))))
    lo = min(meds, key=lambda t: t[1]); hi = max(meds, key=lambda t: t[1])
    P(f"  {law}: leave-one-out median delta ranges {lo[1]:+.3f} (dropping {lo[0]}) to {hi[1]:+.3f} (dropping {hi[0]})")
P("\n(c) route factor M_ind / M_fit (SED M* / (1 - f_molgas) over the fitted M_bary), per galaxy:")
for g in same9:
    Mind = 10 ** g["logMstar"] / (1 - g["f_molgas"])
    P(f"  {g['id']:>6s}: log M_fit {g['logMfit']:.2f}, log M_ind {math.log10(Mind):.2f}, factor {Mind / 10 ** g['logMfit']:.2f} "
      f"(f_molgas {g['f_molgas']:.2f})")
open(os.path.join(LANE, "cfg213_posthoc.out"), "w").write("\n".join(out) + "\n")
