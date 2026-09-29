#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG182 part B -- THE SKY DIPOLE OF a0 IN SPARC: global fit a0(n) = a0_bar (1 + D.n) over all points of the clean sample
with the per-galaxy nuisances profiled (part A's curves), the permutation null (simple and Ursa-Major-block), the
curve-level Gaussian-noise null, the galaxy bootstrap, fixed-direction fits (CMB, bulk flow, the two published
directions), the hemisphere scan (the Zhou et al. 2017 statistic), the systematics (distance-method split, inclination
split, footprint, peculiar-velocity template, distance trend), variants (no Birge scaling, kernels P2 and simple, all
usable galaxies), the Neyman upper limit A95, the orientation-quadrupole reading, and the G8 translation.

Frozen question, pass lines and MUTATE control: FROZEN_QUESTION.md (written before any script; Addendum 1 before this one).
  SIGNAL only if S1 (p_A < 0.003, the larger of the simple and block permutation p) AND S2 (distance-split stability)
  AND S3 (fitted direction not aligned with the footprint axis within the 95% bootstrap cone).  Otherwise NULL + A95.
MUTATE=1 reads cfg182_a_profiles_MUTATE.npz (a dipole A = 0.20 injected at the point level in a random direction) and
requires M1: D_mut - D_obs has amplitude 0.20 +- 0.05 and lies within 25 deg of the injected direction.
kappa = 1/2 stays FITTED; a0_bar is fitted here.
Run:  python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_b_dipole.py        (MUTATE=1 for the control)
"""
import os
import sys
import math
import json
import numpy as np
from scipy.stats import chi2 as chi2dist
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg182_common as C

R = C.Run("cfg182_b_dipole")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip())
SUF = R.suf
NPERM, NBOOT, NGAUSS, NBOOT_SUB, NPERM_VAR, NPERM_HEMI, NPERM_OR, NTRIAL_UL = 5000, 2000, 5000, 1000, 2000, 2000, 500, 300
KN = "nu_mono"

# ================================================================================================ data
z = np.load(os.path.join(C.HERE, f"cfg182_a_profiles{SUF}.npz"))
GRID = z["grid"]
SEL = z["clean"]
n_all = z["n"]
N = int(SEL.sum())
n = n_all[SEL]
fD = z["fD"][SEL]
Inc = z["Inc"][SEL]
Dm = z["D"][SEL]
npt = z["npt"][SEL]
names = z["names"][SEL]
cv = C.Curves(GRID, z[f"chi_{KN}"][SEL], npt, birge=True)
ST7 = [np.zeros(3)] + [0.3 * s * e for e in np.eye(3) for s in (1, -1)]
rng = np.random.default_rng(1820 + (1 if C.MUTATE else 0))

DIRS = {"CMB dipole (264.0, 48.3)": C.unitvec(264.0, 48.3),
        "bulk flow, Carrick+2015 (304, 6), from memory": C.unitvec(304.0, 6.0),
        "Chang+2018 (171.30, -15.41)": C.unitvec(171.30, -15.41),
        "Zhou+2017 max hemisphere (175.5, -6.5)": C.unitvec(175.5, -6.5),
        "Virgo (283.8, 74.5), from memory": C.unitvec(283.8, 74.5)}
uma = np.where(fD == 4)[0]
n_uma = n[uma].mean(axis=0)
n_uma /= np.linalg.norm(n_uma)
DIRS["Ursa Major members' mean " + str(tuple(round(v, 1) for v in C.lb_of(n_uma)))] = n_uma


def Ahat(r):
    return float(np.linalg.norm(r["theta"]))


def fit_free(cvx, nv, w=None, delta=None, starts=None):
    return C.fit_template(cvx, nv, w=w, delta=delta, starts=starts)


def fit_fixed(cvx, nv, d, w=None, delta=None):
    r = C.fit_template(cvx, (nv @ d)[:, None], w=w, delta=delta)
    return float(r["theta"][0]), r


def boot_multi(Nx):
    return rng.multinomial(Nx, np.full(Nx, 1.0 / Nx)).astype(float)


def pval(null, obs):
    null = np.asarray(null)
    return (1 + np.sum(null >= obs - 1e-12)) / (1 + len(null))


def cone(vecs, dhat, q):
    ang = np.array([C.angle_deg(v, dhat) if np.linalg.norm(v) > 0 else 180.0 for v in vecs])
    return float(np.percentile(ang, q))


# ================================================================================================ B0
banner("B0  SAMPLE, ERROR SCALING, FOOTPRINT")
f_vec = n.mean(axis=0)
f_hat = f_vec / np.linalg.norm(f_vec)
P(f"  clean sample: {N} galaxies, {int(npt.sum())} points; f_D counts: " +
  ", ".join(f"{k}: {int(np.sum(fD == k))}" for k in (1, 2, 3, 4, 5)))
P(f"  Birge factors s_i: median {np.median(cv.s):.2f}, 84% {np.percentile(cv.s, 84):.2f}, max {cv.s.max():.1f}; "
  f"galaxies with s_i > 1: {int(np.sum(cv.s > 1))}")
P(f"  per-galaxy (scaled) Delta chi2 = 1 half-width in log a0: median {np.median(cv.sig):.3f} dex, 16-84% "
  f"[{np.percentile(cv.sig, 16):.3f}, {np.percentile(cv.sig, 84):.3f}]")
P(f"  footprint: mean position vector |<n>| = {np.linalg.norm(f_vec):.3f} toward (l, b) = "
  f"({C.lb_of(f_hat)[0]:.1f}, {C.lb_of(f_hat)[1]:.1f}); galaxies with b > 0: {int(np.sum(n[:, 2] > 0))}/{N}")
R.num("sample", {"N": N, "npts": int(npt.sum()), "birge_median": np.median(cv.s), "halfwidth_median_dex": np.median(cv.sig),
                 "footprint_amp": np.linalg.norm(f_vec), "footprint_lb": C.lb_of(f_hat)})

# ================================================================================================ B1
banner("B1  PRIMARY: global fit a0_i = a0_bar (1 + D.n_i), nu_mono, Birge scaling, profiled nuisances")
r0 = C.fit_const(cv)
F0, L0 = r0["F"], r0["L"]
r1 = fit_free(cv, n, starts=ST7)
D_obs = r1["theta"].copy()
A_obs = Ahat(r1)
d_obs = D_obs / A_obs
lb_obs = C.lb_of(d_obs)
dchi_obs = F0 - r1["F"]
fun = C.obj_template(cv, n)
Hs = C.hessian(fun, r1["q"])
cov = 2.0 * np.linalg.inv(Hs)
sigA_fisher = float(math.sqrt(d_obs @ cov[1:, 1:] @ d_obs))
HDD = Hs[1:, 1:] - np.outer(Hs[1:, 0], Hs[0, 1:]) / Hs[0, 0]
ev, evec = np.linalg.eigh(HDD)
d_weak = evec[:, 0]
P(f"  no-dipole fit: log a0_bar = {L0:.4f} (a0_bar = {10 ** L0:.3e} m/s^2), scaled chi2 = {F0:.2f} over {N} curves")
P(f"  dipole fit:    log a0_bar = {r1['L']:.4f}; D = ({D_obs[0]:+.4f}, {D_obs[1]:+.4f}, {D_obs[2]:+.4f}); "
  f"A = {A_obs:.4f} toward (l, b) = ({lb_obs[0]:.1f}, {lb_obs[1]:.1f}); Delta chi2 = {dchi_obs:.3f} (3 extra parameters)")
P(f"  Fisher (curvature) sigma_A along the fitted direction = {sigA_fisher:.4f} (reference only); least-constrained direction "
  f"of D: (l, b) = {tuple(round(v, 1) for v in C.lb_of(d_weak))} with sigma {math.sqrt(2 / ev[0]):.3f}, best-constrained "
  f"sigma {math.sqrt(2 / ev[2]):.3f}")
P(f"  (framework footings for reference: canonical 9.36e-11, alt 1.13e-10; the fitted a0_bar is kernel- and prior-conditional)")
R.num("primary", {"L0": L0, "a0_bar_nodipole": 10 ** L0, "F0": F0, "L": r1["L"], "D": D_obs, "A": A_obs, "l": lb_obs[0],
                  "b": lb_obs[1], "dchi2": dchi_obs, "sigA_fisher": sigA_fisher, "weak_dir_lb": C.lb_of(d_weak),
                  "sig_weak": math.sqrt(2 / ev[0]), "sig_strong": math.sqrt(2 / ev[2])})

# single-start vs seven-start agreement on 200 permutations
dd = 0.0
for k in range(200):
    p = rng.permutation(N)
    a1 = Ahat(fit_free(cv, n[p]))
    a7 = Ahat(fit_free(cv, n[p], starts=ST7))
    dd = max(dd, abs(a1 - a7))
check("K1 the one-start fit used in the nulls agrees with the seven-start fit (200 permutations, |dA| < 1e-3)", f"max |dA| = {dd:.2e}",
      dd < 1e-3)

# ================================================================================================ B2
banner(f"B2  GALAXY BOOTSTRAP ({NBOOT} resamples; positions travel with galaxies)")
Db, Lb = [], []
for k in range(NBOOT):
    w = boot_multi(N)
    r = fit_free(cv, n, w=w, starts=[np.zeros(3), D_obs])
    Db.append(r["theta"])
    Lb.append(r["L"])
Db = np.array(Db)
Sig_boot = np.cov(Db.T)
sigA_boot = float(math.sqrt(d_obs @ Sig_boot @ d_obs))
Ab = np.linalg.norm(Db, axis=1)
th68, th95 = cone(Db, d_obs, 68), cone(Db, d_obs, 95)
P(f"  sigma of D components: {np.sqrt(np.diag(Sig_boot)).round(4).tolist()}; sigma_A along the fitted direction = {sigA_boot:.4f}")
P(f"  bootstrap |D|: median {np.median(Ab):.3f}, 16-84% [{np.percentile(Ab, 16):.3f}, {np.percentile(Ab, 84):.3f}]; "
  f"sigma(log a0_bar) = {np.std(Lb):.4f}")
P(f"  direction cone about (l, b) = ({lb_obs[0]:.1f}, {lb_obs[1]:.1f}): 68% within {th68:.1f} deg, 95% within {th95:.1f} deg")
R.num("bootstrap", {"sigA": sigA_boot, "sig_components": np.sqrt(np.diag(Sig_boot)), "A_median": np.median(Ab),
                    "A_p16": np.percentile(Ab, 16), "A_p84": np.percentile(Ab, 84), "cone68": th68, "cone95": th95,
                    "sig_L": np.std(Lb)})

# ================================================================================================ B3
banner(f"B3  PERMUTATION NULL ({NPERM} each): simple, and Ursa-Major block (one unit, one position)")
A_ps, dchi_ps = np.zeros(NPERM), np.zeros(NPERM)
for k in range(NPERM):
    r = fit_free(cv, n[rng.permutation(N)])
    A_ps[k], dchi_ps[k] = Ahat(r), F0 - r["F"]
# block scheme
unit_of = np.zeros(N, int)
others = np.where(fD != 4)[0]
unit_of[uma] = 0
unit_of[others] = np.arange(1, len(others) + 1)
pos_units = np.vstack([n_uma[None, :], n[others]])
n_block = pos_units[unit_of]
rb = fit_free(cv, n_block, starts=ST7)
A_obs_b, dchi_obs_b = Ahat(rb), F0 - rb["F"]
A_pb, dchi_pb = np.zeros(NPERM), np.zeros(NPERM)
for k in range(NPERM):
    pu = rng.permutation(len(pos_units))
    r = fit_free(cv, pos_units[pu][unit_of])
    A_pb[k], dchi_pb[k] = Ahat(r), F0 - r["F"]
pA_s, pA_b = pval(A_ps, A_obs), pval(A_pb, A_obs_b)
pX_s, pX_b = pval(dchi_ps, dchi_obs), pval(dchi_pb, dchi_obs_b)
pA = max(pA_s, pA_b)
P(f"  simple: A_obs = {A_obs:.4f}; null A median {np.median(A_ps):.3f}, 95% {np.percentile(A_ps, 95):.3f}, 99.7% "
  f"{np.percentile(A_ps, 99.7):.3f}; p_A = {pA_s:.4f}; Delta chi2 {dchi_obs:.2f}: null 95% {np.percentile(dchi_ps, 95):.2f}, "
  f"p = {pX_s:.4f}")
P(f"  block:  A_obs = {A_obs_b:.4f} (UMa members at their mean position); null A median {np.median(A_pb):.3f}, 95% "
  f"{np.percentile(A_pb, 95):.3f}; p_A = {pA_b:.4f}; Delta chi2 {dchi_obs_b:.2f}: p = {pX_b:.4f}  {R.el()}")
R.num("permutation", {"A_obs": A_obs, "pA_simple": pA_s, "pA_block": pA_b, "pA": pA, "p_dchi_simple": pX_s,
                      "p_dchi_block": pX_b, "A_obs_block": A_obs_b, "null_A_simple_p50_p95_p997":
                      [np.median(A_ps), np.percentile(A_ps, 95), np.percentile(A_ps, 99.7)],
                      "null_A_block_p50_p95": [np.median(A_pb), np.percentile(A_pb, 95)]})
S1 = pA < 0.003
check("S1 p_A < 0.003 against the permutation null (larger of simple and block)", f"p_A = {pA:.4f} (simple {pA_s:.4f}, "
      f"block {pA_b:.4f})", S1, load_bearing=False)

# ================================================================================================ B4
banner(f"B4  GAUSSIAN-NOISE NULL, curve level ({NGAUSS}): each galaxy's preferred a0 redrawn about a0_bar")
xh, sg = cv.xhat, cv.sig


def nll(q):
    L, lt = q
    v = sg ** 2 + math.exp(2 * lt)
    return np.sum((xh - L) ** 2 / v + np.log(v))


rt = minimize(nll, [L0, math.log(0.1)], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
L_t, tau = rt.x[0], math.exp(rt.x[1])
if tau < 1e-3:
    tau = 0.0
chi_gal = np.sum((xh - L0) ** 2 / sg ** 2) / (N - 1)
P(f"  galaxy-level reduced chi2 of the per-galaxy best log a0 about a0_bar (scaled widths): {chi_gal:.2f}; ML extra "
  f"inter-galaxy scatter tau = {tau:.3f} dex (L = {L_t:.3f})")
A_g = np.zeros(NGAUSS)
sd = np.sqrt(sg ** 2 + tau ** 2)
for k in range(NGAUSS):
    delta = (L0 + rng.normal(0, sd)) - xh
    A_g[k] = Ahat(fit_free(cv, n, delta=delta))
pG = pval(A_g, A_obs)
P(f"  Gaussian null A: median {np.median(A_g):.3f}, 95% {np.percentile(A_g, 95):.3f}, 99.7% {np.percentile(A_g, 99.7):.3f}; "
  f"p_A = {pG:.4f}  {R.el()}")
R.num("gauss_curve_null", {"chi_red_gal": chi_gal, "tau": tau, "pA": pG, "null_A_p50_p95": [np.median(A_g), np.percentile(A_g, 95)]})

# ================================================================================================ B5
banner("B5  FIXED-DIRECTION AMPLITUDES (bootstrap sigma, 1000) and alignments with the fitted direction")
FIX = {}
for lab, d in list(DIRS.items()) + [("footprint axis <n>", f_hat), ("least-constrained Fisher direction", d_weak)]:
    a, _ = fit_fixed(cv, n, d)
    ab = np.array([fit_fixed(cv, n, d, w=boot_multi(N))[0] for _ in range(NBOOT_SUB)])
    s = float(np.std(ab))
    ang = C.angle_deg(d_obs, d)
    ax = min(ang, 180 - ang)
    FIX[lab] = {"A": a, "sig": s, "lo95": a - 1.96 * s, "hi95": a + 1.96 * s, "angle_deg": ang, "axis_angle_deg": ax,
                "in68": ang <= th68, "in95": ang <= th95, "lb": C.lb_of(d)}
    P(f"  {lab:48s} A = {a:+.3f} +- {s:.3f} (95%: [{a - 1.96 * s:+.3f}, {a + 1.96 * s:+.3f}]); angle to fit {ang:5.1f} deg "
      f"(axis {ax:4.1f}); in 68% cone: {ang <= th68}; in 95% cone: {ang <= th95}")
R.num("fixed_directions", FIX)

# ================================================================================================ B6
banner(f"B6  HEMISPHERE SCAN (the Zhou et al. 2017 statistic; HEALPix nside 16; >= 10 galaxies per side)")
dirs16 = C.healpix_dirs(16)
Hh, xN, xS = C.hemisphere_scan(cv, n, dirs16)
jm = int(np.nanargmax(Hh))
Hmax = float(Hh[jm])
lb_H = C.lb_of(dirs16[jm])


def argmin_par(S):
    j = int(np.clip(np.argmin(S), 1, len(S) - 2))
    y0, y1, y2 = S[j - 1], S[j], S[j + 1]
    den = y0 - 2 * y1 + y2
    off = 0.5 * (y0 - y2) / den if den > 0 else 0.0
    return cv.x0 + (j + np.clip(off, -1, 1)) * cv.h


def hemi_axis(nv, d, w=None):
    m = nv @ d > 0
    Cw = cv.C * (1.0 if w is None else w[:, None])
    aN, aS = 10 ** argmin_par(Cw[m].sum(0)), 10 ** argmin_par(Cw[~m].sum(0))
    return 2 * (aN - aS) / (aN + aS), aN, aS, int(m.sum())


dz = DIRS["Zhou+2017 max hemisphere (175.5, -6.5)"]
Hz, aNz, aSz, nNz = hemi_axis(n, dz)
Hzb = np.array([hemi_axis(n, dz, boot_multi(N))[0] for _ in range(NBOOT_SUB)])
sHz = float(np.std(Hzb))
Hmax_null = np.zeros(NPERM_HEMI)
for k in range(NPERM_HEMI):
    Hp, _, _ = C.hemisphere_scan(cv, n, dirs16, idx_perm=rng.permutation(N))
    Hmax_null[k] = np.nanmax(Hp)
pH = pval(Hmax_null, Hmax)
P(f"  H_max = {Hmax:.3f} toward (l, b) = ({lb_H[0]:.1f}, {lb_H[1]:.1f}); permutation null H_max: median "
  f"{np.median(Hmax_null):.3f}, 95% {np.percentile(Hmax_null, 95):.3f}; p = {pH:.4f}  {R.el()}")
P(f"  at Zhou's axis (175.5, -6.5): H = {Hz:+.3f} +- {sHz:.3f} (a_N = {aNz:.3e} with {nNz} galaxies, a_S = {aSz:.3e} with "
  f"{N - nNz})")
R.num("hemisphere", {"Hmax": Hmax, "lb": lb_H, "p": pH, "null_p50_p95": [np.median(Hmax_null), np.percentile(Hmax_null, 95)],
                     "H_zhou_axis": Hz, "sig_H_zhou_axis": sHz, "aN": aNz, "aS": aSz, "nN": nNz})

# ================================================================================================ B7
banner("B7  SYSTEMATICS: distance-method split, inclination split, footprint, peculiar-velocity template, distance trend")


def sub_fit(idx, label):
    cvs = cv.subset(idx)
    ns = n[idx]
    r = fit_free(cvs, ns, starts=ST7)
    Dv = r["theta"]
    Dbs = []
    apar = []
    for _ in range(NBOOT_SUB):
        w = boot_multi(len(idx))
        Dbs.append(fit_free(cvs, ns, w=w, starts=[np.zeros(3), Dv])["theta"])
        apar.append(fit_fixed(cvs, ns, d_obs, w=w)[0])
    Dbs = np.array(Dbs)
    Sg = np.cov(Dbs.T)
    a_par, _ = fit_fixed(cvs, ns, d_obs)
    s_par = float(np.std(apar))
    A_s = float(np.linalg.norm(Dv))
    lbs = C.lb_of(Dv) if A_s > 0 else (float("nan"), float("nan"))
    P(f"  {label:34s} N = {len(idx):3d}: A = {A_s:.3f} toward ({lbs[0]:.1f}, {lbs[1]:.1f}); amplitude along the full-sample "
      f"direction {a_par:+.3f} +- {s_par:.3f}; log a0_bar = {r['L']:.3f}")
    return dict(N=len(idx), D=Dv, A=A_s, lb=lbs, Sig=Sg, a_par=a_par, s_par=s_par, L=r["L"])


iH = np.where(fD == 1)[0]
iI = np.where(np.isin(fD, [2, 3, 5]))[0]
iU = uma
sH, sI, sU = sub_fit(iH, "H: Hubble flow (f_D = 1)"), sub_fit(iI, "I: TRGB/Cepheid/SNIa (f_D = 2,3,5)"), \
    sub_fit(iU, "UMa cluster (f_D = 4)")
dD = sH["D"] - sI["D"]
chi_split = float(dD @ np.linalg.solve(sH["Sig"] + sI["Sig"], dD))
p_split = float(chi2dist.sf(chi_split, 3))
S2a = p_split > 0.05
S2b = (sH["a_par"] / sH["s_par"] >= 1.0) and (sI["a_par"] / sI["s_par"] >= 1.0)
S2 = S2a and S2b
P(f"  H vs I dipole vectors: chi2 = {chi_split:.2f} (3 dof), p = {p_split:.3f}; along-direction amplitudes H "
  f"{sH['a_par'] / sH['s_par']:+.2f} sigma, I {sI['a_par'] / sI['s_par']:+.2f} sigma")
check("S2 distance-split stability: H and I vectors agree (p > 0.05) AND both positive at >= 1 sigma along the full-sample "
      "direction", f"p = {p_split:.3f} (S2a {S2a}); H {sH['a_par'] / sH['s_par']:+.2f} sigma, I {sI['a_par'] / sI['s_par']:+.2f} "
      f"sigma (S2b {S2b})", S2, load_bearing=False)
R.num("split_distance", {"H": {k: v for k, v in sH.items() if k != "Sig"}, "I": {k: v for k, v in sI.items() if k != "Sig"},
                         "UMa": {k: v for k, v in sU.items() if k != "Sig"}, "chi2": chi_split, "p": p_split, "S2a": S2a,
                         "S2b": S2b})
imed = np.median(Inc)
sLo, sHi = sub_fit(np.where(Inc < imed)[0], f"Inc < {imed:.0f} deg"), sub_fit(np.where(Inc >= imed)[0], f"Inc >= {imed:.0f} deg")
dDi = sLo["D"] - sHi["D"]
chi_inc = float(dDi @ np.linalg.solve(sLo["Sig"] + sHi["Sig"], dDi))
P(f"  inclination halves: chi2 = {chi_inc:.2f} (3 dof), p = {chi2dist.sf(chi_inc, 3):.3f}")
R.num("split_inclination", {"median_inc": imed, "lo": {k: v for k, v in sLo.items() if k != "Sig"},
                            "hi": {k: v for k, v in sHi.items() if k != "Sig"}, "chi2": chi_inc, "p": chi2dist.sf(chi_inc, 3)})

ang_fp = C.angle_deg(d_obs, f_hat)
ax_fp = min(ang_fp, 180 - ang_fp)
aligned = ax_fp <= th95
S3 = not aligned
P(f"  footprint axis +-<n> = ({C.lb_of(f_hat)[0]:.1f}, {C.lb_of(f_hat)[1]:.1f}): angle to the fitted direction {ang_fp:.1f} deg "
  f"(axis {ax_fp:.1f}); 95% cone {th95:.1f} deg -> aligned within errors: {aligned}")
P(f"  least-constrained Fisher direction ({C.lb_of(d_weak)[0]:.1f}, {C.lb_of(d_weak)[1]:.1f}): axis angle to the fit "
  f"{min(C.angle_deg(d_obs, d_weak), 180 - C.angle_deg(d_obs, d_weak)):.1f} deg")
check("S3 the fitted direction is NOT aligned with the footprint axis (axis outside the 95% bootstrap cone)",
      f"axis angle {ax_fp:.1f} deg vs cone {th95:.1f} deg", S3, load_bearing=False)
R.num("footprint_alignment", {"angle": ang_fp, "axis_angle": ax_fp, "cone95": th95, "aligned": aligned})

# peculiar-velocity template (Hubble-flow galaxies only), W in units of 1000 km/s
Tpv = np.where(fD == 1, -2.0 * 1000.0 / (C.H0_SPARC * Dm), 0.0)[:, None] * n
rpv = C.fit_template(cv, Tpv, starts=[np.zeros(3)] + [0.1 * s * e for e in np.eye(3) for s in (1, -1)], theta_max=1.5)
W = rpv["theta"] * 1000.0
dchi_pv = F0 - rpv["F"]
pv_null = np.zeros(1000)
for k in range(1000):
    p = rng.permutation(N)
    Tp = np.where(fD == 1, -2.0 * 1000.0 / (C.H0_SPARC * Dm), 0.0)[:, None] * n[p]
    pv_null[k] = F0 - C.fit_template(cv, Tp, theta_max=1.5)["F"]
p_pv = pval(pv_null, dchi_pv)
P(f"  peculiar-velocity template: |W| = {np.linalg.norm(W):.0f} km/s toward ({C.lb_of(W)[0]:.1f}, {C.lb_of(W)[1]:.1f}); "
  f"Delta chi2 = {dchi_pv:.2f} vs the dipole's {dchi_obs:.2f} (both 3 parameters); permutation p = {p_pv:.3f}")
R.num("pv_template", {"W_kms": np.linalg.norm(W), "lb": C.lb_of(W), "dchi2": dchi_pv, "dchi2_dipole": dchi_obs, "p": p_pv})

# distance trend
Zd = np.log10(Dm / 10.0)[:, None]
rdt = C.fit_template(cv, n, Z=Zd, starts=ST7)
rbeta = C.fit_template(cv, np.zeros((N, 1)), Z=Zd)
P(f"  distance trend: beta alone = {rbeta['beta'][0]:+.3f} dex per dex (Delta chi2 {F0 - rbeta['F']:.2f}); with the dipole: "
  f"beta = {rdt['beta'][0]:+.3f}, A = {np.linalg.norm(rdt['theta']):.3f} toward "
  f"({C.lb_of(rdt['theta'])[0]:.1f}, {C.lb_of(rdt['theta'])[1]:.1f})  {R.el()}")
R.num("distance_trend", {"beta_alone": rbeta["beta"][0], "dchi2_beta": F0 - rbeta["F"], "beta_with_dipole": rdt["beta"][0],
                         "A_with_trend": np.linalg.norm(rdt["theta"]), "lb_with_trend": C.lb_of(rdt["theta"])})

# ================================================================================================ B8
banner(f"B8  VARIANTS (reported; each with its own simple permutation null, {NPERM_VAR})")
VAR = {}


def variant(label, cvx, nv):
    r = fit_free(cvx, nv, starts=ST7)
    a = Ahat(r)
    nul = np.array([Ahat(fit_free(cvx, nv[rng.permutation(len(nv))])) for _ in range(NPERM_VAR)])
    pv_ = pval(nul, a)
    lbv = C.lb_of(r["theta"])
    P(f"  {label:44s} N = {len(nv):3d}: A = {a:.3f} toward ({lbv[0]:.1f}, {lbv[1]:.1f}); null 95% {np.percentile(nul, 95):.3f}; "
      f"p_A = {pv_:.4f}")
    VAR[label] = {"N": len(nv), "A": a, "lb": lbv, "p": pv_, "null95": np.percentile(nul, 95)}


variant("no Birge scaling", C.Curves(GRID, z[f"chi_{KN}"][SEL], npt, birge=False), n)
if not C.MUTATE:
    for kk in ("P2", "simple"):
        variant(f"kernel {kk}", C.Curves(GRID, z[f"chi_{kk}"][SEL], npt, birge=True), n)
variant("all usable galaxies (Q = 3 and Inc < 30 included)", C.Curves(GRID, z[f"chi_{KN}"], z["npt"], birge=True), n_all)
R.num("variants", VAR)
P(f"  {R.el()}")

# ================================================================================================ B9
banner(f"B9  NEYMAN UPPER LIMIT: dipoles injected into position-permuted data, random directions ({NTRIAL_UL} per A_inj)")
AINJ = np.round(np.arange(0.0, 0.9001, 0.025), 3)
UL = {}
for scheme in ("simple", "block"):
    frac, meanA, angerr = [], [], []
    Aref = A_obs if scheme == "simple" else A_obs_b
    for ai in AINJ:
        cnt, As, angs = 0, [], []
        for t in range(NTRIAL_UL):
            if scheme == "simple":
                nv = n[rng.permutation(N)]
            else:
                nv = pos_units[rng.permutation(len(pos_units))][unit_of]
            d = C.random_unit(rng)
            delta = np.log10(1.0 + ai * (nv @ d))
            r = fit_free(cv, nv, delta=delta)
            a = Ahat(r)
            As.append(a)
            cnt += a >= Aref
            if ai > 0:
                angs.append(C.angle_deg(r["theta"], d) if a > 0 else 180.0)
        frac.append(cnt / NTRIAL_UL)
        meanA.append(float(np.mean(As)))
        angerr.append(float(np.median(angs)) if angs else float("nan"))
    frac = np.array(frac)
    ok = np.where(frac >= 0.95)[0]
    A95 = float(AINJ[ok[0]]) if len(ok) else float("inf")
    UL[scheme] = {"A95": A95, "frac": frac, "meanA": meanA, "median_angle_err": angerr}
    P(f"  {scheme:6s}: A95 = {A95} (A_obs = {Aref:.3f}); P(A_hat >= A_obs) at A_inj = 0, 0.1, 0.2, 0.3, 0.4, 0.5: "
      + ", ".join(f"{frac[int(round(x / 0.025))]:.2f}" for x in (0, 0.1, 0.2, 0.3, 0.4, 0.5)))
    P(f"          recovery <A_hat> at A_inj = 0, 0.1, 0.2, 0.3, 0.5, 0.7: "
      + ", ".join(f"{meanA[int(round(x / 0.025))]:.3f}" for x in (0, 0.1, 0.2, 0.3, 0.5, 0.7))
      + "; median direction error at 0.2, 0.3, 0.5: "
      + ", ".join(f"{angerr[int(round(x / 0.025))]:.0f}" for x in (0.2, 0.3, 0.5)) + " deg")
A95 = max(UL["simple"]["A95"], UL["block"]["A95"])
R.num("upper_limit", {"A95": A95, "A95_simple": UL["simple"]["A95"], "A95_block": UL["block"]["A95"], "grid": AINJ,
                      "detail": UL})
P(f"  A95 (the larger of the two schemes) = {A95}  {R.el()}")
rec_hi = UL["simple"]["meanA"][int(round(0.7 / 0.025))]
check("K2 the injection machinery recovers a large dipole (A_inj = 0.7: <A_hat> within 0.1)", f"<A_hat> = {rec_hi:.3f}",
      abs(rec_hi - 0.7) < 0.1, load_bearing=False)

# ================================================================================================ B10
banner("B10  THE PUBLISHED CLAIMS")
fc = FIX["Chang+2018 (171.30, -15.41)"]
z1 = (0.25 - fc["A"]) / fc["sig"]
C1_excl = not (fc["lo95"] <= 0.25 <= fc["hi95"])
P(f"  C1 Chang+2018 dipole 0.25 +- 0.04 toward (171.30, -15.41): this lane along that direction A = {fc['A']:+.3f} +- "
  f"{fc['sig']:.3f}; 0.25 lies {z1:+.2f} sigma above; excluded at 95%: {C1_excl}")
z2 = (0.37 - Hz) / math.sqrt(sHz ** 2 + 0.04 ** 2)
P(f"  C2 Zhou+2017 hemisphere anisotropy 0.37 +- 0.04 at (175.5, -6.5): this lane H = {Hz:+.3f} +- {sHz:.3f}; difference "
  f"{z2:+.2f} sigma (combined); this lane's own H_max = {Hmax:.3f} toward ({lb_H[0]:.1f}, {lb_H[1]:.1f}), p = {pH:.4f}")
R.num("claims", {"C1_A_along_chang": fc["A"], "C1_sig": fc["sig"], "C1_z_of_0p25": z1, "C1_excluded95": C1_excl,
                 "C2_H_zhou": Hz, "C2_sig": sHz, "C2_z_of_0p37": z2, "Hmax": Hmax, "Hmax_lb": lb_H, "Hmax_p": pH})

# ================================================================================================ B11
banner(f"B11  ORIENTATION READING (reported): a0_i = a0_bar (1 + eps [1/2 sin^2 i - 1/3 + P2(cos i) (n_i.f)^2])")
dirs4 = C.healpix_dirs(4)
dirs4 = dirs4[dirs4[:, 2] >= 0]                               # f and -f are the same model
si2 = np.sin(np.radians(Inc)) ** 2
P2c = 0.5 * (3 * np.cos(np.radians(Inc)) ** 2 - 1)


def orient_best(nv):
    best = None
    for f in dirs4:
        m = (0.5 * si2 - 1.0 / 3.0 + P2c * (nv @ f) ** 2)[:, None]
        r = C.fit_template(cv, m, theta_max=2.0)
        if best is None or r["F"] < best[0]:
            best = (r["F"], float(r["theta"][0]), f)
    return best


ob = orient_best(n)
dchi_or = F0 - ob[0]
or_null = np.array([F0 - orient_best(n[rng.permutation(N)])[0] for _ in range(NPERM_OR)])
p_or = pval(or_null, dchi_or)
P(f"  best eps = {ob[1]:+.3f} with flow axis (l, b) = ({C.lb_of(ob[2])[0]:.1f}, {C.lb_of(ob[2])[1]:.1f}); Delta chi2 = "
  f"{dchi_or:.2f}; permutation p = {p_or:.3f} ({NPERM_OR})  {R.el()}")
R.num("orientation", {"eps": ob[1], "lb": C.lb_of(ob[2]), "dchi2": dchi_or, "p": p_or})

# ================================================================================================ B12 verdict + G8
banner("B12  VERDICT AND THE G8 TRANSLATION")
SIGNAL = bool(S1 and S2 and S3)
P(f"  S1 (p_A < 0.003): {S1} [p_A = {pA:.4f}];  S2 (distance split stable): {S2};  S3 (not footprint-aligned): {S3}")
P(f"  VERDICT: {'SIGNAL (passes S1-S3)' if SIGNAL else 'NULL (no directional signal passing the frozen lines)'}")
P(f"  A = {A_obs:.3f} +- {sigA_boot:.3f} (bootstrap, along the fitted direction) toward ({lb_obs[0]:.1f}, {lb_obs[1]:.1f}); "
  f"A95 (random direction) = {A95}")
P(f"  G8: a sky-direction modulation a0 (1 + eps f.n) of the owner's flow needs eps < {A95} (95%, random direction); the "
  f"deep-MOND force goes as sqrt(a0), so the force anisotropy is < {A95 / 2:.3f}; along named directions (95% two-sided "
  f"upper ends): " + ", ".join(f"{k.split(' (')[0].split(',')[0]} {v['hi95']:.2f}" for k, v in FIX.items()
                               if not k.startswith("least") and not k.startswith("footprint")))
R.num("verdict", {"S1": S1, "S2": S2, "S3": S3, "SIGNAL": SIGNAL, "A": A_obs, "sigA_boot": sigA_boot, "A95": A95,
                  "G8_force_anisotropy_bound": A95 / 2})

# ================================================================================================ MUTATE M1
if C.MUTATE:
    banner("M1  MUTATE RECOVERY: the fitted dipole vector must move by the injected vector")
    D_inj = z["D_inj"]
    z0 = np.load(os.path.join(C.HERE, "cfg182_a_profiles.npz"))
    cv0 = C.Curves(z0["grid"], z0[f"chi_{KN}"][z0["clean"]], z0["npt"][z0["clean"]], birge=True)
    r_un = fit_free(cv0, z0["n"][z0["clean"]], starts=ST7)
    dmove = D_obs - r_un["theta"]
    amp = float(np.linalg.norm(dmove))
    angm = C.angle_deg(dmove, D_inj)
    sA0dir = []
    for _ in range(500):
        rr = fit_free(cv0, z0["n"][z0["clean"]], w=boot_multi(cv0.N), starts=[np.zeros(3), r_un["theta"]])
        sA0dir.append(rr["theta"] @ (r_un["theta"] / max(np.linalg.norm(r_un["theta"]), 1e-12)))
    sA0 = float(np.std(sA0dir))
    P(f"  injected D = {np.round(D_inj, 4).tolist()} (A = 0.20 toward {tuple(round(v, 1) for v in C.lb_of(D_inj))}); "
      f"unmutated D = {np.round(r_un['theta'], 4).tolist()}; mutated D = {np.round(D_obs, 4).tolist()}")
    P(f"  D_mut - D_obs: amplitude {amp:.4f}, angle to the injected direction {angm:.1f} deg")
    m1 = (abs(amp - 0.20) <= 0.05) and (angm <= 25.0)
    check("M1 MUTATE recovery: |D_mut - D_obs| = 0.20 +- 0.05 and within 25 deg of the injected direction",
          f"amplitude {amp:.4f}, angle {angm:.1f} deg", m1)
    need = 0.20 >= 4 * sA0
    P(f"  M2: real-data sigma_A (bootstrap, 500) = {sA0:.3f}; 0.20 >= 4 sigma_A: {need}; mutated-data p_A = {pA:.4f}")
    check("M2 (power statement) mutated p_A < 0.003 is required only if 0.20 >= 4 sigma_A of the real data",
          f"required: {need}; p_A = {pA:.4f}", (pA < 0.003) or (not need), load_bearing=False)
    R.num("mutate", {"D_inj": D_inj, "D_unmutated": r_un["theta"], "D_mutated": D_obs, "move_amp": amp, "move_angle": angm,
                     "M1": m1, "sigA_real_500": sA0, "M2_required": need, "pA_mutated": pA})

# ================================================================================================ outputs
np.savez_compressed(os.path.join(C.HERE, f"cfg182_b_nulls{SUF}.npz"), A_perm_simple=A_ps, A_perm_block=A_pb,
                    dchi_perm_simple=dchi_ps, dchi_perm_block=dchi_pb, A_gauss=A_g, D_boot=Db, Hmax_null=Hmax_null,
                    pv_null=pv_null, or_null=or_null)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def mw(v):
        l, b = C.lb_of(v)
        l = (l + 180) % 360 - 180
        return -math.radians(l), math.radians(b)

    fig = plt.figure(figsize=(10, 5.6))
    ax = fig.add_subplot(111, projection="mollweide")
    res = np.clip(cv.xhat - L0, -0.6, 0.6)
    L_ = np.array([(lb[0] + 180) % 360 - 180 for lb in map(C.lb_of, n)])
    B_ = np.array([C.lb_of(v)[1] for v in n])
    sc = ax.scatter(-np.radians(L_), np.radians(B_), c=res, cmap="coolwarm", s=18, vmin=-0.6, vmax=0.6, edgecolors="k",
                    linewidths=0.3)
    for lab, v, mk in [("fit", d_obs, "*"), ("CMB", DIRS["CMB dipole (264.0, 48.3)"], "^"),
                       ("Chang+18", DIRS["Chang+2018 (171.30, -15.41)"], "s"),
                       ("Zhou+17", DIRS["Zhou+2017 max hemisphere (175.5, -6.5)"], "D"), ("footprint", f_hat, "o")]:
        x, y = mw(v)
        ax.plot(x, y, marker=mk, ms=12, mfc="none" if mk != "*" else "gold", mec="k", ls="none")
        ax.text(x, y + 0.08, lab, fontsize=8, ha="center")
    ax.set_xticklabels([f"{t}" for t in (150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210)], fontsize=7)
    ax.grid(alpha=0.3)
    plt.colorbar(sc, orientation="horizontal", pad=0.07, fraction=0.05, label="per-galaxy best log a0 minus log a0_bar (dex)")
    ax.set_title(f"CFG182{' MUTATE' if C.MUTATE else ''}: SPARC clean sample, Galactic (l increasing leftward); "
                 f"A = {A_obs:.2f} +- {sigA_boot:.2f}, p = {pA:.3f}", fontsize=9)
    fig.savefig(os.path.join(C.HERE, f"cfg182_b_skymap{SUF}.png"), dpi=130, bbox_inches="tight")
    P(f"  wrote cfg182_b_skymap{SUF}.png")
except Exception as e:                                       # the figure is decoration only
    P(f"  (figure skipped: {e})")
sys.exit(R.finish())
