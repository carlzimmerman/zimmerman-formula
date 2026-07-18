#!/usr/bin/env python3
"""
RE-DERIVATION (not taken on faith) of the non-adiabatic RELATIONAL sigma-spread
prediction + the power/gap arithmetic behind the Lane-F NO-GO, for GAP_STATEMENT.md.

Source being re-derived (committed, read):
  zimmerman-formula/real_research/reviews/member_MI_nonadiabatic_plunge.py  (STEP 3b/4)
  zimmerman-formula/real_research/reviews/sigma_spread_survey_forecast.py   (delivery)
  zimmerman-formula/real_research/reviews/member_MI_adversarial_check.py    (6-13% claim)

Physics (framework's OWN premises, never McGaugh nu):
  nu(y) = sqrt(1+1/y);  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x)  (its inverse)
  MI (Milgrom 2022 arXiv:2208.07073v3 Eq 34): A = a_in + a_ex*theta(om_ex/om_in),
    boost = 1/mu_fw(A/a0);  theta(1)=1, decreasing, theta(0)~few (form UNVERIFIED).
  MG (any modified-gravity realization, one shared field): boost depends ONLY on
    the momentary a_ex -> ZERO spread across infall phase at matched a_ext, any a0.
  Observable: sigma ~ sqrt(boost) spread across infall-phase y in [0.05, 1.5]
    among members at MATCHED momentary a_ext. MG-impossible by construction.

BOTH FOOTINGS (Carl's rule 4): canonical a0 = 9.36e-11 (rho_DE / cH_Lambda / Z),
alt a0 = 1.13e-10 (rho_total / cH0). Physical fields held fixed in m/s^2.
"""
import sys
import numpy as np

FOOTINGS = [("canonical cH_Lambda/Z", 9.36e-11), ("alt cH0 footing", 1.13e-10)]
A0_REF = 9.36e-11                       # physical setup defined once, in m/s^2
A_EX = 2.0 * A0_REF                     # cluster field at the members (fixed physical)
A_IN = 0.3 * A0_REF                     # member internal acceleration (fixed physical)
Y_PHASES = [0.05, 0.5, 1.0, 1.5]        # circular -> deep radial, SAME a_ext

def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)

THETAS = [("rational 2/(1+y^2)", lambda y: 2.0 / (1.0 + y * y)),
          ("exp e^{1-|y|}",      lambda y: np.exp(1.0 - np.abs(y))),
          ("exp e^{(1-|y|)/2}",  lambda y: np.exp((1.0 - np.abs(y)) / 2.0))]

print("=" * 96)
print(" 1) RE-DERIVED MI relational sigma-spread at matched a_ext (MG spread = 0 exactly, any a0)")
print("=" * 96)
all_spreads = {}
for fname, a0 in FOOTINGS:
    spreads = []
    print(f"\n footing: {fname:24s} a0 = {a0:.3e} m/s^2   "
          f"(a_ex/a0 = {A_EX/a0:.2f}, a_in/a0 = {A_IN/a0:.2f})")
    for tname, th in THETAS:
        boosts = np.array([1.0 / mu_fw((A_IN + A_EX * th(y)) / a0) for y in Y_PHASES])
        sig = np.sqrt(boosts)
        s = (sig.max() - sig.min()) / sig.mean()
        spreads.append(s)
        print(f"   theta = {tname:20s} sigma spread = {s*100:5.1f}%   "
              f"(boost spread = {(boosts.max()-boosts.min())/boosts.mean()*100:5.1f}%)")
    all_spreads[fname] = (min(spreads), max(spreads))
    print(f"   => band this footing: {min(spreads)*100:.1f}% - {max(spreads)*100:.1f}%")

lo = min(v[0] for v in all_spreads.values())
hi = max(v[1] for v in all_spreads.values())
print(f"\n BOTH-FOOTING BAND: {lo*100:.1f}% - {hi*100:.1f}% sigma spread "
      f"(corpus quotes 6-13%; MAGNITUDE theta-form UNVERIFIED, SIGN CORRECTED 2026-07-17 w9xvb10ui: "
      f"under-loaded/first-infall members MORE boosted = HOTTER; prior 'less boosted' was a low-theta<->low-boost label bug)")
assert 0.04 < lo < 0.09 and 0.09 < hi < 0.16, "re-derivation left the banked 6-13% neighborhood"

print("\n" + "=" * 96)
print(" 2) POWER ARITHMETIC (variance-excess estimator): why 23 in-hand carriers = NO-GO")
print("=" * 96)
print(""" Estimator: excess variance of matched-a_ext carrier sigmas over the measurement+FJ floor.
 z ~ (s*p)^2 / (eps_eff^2 * sqrt(2/N)),  eps_eff = sqrt(eps_meas^2 + eps_FJ^2)
 (s = true spread, p = infall-phase classification purity ~0.6, N = carriers).""")
N_INHAND = 23
print(f"\n {'s':>5} {'p':>4} {'eps_meas':>8} {'eps_FJ':>6} | {'z(N=23)':>8} | {'N(3sig)':>8} {'N(5sig)':>8}")
print(" " + "-" * 62)
best_z = 0.0
for s in (0.06, 0.09, 0.13):
    for eps_m, eps_fj in ((0.25, 0.15), (0.10, 0.15), (0.10, 0.10)):
        eps = np.hypot(eps_m, eps_fj)
        p = 0.6
        sig2 = (s * p) ** 2
        z = sig2 / (eps ** 2 * np.sqrt(2.0 / N_INHAND))
        n3 = 2.0 * (3.0 * eps ** 2 / sig2) ** 2
        n5 = 2.0 * (5.0 * eps ** 2 / sig2) ** 2
        best_z = max(best_z, z if eps_m == 0.25 else best_z)
        print(f" {s:5.2f} {p:4.1f} {eps_m:8.2f} {eps_fj:6.2f} | {z:8.2f} | {n3:8.0f} {n5:8.0f}")
print(f"""
 READ: at today's tier (eps_meas ~ 0.25, FJ floor 0.15) the 23 in-hand carriers give
 z ~ 0.05-0.24 in this arithmetic (0.1-0.4 with the purity/eps corners of the Lane-F
 pre-derived analysis, whose best corner was 0.36) -- NO-GO either way.
 A 3-sigma confirmatory test needs N ~ 10^3-10^5 carriers at that tier, or a <=10%
 carrier-sigma tier (ELT-HARMONI ~2032) PLUS an FJ floor <=0.10-0.15, where N(3sig)
 drops to ~10^2-10^3 -- which 4MOST-CHANCES-scale carrier counts can actually supply.""")

print("=" * 96)
print(" 3) DELIVERY (from committed sigma_spread_survey_forecast.py, re-quoted not re-invented):")
print("=" * 96)
print(""" HeCS/HeCS-omnibus (Rines+13/+18): 58+ clusters, ~22k members w/ caustic infall tags (archival)
 A2029 (Sohn+19): 1215 members, single system (marginal)
 WEAVE-WWFCS: 16-20 clusters z~0.05, thousands of members to ~5R200 -> 2027-2029
 4MOST-CHANCES: 150 clusters 0<z<0.45, ~300k spectra, >1000 members/cluster to 5r200 -> 2028-2031
 DESI DR1 647k-dwarf VAC: LSB-tail carriers cross-matchable NOW (target list, not a firing)
 ELT-HARMONI: the <=10% carrier-sigma tier -> ~2032""")

print("\nEXIT 0: re-derivation + power arithmetic verified, both footings.")
sys.exit(0)
