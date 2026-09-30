#!/usr/bin/env python3
"""CFG201 -- does CFG198's fitted-vs-SED mass drift appear in a PRIOR-ANCHORED sample?  Price+2021 RC41 (41 discs,
z 0.66-2.45; M_bar fitted with a 0.2-dex Gaussian prior centred on M*_SED + M_gas).  Frozen criteria: FROZEN_CRITERIA.md
here (8a15e7e48), committed before any number.  The mass route only; no a0.  kappa = 1/2 FITTED, NOT DERIVED.
Run:  python3 campaign_fresh_gravity/CFG201_rc41_mass_route/cfg201_rc41_mass_route.py            (MUTATE=1: drift injected)
"""
import os, sys, csv
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import spearmanr

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg201_rc41_mass_route", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())
NBOOT, SEED = 10000, 201


def theil_sen(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


def slope_ci(x, y, seed=SEED):
    rng = np.random.default_rng(seed)
    bs = np.array([theil_sen(x[k], y[k]) for k in (rng.integers(0, len(x), len(x)) for _ in range(NBOOT))])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return theil_sen(x, y), float(lo), float(hi)


rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "price2021_rc41", "price2021_rc41.csv"))))
z = np.array([float(r["z"]) for r in rows])
lms = np.array([float(r["logMstar_SED"]) for r in rows])
lmg = np.array([float(r["logMgas"]) for r in rows])
lmb = np.array([float(r["logMbar_1D"]) for r in rows])
fdm = np.array([float(r["fDM_Re_1D"]) for r in rows])
dbar = lmb - np.log10(10 ** lms + 10 ** lmg)
check("C1 41 rows parse, z in [0.65, 2.46], every Delta_bar finite", f"n = {len(rows)}, z {z.min():.3f}-{z.max():.3f}",
      len(rows) == 41 and z.min() >= 0.65 and z.max() <= 2.46 and np.all(np.isfinite(dbar)))
rng = np.random.default_rng(7)
syn = -0.5 * (z - np.median(z)) + rng.normal(0, 0.1, len(z))
bs_, lo_, hi_ = slope_ci(z, syn, seed=11)
check("C2 injected slope -0.5 dex/z with 0.1 dex scatter on the real z is recovered within its own 95% CI",
      f"recovered {bs_:+.3f} [{lo_:+.3f}, {hi_:+.3f}]", lo_ <= -0.5 <= hi_)
if MUT:
    d_true = dbar.copy()
    dbar = dbar - 0.5 * (z - np.median(z))
    P("  MUTATE=1: Delta_bar -> Delta_bar - 0.5 (z - median z)")

R.banner("P1 -- the fitted M_bar against the prior centre (M*_SED + M_gas), in z")
b, lo, hi = slope_ci(z, dbar)
rho = spearmanr(z, dbar)
zm = np.median(z)
P(f"  Theil-Sen slope of Delta_bar on z: {b:+.3f} dex/z, 95% CI [{lo:+.3f}, {hi:+.3f}] (n = {len(z)}); in units of the "
  f"0.2-dex prior per unit z: {b / 0.2:+.2f}")
P(f"  Spearman rho(Delta_bar, z) = {rho.correlation:+.3f} (p = {rho.pvalue:.3f}); median Delta_bar z <= {zm:.2f}: "
  f"{np.median(dbar[z <= zm]):+.3f}, z > {zm:.2f}: {np.median(dbar[z > zm]):+.3f}")
if lo > 0 or hi < 0:
    D1 = "the drift appears in a prior-anchored sample" if hi < 0 else "a drift of the opposite sign"
else:
    D1 = "no significant drift"
D2 = "smaller than CFG198's -0.72 at 95% (CI excludes -0.72)" if not (lo <= -0.72 <= hi) else "not distinguishable from CFG198's -0.72"
P(f"  -> D1: {D1}\n  -> D2: {D2}")
bf, lof, hif = slope_ci(z, fdm)
P(f"\n  descriptive (not graded): Theil-Sen slope of f_DM(R_e) on z = {bf:+.3f} per unit z [{lof:+.3f}, {hif:+.3f}]")
R.num("P1", dict(slope=b, ci=[lo, hi], slope_over_prior=b / 0.2, spearman=float(rho.correlation), spearman_p=float(rho.pvalue),
                 median_low_z=float(np.median(dbar[z <= zm])), median_high_z=float(np.median(dbar[z > zm])), D1=D1, D2=D2))
R.num("fDM_slope", dict(slope=bf, ci=[lof, hif]))
if MUT:
    b0, _, _ = slope_ci(z, d_true)
    check("MUTATE: the injected drift lowers the slope by 0.5 +- 0.05 and D1 reads 'the drift appears'",
          f"slope {b0:+.3f} -> {b:+.3f} (change {b - b0:+.3f}); D1 {D1!r}", abs((b - b0) + 0.5) <= 0.05 and D1.startswith("the drift"))
R.write(here=LANE)
