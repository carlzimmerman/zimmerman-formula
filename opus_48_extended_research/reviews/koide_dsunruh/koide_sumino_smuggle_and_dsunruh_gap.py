#!/usr/bin/env python3
"""
ROUTE D -- ADVERSARIAL / NULL.  PART (a): locate the EXACT smuggle-point in each route's
claimed derivation, and quantify the dS-Unruh magnitude gap that any "dS supplies the
Sumino cancellation" claim must close.

Sumino QED breaking (arXiv:0812.2103, Eq.2):
    m_i^pole = [ 1 + (alpha/pi)( (3/4) log(mu^2/mbar_i^2) + 1 ) ] mbar_i(mu)
The ONLY Koide-breaking piece is  -(3 alpha/4pi) mbar_i log(mbar_i^2)  (the rest is
const.*mbar_i = length-only, direction-preserving).  We:
  (1) show numerically that this log term TILTS the (sqrt m) vector off 45 deg by ~0.1-0.2%
      in Q -- i.e. nature's Koide is exact at POLE masses only via Sumino's cancellation;
  (2) state the dS-Unruh floor magnitude and show the gap to the required 3 alpha/8pi
      coefficient (the banked ~10^36, reproduced independently here);
  (3) enumerate WHERE each route smuggles in 2/3 / r=sqrt2.
"""
import numpy as np
from math import pi, log, sqrt

alpha = 1/137.035999084
# pole masses (MeV)
mpole = np.array([0.51099895000, 105.6583755, 1776.86])

def Qgeo(m):
    s = np.sqrt(m); return m.sum()/s.sum()**2

print("="*72)
print("(1) The QED log term is what BREAKS Koide -- Sumino must cancel it (IR statement)")
print("="*72)
# Invert Eq.2 at mu = M_Z to get mbar from mpole (1-loop), then see Q at mbar vs pole.
mu = 91187.6  # MeV
# mpole = [1 + (a/pi)((3/4)ln(mu^2/mbar^2)+1)] mbar ; solve iteratively for mbar
mbar = mpole.copy()
for _ in range(60):
    fac = 1 + (alpha/pi)*((3/4)*np.log(mu**2/mbar**2) + 1)
    mbar = mpole/fac
Q_pole = Qgeo(mpole)
Q_bar  = Qgeo(mbar)
print(f"  Q_geo at POLE masses (what nature shows) = {Q_pole:.7f}  (45deg=0.6666667)")
print(f"  Q_geo at MSbar(M_Z) masses               = {Q_bar:.7f}")
print(f"  shift from the QED log alone             = {(Q_bar-Q_pole)/Q_pole*100:+.3f}%")
print("  => Koide is a POLE-mass (IR) relation; the breaking is the per-flavor -3a/4pi log.")
print("     A real mechanism must cancel THIS log -> Sumino's U(3) family loop. IR, not UV.")
print()
# The Sumino cancellation coefficient that must be reproduced:
coeff_required = 3*alpha/(8*pi)
print(f"  Required Sumino-scale coefficient 3*alpha/(8pi) = {coeff_required:.4e}")

print()
print("="*72)
print("(2) dS-Unruh magnitude gap (independent reproduction of the banked ~10^36)")
print("="*72)
hbar = 1.054571817e-34; c = 2.99792458e8; kB = 1.380649e-23
H_Lambda = 1.78e-18   # s^-1  (cH_Lambda/c; from Lambda)
# dS-Unruh rest-frame floor energy E0 = (hbar/2pi) * H_Lambda   (a->0 limit of Deser-Levin)
E0 = (hbar/(2*pi))*H_Lambda     # Joules
E0_eV = E0/1.602176634e-19
m_e_eV = 0.51099895000e6
dm_over_m = E0_eV/m_e_eV
print(f"  dS-Unruh rest-frame floor E0 = (hbar/2pi)H_Lambda = {E0_eV:.3e} eV")
print(f"  fractional shift on the electron dm/m = {dm_over_m:.3e}")
print(f"  required Sumino-class shift 3alpha/8pi = {coeff_required:.3e}")
print(f"  GAP = required/available = {coeff_required/dm_over_m:.3e}  "
      f"(log10 = {np.log10(coeff_required/dm_over_m):.1f})")
print("  => dS-Unruh floor is ~10^36 too small to act as the Sumino cancellation. CONFIRMED.")

print()
print("="*72)
print("(3) SMUGGLE-POINT LEDGER -- where each route inserts 2/3 / r=sqrt2 by hand")
print("="*72)
ledger = [
 ("Koide original ansatz  sqrt(m_i)=M(1+sqrt2 k cos(2pi i/3+d))",
  "the '2' under the sqrt is the NORMALIZATION choice; setting k=1 IS Q=2/3. "
  "sqrt2 chosen so the coeff is 'nice'; k_f!=1 for quarks. SMUGGLE: k=1."),
 ("Foot geometric  cos theta = 1/sqrt2  (theta=45 deg)",
  "Foot WRITES 'if we choose theta=pi/4 we get Koide' (paper line 300). "
  "OBSERVED, not derived; quark version 'unsuccessful' (line 815). SMUGGLE: choose 45."),
 ("Sumino U(3)  condition (34): (Phi_0)^2 = Phi_a Phi_a",
  "this IS the 45-deg / Koide constraint imposed on the VEV (Fig.5); paper line 1227 "
  "'it is unclear what mechanism protects condition (34)'. SMUGGLE: assume cond.(34)."),
 ("Framework 'CUBE/GAUGE = 8/12 = 2/3'  &  '2/3 = 2/N_gen'",
  "164 catalogued re-labelings; gives 2/3 for any 3-fold structure -> 2/3 for quarks too "
  "-> cross-fermion FALSIFIED. SMUGGLE: identify a 2/3-valued ratio and call it Q."),
 ("Framework 'kappa=1/2 -> 1/sqrt(kappa) = sqrt2'",
  "cross-sector (kappa is the gravity-action normalization), mechanism-free, and "
  "quark-Koide-falsified. SMUGGLE: borrow an unrelated sqrt2-valued O(1)."),
 ("Framework 'sqrt(2/Z) = (3/8pi)^1/4 machine-exact'",
  "TRUE and forced -- but it is the COSMIC seesaw coeff (rho_DE), contains NO lepton; "
  "its value 0.588 != sqrt2=1.414. Does not even hit the target. SMUGGLE: domain-jump."),
 ("Any dS-Unruh 'IR cancellation supplies Sumino's loop'",
  "fails by ~10^36 in magnitude (above), couples to kinematic |a| absent in loops, "
  "1/m vs log per-flavor shape, cosmological vs TeV scale. SMUGGLE: none works -> NULL."),
]
for i,(route, smug) in enumerate(ledger,1):
    print(f"\n [{i}] {route}")
    print(f"     SMUGGLE: {smug}")

print()
print("="*72)
print("NET VERDICT (null held): every route either (a) inputs Q=2/3 via an ansatz/")
print("normalization/condition, or (b) gives 2/3 universally and is cross-fermion-refuted,")
print("or (c) is a domain-jump O(1) that doesn't even land on sqrt2.  dS-Unruh adds nothing")
print("(10^36 short, wrong channel/shape/scale).  r=sqrt2 stays FREE -- a re-labeling.")
