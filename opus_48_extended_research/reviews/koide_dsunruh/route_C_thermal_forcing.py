#!/usr/bin/env python3
"""
ROUTE C core: does a dS-Unruh THERMAL amplitude FORCE the Koide circulant amplitude
r = sqrt(2)?   And does the SAME mechanism pass the CROSS-FERMION falsification?

Canonical Koide:  Q = (sum m)/(sum sqrt m)^2 = 1/3 + r^2/6 = 2/3  <=>  r = sqrt(2).
The ENTIRE unforced content of Koide is the single amplitude r (phase delta drops out).

We test, BOTH WAYS, each candidate that could make r=sqrt(2) NOT a free fit:
  (A) 2-dof thermal QUADRATURE  -> amplitude sqrt(2)?  (the suggestive one)
  (B) Bose thermal OCCUPATION of 3 democratic family modes -> does equal-weight force r?
  (C) the dS geometry sqrt(2/Z)=(3/8pi)^(1/4)=0.588 -> is THAT the amplitude? (No: 0.588!=1.414)
  (D) fluctuation-dissipation amplitude.
And the CROSS-FERMION test: a forced r=sqrt(2) from 3 equal-dS-coupled families MUST
explain why up-quarks (Q~0.89), down-quarks (~0.74), neutrinos (~1/3..0.6) do NOT obey it.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 30
import numpy as np

print("="*78)
print("ROUTE C: dS-Unruh THERMAL amplitude -> r=sqrt(2)?  FORCED or FREE?  + cross-fermion")
print("="*78)

# ---------------------------------------------------------------------------
# (A) The 2-dof thermal QUADRATURE sqrt(2).  The suggestive idea: a thermal mode
#     has 2 quadratures (x,p), RMS amplitude ~ sqrt(2) x zero-point. Does that set r?
# ---------------------------------------------------------------------------
print("\n[A] 2-dof thermal quadrature sqrt(2):")
print("    A harmonic mode in a thermal/coherent state: <x^2>+<p^2> has a sqrt(2) in the")
print("    RMS of the TOTAL quadrature vector vs a single quadrature.  BUT: the Koide r is")
print("    the amplitude of a CIRCULANT (3-family, phase 2pi/3) deviation of sqrt-MASS, a")
print("    DC/static VEV pattern across 3 generations -- NOT a per-mode quadrature RMS.")
print("    To equate them you must MAP {x,p} of one oscillator onto {gen-2, gen-3} family")
print("    directions. That map is a CHOICE (a re-labeling), not forced: nothing ties the")
print("    2 transverse family directions (the 2-dim 'standard' rep of S3) to the (x,p) of")
print("    a thermal oscillator with a fixed relative amplitude sqrt(2).  => r=sqrt(2) here")
print("    is INPUT by identifying 'the 2 thermal dof' with 'the 2 non-democratic families'.")
print("    VERDICT(A): suggestive numeric coincidence, NOT a forced amplitude (re-labeling).")

# Quantify: a thermal occupation n gives mode amplitude^2 ~ (2n+1)/2 (zero-pt) ... the
# ratio that would give 'r' is (transverse RMS)/(mean) which depends on n => FREE, not sqrt2.
n_occ = sp.symbols('n', positive=True)
# If sqrt(m_i) ~ mean + fluctuation with <fluct^2>/mean^2 set by occupation, r is a FUNCTION of n:
print("    Concretely: r^2 = (transverse var)/(mean^2) is a FREE FUNCTION of occupation n;")
print("    only the specific tuned n that makes r^2=2 reproduces Koide -> not forced by thermality.")

# ---------------------------------------------------------------------------
# (B) Democratic (equal-weight) dS-Unruh thermal occupation of 3 family states.
#     The claim to test: equal coupling of 3 families to the SAME dS bath forces the
#     sqrt-mass vector to sit at a FIXED angle to (1,1,1).
# ---------------------------------------------------------------------------
print("\n[B] Equal-weight dS-Unruh occupation of 3 family modes:")
print("    The dS-Unruh / Gibbons-Hawking bath is FAMILY-BLIND (one temperature T_dS for all).")
print("    A family-blind bath adds a COMMON-MODE shift to all 3 sqrt-masses (a multiple of")
print("    the democratic vector (1,1,1)).  KEY GEOMETRIC FACT: adding c*(1,1,1) to v MOVES")
print("    the angle theta(v) -- it does NOT fix it at 45deg unless c is tuned per-triple.")
# Demonstrate: start from any v, add lambda*(1,1,1), show angle is a free function of lambda.
lam = sp.symbols('lambda', real=True)
# generic v with some transverse content t and democratic content d:
d, t = sp.symbols('d t', positive=True)   # d=democratic comp, t=transverse magnitude
# |v|^2 = 3d^2 + t^2 ; v.n = 3d ; after adding lam*(1,1,1): d->d+lam
cos2_of_lam = (3*(d+lam))**2 / ( (3*(d+lam)**2 + t**2) * 3 )
cos2_simpl = sp.simplify(cos2_of_lam)
print("    cos^2 theta(lambda) =", cos2_simpl)
dcos2 = sp.simplify(sp.diff(cos2_of_lam, lam))
print("    d(cos^2)/d(lambda) =", sp.simplify(dcos2), " (nonzero => a family-blind shift MOVES the angle)")
print("    => A democratic dS bath does NOT pin cos^2=3/4; it slides the angle with its amplitude.")
print("    Equal-weight occupation forces the COMMON-MODE direction (good: that is the (1,1,1)")
print("    democratic axis = the right S3 home) but leaves the TRANSVERSE magnitude t (=> r) FREE.")
print("    VERDICT(B): democratic dS coupling forces the DEMOCRATIC AXIS, NOT the 45deg amplitude.")

# ---------------------------------------------------------------------------
# (C) Is the dS geometric O(1) the amplitude?  sqrt(2/Z)=(3/8pi)^(1/4)=0.5878.
# ---------------------------------------------------------------------------
print("\n[C] dS geometry hands sqrt(2/Z)=0.5878, the Koide amplitude is r=sqrt(2)=1.4142:")
Z = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
s2Z = mp.sqrt(2/mp.mpf(sp.N(Z,30)))
print("    sqrt(2/Z) =", s2Z, "   r_Koide=sqrt(2) =", mp.sqrt(2))
print("    ratio r/sqrt(2/Z) =", mp.sqrt(2)/s2Z, "  (= sqrt(Z) =", mp.sqrt(mp.mpf(sp.N(Z,30))), ")")
print("    The framework's forced dS O(1) is 0.588, NOT 1.414. To get r=sqrt(2) you would need")
print("    a SEPARATE sqrt(Z) factor with no dS-thermal justification.  => not the same number.")
print("    VERDICT(C): the one machine-exact dS amplitude (0.588) is NOT the Koide r (1.414).")

# ---------------------------------------------------------------------------
# (D) Fluctuation-dissipation amplitude: does FDT fix r?
# ---------------------------------------------------------------------------
print("\n[D] Fluctuation-dissipation: FDT sets <fluct^2> ~ 2 k_B T Im[chi]/omega (the '2' is the")
print("    Nyquist factor).  This '2' is an amplitude-SQUARED normalization of a SPECTRAL DENSITY,")
print("    not the ratio of transverse-to-democratic VEV across 3 GENERATIONS. Equating the FDT")
print("    '2' to r^2=2 again requires identifying the 3 family VEVs with thermal fluctuations of")
print("    a single mode at one T -- a mapping choice. And FDT gives a SPECTRUM (all frequencies),")
print("    not 3 discrete masses; nothing selects exactly 3 modes at the 2pi/3 circulant phases.")
print("    VERDICT(D): the FDT '2' is a spectral-density Nyquist factor, NOT forced to be r^2.")

# ---------------------------------------------------------------------------
# CROSS-FERMION FALSIFICATION (the decisive test).
# Real data: compute Q for charged leptons, up-quarks, down-quarks, neutrinos.
# A dS bath that couples EQUALLY to all 3 families of EVERY fermion type would give
# the SAME geometric angle for all -> would predict Koide for quarks/neutrinos too (FALSE).
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("CROSS-FERMION FALSIFICATION (PDG/global-fit central values, MS-bar @2GeV / pole):")
print("="*78)

def Q_of(masses):
    s = sum(mp.sqrt(m) for m in masses)
    sm = sum(masses)
    return sm/s**2

# charged leptons (pole, MeV):
lept = [mp.mpf('0.51099895'), mp.mpf('105.6583755'), mp.mpf('1776.86')]
# up-type quarks (u,c,t) MS-bar (u,c at 2GeV-ish / running; t pole) MeV:
up   = [mp.mpf('2.16'), mp.mpf('1270'), mp.mpf('172570')]      # PDG 2024 central
# down-type (d,s,b) MeV:
down = [mp.mpf('4.67'), mp.mpf('93.4'), mp.mpf('4180')]
# neutrinos: normal ordering, m1~0 example with Delta m^2 (eV); use a representative NO set:
# m1=0.001, m2=sqrt(7.42e-5+m1^2), m3=sqrt(2.51e-3+m1^2) eV
m1 = mp.mpf('0.001'); m2 = mp.sqrt(mp.mpf('7.42e-5')+m1**2); m3 = mp.sqrt(mp.mpf('2.51e-3')+m1**2)
nu_no = [m1, m2, m3]
# also degenerate-ish and inverted for range:
nu_deg = [mp.mpf('0.05'), mp.mpf('0.0505'), mp.mpf('0.0512')]

for name, mm in [("charged leptons (e,mu,tau)", lept),
                 ("up quarks (u,c,t)", up),
                 ("down quarks (d,s,b)", down),
                 ("neutrinos NO (m1=1meV)", nu_no),
                 ("neutrinos near-degenerate", nu_deg)]:
    q = Q_of(mm)
    cos2 = 1/(2*q) if False else (sum(mp.sqrt(x) for x in mm))**2/(3*sum(mm))
    ang = mp.degrees(mp.acos(mp.sqrt(cos2)))
    # implied r from Q=1/3+r^2/6:
    r2 = 6*(q-mp.mpf(1)/3)
    rr = mp.sqrt(r2) if r2>0 else mp.mpf('nan')
    flag = "  <== Koide 2/3!" if abs(q-mp.mpf(2)/3)<mp.mpf('1e-3') else ""
    print(f"  {name:32s} Q={float(q):.4f}  angle={float(ang):6.3f}deg  r={float(rr):.3f}{flag}")

print("\n  ONLY charged leptons hit Q=2/3 (r=sqrt2, 45deg). Quarks & neutrinos do NOT.")
print("  => a FAMILY-BLIND dS-Unruh bath (same T, same equal coupling to 3 families of EVERY")
print("     fermion) would give the SAME angle for all charged fermions -> it would WRONGLY")
print("     predict Koide for up/down quarks too.  The dS thermal mechanism has NO knob that")
print("     selects charged-LEPTONS specifically (it is blind to QED/QCD charge and to the")
print("     Yukawa sector). CROSS-FERMION: dS-thermal route FAILS the lepton-specificity test.")
print("="*78)
