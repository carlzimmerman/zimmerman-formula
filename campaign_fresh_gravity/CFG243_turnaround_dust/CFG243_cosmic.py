#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_cosmic -- GATE 1 (COSMIC), run exactly as frozen: can a turnaround-triggered source supply the cold matter the CMB needs at
recombination?  Frozen text: campaign_fresh_gravity/CFG243_FROZEN_CRITERIA.md section 2, Gate 1.

DECLARED ESTIMATOR (frozen): Press-Schechter turned-around mass fraction F_ta(z; M > M_min) = erfc(delta_ta(z) / (sqrt2 sigma(M_min, z))) with the
frozen thresholds delta_ta = 1.0624 (z >= 10, the EdS value), 1.076 (z = 2.5), 1.276 (z = 0).  Phase 2 replaces the memory-level sigma(M, z)
and D(z) by CLASS (3.x, the Planck 2018 inputs of CFG4_cosmology.py): sigma(M, z) from the CLASS matter transfer function d_m(k, z) with the
primordial P_R(k) = A_s (k/0.05)^(n_s - 1), a spherical top-hat window, rho_m = Omega_m rho_crit,0.  M_min in {1e5, 1e8, 1e10} Msun (declared).
MOST GENEROUS READING (frozen): the amount is normalised so that Omega_dust(z = 0) = Omega_c (so Omega_dust h^2(z) = 0.1200 F_ta(z)/F_ta(0));
the collapse fractions use the LCDM sigma(M), which presupposes the cold matter the class does not have: circular in the class's favour.
BINDING LINE: Omega_dust h^2(z = 1100) >= 0.5 x 0.1200 = 0.060.  A shortfall of an order of magnitude or more (<= 0.006) is the binding FAIL.
The verdict cell uses the most favourable of the three M_min (M_min = 1e5 Msun, which maximises F_ta at high z).

