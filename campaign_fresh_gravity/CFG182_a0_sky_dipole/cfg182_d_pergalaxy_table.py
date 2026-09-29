#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG182 part D -- SECONDARY: the sky dipole on the repo's per-galaxy a0 table, real_research/data/sparc_a0_environment_table.csv
(122 galaxies).  LABEL: this table INHERITS PER-GALAXY FITTING NOISE AND FIXED NUISANCES.  Its log10 a0 is the median over
each galaxy's deep points (g_bar < 4e-11) of 2 log g_obs - log g_bar at fixed Upsilon_disk = 0.5, Upsilon_bul = 0.7, the
catalogue distance and inclination (real_research/reviews/project_sparc_a0_vs_cosmicweb.py); it carries no errors, so every
galaxy gets equal weight.  It is closest in spirit to per-galaxy a0 fits with nuisances held fixed.

Statistic, null and lines as in part B (FROZEN_QUESTION.md): free-direction dipole log a0_i = L + log10(1 + D.n_i) (equal
weights, least squares), permutation null (simple and Ursa-Major block, 5000 each), galaxy bootstrap (2000), hemisphere
scan (HEALPix nside 16, >= 10 per side) with its permutation null (2000), fixed-direction amplitudes along the published
and reference directions, the distance-method split (H: f_D = 1; I: f_D in {2, 3, 5}).  Reported; the PRIMARY is part B.
Also the Q <= 2, Inc >= 30 subset.

