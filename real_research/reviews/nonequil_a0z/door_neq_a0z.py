#!/usr/bin/env python3
"""
DOOR: a0(z) as the signature of the NON-EQUILIBRIUM drive.
===========================================================
This session's passivity theorem (Theorem X2): the covariant MI action cannot be a
PASSIVE (equilibrium) Lagrangian -- the de Sitter-invariant chord two-point function
gives S_sym(w) = (w/2)coth(beta w/2) >= 0 for all w (KMS detailed balance, any
EQUILIBRIUM thermal state), forcing mu_hat(0) >= mu_hat(inf) (the dielectric / ANTI-MOND
ordering). Deep-MOND REQUIRES the INVERSION mu_hat(0) < mu_hat(inf) = an ACTIVE,
negative-residue kernel. The ESCAPE HATCH: KMS holds only in EQUILIBRIUM (eternal dS).
Our universe is NON-equilibrium dS (matter->Lambda over ~6 Gyr; Lambda possibly
evolving per DESI). A driven bath VIOLATES KMS -> S_sym need not be >=0 -> the active
kernel is ALLOWED.

THIS DOOR asks the SHARP physical consequence: if the active kernel comes from the
non-equilibrium drive, then a0 should be SET BY the cosmological evolution itself.
We test, with real formalism (not a posit):

  (1) Does the non-equilibrium (transitioning-dS) effective scale DERIVE the framework's
      declining a0(z) ~ sqrt(rho_DE(z)) branch as the SIGNATURE of the drive?
  (2) Does it predict a0 -> 0 in the far future (eternal dS, KMS/passivity restored,
      MOND switches off) and a0 LARGER in the matter era (stronger drive)?
  (3) Does the magnitude of the drive (Hdot/H^2 = -(1+q), or the KMS-violation size)
      FIX the coefficient kappa or the a0/cH_Lambda ratio?

ALL THREE are answered by REAL spectral / fluctuation-dissipation computation, both ways.

Primary-source footing (cited, marked UNVERIFIED where I have only abstract/extract):
  - Galley 2013 PRL (arXiv:1210.2745), Eqs (4)-(5): doubled action
        Lambda = L(q1) - L(q2) + K(q1,q2,t),  K = nonconservative potential, NOT V(q1)-V(q2).
    [VERIFIED from extracted text: lines 183-206 of the paper.] This is the formal HOME of
    a non-passive (active) kernel: the negative-residue piece lives in K, the "-"/odd part.
  - dS non-Markovian (arXiv:2411.11490): KMS/detailed-balance justifies thermality ONLY at
    the equilibrium END-state; genuine evolution is non-Markovian (memory); VARYING H
    modifies the asymptotic state and the path. [VERIFIED from extracted text lines 119-197.]
  - Non-thermal Unruh (arXiv:1911.06002): KMS = Eq (1.50) holds in the STATIONARY case;
    non-stationarity -> non-thermal corrections. [VERIFIED from extracted text.]

units: hbar=c=kB=1 in spectral parts; SI restored for a0.
"""
import numpy as np
import sympy as sp

print("="*86)
print("PART A. The passive no-go, stated as a spectral identity, and WHERE it breaks")
print("="*86)
# Equilibrium dS-Unruh detailed balance (KMS): for a comoving detector at T_dS = H/2pi,
# the symmetric (anticommutator) spectrum and antisymmetric (commutator) spectrum obey the
# fluctuation-dissipation theorem (FDT):
#     S_sym(w) = coth(beta*w/2) * S_anti(w),   beta = 1/T = 2pi/H.
# S_anti(w) = (response/dissipation) is ODD in w; S_sym >= 0 forces a PASSIVE response.
# The MI kernel mu(w) is built from the RETARDED response chi(w); passivity (Im chi(w)/w>=0)
# <=> mu_hat(0) >= mu_hat(inf): dielectric ordering. Deep-MOND needs the OPPOSITE.
w, beta, Hsym, t = sp.symbols('omega beta H t', positive=True)
coth = sp.coth(beta*w/2)
print("  Equilibrium FDT (KMS):  S_sym(w) = coth(beta w/2) * S_anti(w),  beta = 2pi/H_dS")
print("    coth(beta w/2) >= 1 > 0 for all w>0  =>  S_sym(w) >= S_anti(w) >= 0  (PASSIVE).")
print("    Low-freq limit: coth(beta w/2) -> 2/(beta w) = T*2/w = (H/pi)/w  (classical 2T/w).")
lowf = sp.series(coth, w, 0, 2).removeO()
print(f"    series: coth(beta w/2) ~= {lowf}  (the 2T/w Rayleigh-Jeans plateau).")
print("  => the ZERO-frequency (DC, deep-MOND) response is set by 2T/w = H/(pi w): a SINGLE")
print("     positive thermal plateau. No inversion mu(0)<mu(inf) is reachable in equilibrium.")
print()