ROWS: C1 (binding), C2 (z = 10, 2.5), C3 (sigma needed for F_ta(1100) = 0.5), C4 (baryon-only linear sigma_b at z = 0 against delta_ta(0) = 1.276),
C5 (max |delta theta_b|/(3H) at z = 1100 and the rms; CLASS Newtonian-gauge t_b), C6 (CFG4's cold budget at z = 0, restated).

MUTATE=1: the turnaround trigger is replaced by creation of Omega_c h^2 = 0.12 of uniform dust at z_i = 1e5 (initial data).  C1 must flip FAIL -> PASS.
MUTATE=2: the pass line is evaluated at z = 0 instead of z = 1100.  C1 must flip FAIL -> PASS.
ROBUST=1 (frozen as expected NOT to bite): the requirement is lowered from 0.1200 to 0.01 (line 0.5 x 0.01).
ROBUST=2 (expected NOT to bite): delta_ta(1100) = 0.5 instead of 1.0624.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG243_common as C

R = C.Run("CFG243_cosmic")
P = R.P
MUT, ROB = R.mutate, R.robust
P(__doc__.strip())

ZS = (1100, 10, 2.5, 0)
MMINS = (1e5, 1e8, 1e10)
def _cv():
    try:
        import importlib.metadata as _m
        return _m.version("classy")
    except Exception:
        return "unknown"


c = C.class_cosmo([0, 2.5, 10, 100, 1100])
h = c.h()
P(f"\n  CLASS (python wrapper 'classy', version {_cv()}): h = {h:.6f}, Omega_m = {c.Omega_m():.5f}, Omega_b = {c.Omega_b():.5f}; requirement Omega_c h^2 = {C.OMC_H2_COMPARE}; line = {C.COSMIC_LINE_FRAC} x requirement")

R.banner("sigma(M, z) from CLASS and the Press-Schechter turned-around fractions")
sig = {}
for z in (0, 2.5, 10, 100, 1100):
    k, D2 = C.delta2(c, z, "d_m")
    for M in (1e5, 1e6, 1e8, 1e10, 1e12):
        sig[(z, M)] = C.sigma_R(k, D2, C.R_of_M(M))
P("  sigma(M, z):          " + "".join(f"M={M:8.0e}   " for M in (1e5, 1e6, 1e8, 1e10, 1e12)))
for z in (0, 2.5, 10, 100, 1100):
    P(f"    z = {z:6g}   " + "".join(f"{sig[(z, M)]:12.5g} " for M in (1e5, 1e6, 1e8, 1e10, 1e12)))
sig8 = C.sigma_R(*C.delta2(c, 0, "d_m"), 8.0 / h)
R.check("S0 sigma_8 from this lane's sigma(R) = 0.8116 (CFG4_cosmology.out), |diff| <= 1e-3", abs(sig8 - 0.8116) <= 1e-3, f"{sig8:.5f}")
# M* (sigma = 1.686 at z = 0) by interpolation, a memory-free replacement for 'M* ~ 3e12'
Ms = np.geomspace(1e8, 1e15, 29)
ss = np.array([C.sigma_R(*C.delta2(c, 0, "d_m"), C.R_of_M(M)) for M in Ms])
Mstar = float(np.exp(np.interp(-1.686, -ss, np.log(Ms))))
P(f"  M* (sigma(M*, z=0) = 1.686) = {Mstar:.2e} Msun (memory said ~3e12)")
R.num("M_star", Mstar)

thr = dict(C.DELTA_TA_FROZEN)
if ROB == "2":
    thr[1100] = 0.5
    P("  *** ROBUST=2: delta_ta(1100) = 0.5 ***")
rows = {}
for M in MMINS:
    for z in ZS:
        s = sig[(z, M)] if z != 1100 or True else None
        zz = z if z in (0, 2.5, 10, 1100) else None
        F, lF = C.ps_F(thr[z], sig[(z, M)])
        rows[(z, M)] = (F, lF, sig[(z, M)])
req = C.OMC_H2_COMPARE
line = C.COSMIC_LINE_FRAC * req
if ROB == "1":
    req = 0.01
    line = C.COSMIC_LINE_FRAC * req
    P(f"  *** ROBUST=1: requirement lowered to {req}, line {line} ***")
P(f"\n  F_ta(z; M > M_min), frozen thresholds {thr}:")
P("   M_min     " + "".join(f"  z={z:<6g} sigma     log10 F   " for z in ZS))
for M in MMINS:
    P(f"   {M:7.0e} " + "".join(f"  {rows[(z, M)][2]:11.4g}  {rows[(z, M)][1]:9.2f} " for z in ZS))
omc = {}      # Omega_dust h^2 under the generous normalisation (supplied abundance), as log10 and value
for M in MMINS:
    for z in ZS:
        lr = rows[(z, M)][1] - rows[(0, M)][1]
        omc[(z, M)] = (lr, C.OMC_H2_COMPARE * 10.0 ** max(lr, -300.0))
P("\n  Omega_dust h^2(z) = 0.1200 F_ta(z)/F_ta(0) (generous normalisation; the ratio is log10-resolved, no underflow):")
P("   M_min       z=1100                z=10        z=2.5        z=0")
for M in MMINS:
    P(f"   {M:7.0e}   10^{omc[(1100, M)][0]:8.2f} x0.1200    {omc[(10, M)][1]:.4f}      {omc[(2.5, M)][1]:.4f}      {omc[(0, M)][1]:.4f}")
R.num("omega_dust_h2", {f"M{M:.0e}": {str(z): omc[(z, M)][1] for z in ZS} for M in MMINS})
R.num("log10_ratio_1100", {f"M{M:.0e}": omc[(1100, M)][0] for M in MMINS})
R.num("sigma_table", {f"z{z}_M{M:.0e}": sig[(z, M)] for (z, M) in sig})

R.banner("C1 (BINDING): Omega_dust h^2 at z = 1100 against the 0.5 x requirement line")
best = max(MMINS, key=lambda M: omc[(1100, M)][0])      # the most favourable M_min
lr_best = omc[(1100, best)][0]
supplied = C.OMC_H2_COMPARE * 10.0 ** max(lr_best, -300.0)
P(f"  most favourable M_min = {best:.0e} Msun: Omega_dust h^2(1100) = 0.1200 x 10^{lr_best:.1f}  (requirement {req}, line {line:g})")
sup_log = lr_best + math.log10(C.OMC_H2_COMPARE)
short_log = math.log10(line) - sup_log
P(f"  supplied abundance: 10^{sup_log:.1f}; shortfall against the line: 10^{short_log:.1f}; against the total 0.1200: 10^{math.log10(C.OMC_H2_COMPARE) - sup_log:.1f}")
c1_pass = sup_log >= math.log10(line)
c1_order = sup_log <= math.log10(0.1 * line)
if MUT == "1":
    P("  *** MUTATE=1: creation of Omega_c h^2 = 0.12 of uniform dust at z_i = 1e5 (initial data): the supplied abundance at z = 1100 is the whole 0.1200 ***")
    sup_log = math.log10(C.OMC_H2_COMPARE)
    c1_pass = sup_log >= math.log10(line)
    c1_order = False
if MUT == "2":
    P("  *** MUTATE=2: the pass line is evaluated at z = 0 (Omega_dust h^2(0) = 0.1200 by the normalisation) ***")
    sup_log = math.log10(omc[(0, best)][1])
    c1_pass = sup_log >= math.log10(line)
    c1_order = False
R.check("C1 COSMIC: Omega_dust h^2 at the evaluation epoch >= 0.5 x requirement", c1_pass,
        f"supplied 10^{sup_log:.1f} vs line {line:g}; shortfall factor 10^{math.log10(line) - sup_log:.1f}", kind="result")
R.check("C1b COSMIC: the shortfall is NOT an order of magnitude or more (the binding FAIL if this fails)", not c1_order,
        f"order-of-magnitude line {0.1 * line:g}", kind="result")
R.verdict("COSMIC", "PASS" if c1_pass else "FAIL (BINDING: STOP)",
          f"Omega_dust h^2 = 10^{sup_log:.1f} against the line {line:g} (total needed {req}); the run stops here for the frozen verdict")

R.banner("C2 (reported): z = 10 and z = 2.5 (the cold-early requirement R05 / G2)")
for M in MMINS:
    P(f"  M_min = {M:.0e}: Omega_dust h^2(z=10) = {omc[(10, M)][1]:.4f} ({omc[(10, M)][1] / C.OMC_H2_COMPARE:.3f} of 0.1200; shortfall {C.OMC_H2_COMPARE / omc[(10, M)][1]:.1f}x); "
      f"z = 2.5: {omc[(2.5, M)][1]:.4f} ({omc[(2.5, M)][1] / C.OMC_H2_COMPARE:.3f})")

R.banner("C3 (reported): the sigma(M) that would be needed for F_ta(1100) = 0.5")
x_half = 0.4769362762044699
s_need = thr[1100] / (math.sqrt(2.0) * x_half)
for M in MMINS:
    s1100 = sig[(1100, M)]
    amp = s_need / s1100
    s0_equiv = s_need / (s1100 / sig[(0, M)])
    P(f"  M_min = {M:.0e}: needs sigma(M, 1100) = {s_need:.3f} against CLASS {s1100:.4g}: amplification x{amp:.3g}; equivalent z = 0 sigma = {s0_equiv:.4g} (CLASS z = 0: {sig[(0, M)]:.3g})")
    R.num(f"sigma0_equiv_needed_M{M:.0e}", s0_equiv)

R.banner("C4 (reported, with its own line): linear baryon-only sigma_b(R, z = 0) against delta_ta(0) = 1.276")
cb = C.class_cosmo([0], baryon_only=True)
kb, D2b = C.delta2(cb, 0, "d_b")
Rg = np.geomspace(1e-3, 100.0, 120)
sb = np.array([C.sigma_R(kb, D2b, r) for r in Rg])
Rm = float(Rg[int(np.argmax(sb))])
P(f"  baryon-only run: omega_cdm = 1e-7, flat (Omega_Lambda = {cb.Omega_Lambda():.4f}); max over R in [1e-3, 100] Mpc of sigma_b(R, z = 0) = {sb.max():.4g} at R = {Rm:.3g} Mpc")
for M in (1e8, 1e10, 1e12):
    P(f"    at the LCDM-mass radius of M = {M:.0e}: sigma_b = {C.sigma_R(kb, D2b, C.R_of_M(M)):.4g} (LCDM sigma = {sig[(0, M)] if (0, M) in sig else float('nan'):.3g})")
c4_pass = sb.max() >= thr[0]
R.check("C4 the baryon-only linear field reaches delta_ta(0) = 1.276 on some scale at z = 0 (the trigger can fire without any cold matter)", c4_pass,
        f"max sigma_b = {sb.max():.4g}; shortfall {thr[0] / sb.max():.3g}x", kind="result")
R.num("sigma_b_max", float(sb.max()))

R.banner("C5 (reported): the acoustic baryon velocity divergence against the Hubble value, |delta theta_b|/(3H), k <= 100/Mpc")
cn = C.class_cosmo([10, 1100], newtonian=True)
for z in (1100, 10):
    tr = cn.get_transfer(z)
    k = tr["k (h/Mpc)"] * cn.h()
    calH = cn.Hubble(float(z)) / (1.0 + z)
    sel = k <= 100.0
    A = np.sqrt(C.PR_k(k)) * np.abs(tr["t_b"]) / (3.0 * calH)
    rms = math.sqrt(np.trapz((C.PR_k(k) * tr["t_b"] ** 2 / (3.0 * calH) ** 2)[sel], np.log(k[sel])))
    P(f"  z = {z}: max over k <= 100/Mpc of sqrt(P_R)|theta_b|/(3 calH) = {A[sel].max():.3e} at k = {k[sel][np.argmax(A[sel])]:.3g}/Mpc; rms = {rms:.3e}  (trigger needs ~1)")
    R.num(f"theta_b_over_3H_max_z{z}", float(A[sel].max()))
    R.num(f"theta_b_over_3H_rms_z{z}", rms)
R.check("C5 the acoustic theta_b reaches the Hubble value 3H at z = 1100 (the trigger can fire in the plasma)", R.nums["theta_b_over_3H_max_z1100"] >= 1.0,
        f"max {R.nums['theta_b_over_3H_max_z1100']:.2e}", kind="result")

R.banner("C6 (reported): CFG4's z = 0 cold budget, restated (not a new number)")
txt = open(os.path.join(C.REPO, "campaign_fresh_gravity", "CFG4_README.md")).read()
has = ("0.47" in txt and "0.55" in txt and "0.265" in txt)
P("  CFG4_README.md (cold budget, H3): Omega_ph = 0.47-0.55 if every galaxy's phantom ran to its turnaround radius, against Omega_c = 0.265; "
  "the budget edge x <= 0.46 uses all of Omega_c at z = 0 (canonical). Restated, not a pass: it is CFG4's own budget row.")
R.check("C6 CFG4_README.md carries the quoted budget numbers (0.47-0.55 against 0.265)", has, "", kind="control")

if MUT:
    R.finish([R.main_cells().get("C1 COSMIC: Omega_dust h^2 at the evaluation epoch >= 0.5 x requirement") is False, c1_pass])
elif ROB:
    R.finish([c1_pass])           # bites iff the COSMIC cell flips to PASS under the robustness variant
else:
    R.finish()
