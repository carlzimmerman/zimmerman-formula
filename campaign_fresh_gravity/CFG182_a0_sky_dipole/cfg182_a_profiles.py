#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG182 part A -- the per-galaxy PROFILE likelihood curves chi2_i(log10 a0) for every usable SPARC galaxy.

For each galaxy and each log10 a0 on the grid -11.30 ... -9.00 (step 0.01) the four nuisances are minimised with the
Li, McGaugh & Lelli 2018 priors: Upsilon_disk (log-normal about 0.5, 0.1 dex), Upsilon_bul (about 0.7, 0.1 dex), distance
(Gaussian, sigma = e_D; g_bar invariant, predicted observed velocity x sqrt(D'/D)), inclination (Gaussian, sigma = e_Inc;
velocity x sin i'/sin i); chi2 in velocity space with the published e_V.  Kernels: nu_mono (primary, the 09-26
decision), P2 = sqrt(1 + 1/y) (CFG4's definition), simple = 1/2 + sqrt(1/4 + 1/y).  Sky positions from the VizieR copy of
Lelli et al. 2016 table 1, converted to Galactic and cross-checked against sparc_cosmicweb_match.csv.

MUTATE=1: a dipole A = 0.20 in a random direction (seed 182) is injected into the DATA at the point level before the
curves are built: V_obs -> V_obs sqrt(nu(y_i')/nu(y)), y = g_bar,fid/a0_ref, y_i' = g_bar,fid/(a0_ref (1 + D_inj.n_i)),
a0_ref = 1.2e-10 (declared), e_V unchanged; nu_mono only.  Output: cfg182_a_profiles_MUTATE.npz.

Nothing here fits a dipole.  Frozen question: FROZEN_QUESTION.md (written before this script).
Run:  python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_a_profiles.py      (MUTATE=1 for the control)
"""
import os
import sys
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg182_common as C

R = C.Run("cfg182_a_profiles")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Nothing here")[0].strip())
GR = C.GRID

banner("A1  DATA: SPARC curves, master table, sky positions")
G = C.load_galaxies()
N = len(G)
use = [g for g in G if g["usable"]]
clean = [g for g in G if g["clean"]]
P(f"  galaxies with master-table row and position: {N}; usable (>= 5 points): {len(use)}; clean (Q <= 2, Inc >= 30, >= 5 pts): "
  f"{len(clean)}; points in clean sample: {sum(g['npt'] for g in clean)}")
P(f"  distance methods (clean): " + ", ".join(f"f_D={k}: {sum(1 for g in clean if g['fD'] == k)}" for k in (1, 2, 3, 4, 5)))
R.num("n_all", N)
R.num("n_usable", len(use))
R.num("n_clean", len(clean))
check("POS all 175 SPARC galaxies have a VizieR position and a master-table row", f"{N}/175", N == 175)

cw = C.load_cosmicweb()
seps = []
for g in G:
    r = cw.get(g["name"])
    if r is None or r["l_gal"] in ("", None):
        continue
    v2 = C.unitvec(float(r["l_gal"]), float(r["b_gal"]))
    seps.append((C.angle_deg(g["n"], v2), g["name"]))
seps.sort(reverse=True)
nbad = sum(1 for s, _ in seps if s > 0.5)
P(f"  cross-check with sparc_cosmicweb_match.csv: {len(seps)} galaxies compared; max separation {seps[0][0]:.3f} deg "
  f"({seps[0][1]}); > 0.5 deg: {nbad}  " + ", ".join(f"{n} {s:.2f}" for s, n in seps[:5]))
R.num("pos_crosscheck", {"n": len(seps), "max_sep_deg": seps[0][0], "n_gt_0p5deg": nbad, "worst": seps[:5]})
check("POSX the VizieR positions agree with the cosmic-web table (<= 0.5 deg) for every galaxy resolved in both",
      f"max {seps[0][0]:.3f} deg; {nbad} above 0.5 deg", nbad == 0, load_bearing=False,
      reading="any disagreement is listed; the VizieR (SPARC catalogue) position is the one used")

# ------------------------------------------------------------------------------------------------ MUTATE injection
V_over = None
if C.MUTATE:
    banner("A1m  *** MUTATE=1: injecting a dipole A = 0.20 in a random direction into the data (point level) ***")
    rng = np.random.default_rng(182)
    d_inj = C.random_unit(rng)
    D_inj = 0.20 * d_inj
    l_i, b_i = C.lb_of(d_inj)
    P(f"  injected direction (l, b) = ({l_i:.2f}, {b_i:.2f}); D_inj = {np.round(D_inj, 4).tolist()}")
    R.num("mutate_injection", {"A": 0.20, "l": l_i, "b": b_i, "D_inj": D_inj, "a0_ref": C.A0_REF, "seed": 182})
    nuf = C.KERNELS["nu_mono"]
    V_over = []
    for g in use:
        S = g["Vg"] * np.abs(g["Vg"]) + C.UPS_D0 * g["Vd"] ** 2 + C.UPS_B0 * g["Vb"] ** 2
        y = S * 1e6 / (g["R"] * C.KPC_M) / C.A0_REF
        fac = 1.0 + float(D_inj @ g["n"])
        V_over.append(g["V"] * np.sqrt(nuf(y / fac) / nuf(y)))
    ratio = np.concatenate([v / g["V"] for v, g in zip(V_over, use)])
    P(f"  velocity factors: min {ratio.min():.4f}, median {np.median(ratio):.4f}, max {ratio.max():.4f}")

# ------------------------------------------------------------------------------------------------ profiles
banner("A2  PROFILE CURVES chi2_i(log10 a0), nuisances profiled (LML 2018 priors)")
kernels = ["nu_mono"] if C.MUTATE else ["nu_mono", "P2", "simple"]
store = {}
for kn in kernels:
    chi, par = C.compute_profiles(use, kn, GR, V_override=V_over)
    store[kn] = (chi, par)
    jm = np.nanargmin(chi, axis=1)
    xb = GR[jm]
    edge = np.sum((jm == 0) | (jm == len(GR) - 1))
    P(f"  {kn:8s}: {chi.shape[0]} curves x {chi.shape[1]} grid points {R.el()}; all finite: {np.all(np.isfinite(chi))}; "
      f"per-galaxy best log a0: median {np.median(xb):.3f}, 16-84% [{np.percentile(xb, 16):.3f}, {np.percentile(xb, 84):.3f}]; "
      f"minima at a grid edge: {edge}")
    R.num(f"per_galaxy_best_loga0_{kn}", {"median": np.median(xb), "p16": np.percentile(xb, 16), "p84": np.percentile(xb, 84),
                                          "n_edge": int(edge)})
    check(f"FIN_{kn} every profile curve is finite", f"{np.sum(~np.isfinite(chi))} non-finite values", np.all(np.isfinite(chi)))

# optimizer check: warm-started profile vs multi-start cold fits at random (galaxy, grid) pairs
banner("A3  OPTIMIZER CHECK: warm-started profile vs 6 cold starts at 60 random (galaxy, grid point) pairs")
rng = np.random.default_rng(7)
chi, par = store["nu_mono"]
worst = 0.0
nuf = C.KERNELS["nu_mono"]
for t in range(60):
    i = int(rng.integers(len(use)))
    j = int(rng.integers(20, len(GR) - 20))
    g = use[i]
    Vo = g["V"] if V_over is None else V_over[i]
    lo, hi = C._bounds(g)
    if g["eInc"] <= 0:
        lo[3], hi[3] = -1e-9, 1e-9
    bestc = np.inf
    for s in range(6):
        p0 = np.clip(rng.normal(0, 1.5, 4), lo + 1e-6, hi - 1e-6)
        r = C.least_squares(C._resid, p0, jac=C._jac, bounds=(lo, hi), args=(g, 10 ** GR[j], nuf, Vo), method="trf",
                            xtol=1e-10, ftol=1e-10, gtol=1e-10, max_nfev=400)
        bestc = min(bestc, 2 * r.cost)
    worst = max(worst, chi[i, j] - bestc)
P(f"  largest (warm - best cold) chi2 over the 60 pairs: {worst:.4f}")
R.num("optimizer_worst_excess", worst)
check("OPT the warm-started profile is never worse than 6 cold starts by more than 0.05 in chi2", f"{worst:.4f}", worst <= 0.05)

# smoothness: second differences of the curves near their minima (continuity of the warm start)
C2 = np.abs(np.diff(chi, 2, axis=1))
rough = np.max(np.nanmedian(C2, axis=1))
P(f"  median |second difference| per curve, worst galaxy: {rough:.3f} (a smooth parabola of width 0.1 dex gives ~0.02)")

# ------------------------------------------------------------------------------------------------ save
out = dict(grid=GR, names=np.array([g["name"] for g in use]), l=np.array([g["l"] for g in use]),
           b=np.array([g["b"] for g in use]), n=np.array([g["n"] for g in use]), D=np.array([g["D"] for g in use]),
           eD=np.array([g["eD"] for g in use]), fD=np.array([g["fD"] for g in use]), Inc=np.array([g["Inc"] for g in use]),
           eInc=np.array([g["eInc"] for g in use]), Q=np.array([g["Q"] for g in use]), npt=np.array([g["npt"] for g in use]),
           clean=np.array([g["clean"] for g in use]))
for kn, (chi, par) in store.items():
    out[f"chi_{kn}"] = chi
    out[f"par_{kn}"] = par
if C.MUTATE:
    out["D_inj"] = D_inj
npz = os.path.join(C.HERE, f"cfg182_a_profiles{R.suf}.npz")
np.savez_compressed(npz, **out)
P(f"\n  wrote {os.path.basename(npz)}")
sys.exit(R.finish())