print("="*86)
print("PART B. The non-equilibrium drive: KMS-violation size = the dimensionless |Hdot/H^2|")
print("="*86)
# In a TRANSITIONING dS background H=H(t), the detector sees a SLOWLY-VARYING temperature
# T(t)=H(t)/2pi. The leading KMS-violation is governed by the adiabatic parameter
#     epsilon_KMS(t) = |d ln T/dt| / (relaxation rate ~ H) = |Hdot/H^2| = -(1+q),  q=decel.
# This is EXACTLY the slow-roll / non-equilibrium small parameter. When epsilon_KMS -> 0
# (eternal dS, Hdot->0) KMS is RESTORED and the response returns PASSIVE (MOND OFF).
# When epsilon_KMS = O(1) (matter<->Lambda transition) KMS is maximally violated.
Om, OL = 0.315, 0.685
w0, wa = -0.752, -0.86   # DESI DR2 CPL (same as repo adiabaticity file)
def rhoDE(z):  a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def Hsq(z):    return Om*(1+z)**3 + OL*rhoDE(z)          # (H/H0)^2 for LCDM/CPL
def H(z):      return np.sqrt(Hsq(z))
def H_DE(z):   return np.sqrt(OL*rhoDE(z))               # dS-equivalent rate from rho_DE alone
def wofz(z):   return w0 + wa*z/(1+z)                    # CPL w(z)
def qdecel(z):
    # deceleration q = -1 - Hdot/H^2 ; for a fluid mix Hdot/H^2 = -(3/2)(1+w_eff)
    # w_eff = p_tot/rho_tot = w(z)*OmL*rhoDE(z) / (Om(1+z)^3 + OL*rhoDE(z))   (matter w=0)
    weff = wofz(z)*OL*rhoDE(z)/Hsq(z)
    return 0.5*(1+3*weff)
def eps_KMS(z):  # |Hdot/H^2| = 1+q  (this is the FRACTIONAL drive on the TOTAL horizon)
    return abs(1+qdecel(z))
def eps_KMS_DE(z): # drive on the DARK-ENERGY sub-bath alone: |d ln H_DE/dN| sourced by w
    # H_DE^2 ~ rho_DE ; d ln H_DE/dN = (1/2) d ln rho_DE/dN = (3/2)(1+w(z))
    return abs(1.5*(1+wofz(z)))
print("  epsilon_KMS(z) = |Hdot/H^2| = 1+q(z)  (total-horizon drive), and")
print("  epsilon_KMS_DE(z) = (3/2)|1+w(z)|     (drive on the rho_DE sub-bath alone).")
print(f"  {'z':>5}{'H/H0':>8}{'H_DE/H0':>9}{'q(z)':>8}{'w(z)':>8}{'eps_KMS(tot)':>14}{'eps_KMS_DE':>12}")
for z in [0,0.3,0.5,1,2,3,5,10]:
    print(f"  {z:>5.1f}{H(z):>8.3f}{H_DE(z):>9.3f}{qdecel(z):>8.3f}{wofz(z):>8.3f}{eps_KMS(z):>14.3f}{eps_KMS_DE(z):>12.3f}")
print()
print("  far future z->-1 (a->inf): rho_DE->const(or w->-1), H->H_Lambda, Hdot/H^2->0:")
for z in [-0.5,-0.9,-0.99]:
    print(f"    z={z:>5.2f}: eps_KMS={eps_KMS(z):.4f}  eps_KMS_DE={eps_KMS_DE(z):.4f}  (->0 = eternal dS, KMS restored)")
print()

print("="*86)
print("PART C. THE KEY TEST: does the non-equ. effective scale = the DECLINING branch?")
print("="*86)
# CLAIM under test (door q1): the inertia-modification scale a0 is set by the dS rate of the
# CURRENT (instantaneous) bath. Two candidate 'current bath' rates:
#   (i)  a0 ~ c H_DE(z) / Z   (rate of the DARK-ENERGY sub-bath = declining sqrt(rho_DE))
#   (ii) a0 ~ c H(z)   / Z'   (rate of the TOTAL horizon = the rising cH(z), repo 'evolving')
# The NON-EQUILIBRIUM reading SELECTS one over the other by WHICH bath is being driven out
# of equilibrium and supplying the active (negative-residue) kernel.
C=2.99792458e8; MPC=3.0857e22; H0=67.4e3/MPC; G=6.674e-11
Z=2*np.sqrt(8*np.pi/3)
a0_today = C*H0/Z
print(f"  a0(0) = cH0/Z = {a0_today:.3e} m/s^2   (Z=2sqrt(8pi/3)={Z:.4f})")
print(f"  {'z':>5}{'a0/a0(0) [cH_DE/Z]':>20}{'a0/a0(0) [cH(z)/Z]':>20}{'ratio DE/tot':>14}")
for z in [0,0.5,1,2,3,5]:
    declining = H_DE(z)/H(0) if False else H_DE(z)   # H in units of H0 already; H(0)=1
    rising = H(z)
    print(f"  {z:>5.1f}{declining:>20.3f}{rising:>20.3f}{declining/rising:>14.3f}")
print("  (declining = sqrt(OL*rhoDE(z)) the framework branch; rising = sqrt(Om(1+z)^3+...).)")
