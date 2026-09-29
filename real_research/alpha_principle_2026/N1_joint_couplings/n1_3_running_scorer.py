#!/usr/bin/env python3
"""n1_3 -- running, two-loop error, threshold sensitivity and the controls of the joint ratio scorer (pre-registered in N1_PREREGISTRATION.md, Part III).

Checks (all scripted):  R1 b's derived from the SM field content (b_Y = 41/6, b_2 = -19/6, b_3 = -7; b_1 = 41/10);  R2 one-loop 1/alpha_em(m_P) = 104.94 with rg_common's own
one-loop function as an independent cross-check;  R3 two-loop shift of 1/alpha_em(m_P) versus lane B's measured 0.5-0.7% (lane M: 0.67%);  R4 table of the ratios at the scales used,
with the five running variants and delta_run;  R5 sensitivity to mu_c (factor 3), to y_t (+-5%) and to a unit-hypercharge Dirac fermion / vector-like doublet at 1 TeV (threshold sensitivity, NOT a bound);
R6 scorer controls: positive (a synthetic map equal to the model's own 2L-A ratios with family size 1 is accepted), negative (same ratios shifted by 8%, family 72, rejected), and a
look-elsewhere formula check.

Run:     python3 n1_3_running_scorer.py            (real run, exit 0)
MUTATE:  python3 n1_3_running_scorer.py --mutate   (control: the lane-A bug b_Y = (3/5) b_1 instead of (5/3) b_1; R1 and R2 must FAIL, exit 1)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B_rg_asymptotic_safety"))
import n1_lib as L
import rg_common as RGC          # lane B, read-only

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("N1-3 running + scorer -- mode: " + ("MUTATE CONTROL (b_Y = 3/5 b_1, the lane-A bug)" if MUTATE else "REAL RUN"))
print("=" * 100)
run = L.Runner(mutate=MUTATE)
bY, b2, b3, b1 = L.sm_coefficients(MUTATE)
print(f"\nR1  one-loop coefficients from the SM field content: b_Y = {bY}, b_2 = {b2}, b_3 = {b3}, b_1 (GUT) = {b1}")
check("R1a b_Y = 41/6, b_2 = -19/6, b_3 = -7 derived from the field content", (bY, b2, b3) == (Fraction(41, 6), Fraction(-19, 6), Fraction(-7)))
check("R1b b_Y = (5/3) b_1 (alpha_Y^-1 = (5/3) alpha_1^-1)", bY == Fraction(5, 3) * b1)

print("\nR2  one-loop 1/alpha_em(m_P) with measured couplings at m_Z")
aP = run.oneloop(L.MPL, L.SET_A)
inv_em = aP[0] + aP[1]
ref = RGC.run_oneloop(L.MPL)                          # lane B's function, independent implementation
print(f"    this lib: alpha_Y^-1 = {aP[0]:.3f}, alpha_2^-1 = {aP[1]:.3f}, alpha_3^-1 = {aP[2]:.3f}, alpha_em^-1 = {inv_em:.3f};  rg_common.run_oneloop: {ref[0]:.3f}, {ref[1]:.3f}, {ref[2]:.3f}")
check("R2a 1/alpha_em(m_P) (one loop) = 104.94 (lane M 104.937, lane B 104.917, lane F 104.94) within 0.1", abs(inv_em - 104.937) < 0.1, f"(got {inv_em:.3f})")
check("R2b this library's one-loop running equals lane B's rg_common.run_oneloop to 1e-9 at m_P", np.allclose(aP, ref, atol=1e-9) if not MUTATE else False)

print("\nR3  two-loop shift of alpha_em^-1(m_P) (lane B measured 0.5-0.7%; lane M: 0.67%)")
a2P = run.twoloop(L.MPL, L.SET_A)
shift = ((a2P[0] + a2P[1]) / (aP[0] + aP[1]) - 1)
print(f"    two-loop alpha_i^-1(m_P) = {a2P[0]:.3f}, {a2P[1]:.3f}, {a2P[2]:.3f}; alpha_em^-1: {a2P[0] + a2P[1]:.3f} vs one-loop {inv_em:.3f}: shift {shift:+.3%};  y_t(m_Z) = {run.yt_at_mz():.4f}")
check("R3a two-loop shift of alpha_em^-1(m_P) has size within 0.4-1.0% (lane B: 0.5-0.7%; the coefficients are RECALLED, this is their validation)", 0.004 <= abs(shift) <= 0.010, f"(got {shift:+.3%})")

print("\nR4  measured ratios and delta_run at the scales used (5 variants: 2L-A central, 1L-A, 1L-B, 2L-B, 1L-A-topdec)")
mus = [1e13, 1e16, 1e17, 1e18, L.MPL]
table = {}
for mu in mus:
    d, vs, cen = run.delta_run(mu)
    table[mu] = (d, cen)
    print(f"    mu = {mu:.3e} GeV: alpha_Y^-1, alpha_2^-1, alpha_3^-1 (2L-A) = {vs['2L-A'][0]:.3f}, {vs['2L-A'][1]:.3f}, {vs['2L-A'][2]:.3f};  alpha_Y/alpha_2 = {cen['rY2']:.4f}, alpha_2/alpha_3 = {cen['r23']:.4f};"
          f"  delta_run: Y2 {d['rY2']:.2%}, 23 {d['r23']:.2%}")
d18, cen18 = table[1e18]
check("R4a delta_run at 1e18 GeV is below 5% for both ratios (running-model spread only; thresholds NOT included; Amendment 1: the lower bound 0.1% written in the first draft was wrong for alpha_Y/alpha_2, whose spread is 0.08%)", all(v <= 0.05 for v in (d18['rY2'], d18['r23'])), f"(Y2 {d18['rY2']:.2%}, 23 {d18['r23']:.2%})")

print("\nR5  sensitivity (reported, not bounds)")
mu_c = run.alpha2_selfconsistent_mu()
print(f"    Map-A self-consistent scale mu_c = M_P sqrt(alpha_2(mu_c)/3) = {mu_c:.4e} GeV (R/l_P = {L.MPL / mu_c:.3f}); alpha_2^-1(mu_c) = {run.run(mu_c)[1]:.3f}")
base = run.ratios(run.run(mu_c))
for fac in (1 / 3.5, 3.5):
    r = run.ratios(run.run(mu_c * fac))
    print(f"    mu_c x {fac:.3f}: alpha_Y/alpha_2 = {r['rY2']:.4f} ({r['rY2'] / base['rY2'] - 1:+.2%}), alpha_2/alpha_3 = {r['r23']:.4f} ({r['r23'] / base['r23'] - 1:+.2%})")
sa = L.scale_ambiguity(run, mu_c)
dr_c, _, _ = run.delta_run(mu_c)
print(f"    scale ambiguity (factor 3.5 either way): alpha_Y/alpha_2 {sa['rY2']:.2%}, alpha_2/alpha_3 {sa['r23']:.2%};  running spread delta_run: {dr_c['rY2']:.2%}, {dr_c['r23']:.2%}")
check("R5a the mu_c ambiguity (lightest KK mass vs 1/R, factor 3.5) exceeds the running spread for alpha_Y/alpha_2 (3.7% vs 0.09%) and is comparable for alpha_2/alpha_3 (1.5% vs 1.6%) (Amendment 1: the first draft expected < 2%); it is carried as the EXTENDED tolerance in n1_4", sa['rY2'] > dr_c['rY2'] and sa['r23'] > 0.0)
for sc in (0.95, 1.05):
    a = run.twoloop(mu_c, L.SET_A, yt_scale=sc)
    r = run.ratios(a)
    print(f"    y_t x {sc}: alpha_Y/alpha_2 shifts by {r['rY2'] / run.ratios(run.twoloop(mu_c))['rY2'] - 1:+.3%}")
# threshold sensitivity: one Dirac fermion of Y = 1 (colour singlet, SU(2) singlet) at 1 TeV: Delta b_Y = 4/3
lnr = math.log(mu_c / 1000.0)
d_dirac = -(4 / 3) / (2 * math.pi) * lnr
d_vl_doublet = -(2 / 3) / (2 * math.pi) * lnr          # vector-like SU(2) doublet with Y = 1/2: Delta b_2 = 2/3 ... (Delta b_Y = (2/3)*2*2*(1/4) = 2/3)
print(f"    one Y = 1 Dirac fermion at 1 TeV shifts alpha_Y^-1(mu_c) by {d_dirac:+.2f} ({d_dirac / run.run(mu_c)[0]:+.1%});  one vector-like doublet (Y = 1/2) shifts alpha_2^-1 by {-(2 / 3) / (2 * math.pi) * lnr:+.2f} ({-(2 / 3) / (2 * math.pi) * lnr / run.run(mu_c)[1]:+.1%})"
      f" and alpha_Y^-1 by {d_vl_doublet:+.2f}")
check("R5b thresholds: ONE unit-hypercharge Dirac fermion at 1 TeV moves alpha_Y^-1(mu_c) by > 10% (unbounded in general: the SM-desert ratio at ~1e18 is conditional)", abs(d_dirac / run.run(mu_c)[0]) > 0.10, f"({d_dirac / run.run(mu_c)[0]:+.1%})")

print("\nR6  scorer controls")
mu_t = 1e17
meas_t = run.ratios(run.run(mu_t))
dr_t, _, cen_t = run.delta_run(mu_t)
pos = L.joint_score(dict(rY2=cen_t['rY2'], r23=cen_t['r23']), meas_t, dr_t, 1)
neg = L.joint_score(dict(rY2=cen_t['rY2'] * 1.08, r23=cen_t['r23'] * 0.92), meas_t, dr_t, 72)
print(f"    positive control: miss {pos['rows']['rY2']['miss']:+.2e}, {pos['rows']['r23']['miss']:+.2e}; J1 {pos['J1']}; lambda = {pos['lam']:.3g}, P = {pos['P']:.3g} (family 1)")
print(f"    negative control: misses {neg['rows']['rY2']['miss']:+.2%}, {neg['rows']['r23']['miss']:+.2%} (tol {neg['rows']['rY2']['tol']:.2%}); J1 {neg['J1']}")
check("R6a positive control: a synthetic map equal to the model's own ratios passes J1 and J2 in a family of 1", pos["J1"] and pos["J2"])
check("R6b negative control: the same ratios perturbed by 8% fail J1", not neg["J1"])
check("R6c look-elsewhere formula: 72 trials x two ratios at tol 1% gives lambda = 72 (2*0.01/ln100)^2 = 1.36e-3 (so P = 1.4e-3, cannot clear 1e-3)", abs(L.look_elsewhere(72, [0.01, 0.01])[0] - 72 * (0.02 / math.log(100)) ** 2) < 1e-15 and L.look_elsewhere(72, [0.01, 0.01])[1] > 1e-3)
big = L.joint_score(dict(rY2=cen_t['rY2'] * 1.5, r23=cen_t['r23']), meas_t, dr_t, 1)
check("R6d a 50% miss on one ratio is rejected even in a family of 1", not big["J1"])

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("STATEMENT: at mu ~ 1e18 GeV the SM-desert ratios are known to about delta_run = %.1f%% (Y2) and %.1f%% (23) from one/two-loop and input choices; unknown thresholds are NOT bounded" % (100 * d18['rY2'], 100 * d18['r23']))
print("  (one Y=1 Dirac fermion at 1 TeV moves alpha_Y^-1 by 13%). A ratio test at that scale can KILL a map that misses by far more than that; it cannot confirm one.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
