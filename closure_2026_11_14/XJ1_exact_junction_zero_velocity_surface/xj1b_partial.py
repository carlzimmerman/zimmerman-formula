#!/usr/bin/env python3
"""XJ1 build B: a PARTIAL look at the first pass while it is paused (disclosed in RESULT.md; not a graded number and not
the frozen statistic). The frozen D needs 4 seeds in all 12 bins. This reads only the redshift bins that already have
all 4 seeds and prints, per case, the flux Delta chi^2 of those bins alone (their own block of the covariance) with its
jackknife standard error over the seed index. No rule, case or threshold was changed after this look.
  python3 -I -B xj1b_partial.py [parts_dir] -> printed only
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xj1_lib as XL
X = XL.X
PARTS = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "parts_b")
FD = X.forest_data(); cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); COV = Uc.T @ Uc
def dchi2(r, sel):
    d = ((r - 1.0) * FD["Pd"])[sel]; return float(d @ np.linalg.solve(COV[np.ix_(sel, sel)], d))
for ft in X.FOOTS:
    PR = {}
    for f in sorted(glob.glob(os.path.join(PARTS, f"prim_z*_s*_{ft}.json"))):
        d = json.load(open(f)); PR.setdefault(d["z"], {})[d["seed"]] = d
    zs = [z for z in X.ZB if len(PR.get(z, {})) == 4]; seeds = [0, 1, 2, 3]
    if not zs: print(f"[{ft}] no complete bin"); continue
    kv = {z: np.array(PR[z][0]["kv"]) for z in zs}; sel = np.isin(FD["zs"], zs)
    names = [n for n in PR[zs[0]][0]["flux"]["primary"] if n not in ("R",)]
    def D(nm, ss, zz=None):
        r = np.ones(FD["NB"])
        for z in (zz or zs):
            if nm not in PR[z][ss[0]]["flux"]["primary"]: continue
            R = sum(np.array(PR[z][s]["flux"]["primary"][nm]["p"]) for s in ss) / sum(np.array(PR[z][s]["flux"]["primary"]["R"]["p"]) for s in ss)
            s_ = FD["zs"] == round(z, 2); r[s_] = np.interp(np.log(FD["ks"][s_]), np.log(kv[z][1:]), R[1:])
        return dchi2(r, sel)
    print(f"[{ft}] PARTIAL, bins with 4 seeds: {zs} ({int(sel.sum())} of {FD['NB']} points)")
    for nm in names:
        if nm.startswith("TWB"): continue
        d0 = D(nm, seeds); dj = np.array([D(nm, [s for s in seeds if s != j]) for j in seeds]); se = math.sqrt(3 / 4 * np.sum((dj - dj.mean()) ** 2))
        print(f"[{ft}]   {nm:6s} partial Delta chi^2 {d0:9.4f}  SE {se:7.4f}   per bin: " + " ".join(f"{z}:{D(nm, seeds, [z]):.3g}" for z in zs))
