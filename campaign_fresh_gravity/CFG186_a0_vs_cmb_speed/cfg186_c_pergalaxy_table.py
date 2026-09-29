#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG186 part C -- SECONDARY: the speed dependence on the record's per-galaxy a0 table.

real_research/data/sparc_a0_environment_table.csv (122 galaxies), made by
real_research/reviews/project_sparc_a0_vs_cosmicweb.py (fit_a0_per_galaxy + write_outputs): log10 a0 = median over the
deep points (g_bar < 1.2e-10/3) of 2 log g_obs - log g_bar, fixed Upsilon_disk = 0.5 and Upsilon_bul = 0.7, catalogue
distance and inclination, no errors.  It inherits fixed nuisances and per-galaxy fitting noise; SECONDARY everywhere.
Refit here on its f_D != 1 galaxies (redshift-independent distances) with u at the catalogue distance (W1, H0 = 67.66;
H0 = 73 reported): log10 a0_i = L + log10(1 + beta (u_i/600 km/s)^2), unweighted least squares, 2000 bootstrap
resamples, 2000 speed shuffles.  kappa = 1/2 stays FITTED.  Run from the repository root:
    python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_c_pergalaxy_table.py
"""
import os
import sys
import csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import least_squares
import cfg186_common as C

if C.MUTATE:
    print("part C has no MUTATE mode (the table is fixed); run without MUTATE")
    sys.exit(0)
R = C.Run("cfg186_c_pergalaxy_table")
P, check = R.P, R.check
P(__doc__.split("kappa = 1/2")[0].strip())

R.banner("C1  THE TABLE, ITS PROVENANCE, THE SAMPLE")
rows = list(csv.DictReader(open(os.path.join(C.DATA, "sparc_a0_environment_table.csv"))))
gals, _ = C.load_galaxies()
gd = {g["name"]: g for g in gals}
sel, dcz = [], []
for r in rows:
    g = gd.get(r["name"])
    if g is None or g["fD"] == 1 or not np.isfinite(g["cz_hel"]):
        continue
    if r["cz_kms"].strip():
        dcz.append(float(r["cz_kms"]) - g["cz_hel"])
    sel.append((g, float(r["log10_a0"])))
P(f"  table rows: {len(rows)}; with f_D != 1 and a velocity: {len(sel)} "
  f"(clean among them: {sum(1 for g, _ in sel if g['clean'])})")
if dcz:
    dcz = np.array(dcz)
    P(f"  the table's cz vs this lane's velocity: median |d| = {np.median(np.abs(dcz)):.1f} km/s, max {np.abs(dcz).max():.0f}")
x = np.array([a for _, a in sel])
P(f"  log10 a0: median {np.median(x):.3f}, sd {np.std(x):.3f} dex")
R.num("N", len(sel))


def fit(x, z):
    zmax = max(z.max(), 1e-6)

    def res(p):
        return x - p[0] - np.log10(np.maximum(1 + p[1] * z, 1e-6))
    best = None
    for b0 in (0.0, 0.5, 2.0):
        r = least_squares(res, [np.median(x), b0], bounds=([-12, -0.95 / zmax], [-8, 20]))
        if best is None or r.cost < best.cost:
            best = r
    return best.x


R.banner("C2  FIT, BOOTSTRAP, SPEED SHUFFLE")
out = {}
for lab, H0 in (("H0 = 67.66 (primary)", C.H0_PRIMARY), ("H0 = 73", C.H0_VARIANT)):
    u = np.array([C.u_los(g["cz_hel"], g["n"], g["D"], H0) for g, _ in sel])
    z = (u / C.W_REF) ** 2
    L, b = fit(x, z)
    rng = np.random.default_rng(186)
    bb = np.array([fit(x[i], z[i])[1] for i in (rng.integers(0, len(x), len(x)) for _ in range(2000))])
    bp = np.array([fit(x, z[rng.permutation(len(x))])[1] for _ in range(2000)])
    sb = 0.5 * (np.percentile(bb, 84) - np.percentile(bb, 16))
    p2 = (1 + np.sum(np.abs(bp) >= abs(b))) / (len(bp) + 1)
    P(f"  {lab:22s}: beta = {b:+.3f} +- {sb:.3f} (boot; 2.5-97.5% [{np.percentile(bb, 2.5):+.2f}, "
      f"{np.percentile(bb, 97.5):+.2f}]); shuffle null 16-84% [{np.percentile(bp, 16):+.2f}, {np.percentile(bp, 84):+.2f}], "
      f"p = {p2:.3f}; log a0_bar = {L:.3f}; bootstrap 95th percentile {np.percentile(bb, 95):.2f}")
    out[lab] = {"beta": b, "sigma_boot": sb, "p_shuffle": p2, "L": L, "boot95": float(np.percentile(bb, 95))}
R.num("secondary", out)
check("SEC (reported) the SECONDARY table gives no speed dependence at p < 0.003", out["H0 = 67.66 (primary)"],
      out["H0 = 67.66 (primary)"]["p_shuffle"] >= 0.003, load_bearing=False)
sys.exit(R.finish())
