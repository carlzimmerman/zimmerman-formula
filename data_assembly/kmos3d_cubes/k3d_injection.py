#!/usr/bin/env python3
"""C2 / C2b of FROZEN_CRITERIA_2026-09-30.md: inject an arctan disk into a galaxy's own PSF and empirical noise level, refit with the identical pipeline.
usage: python3 k3d_injection.py [base|flat|slow] [n_max]"""
import sys, time, json, numpy as np, pandas as pd
from multiprocessing import Pool
import k3d_fit as K
D = "/Users/carlzimmerman/new_physics/_external_data/kmos3d/cubes/"
cat = pd.read_csv("../kmos3d_phibss/kmos3d_catalog.csv")
def load(row, q0=0.2):
    return K.Cube(D + row.FILE, row.Z, row.RA, row.DEC, row.RHALF, row.Q, row.SPEC_RES, q0=q0)
def pick():
    s = cat[(cat.Z >= 2) & (cat.OBSBAND == "K") & (cat.HAFIT_FLUX_HA / cat.HAFIT_FLUX_HA_ERR >= 10) & (cat.HAFIT_PRESENT == 1)].sort_values("ID").reset_index(drop=True)
    idx = list(range(0, len(s), 15))[:12]; return s.iloc[idx], len(s)
def scenario(name):
    return {"base": (200.0, 0.4), "flat": (200.0, 0.1), "slow": (300.0, 1.2)}[name]
def run(args):
    row, name, seed = args; row = pd.Series(row); rng = np.random.default_rng(seed)
    va, rt = scenario(name); cube = load(row); pa = rng.uniform(0, 360)
    f0 = 1e-3 * row.HAFIT_FLUX_HA * (row.HAFIT_FLUX_AP_CORR if np.isfinite(row.HAFIT_FLUX_AP_CORR) else 1.0)   # catalogue flux is in 1e-17 erg/s/cm2 = 1e-3 x (1e-17 W/m2), the cube flux unit
    truth = np.array([0, 0, pa, va, rt, 60.0, 0, f0, 0.2])
    m = cube.model(truth); noise = rng.normal(0, 1, m.shape) * cube.s
    # the 'true' data = model + noise at the empirical level; the continuum is zero here
    cube.d = np.where(cube.ok, m + noise, 0.0)
    t = time.time(); r = K.fit(cube, f0); out = K.summarize(cube, r)
    vt22 = (2 / np.pi) * va * np.arctan(2.2 * cube.rd / rt)
    out.update(ID=row.ID, scenario=name, PA_true=pa, V22_true=vt22, ratio=out["V22"] / vt22, secs=time.time() - t, inc_true_deg=out["inc_deg"])
    return out
if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "base"; nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    sel, n = pick(); sel = sel.iloc[:nmax]; print("highSN K z>=2 list length", n, "injection cubes", len(sel), flush=True)
    jobs = [(r.to_dict(), name, 20260930 + i) for i, (_, r) in enumerate(sel.iterrows())]
    with Pool(min(len(jobs), 12)) as p: res = p.map(run, jobs)
    df = pd.DataFrame(res); df.to_csv(f"k3d_injection_{name}.csv", index=False)
    print(df[["ID", "PA_true", "PA", "V22_true", "V22", "ratio", "chi2r", "edge", "secs"]].round(2).to_string())
    print("median ratio %.3f  rms %.3f" % (df.ratio.median(), df.ratio.std()))
