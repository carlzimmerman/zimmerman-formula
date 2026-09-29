#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG186 part A -- velocities, sample, the per-galaxy 2D profile curves C_i(log10 a0, distance), and the POWER ROW.

Frozen question: FROZEN_QUESTION.md (this directory), written before this script.  This script fits NO speed dependence
on the real speeds: the power row uses the curves' widths, the intrinsic scatter at beta = 0 (no speed information), and
curve-level mocks in which each galaxy's preferred a0 is replaced by noise.  It writes the DIAGNOSTIC / NON-DIAGNOSTIC
verdict that part B prints before its fit.

MUTATE=1: beta = 0.30 is injected into the DATA at the point level before the curves are built:
V_obs -> V_obs sqrt(nu(y')/nu(y)), y = g_bar,fid/a0_ref, y' = y/(1 + 0.30 z_i(0)), z_i(0) = (u_i(D_SPARC)/600 km/s)^2
(W1, H0 = 67.66), a0_ref = 1.2e-10 m/s^2 (declared); galaxies without a velocity are not injected.  Output *_MUTATE.*.

kappa = 1/2 stays FITTED; a0 is fitted (a0_bar free).  Run from the repository root:
    python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_a_curves_power.py
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cfg186_common as C

R = C.Run("cfg186_a_curves_power")
P, check = R.P, R.check
P(__doc__.split("Frozen question")[0].strip())
P(f"mode: {'MUTATE (beta = 0.30 injected at the point level)' if C.MUTATE else 'REAL DATA'}")

# ============================================================================================ A1
R.banner("A1  DATA: SPARC curves, master table, positions, heliocentric velocities, the CMB frame")
gals, vdiag = C.load_galaxies()
clean = [g for g in gals if g["clean"]]
P(f"  galaxies with master-table row and position: {len(gals)}; clean (Q <= 2, Inc >= 30, >= 5 pts): {len(clean)}")
from collections import Counter
cnt = Counter(g["cz_src"] or "none" for g in gals)
P(f"  velocity source used (first available of NED > UNGC > KT17 > 2MRS): {dict(cnt)}")
P(f"  KT2017: {vdiag['KT17_groups_multi']} multi-member groups, {vdiag['KT17_groups_distinct_frac']:.3f} carry distinct "
  f"member velocities -> used as per-galaxy velocities: {vdiag['KT17_used']}")
R.num("velocity_sources", dict(cnt))
R.num("KT17_diag", vdiag)
over, disagree = [], []
for g in gals:
    v0, k0 = C.pick_velocity(g["vsrc"])
    for k, v in g["vsrc"].items():
        if k != k0:
            over.append(abs(v - v0))
            if abs(v - v0) > 50:
                disagree.append((g["name"], k0, v0, k, v))
P(f"  overlapping sources: {len(over)} pairs, median |dv| = {np.median(over):.1f} km/s; |dv| > 50 km/s: {len(disagree)}")
for d in disagree:
    P(f"     {d[0]:12s} used {d[1]} {d[2]:.0f}  vs  {d[3]} {d[4]:.0f} km/s")
R.num("velocity_overlap_median_abs_dv", float(np.median(over)))
R.num("velocity_disagreements", disagree)
noV = [g["name"] for g in gals if not np.isfinite(g["cz_hel"])]
P(f"  no velocity in any source ({len(noV)}): {', '.join(noV)}")

prim = [g for g in clean if g["fD"] != 1 and np.isfinite(g["cz_hel"])]
hf = [g for g in clean if g["fD"] == 1 and np.isfinite(g["cz_hel"])]
P(f"  PRIMARY (clean, f_D in {{2,3,4,5}}, velocity): {len(prim)}  "
  f"[TRGB {sum(g['fD'] == 2 for g in prim)}, Cepheid {sum(g['fD'] == 3 for g in prim)}, "
  f"UMa {sum(g['fD'] == 4 for g in prim)}, SNIa {sum(g['fD'] == 5 for g in prim)}]; "
  f"clean Hubble-flow with velocity (CIRCULAR rows only): {len(hf)}")
R.num("N_primary", len(prim))
R.num("N_hubbleflow_clean_with_v", len(hf))
check("SAMP the primary sample has >= 30 galaxies with a redshift-independent distance and a velocity", len(prim),
      len(prim) >= 30)

# the declared frames
vsl = C.V_SLG * C.unitvec(C.L_SLG, C.B_SLG)
vlg_implied = C.VEC_SUN - vsl
lgl, lgb = C.lb_of(vlg_implied)
P(f"  v_sun,CMB = {C.V_SUN} km/s toward ({C.L_SUN}, {C.B_SUN}); declared V_LG = {C.V_LG} toward ({C.L_LG}, {C.B_LG}) "
  f"[from memory]; v_sun,CMB - v_sun,LG (318 toward (106, -6), from memory) = {np.linalg.norm(vlg_implied):.0f} km/s "
  f"toward ({lgl:.1f}, {lgb:.1f}), {C.angle_deg(vlg_implied, C.VEC_LG):.1f} deg from the declared V_LG")
R.num("V_LG_implied", {"v": float(np.linalg.norm(vlg_implied)), "l": lgl, "b": lgb,
                       "angle_to_declared_deg": C.angle_deg(vlg_implied, C.VEC_LG)})
check("LG the declared V_LG agrees with v_sun,CMB - v_sun,LG to 30 km/s and 5 deg (both from memory: a consistency check)",
      f"{np.linalg.norm(vlg_implied):.0f} km/s, {C.angle_deg(vlg_implied, C.VEC_LG):.1f} deg",
      abs(np.linalg.norm(vlg_implied) - C.V_LG) < 30 and C.angle_deg(vlg_implied, C.VEC_LG) < 5, load_bearing=False)

# velocities at the catalogue distance; the distance error on u
P("\n  line-of-sight CMB-frame peculiar velocity u = c (z_CMB - z_cos(D))/(1 + z_cos(D)) at the catalogue distance:")
P(f"  {'method':10s} {'N':>3s} {'D med':>6s} {'e_D/D':>6s} {'sigma_u=H0 e_D (med, max)':>28s} {'u med':>7s} "
  f"{'u 16-84%':>14s} {'|u| max':>8s}")
rows_meth = {}
for lab, sel in (("TRGB", lambda g: g["fD"] == 2), ("Cepheid", lambda g: g["fD"] == 3), ("UMa", lambda g: g["fD"] == 4),
                 ("SNIa", lambda g: g["fD"] == 5), ("HubbleFl", lambda g: g["fD"] == 1)):
    gg = [g for g in (prim + hf) if sel(g)]
    if not gg:
        continue
    u = np.array([C.u_los(g["cz_hel"], g["n"], g["D"], C.H0_PRIMARY) for g in gg])
    su = np.array([C.H0_PRIMARY * g["eD"] for g in gg])
    Dm = np.median([g["D"] for g in gg])
    fe = np.median([g["eD"] / g["D"] for g in gg])
    P(f"  {lab:10s} {len(gg):3d} {Dm:6.1f} {fe:6.3f} {np.median(su):13.0f} {su.max():13.0f}  {np.median(u):7.0f} "
      f"[{np.percentile(u, 16):5.0f},{np.percentile(u, 84):5.0f}] {np.abs(u).max():8.0f}")
    rows_meth[lab] = dict(N=len(gg), D_med=Dm, eD_frac_med=fe, sigma_u_med=float(np.median(su)), sigma_u_max=float(su.max()),
                          u_med=float(np.median(u)), u16=float(np.percentile(u, 16)), u84=float(np.percentile(u, 84)))
R.num("velocity_by_method", rows_meth)
k0 = int(np.argmin(np.abs(C.TFINE)))
U1 = C.u_matrix(prim, C.H0_PRIMARY)
U73 = C.u_matrix(prim, C.H0_VARIANT)
VP2 = np.array([C.vperp2_lg(g["n"]) for g in prim])
Z_W1 = C.zmat(U1, np.zeros(len(prim)))
Z_W2 = C.zmat(U1, VP2)
Z_73 = C.zmat(U73, np.zeros(len(prim)))
lgproj = np.array([g["n"] @ C.VEC_LG for g in prim])
r_lg = np.corrcoef(U1[:, k0], lgproj)[0, 1]
P(f"\n  primary: z = (u/600)^2 at the catalogue distance: median {np.median(Z_W1[:, k0]):.3f}, 16-84% "
  f"[{np.percentile(Z_W1[:, k0], 16):.3f}, {np.percentile(Z_W1[:, k0], 84):.3f}], sd {np.std(Z_W1[:, k0]):.3f}; "
  f"W2 z: sd {np.std(Z_W2[:, k0]):.3f} (median {np.median(Z_W2[:, k0]):.3f})")
P(f"  correlation of u with the LG-motion projection V_LG.n: r = {r_lg:.3f} (u ~ V_LG.n + local => the los proxy mostly "
  f"measures the sky pattern (V_LG.n)^2 if the local flow is coherent)")
R.num("z_W1_catalogue", {"median": float(np.median(Z_W1[:, k0])), "sd": float(np.std(Z_W1[:, k0]))})
R.num("z_W2_catalogue", {"median": float(np.median(Z_W2[:, k0])), "sd": float(np.std(Z_W2[:, k0]))})
R.num("corr_u_VLGproj", float(r_lg))

# ============================================================================================ A2
R.banner("A2  2D PROFILE CURVES C_i(log10 a0, t = (D - D_SPARC)/e_D); Upsilon_d, Upsilon_b, inclination profiled")
use = clean
V_override = None
if C.MUTATE:
    V_override = []
    ninj = 0
    for g in use:
        if np.isfinite(g["cz_hel"]):
            z0 = (C.u_los(g["cz_hel"], g["n"], g["D"], C.H0_PRIMARY) / C.W_REF) ** 2
            V_override.append(C.mutate_velocities(g, z0))
            ninj += 1
        else:
            V_override.append(g["V"].copy())
    P(f"  MUTATE: beta = {C.BETA_MUT} injected into {ninj} clean galaxies (point level, a0_ref = {C.A0_REF:.2e})")
t0 = __import__("time").time()
chi, par = C.compute_profiles(use, V_override=V_override)
feas = np.array([C.feasible_t(g) for g in use])
fin = np.isfinite(chi) | ~feas[:, :, None]
P(f"  {len(use)} galaxies x {len(C.TGRID)} t x {len(C.XGRID)} x cells [{__import__('time').time() - t0:.0f} s]; "
  f"non-finite feasible cells: {int((~fin).sum())}; infeasible t cells (D < 0.3 D_SPARC): {int((~feas).sum())} "
  f"(x-rows) in {int((~feas).any(axis=1).sum())} galaxies")
check("FIN every feasible cell of every 2D curve is finite", int((~fin).sum()), int((~fin).sum()) == 0)
jm = np.array([np.unravel_index(np.nanargmin(np.where(feas[i][:, None], chi[i], np.inf)), chi[i].shape) for i in range(len(use))])
edge_t = [use[i]["name"] for i in range(len(use)) if jm[i][0] in (0, len(C.TGRID) - 1) or not feas[i][max(jm[i][0] - 1, 0)]]
edge_x = [use[i]["name"] for i in range(len(use)) if jm[i][1] in (0, len(C.XGRID) - 1)]
isprim = np.array([(g["fD"] != 1 and np.isfinite(g["cz_hel"])) for g in use])
P(f"  joint minimum at a t edge (|t| = 4 or the D floor): {len(edge_t)} galaxies "
  f"({sum(1 for i in range(len(use)) if isprim[i] and use[i]['name'] in edge_t)} primary): {', '.join(edge_t)}")
P(f"  joint minimum at an x edge: {len(edge_x)}: {', '.join(edge_x)}")
R.num("t_edge_minima", edge_t)
R.num("x_edge_minima", edge_x)

# ============================================================================================ A3
R.banner("A3  OPTIMIZER AND INTERPOLATION CHECKS")
rng = np.random.default_rng(186)
worst = 0.0
for _ in range(60):
    i = int(rng.integers(len(use)))
    kk = np.where(feas[i])[0]
    k = int(rng.choice(kk))
    j = int(rng.integers(len(C.XGRID)))
    bc = C.cell_cold(use[i], k, j, None if V_override is None else V_override[i], seed=int(rng.integers(1 << 30)))
    worst = max(worst, chi[i, k, j] - bc)
P(f"  largest (warm - best of 6 cold starts) chi2 over 60 random (galaxy, t, x) cells: {worst:.4f}")
R.num("optimizer_worst_excess", worst)
check("OPT the warm-started 2D profile is never worse than 6 cold starts by more than 0.05 in chi2", f"{worst:.4f}",
      worst <= 0.05)

Cf = C.fine_curves(chi, feas)
# spline check (Addendum 1): direct profiles at off-grid t versus the spline, (a) in cells within Delta chi2 <= 25 of the
# galaxy's minimum (load-bearing), (b) in random cells, as a relative error (reported)
def direct_cell(i, tf, j):
    g = use[i]
    lo, hi = C._bounds(g)
    rD = 1.0 + (g["eD"] / g["D"]) * tf
    Vo = g["V"] if V_override is None else V_override[i]
    kk = np.where(feas[i])[0]
    best = np.inf
    starts = [par[i, kk[np.argmin(np.abs(C.TGRID[kk] - tf))], j], np.zeros(3)] + [rng.uniform(-2.5, 2.5, 3) for _ in range(3)]
    for p0 in starts:
        r = C._ls(p0, g, 10 ** C.XGRID[j], C.C4.nu_mono, Vo, rD, lo, hi)
        best = min(best, 2 * r.cost + tf ** 2)
    return best


near_err, rel_err = [], []
while len(near_err) < 40:
    i = int(rng.integers(len(use)))
    ch = np.where(feas[i][:, None], chi[i], np.inf)
    cm = np.min(ch)
    ok = np.argwhere(ch - cm <= 25.0)
    k, j = ok[int(rng.integers(len(ok)))]
    tf = float(np.clip(C.TGRID[k] + rng.choice([-0.1, -0.05, 0.05, 0.1, 0.15]), C.TGRID[np.where(feas[i])[0][0]], 4.0))
    kf = int(np.argmin(np.abs(C.TFINE - tf)))
    tf = float(C.TFINE[kf])
    near_err.append(abs(Cf[i, kf, j] - direct_cell(i, tf, j)))
for _ in range(24):
    i = int(rng.integers(len(use)))
    kk = np.where(feas[i])[0]
    tf = float(C.TFINE[np.argmin(np.abs(C.TFINE - rng.uniform(C.TGRID[kk[0]] + 0.25, C.TGRID[kk[-1]] - 0.25)))])
    kf = int(np.argmin(np.abs(C.TFINE - tf)))
    j = int(rng.integers(len(C.XGRID)))
    cm = np.nanmin(np.where(feas[i][:, None], chi[i], np.inf))
    d = direct_cell(i, tf, j)
    rel_err.append(abs(Cf[i, kf, j] - d) / (1.0 + d - cm))
near_err, rel_err = np.array(near_err), np.array(rel_err)
P(f"  spline along t vs direct profiles, 40 off-grid cells within Delta chi2 <= 25 of the minimum: median |d| = "
  f"{np.median(near_err):.4f}, max = {near_err.max():.4f}; 24 random cells: max relative error {rel_err.max():.4f}")
R.num("spline_check", {"near_median": float(np.median(near_err)), "near_max": float(near_err.max()),
                       "random_rel_max": float(rel_err.max())})
check("SPL the spline in t reproduces direct profiles near each galaxy's minimum (max |d chi2| <= 0.1; Addendum 1)",
      f"{near_err.max():.4f}", near_err.max() <= 0.1)
check("SPLR relative spline error in random cells <= 1% (Addendum 1)", f"{rel_err.max():.4f}", rel_err.max() <= 0.01,
      load_bearing=False)

# cross-check against CFG182's 1D distance-profiled curves (another lane; reported)
cfg182 = os.path.join(C.CFGDIR, "CFG182_a0_sky_dipole", "cfg182_a_profiles.npz")
if os.path.exists(cfg182) and not C.MUTATE:
    z = np.load(cfg182, allow_pickle=True)
    nm182 = list(z["names"])
    g182 = np.round(z["grid"], 2)
    jx = np.array([int(np.argmin(np.abs(g182 - x))) for x in C.XGRID])
    diffs = []
    for i, g in enumerate(use):
        if g["name"] not in nm182:
            continue
        a = nm182.index(g["name"])
        c182 = z["chi_nu_mono"][a][jx]
        tD182 = z["par_nu_mono"][a][jx][:, 2]
        mine = np.min(Cf[i], axis=0)
        near = (c182 - c182.min() <= 9.0) & (np.abs(tD182) <= 3.5)
        diffs.extend(list(mine[near] - c182[near]))
    diffs = np.array(diffs)
    P(f"  min_t C_i(x, t) vs CFG182's distance-profiled curve (cells within Delta chi2 <= 9 of its minimum and |t_D| <= 3.5): "
      f"{len(diffs)} cells, median (mine - CFG182) = {np.median(diffs):+.4f}, 95% |d| = {np.percentile(np.abs(diffs), 95):.4f}")
    R.num("cfg182_crosscheck", {"n": len(diffs), "median": float(np.median(diffs)),
                                "p95_abs": float(np.percentile(np.abs(diffs), 95))})
    check("X182 the distance-profiled 2D curves reproduce CFG182's 1D curves near their minima (95% |d chi2| <= 0.1)",
          f"median {np.median(diffs):+.4f}, 95% {np.percentile(np.abs(diffs), 95):.4f}",
          np.percentile(np.abs(diffs), 95) <= 0.1, load_bearing=False)
else:
    P("  CFG182 cross-check skipped (file absent or MUTATE)")

# ============================================================================================ A4
R.banner("A4  SCALED CURVES, WIDTHS, INTRINSIC SCATTER AT beta = 0 (no speed information)")
npt = np.array([g["npt"] for g in use])
cv_all = C.Curves(Cf, npt, birge=True)
ip = np.where(isprim)[0]
cvp0 = cv_all.subset(ip)
L0, tau = C.fit_tau(cvp0.xhat, cvp0.sig)
cv_all = cv_all.with_tau(tau)
cvp = cv_all.subset(ip)
qmed = float(np.median(cvp.qt[cvp.rows][:, cvp.k0]))
P(f"  primary ({len(ip)}): Birge s median {np.median(cvp.s):.2f} (max {cvp.s.max():.1f}); distance-profiled half-widths "
  f"sigma_i median {np.median(cvp.sig):.3f} dex, 16-84% [{np.percentile(cvp.sig, 16):.3f}, {np.percentile(cvp.sig, 84):.3f}]")
P(f"  preferred log a0: median {np.median(cvp.xhat):.3f}, 16-84% [{np.percentile(cvp.xhat, 16):.3f}, "
  f"{np.percentile(cvp.xhat, 84):.3f}]; ML (Gaussian approx.) L0 = {L0:.3f}, tau = {tau:.3f} dex; fixed-distance widths "
  f"sx(t=0) median {np.median(cvp.sx[cvp.rows][:, cvp.k0]):.3f} dex -> softening q_i(t=0) median {qmed:.2f} (data part only; "
  f"the distance prior is unscaled, Addendum 2)")
edge_p = (cvp.xhat <= C.XGRID[0] + 1e-6) | (cvp.xhat >= C.XGRID[-1] - 1e-6)
L0e, taue = C.fit_tau(cvp.xhat[~edge_p], cvp.sig[~edge_p])
P(f"  sensitivity (Addendum 1): without the {int(edge_p.sum())} primary galaxies whose preferred value lies at a grid edge "
  f"({', '.join(np.array([use[i]['name'] for i in ip])[edge_p])}): L0 = {L0e:.3f}, tau = {taue:.3f} dex (declared tau kept)")
R.num("tau_without_edge_galaxies", taue)
R.num("primary_sigma_median", float(np.median(cvp.sig)))
R.num("L0", L0)
R.num("tau", tau)

# ============================================================================================ A5
R.banner("A5  FITTER EXACTNESS (synthetic noiseless curves with beta = 0.30)")
Csyn = np.array([((C.XGRID[None, :] - L0 - np.log10(1 + 0.30 * Z_W1[i][:, None])) ** 2) / cvp.sig[i] ** 2
                 + C.TFINE[:, None] ** 2 for i in range(len(ip))])
cvs = C.Curves(Csyn, np.full(len(ip), 10 ** 7), birge=False)
rs = C.Fitter(cvs, Z_W1, use_q=False).fit(beta_starts=(0.0, 0.5))
P(f"  synthetic: beta_hat = {rs['beta']:.4f}, L_hat = {rs['L']:.4f} (true 0.30, {L0:.4f})")
check("FIT0 the fitter returns beta = 0.300 +- 0.005 on noiseless synthetic curves", f"{rs['beta']:.4f}",
      abs(rs["beta"] - 0.30) <= 0.005)

# ============================================================================================ A6
R.banner("A6  POWER ROW (before any beta fit on the real speeds)")
st = {"cv": cvp, "L0": L0, "tau": tau, "k0": k0, "use_q": True}
power = {}
for lab, Z in (("W1_H67.66", Z_W1), ("W2_H67.66", Z_W2), ("W1_H73", Z_73)):
    sF = C.fisher_sigma_beta(Z[:, k0], cvp.sig, tau)
    st["Z"] = Z
    t1 = __import__("time").time()
    bm = np.array(C.run_pool(C.task_noise, list(range(1000, 1500)), st))
    sM = 0.5 * (np.percentile(bm, 84) - np.percentile(bm, 16))
    bdet = 2 * max(sF, sM)
    power[lab] = dict(sigma_fisher=sF, sigma_mock=sM, mock_mean=float(np.mean(bm)), mock_median=float(np.median(bm)),
                      mock_p16=float(np.percentile(bm, 16)), mock_p84=float(np.percentile(bm, 84)), beta_det_2sigma=bdet,
                      beta_80pct=2.84 * max(sF, sM), diagnostic=bool(bdet <= C.BETA_G7))
    P(f"  {lab:10s}: sigma_beta Fisher = {sF:.3f}, mocks (500, beta = 0) = {sM:.3f} (mean beta_hat {np.mean(bm):+.3f}) "
      f"[{__import__('time').time() - t1:.0f} s] -> beta_det(2 sigma) = {bdet:.3f}, 80%-power {2.84 * max(sF, sM):.3f}; "
      f"G7 line 0.10 -> {'DIAGNOSTIC' if bdet <= C.BETA_G7 else 'NON-DIAGNOSTIC'}")
R.num("power", power)
prim_diag = power["W1_H67.66"]["diagnostic"]
R.num("POWER_VERDICT", "DIAGNOSTIC" if prim_diag else "NON-DIAGNOSTIC")
P(f"\n  POWER VERDICT (primary W1, H0 = 67.66): {'DIAGNOSTIC' if prim_diag else 'NON-DIAGNOSTIC'} for G7: the smallest "
  f"beta detectable at 2 sigma is {power['W1_H67.66']['beta_det_2sigma']:.2f}, "
  f"{power['W1_H67.66']['beta_det_2sigma'] / C.BETA_G7:.1f}x the G7 line (beta = 0.10 = 10% at 600 km/s).")
check("PWR the power row was computed before the fit (reported: DIAGNOSTIC is not required -- a NON-DIAGNOSTIC row is a "
      "valid result)", R.OUT["numbers"]["POWER_VERDICT"], True, load_bearing=False)
mean_bias = power["W1_H67.66"]["mock_mean"]
check("MOCK the beta = 0 mocks are unbiased (|mean beta_hat| < 0.25 sigma_mock)", f"mean {mean_bias:+.4f}, median "
      f"{power['W1_H67.66']['mock_median']:+.4f}, 16-84% [{power['W1_H67.66']['mock_p16']:+.3f}, "
      f"{power['W1_H67.66']['mock_p84']:+.3f}]",
      abs(mean_bias) < 0.25 * power["W1_H67.66"]["sigma_mock"], load_bearing=False)

# ============================================================================================ save
out = dict(xgrid=C.XGRID, tgrid=C.TGRID, tfine=C.TFINE, names=np.array([g["name"] for g in use]),
           chi=chi.astype(np.float32), feas=feas, npt=npt, isprim=isprim,
           fD=np.array([g["fD"] for g in use]), D=np.array([g["D"] for g in use]), eD=np.array([g["eD"] for g in use]),
           l=np.array([g["l"] for g in use]), b=np.array([g["b"] for g in use]), n=np.array([g["n"] for g in use]),
           cz_hel=np.array([g["cz_hel"] for g in use]), cz_src=np.array([g["cz_src"] for g in use]),
           L0=L0, tau=tau)
npz = os.path.join(C.HERE, f"cfg186_a_curves{R.suf}.npz")
np.savez_compressed(npz, **out)
P(f"\n  wrote {os.path.basename(npz)}")
sys.exit(R.finish())
