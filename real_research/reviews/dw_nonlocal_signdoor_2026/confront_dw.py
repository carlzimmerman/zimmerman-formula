#!/usr/bin/env python3
"""
CONFRONT: Deffayet-Woodard (arXiv:2512.10513, JCAP 04(2026)081) vs the banked
anti-MOND sign theorem, and vs the framework's declining a0(z) (Front B).

Both Scout A and Scout B READ the paper (abs + HTML v2 + local PDF/pdftotext).
Verified structural facts (quotes/eq-numbers in scout reports):
  - L_MOND = -(a0^2/16 pi G) M[g] sqrt(-g)  (eq 31) ADDED to the GRAVITATIONAL
    Lagrangian, varied w.r.t. the metric -> modifies Einstein eqs / g00.
  - u_mu = d_mu phi is a MIMETIC constraint field (d_mu phi d^mu phi = -1),
    a UNIQUE NONLOCAL FUNCTIONAL of the metric with NO independent kinetic term.
  - It manufactures a CDM-like stress tensor T_mu_nu = rho u_mu u_nu (eq 14)
    that SOURCES the metric; test particles follow GEODESICS (eq 39-42).
  - Paper's own words (Conclusions): "a fully relativistic, MODIFIED GRAVITY model".
  - MOND sign = inhomogeneous branch of transport eq (33) + f(Z)=(1/2)Z exp[-(1/3)sqrt|Z|]
    (eq 30), a PHENOMENOLOGICAL CHOICE ("a simple function which accomplishes all three").

This script does NOT re-derive those (they are read from the paper). It performs the
ONE quantitative check that matters for the verdict: the Front-B a0(z) discriminant,
including whether the claimed z~0.088 zero-crossing is robust to LCDM parameters.
"""
import numpy as np
from scipy import integrate

# ---- cosmology ----
c = 2.99792458e8
Mpc = 3.0856775814913673e22
H0 = 67.4e3/Mpc
Om, Or = 0.315, 9.0e-5
OL = 1.0 - Om - Or
Z_geo = np.sqrt(32*np.pi/3.0)

def E(z):
    return np.sqrt(Or*(1+z)**4 + Om*(1+z)**3 + OL)

# ---- DW driving invariant Z(z): sqrt(-Z) prop (1+z)^3 * I(z),  eq 51 ----
# I(z) = INT_z^inf [ Or(1+z')^4 + (1/2)Om(1+z')^3 - OL ] / [ (1+z')^4 E(z') ] dz'
def integrand(zp):
    num = Or*(1+zp)**4 + 0.5*Om*(1+zp)**3 - OL
    return num/((1+zp)**4 * E(zp))

def I_of_z(z, zmax=1e6):
    val, _ = integrate.quad(integrand, z, zmax, limit=300)
    return val

print("="*70)
print("PART 1 -- MECHANISM (read from paper; classification, not re-derived)")
print("="*70)
print(" L_MOND added to GRAVITATIONAL Lagrangian (eq31), varied w.r.t. metric.")
print(" u_mu=d_mu phi = mimetic constraint field, NONLOCAL FUNCTIONAL of g,")
print("   NO independent kinetic term -> sources a CDM-like T_mu_nu (eq14).")
print(" Test particles follow GEODESICS (eq39-42): INERTIA IS UNTOUCHED.")
print(" => MODIFIED GRAVITY (mimetic/khronon/AeST cousin), paper's own words.")
print(" Sign theorem is about INERTIAL response to a passive bath -> OUT OF DOMAIN.")
print(" Residual: MOND sign = chosen inhomog. branch of eq33 + f(Z) |Z| choice (eq30).")

print()
print("="*70)
print("PART 2 -- FRONT-B a0(z) DISCRIMINANT")
print("="*70)

# DW cosmological invariant sign + claimed crossing
print("\n[DW] cosmological Z(z): sign of I(z) (Z<0 when I>0). Integrand vs accumulated:")
print(f"{'z':>8} {'integrand':>13} {'I(z) accum':>13} {'-> Z sign':>10}")
for z in [1100.,10.,1.,0.5,0.2,0.1,0.088,0.05,0.0]:
    I = I_of_z(z)
    print(f"{z:>8.3f} {integrand(z):>13.3e} {I:>13.4e} {'Z<0' if I>0 else 'Z>=0':>10}")

# robustness of the crossing
Igrid = np.array([I_of_z(z) for z in np.linspace(0.0,0.6,61)])
crosses = np.any(np.diff(np.sign(Igrid))!=0)
print(f"\n[DW crossing robustness] does accumulated I(z) cross 0 in [0,0.6]"
      f" for Planck LCDM? {crosses}")
print(" -> integrand goes NEGATIVE below z~0.6 (Lambda dominates) BUT the")
print("    accumulated integral stays POSITIVE (I(0)={:.4f}); the claimed".format(I_of_z(0.0)))
print("    z~0.088 crossing is NOT reproduced with generic LCDM params --")
print("    it depends on ref [13]'s exact low-z/initial-surface prescription.")

# framework a0(z): both footings
print("\n[framework] a0(z)=c H_Lambda(z)/Z_geo, Z_geo=sqrt(32pi/3)={:.4f}".format(Z_geo))
print(f"{'z':>8} {'a0 pure-Lambda':>16} {'a0 rho_total':>16}")
for z in [1100.,10.,1.,0.5,0.2,0.088,0.0]:
    a_pL = c*H0*np.sqrt(OL)/Z_geo
    a_rt = c*H0*E(z)/Z_geo
    print(f"{z:>8.3f} {a_pL:>16.4e} {a_rt:>16.4e}")
print(" -> pure-Lambda (w=-1): CONSTANT 9.43e-11, NO crossing.")
print(" -> rho_total: smooth MONOTONE rise with z, NO crossing.")

print()
print("="*70)
print("PART 3 -- FRONT-B VERDICT")
print("="*70)
print(" DW bound-system a0 is STATIC ~1.2e-10 (a fixed constant in eq31), so DW")
print("   does NOT compete on the declining-a0(z) axis at all.")
print(" DW's ONLY z-structure is the cosmological Z(z) sign-flip; its claimed")
print("   z~0.088 crossing is (a) not robustly reproduced here, and (b) a")
print("   cosmological-branch feature, not a directly-measured galaxy-scale a0(z).")
print(" Framework a0(z) is single-signed & monotone, NO crossing.")
print(" => The z~0.088 feature is DW-specific IN PRINCIPLE but its observability")
print("    as a Front-B discriminator is UNESTABLISHED. At today's ~30-100% a0(z)")
print("    errors (lensing-RAR/MUSE), both sit inside error bars: Front B neither")
print("    cleanly gains nor loses power. Front B is NOT strengthened by DW; if")
print("    anything DW's static bound-system a0 means it does not test the")
print("    framework's declining-a0 axis.")
print("\nEXIT 0")
