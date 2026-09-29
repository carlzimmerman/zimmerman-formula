#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D5_B -- Door 5, part B: a general orbit-superposition (Schwarzschild-type) linear programme for the existence of a NON-NEGATIVE f(E, L)
in the CFG44 target's own potential, for ANY anisotropy beta(r): point mass and the exponential sphere at several h/r_M.
See FROZEN_QUESTION.md (written before this script).  Units a0 = G = M_b = 1, r_M = 1.

Orbits are labelled (r_c, eta = L/L_c), weights w >= 0; for each log radial bin the exact time-fraction integrals of an orbit give
   mass rows        sum_i w_i M_i,j          = Int_bin 4 pi r^2 rho_c dr                                    (V1: does ANY f >= 0 generate rho_c)
   beta rows        sum_i w_i Kb_i,j         = 0 ,  Kb = Int [L^2/r^2 - 2(1 - beta(r)) v_r^2] dt/T           (V2: plus the anisotropy beta(r))
   radial-energy    sum_i w_i Kr_i,j         = Int_bin 4 pi r^2 rho_c (V_c^2/2) dr                            (V3: plus sigma_r^2 = V_c^2/2, CFG44's restatement)
min-max relative residual eps* by HiGHS.  FEASIBLE if eps* <= 0.02 at the finest level; INFEASIBLE if eps* >= 0.10 and it does not shrink under refinement.
V2iso imposes beta = 0 (the isotropic-moment reading, for comparison with CFG44 B1's Eddington f(E) >= 0).

CHECKS (PRE-DECLARED)
  B1 CONTROL C1: the isotropic Plummer sphere (a known f(E) >= 0) is FEASIBLE in V2 (beta = 0) and V3 with its true sigma_r^2 = 1/(6 sqrt(1+r^2)).
  B2 CONTROL C2: the same Plummer with sigma_r^2 doubled (Jeans-inconsistent) is INFEASIBLE in V3.
  B3 CONTROL C3: the point-mass V2 verdict agrees with D5_A's Eddington sign (f >= 0 everywhere => FEASIBLE).
  B4 point mass V1, V2, V3: FEASIBLE at the finest level (window [1e-2, 1e2]; convergence window [1e-3, 1e3] at L1).
  B5 exponential sphere h/r_M in {0.03, 0.1, 0.3, 1, 3}, V1, V2, V3: FEASIBLE at the finest level.
  B6 M4 (b): beta(r) != 0 inside the baryons, so a stationary Maxwell-Boltzmann f(E) (beta = 0) is not the target.
MUTATE=1 (D7): the radial-energy rows are doubled (sigma_r^2 pinned at V_c^2 instead of V_c^2/2, a Jeans-inconsistent target, rho and beta unchanged):
  every V3 result of B4/B5 must turn INFEASIBLE (rc = 1 if the normal headline is feasible).
Run: python3 D5_B_orbit_lp.py   (MUTATE=1 for the control;  QUICK=1 runs level L1 only)
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from D5common import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
QUICK = os.environ.get("QUICK", "0") == "1"
R = Report("D5_B_orbit_lp", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: sigma_r^2 pinned at V_c^2 (doubled radial-energy rows) -- every V3 result must turn INFEASIBLE ***")

LEVELS = {"L1": dict(bins_per_decade=12, orbits_per_decade=10, n_tan=10, n_lin=14, npsi=300),
          "L2": dict(bins_per_decade=24, orbits_per_decade=20, n_tan=20, n_lin=28, npsi=400)}


def classify(e1, e2):
    """FEASIBLE: eps <= 0.02 at the finest level; INFEASIBLE: eps >= 0.10 at the finest level and not shrinking (finest >= 0.9 x coarser);
       otherwise UNDECIDED."""
    fin = e2 if e2 is not None else e1
    if fin <= 0.02:
        return "FEASIBLE"
    if fin >= 0.10 and (e2 is None or e2 >= 0.9 * e1):
        return "INFEASIBLE" if e2 is not None else "INFEASIBLE(L1 only)"
    return "UNDECIDED"


def build(pot, lo, hi, lev, sr2_scale=1.0, sr2_fn=None, beta_fn=None):
    Lv = LEVELS[lev]
    nb = int(round(Lv["bins_per_decade"] * math.log10(hi / lo)))
    redges = np.geomspace(lo, hi, nb + 1)
    og = orbit_grid(pot, lo / 30.0, hi * 30.0, Lv["orbits_per_decade"], default_etas(Lv["n_tan"], Lv["n_lin"]))
    mom = orbit_moments(pot, og, redges, beta_fn, npsi=Lv["npsi"])
    base = pot.sr2 if sr2_fn is None else sr2_fn
    bm, br = bin_targets(pot, redges, sr2_fn=lambda r: sr2_scale * base(r))
    return redges, og, mom, bm, br


def run_case(pot, lo, hi, variants, levels, sr2_scale=1.0, sr2_fn=None, tag="", beta_fn=None):
    """returns {variant: (eps L1, eps L2, class)} and the L1 objects for localisation."""
    out = {v: [None, None] for v in variants}
    keep = None
    for lev in levels:
        t0 = time.time()
        redges, og, mom, bm, br = build(pot, lo, hi, lev, sr2_scale=sr2_scale, sr2_fn=sr2_fn, beta_fn=beta_fn)
        if keep is None:
            keep = (redges, og, mom, bm, br)
        for v in variants:
            e, w = solve_lp(mom, bm, br, v)
            out[v][0 if lev == "L1" else 1] = e
        P(f"      [{tag} {lev}: {len(og['rc'])} orbits, {len(bm)} bins, {time.time() - t0:.0f} s]  " + "  ".join(f"{v}: {out[v][0 if lev == 'L1' else 1]:.4f}" for v in variants))
    res = {}
    for v in variants:
        e1, e2 = out[v]
        res[v] = (e1, e2, classify(e1, e2))
    return res, keep


levels = ["L1"] if QUICK else ["L1", "L2"]

# =============================================================================================================== controls
R.banner("C1-C3  CONTROLS OF THE LINEAR PROGRAMME (known answers)")
plummer = Pot("Plummer a=1",
              u=lambda r: np.asarray(r, float) ** 3 / (1 + np.asarray(r, float) ** 2) ** 1.5,
              Phi=lambda r: -1.0 / np.sqrt(1 + np.asarray(r, float) ** 2),
              rho=lambda r: 3 / (FOUR_PI) * (1 + np.asarray(r, float) ** 2) ** -2.5,
              beta=lambda r: np.zeros_like(np.asarray(r, float)),
              uN=lambda r: np.asarray(r, float) ** 3 / (1 + np.asarray(r, float) ** 2) ** 1.5)
plummer.sr2 = lambda r: 1.0 / (6.0 * np.sqrt(1 + np.asarray(r, float) ** 2))          # isotropic Plummer: sigma^2 = GM/(6 sqrt(a^2 + r^2))
# ---- B0: the moment integrals against a direct orbit integration (independent of the psi-substitution)
from scipy.integrate import solve_ivp as _ivp
_pe = exp_sphere(0.3)
_og = orbit_grid(_pe, 1.0, 1.0, 10, [0.4])
_re = np.geomspace(0.05, 20.0, 9)
_mom = orbit_moments(_pe, _og, _re, None, npsi=400)
_L2 = float(_og["L2"][0]); _E = float(_og["E"][0]); _rp = float(_og["rp"][0]); _ra = float(_og["ra"][0])
_gf = lambda r: float(_pe.g(r))
_sol = _ivp(lambda t, y: [y[1], _L2 / y[0] ** 3 - _gf(y[0])], (0, 400.0), [_rp * 1.0000001, 1e-9], t_eval=np.linspace(0, 400.0, 400001), rtol=1e-11, atol=1e-13)
_r, _vr = _sol.y
# whole number of radial periods: use the time of the last minimum of r after which the same phase is reached
_dt = _sol.t[1] - _sol.t[0]
_mins = np.where((_r[1:-1] < _r[:-2]) & (_r[1:-1] <= _r[2:]))[0] + 1
_last = _mins[-1]
_rr, _vv = _r[:_last], _vr[:_last]
_frac = np.array([np.mean((_rr >= _re[j]) & (_rr < _re[j + 1])) for j in range(len(_re) - 1)])
_kr = np.array([np.sum(np.where((_rr >= _re[j]) & (_rr < _re[j + 1]), _vv ** 2, 0.0)) / len(_rr) for j in range(len(_re) - 1)])
_m0, _k0 = _mom["M"][0], _mom["Kr"][0]
_sig = _m0 > 0.02
P(f"  orbit (h=0.3 exp sphere) rc=1, eta=0.4: rp = {_rp:.4f}, ra = {_ra:.4f}; time fractions per bin (direct / moments): " + ", ".join(f"{a:.4f}/{b_:.4f}" for a, b_ in zip(_frac, _m0)))
_e1 = float(np.max(np.abs(_frac[_sig] / _m0[_sig] - 1))); _e2 = float(np.max(np.abs(_kr[_sig] / _k0[_sig] - 1)))
check("B0 the orbit moment integrals (time fraction and Int v_r^2 dt) agree with a direct orbit integration to 1% in every bin holding > 2% of the orbit's time",
      f"max |ratio - 1|: time fraction {_e1:.2e}, v_r^2 moment {_e2:.2e}", _e1 < 0.01 and _e2 < 0.01)
resC1, kC1 = run_case(plummer, 0.05, 30.0, ["V1", "V2", "V3"], levels, tag="Plummer isotropic")
check("B1 CONTROL C1: the isotropic Plummer sphere (known f(E) >= 0, true sigma_r^2) is FEASIBLE in V1, V2, V3",
      f"eps* (finest): " + ", ".join(f"{v}: {(r_[1] if r_[1] is not None else r_[0]):.4f} -> {r_[2]}" for v, r_ in resC1.items()),
      all(r_[2] == "FEASIBLE" for r_ in resC1.values()))
resC2, _ = run_case(plummer, 0.05, 30.0, ["V3"], levels, sr2_scale=2.0, tag="Plummer sigma_r^2 doubled")
check("B2 CONTROL C2: the Plummer with sigma_r^2 doubled (Jeans-inconsistent) is INFEASIBLE in V3",
      f"eps* = {resC2['V3'][0]:.4f} (L1), {resC2['V3'][1]} (L2) -> {resC2['V3'][2]}", resC2["V3"][2].startswith("INFEASIBLE"))
resC4, _ = run_case(plummer, 0.05, 30.0, ["V2"], levels, beta_fn=lambda r: 0.5 * np.ones_like(np.asarray(r, float)), tag="Plummer with beta=+0.5")
check("B2b CONTROL C4: a cored isotropic Plummer with a constant radial bias beta = +0.5 imposed is INFEASIBLE (central cusp-anisotropy theorem: beta_0 <= gamma_0/2 = 0 for a core)",
      f"eps* = {resC4['V2'][0]:.4f} (L1), {resC4['V2'][1]} (L2) -> {resC4['V2'][2]}", resC4["V2"][2].startswith("INFEASIBLE"))
resC4b, _ = run_case(plummer, 0.05, 30.0, ["V2"], levels, beta_fn=lambda r: -0.5 * np.ones_like(np.asarray(r, float)), tag="Plummer with beta=-0.5")
P(f"    (reported, no frozen expectation) Plummer with constant beta = -0.5: eps* = {resC4b['V2'][0]:.4f} (L1), {resC4b['V2'][1]} -> {resC4b['V2'][2]}")
R.num("control_plummer", {k: list(map(str, v)) for k, v in resC1.items()}); R.num("control_plummer_doubled", list(map(str, resC2["V3"])))

# =============================================================================================================== point mass
R.banner("B4  POINT-MASS TARGET (beta = 0 exactly): V1, V2, V3, V2iso")
pm = point_mass()
sc = 2.0 if MUTATE else 1.0                                  # MUTATE: sigma_r^2 pinned at V_c^2 (only V3 reads it; V1/V2 unaffected by construction)
resPM, keepPM = run_case(pm, 1e-2, 1e2, ["V1", "V2", "V2iso", "V3"], levels, sr2_scale=sc, tag="point mass [1e-2,1e2]")
for v, r_ in resPM.items():
    P(f"    point mass  {v:5s}: eps* L1 = {r_[0]:.4f}, L2 = {('%.4f' % r_[1]) if r_[1] is not None else '-'}  ->  {r_[2]}")
resPMw, _ = run_case(pm, 1e-3, 1e3, ["V2", "V3"], ["L1"], sr2_scale=sc, tag="point mass wide [1e-3,1e3]")
for v, r_ in resPMw.items():
    P(f"    point mass wide window [1e-3, 1e3] L1: {v}: eps* = {r_[0]:.4f}")
lam_pm = solve_lp_margin(keepPM[2], keepPM[3], keepPM[4], "V3")
P(f"    SUPPLEMENT (added after the first LP result; not a frozen criterion): interior margin of V3 at 2% tolerance, min weight / mean weight = {lam_pm:.3e}  (> 0 means a strictly positive weight function exists)")
R.num("point_mass_V3_margin", lam_pm)
okPM = all(resPM[v][2] == "FEASIBLE" for v in ("V1", "V2", "V3")) and all(resPMw[v][0] <= 0.02 for v in resPMw)
check("B3 CONTROL C3 + B4: the point-mass V2 verdict agrees with D5_A's Eddington sign (f(E) >= 0 everywhere => FEASIBLE), and V1, V2, V3 are FEASIBLE (also in the wide window)",
      f"V1 {resPM['V1'][2]}, V2 {resPM['V2'][2]}, V2iso {resPM['V2iso'][2]}, V3 {resPM['V3'][2]}; wide: " + ", ".join(f"{v} {resPMw[v][0]:.4f}" for v in resPMw), okPM)
R.num("point_mass", {v: [r_[0], r_[1], r_[2]] for v, r_ in resPM.items()})
R.num("point_mass_wide_L1", {v: r_[0] for v, r_ in resPMw.items()})

# =============================================================================================================== exponential sphere
R.banner("B5  EXTENDED TARGET: exponential sphere, beta(r) = -(3/2) rho_b/rhobar_b, h/r_M in {0.03, 0.1, 0.3, 1, 3}")
allext = {}
for h in (0.03, 0.1, 0.3, 1.0, 3.0):
    pe = exp_sphere(h)
    lo, hi = 0.02 * min(h, 1.0), 50.0 * max(h, 1.0)
    bt = pe.beta(np.geomspace(lo, hi, 400))
    P(f"\n  h/r_M = {h}: window [{lo:.3g}, {hi:.3g}]; beta from {bt.min():.3f} to {bt.max():.3f}")
    res_h, keep_h = run_case(pe, lo, hi, ["V1", "V2", "V2iso", "V3"], levels, sr2_scale=sc, tag=f"exp sphere h={h}")
    for v, r_ in res_h.items():
        P(f"    h = {h:5.2f}  {v:5s}: eps* L1 = {r_[0]:.4f}, L2 = {('%.4f' % r_[1]) if r_[1] is not None else '-'}  ->  {r_[2]}")
    lam_h = solve_lp_margin(keep_h[2], keep_h[3], keep_h[4], "V3")
    P(f"    SUPPLEMENT: interior margin of V3 at 2% tolerance, min weight / mean weight = {lam_h:.3e} (nan when V3 is infeasible at 2%)")
    allext[h] = dict(window=[lo, hi], beta_range=[float(bt.min()), float(bt.max())], margin_V3=lam_h, res={v: [r_[0], r_[1], r_[2]] for v, r_ in res_h.items()})
    # localisation of an infeasible verdict: eps* on sub-windows (L1), edges on decade points of the window
    bad = [v for v in ("V1", "V2", "V3") if res_h[v][2].startswith("INFEASIBLE")]
    if bad:
        redges, og, mom, bm, br = keep_h
        nbins = len(bm)
        lrE = np.log10(redges)
        for v in bad:
            P(f"    localisation for {v} (eps* on sub-windows of the L1 grid; bins are {12}/decade):")
            best_span = None
            dec = np.arange(math.ceil(lrE[0]), math.floor(lrE[-1]) + 1)
            cand = [float(lrE[0])] + [float(d) for d in dec if lrE[0] < d < lrE[-1]] + [float(lrE[-1])]
            for i_ in range(len(cand)):
                for j_ in range(i_ + 1, len(cand)):
                    if cand[j_] - cand[i_] < 1.0 - 1e-9:
                        continue
                    jl = int(np.argmin(abs(lrE - cand[i_]))); jh = int(np.argmin(abs(lrE - cand[j_])))
                    e_, _ = solve_lp(mom, bm, br, v, rows=slice(jl, jh))
                    feas = e_ <= 0.02
                    P(f"       r in [{10 ** cand[i_]:.3g}, {10 ** cand[j_]:.3g}]: eps* = {e_:.4f}  {'FEASIBLE' if feas else ''}")
                    if feas and (best_span is None or cand[j_] - cand[i_] > best_span[1] - best_span[0]):
                        best_span = (cand[i_], cand[j_])
            P(f"    largest feasible sub-window found for {v}: {('[%.3g, %.3g]' % (10 ** best_span[0], 10 ** best_span[1])) if best_span else 'none of >= 1 decade'}")
# reported: the anisotropy is not a free pass: flip its sign (radial instead of tangential bias) on the middle case
_pe = exp_sphere(0.3)
_res_flip, _ = run_case(_pe, 0.006, 50.0, ["V2"], ["L1"], beta_fn=lambda r: -_pe.beta(r), tag="exp sphere h=0.3, beta flipped")
P(f"    (reported) h = 0.3 with the sign of beta flipped, beta = +(3/2) rho_b/rhobar_b: V2 eps* = {_res_flip['V2'][0]:.4f} -> {_res_flip['V2'][2]}")
R.num("exp_sphere_beta_flipped_V2", [_res_flip["V2"][0], _res_flip["V2"][2]])
R.num("exp_sphere", allext)
okext = all(allext[h]["res"][v][2] == "FEASIBLE" for h in allext for v in ("V1", "V2", "V3"))
worst = {v: max((allext[h]["res"][v][1] if allext[h]["res"][v][1] is not None else allext[h]["res"][v][0]) for h in allext) for v in ("V1", "V2", "V3")}
check("B5 exponential sphere, h/r_M in {0.03, 0.1, 0.3, 1, 3}: V1, V2, V3 all FEASIBLE at the finest level",
      "classification: " + "; ".join(f"h={h}: " + "/".join(allext[h]["res"][v][2] for v in ("V1", "V2", "V3")) for h in allext) + f"; worst eps*: {worst}", okext)

# =============================================================================================================== entropy (b)
R.banner("B6  M4(b): the stationary Maxwell-Boltzmann f(E) has beta = 0; the extended target has beta != 0")
mx = max(abs(v["beta_range"][0]) for v in allext.values())
check("B6 (reported) the extended target has |beta| up to 3/2 inside the baryons, so it is not the Boltzmann entropy extremum (f = f(E) only, beta = 0)",
      f"largest |beta| over the h list = {mx:.3f}", mx > 0.1, load_bearing=False)

nf = R.write()
sys.exit(1 if nf else 0)
