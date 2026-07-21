#!/usr/bin/env python3
"""
FROZEN ESTIMATOR for the pre-registered a0(z) gate against the Rubin/LSST SN stream.
Committed 2026-07-21, BEFORE any calibrated Rubin SN cosmology exists (LSST began 2026-06-30).

THE TEST (framework's own terms): the de Sitter-Unruh MODIFIED-INERTIA framework predicts
  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0),   rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
so the acceleration scale evolves iff dark energy evolves. The ratio is Z-INDEPENDENT
(both footings collapse to it). INPUT = a (w0,wa) posterior from Rubin SNe (DESC calibrated
sample when it lands ~2027+; interim = published Rubin w0wa). OUTPUT = a0(z=3)/a0(0), its
significance vs flat, and the PRE-COMMITTED verdict below. No tuning after data.

PRE-COMMITTED DECISION THRESHOLDS (signed + hashed; do NOT edit after the freeze):
  R  := a0(z=3)/a0(0) central;  s_dec := sigma of the decline (R<1) vs flat (R=1)
  A) GATE OPEN (distinctive prediction ALIVE + supported):
       s_dec >= 3  AND  R in [0.55, 0.85]  (the framework's sqrt(rho_DE) band across both footings)
       -> a0 evolves as required; warrants the independent galaxy-side cross-scale confrontation.
  B) GATE DISSOLVED (safe core, NOT falsification):
       no decline (R = 1.0 within 2 sigma)  ->  framework reduces to constant-a0 MOND;
       the distinctive prediction is inapplicable. If ALSO R<=0.85 excluded at >=3 sigma,
       the distinctive decline is positively ruled out (still dissolution, not a kill of MOND-core).
  C) FRAMEWORK STRAINED (cosmology-side tension):
       R > 1 (RISE) at >=3 sigma -> the scale rises with z, contradicting a0 ~ sqrt(rho_DE) under
       evolving DE (this is the rising-cH rival's signature, already disfavored elsewhere).
  (If none: UNDECIDED -- insufficient significance.)
HONEST SCOPE (frozen in): this settles the COSMOLOGY-SIDE gate (does a0 evolve at all), which the
framework INHERITS from w(z); GATE OPEN means the distinctive prediction SURVIVES, NOT that the
framework is confirmed -- the confirming test is the independent galaxy-side a0(z). a0 value + Z
are POSITED. We do NOT build a DIY Hubble diagram from broker light curves (uncalibrated ->
systematics soup); primary input is the DESC calibrated sample.
"""
import numpy as np; np.seterr(all='ignore')
from scipy.special import erfcinv

def a0ratio(z,w0,wa): return np.sqrt((1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))

def gate_verdict(w0,sw0,wa,swa,rho,label,N=400000,z=3.0):
    g=np.random.default_rng(0)
    L=np.linalg.cholesky([[sw0**2,rho*sw0*swa],[rho*sw0*swa,swa**2]])
    pr=np.array([w0,wa])+g.standard_normal((N,2))@L.T
    R=a0ratio(z,pr[:,0],pr[:,1])
    med,lo,hi=np.median(R),np.percentile(R,16),np.percentile(R,84)
    # decline significance vs flat=1
    frac_notdecline=max(np.mean(R>=1.0),0.5/N); s_dec=np.sqrt(2)*erfcinv(2*frac_notdecline)
    frac_notrise=max(np.mean(R<=1.0),0.5/N);    s_rise=np.sqrt(2)*erfcinv(2*frac_notrise)
    # apply the FROZEN thresholds
    if s_rise>=3 and med>1: verdict="C) FRAMEWORK STRAINED (a0 rises with z)"
    elif s_dec>=3 and 0.55<=med<=0.85: verdict="A) GATE OPEN (distinctive prediction ALIVE)"
    elif abs(med-1.0)<=2*((hi-lo)/2): verdict="B) GATE DISSOLVED-ish (consistent with flat; -> constant-a0 MOND)"
    else: verdict="UNDECIDED (insufficient significance / out-of-band)"
    print(f"\n[{label}]  w0={w0:+.3f}+/-{sw0:.3f}  wa={wa:+.2f}+/-{swa:.2f}")
    print(f"    a0(3)/a0(0) = {med:.3f} [{lo:.3f},{hi:.3f}]   decline {s_dec:.1f}sigma / rise {s_rise:.1f}sigma")
    print(f"    FROZEN VERDICT -> {verdict}")
    return med,s_dec,verdict

print("PRE-REGISTERED a0(z) GATE -- frozen decision procedure (Rubin/LSST SN stream)")
print("="*76)
print("Applied to the CURRENT best input (DESI DR2 now) as the baseline the freeze starts from:")
gate_verdict(-0.838,0.055,-0.62,0.22,-0.86,"DESI DR2 2025 (baseline at freeze)")
print("\nForecast Rubin inputs (see forecast_rubin_a0z.py; these are PROJECTED, not data):")
gate_verdict(-0.838,0.040,-0.62,0.15,-0.90,"Rubin SN-alone forecast (FoM~150)")
gate_verdict(-0.838,0.020,-0.62,0.08,-0.90,"Rubin SN+CMB/BAO forecast (FoM~500)")
print("\n" + "="*76)
print("At the freeze (2026-07-21): DESI-now gives a 2.0-sigma HINT -> UNDECIDED by the >=3sigma")
print("threshold. The verdict is committed; only the INPUT (w0,wa) will be updated, from the DESC")
print("calibrated Rubin sample (~2027+). No threshold, band, or estimator may change after this file's hash.")
print("EXIT 0")