MUTATE=1: a dipole A = 0.20 in the random direction of seed 182 is added to the table's log a0 (log10(1 + D_inj.n_i));
required (load-bearing): D_mut - D_obs has amplitude 0.20 +- 0.05 within 25 deg of the injected direction.
Run:  python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_d_pergalaxy_table.py      (MUTATE=1 for the control)
"""
import os
import sys
import csv
import math
import numpy as np
from scipy.stats import chi2 as chi2dist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg182_common as C

R = C.Run("cfg182_d_pergalaxy_table")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip())
NPERM, NBOOT, NPH, NBS = 5000, 2000, 2000, 1000
ST7 = [np.zeros(3)] + [0.3 * s * e for e in np.eye(3) for s in (1, -1)]
rng = np.random.default_rng(1840 + (1 if C.MUTATE else 0))

rows = list(csv.DictReader(open(os.path.join(C.DATA, "sparc_a0_environment_table.csv"))))
G = {g["name"]: g for g in C.load_galaxies()}
rows = [r for r in rows if r["name"] in G and r["log10_a0"] not in ("", None)]
y = np.array([float(r["log10_a0"]) for r in rows])
gl = [G[r["name"]] for r in rows]
n = np.array([g["n"] for g in gl])
fD = np.array([g["fD"] for g in gl])
Q = np.array([g["Q"] for g in gl])
Inc = np.array([g["Inc"] for g in gl])
N = len(y)
P(f"\n  table rows with a value and a SPARC match: {N}; log10 a0 mean {y.mean():.3f}, sd {y.std(ddof=1):.3f} dex")
check("T1 all 122 table rows matched to SPARC positions", f"{N}/122", N == 122)
if C.MUTATE:
    D_inj = 0.20 * C.random_unit(np.random.default_rng(182))
    y_un = y.copy()
    y = y + np.log10(1.0 + n @ D_inj)
    P(f"  *** MUTATE=1: log a0 += log10(1 + D_inj.n), D_inj = {np.round(D_inj, 4).tolist()} ***")

GRID = np.round(np.arange(-12.5, -7.9999, 0.01), 2)
sd = float(np.std(y, ddof=1))


def curves(yv):
    return C.Curves(GRID, (GRID[None, :] - yv[:, None]) ** 2 / sd ** 2, None, birge=False)


cv = curves(y)
A = lambda r: float(np.linalg.norm(r["theta"]))
pval = lambda nul, o: (1 + np.sum(np.asarray(nul) >= o - 1e-12)) / (1 + len(nul))
bm = lambda k: rng.multinomial(k, np.full(k, 1.0 / k)).astype(float)

banner("D1  FREE-DIRECTION DIPOLE, bootstrap, permutation nulls")
r0 = C.fit_const(cv)
r1 = C.fit_template(cv, n, starts=ST7)
D_obs, A_obs = r1["theta"], A(r1)
d_obs = D_obs / A_obs
lb = C.lb_of(d_obs)
Db = np.array([C.fit_template(cv, n, w=bm(N), starts=[np.zeros(3), D_obs])["theta"] for _ in range(NBOOT)])
sA = float(math.sqrt(d_obs @ np.cov(Db.T) @ d_obs))
ang = np.array([C.angle_deg(v, d_obs) for v in Db])
c68, c95 = np.percentile(ang, 68), np.percentile(ang, 95)
nul_s = np.array([A(C.fit_template(cv, n[rng.permutation(N)])) for _ in range(NPERM)])
uma = np.where(fD == 4)[0]
others = np.where(fD != 4)[0]
nu_ = n[uma].mean(0)
nu_ /= np.linalg.norm(nu_)
unit_of = np.zeros(N, int)
unit_of[others] = np.arange(1, len(others) + 1)
pos_u = np.vstack([nu_[None, :], n[others]])
A_obs_b = A(C.fit_template(cv, pos_u[unit_of], starts=ST7))
nul_b = np.array([A(C.fit_template(cv, pos_u[rng.permutation(len(pos_u))][unit_of])) for _ in range(NPERM)])
p_s, p_b = pval(nul_s, A_obs), pval(nul_b, A_obs_b)
P(f"  log a0_bar = {r0['L']:.3f}; dipole A = {A_obs:.3f} +- {sA:.3f} (bootstrap) toward (l, b) = ({lb[0]:.1f}, {lb[1]:.1f}); "
  f"cones 68% {c68:.0f} deg, 95% {c95:.0f} deg")
P(f"  permutation p_A: simple {p_s:.4f} (null median {np.median(nul_s):.3f}, 95% {np.percentile(nul_s, 95):.3f}); block {p_b:.4f}")
R.num("dipole", {"N": N, "L": r0["L"], "A": A_obs, "sigA": sA, "lb": lb, "cone68": c68, "cone95": c95, "p_simple": p_s,
                 "p_block": p_b, "null_median": np.median(nul_s), "null95": np.percentile(nul_s, 95)})
check("S1sec p_A < 0.003 (secondary table; the larger of simple and block)", f"p = {max(p_s, p_b):.4f}", max(p_s, p_b) < 0.003,
      load_bearing=False)

banner("D2  FIXED DIRECTIONS and the hemisphere statistic (the published comparisons)")
DIRS = {"CMB (264.0, 48.3)": C.unitvec(264.0, 48.3), "Chang+2018 (171.30, -15.41)": C.unitvec(171.30, -15.41),
        "Zhou+2017 (175.5, -6.5)": C.unitvec(175.5, -6.5), "bulk flow (304, 6), memory": C.unitvec(304.0, 6.0)}
FIX = {}
for k, d in DIRS.items():
    a = float(C.fit_template(cv, (n @ d)[:, None])["theta"][0])
    s = float(np.std([C.fit_template(cv, (n @ d)[:, None], w=bm(N))["theta"][0] for _ in range(NBS)]))
    FIX[k] = {"A": a, "sig": s}
    P(f"  {k:30s} A = {a:+.3f} +- {s:.3f}")
dirs16 = C.healpix_dirs(16)
H, _, _ = C.hemisphere_scan(cv, n, dirs16)
jm = int(np.nanargmax(H))
Hmax, lbH = float(H[jm]), C.lb_of(dirs16[jm])
Hn = np.array([np.nanmax(C.hemisphere_scan(cv, n, dirs16, idx_perm=rng.permutation(N))[0]) for _ in range(NPH)])
pH = pval(Hn, Hmax)
dz = DIRS["Zhou+2017 (175.5, -6.5)"]


def hz(w=None):
    m = n @ dz > 0
    ww = np.ones(N) if w is None else w
    aN = 10 ** (np.sum(ww[m] * y[m]) / np.sum(ww[m]))
    aS = 10 ** (np.sum(ww[~m] * y[~m]) / np.sum(ww[~m]))
    return 2 * (aN - aS) / (aN + aS)


Hz = hz()
sHz = float(np.std([hz(bm(N)) for _ in range(NBS)]))
P(f"  hemisphere: H_max = {Hmax:.3f} toward ({lbH[0]:.1f}, {lbH[1]:.1f}), permutation p = {pH:.4f} (null median "
  f"{np.median(Hn):.3f}, 95% {np.percentile(Hn, 95):.3f}); at Zhou's axis H = {Hz:+.3f} +- {sHz:.3f} (published 0.37 +- 0.04)")
fc = FIX["Chang+2018 (171.30, -15.41)"]
P(f"  C1 (secondary): along Chang's direction A = {fc['A']:+.3f} +- {fc['sig']:.3f}; 0.25 lies {(0.25 - fc['A']) / fc['sig']:+.2f} "
  f"sigma above")
R.num("fixed", FIX)
R.num("hemisphere", {"Hmax": Hmax, "lb": lbH, "p": pH, "null_median": np.median(Hn), "null95": np.percentile(Hn, 95), "H_zhou": Hz,
                     "sig_H_zhou": sHz})

banner("D3  DISTANCE-METHOD SPLIT and the Q <= 2, Inc >= 30 subset")
out = {}
for lab, idx in (("H f_D=1", np.where(fD == 1)[0]), ("I f_D=2,3,5", np.where(np.isin(fD, [2, 3, 5]))[0]),
                 ("clean Q<=2 Inc>=30", np.where((Q <= 2) & (Inc >= 30))[0])):
    cs = cv.subset(idx)
    r = C.fit_template(cs, n[idx], starts=ST7)
    Ds = r["theta"]
    Dbs = np.array([C.fit_template(cs, n[idx], w=bm(len(idx)), starts=[np.zeros(3), Ds])["theta"] for _ in range(NBS)])
    ap = float(C.fit_template(cs, (n[idx] @ d_obs)[:, None])["theta"][0])
    sp = float(np.std([C.fit_template(cs, (n[idx] @ d_obs)[:, None], w=bm(len(idx)))["theta"][0] for _ in range(NBS)]))
    nul = np.array([A(C.fit_template(cs, n[idx][rng.permutation(len(idx))])) for _ in range(2000)])
    out[lab] = {"N": len(idx), "A": float(np.linalg.norm(Ds)), "lb": C.lb_of(Ds), "D": Ds, "Sig": np.cov(Dbs.T), "a_par": ap,
                "s_par": sp, "p": pval(nul, float(np.linalg.norm(Ds)))}
    P(f"  {lab:20s} N = {len(idx):3d}: A = {np.linalg.norm(Ds):.3f} toward ({C.lb_of(Ds)[0]:.1f}, {C.lb_of(Ds)[1]:.1f}), "
      f"permutation p = {out[lab]['p']:.4f}; along the full-table direction {ap:+.3f} +- {sp:.3f}")
dD = out["H f_D=1"]["D"] - out["I f_D=2,3,5"]["D"]
chi = float(dD @ np.linalg.solve(out["H f_D=1"]["Sig"] + out["I f_D=2,3,5"]["Sig"], dD))
P(f"  H vs I: chi2 = {chi:.2f} (3 dof), p = {chi2dist.sf(chi, 3):.3f}")
R.num("split", {k: {kk: vv for kk, vv in v.items() if kk != "Sig"} for k, v in out.items()})
R.num("split_HI", {"chi2": chi, "p": chi2dist.sf(chi, 3)})

if C.MUTATE:
    banner("M1  MUTATE RECOVERY (secondary)")
    cu = curves(y_un)
    Du = C.fit_template(cu, n, starts=ST7)["theta"]
    mv = D_obs - Du
    amp, an = float(np.linalg.norm(mv)), C.angle_deg(mv, D_inj)
    check("M1sec D_mut - D_obs = 0.20 +- 0.05 within 25 deg of the injected direction", f"amplitude {amp:.4f}, angle {an:.1f} deg",
          abs(amp - 0.2) <= 0.05 and an <= 25)
    R.num("mutate", {"D_inj": D_inj, "move": mv, "amp": amp, "angle": an})
sys.exit(R.finish())
