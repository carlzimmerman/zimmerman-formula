#!/usr/bin/env python3
"""
SCOUT A -- a0(z) BTFR PREDICTION CURVE
de Sitter-Unruh MODIFIED-INERTIA framework.

Deep-MOND BTFR (an inertia relation, exact here): v^4 = G * M_b * a0.
=> log10(v) = (1/4)*[log10(G*M_b) + log10(a0)]
At FIXED M_b, an a0 that changes with z shifts v:
    dlog10(v) = (1/4)*log10( a0(z)/a0(0) )
At FIXED v, it shifts inferred M_b:
    dlog10(M_b) = -log10( a0(z)/a0(0) )

Sign convention (BTFR-offset):
  a0(z) < a0(0)  =>  dlog10(v) < 0  =>  disc lies BELOW the z=0 BTFR (LOW in v).
  a0(z) = a0(0)  =>  ON the z=0 BTFR.
  a0(z) > a0(0)  =>  ABOVE the z=0 BTFR (HIGH in v).

Three branches:
  A (canonical, DECLINING): a0(z)=a0(0)*sqrt(rho_DE(z)/rho_DE(0)), DESI CPL w0,wa.
  B (rising, alt footing):   a0(z) prop c*H(z)=a0(0)*E(z).
  C (constant):              a0(z)=a0(0) (Milgrom null).
"""
import numpy as np

# --- footings ---
a0_canon = 9.36e-11   # rho_DE / cH_Lambda footing
a0_alt   = 1.13e-10   # rho_total / cH0 footing

# --- cosmology ---
Om = 0.315
OL = 1.0 - Om
# DESI DR2-style CPL
w0 = -0.752
wa = -0.86

def a_of_z(z):
    return 1.0/(1.0+z)

def E_of_z(z):
    a = a_of_z(z)
    return np.sqrt(Om*(1.0+z)**3 + OL)

def rho_DE_ratio(z):
    """rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa*(1-a)."""
    a = a_of_z(z)
    # standard CPL DE density evolution
    return a**(-3.0*(1.0+w0+wa)) * np.exp(3.0*wa*(a-1.0))

# BRANCH A: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))
def branchA_ratio(z):
    return np.sqrt(rho_DE_ratio(z))

# BRANCH B: a0(z)/a0(0) = E(z)   (c*H(z) footing)
def branchB_ratio(z):
    return E_of_z(z)

# BRANCH C: constant
def branchC_ratio(z):
    return np.ones_like(np.atleast_1d(z)*1.0)

def dlogv(ratio):
    """BTFR offset in log10 v at fixed M_b."""
    return 0.25*np.log10(ratio)

def dlogMb(ratio):
    return -np.log10(ratio)

zs = np.array([0.5, 1.0, 2.0, 3.0, 4.0])

print("="*78)
print("a0(z)/a0(0) RATIO TABLE  (footing-independent -- ratio cancels a0(0))")
print("="*78)
print(f"{'z':>5} | {'A (decline)':>12} | {'B (rising)':>12} | {'C (const)':>10}")
print("-"*78)
for z in zs:
    rA = branchA_ratio(z)
    rB = branchB_ratio(z)
    rC = 1.0
    print(f"{z:>5.1f} | {rA:>12.4f} | {rB:>12.4f} | {rC:>10.4f}")

# --- z~0.4 bump check for Branch A ---
print()
print("="*78)
print("BRANCH A  z~0.4 BUMP CHECK  (does a0 rise above 1.0 before declining?)")
print("="*78)
zfine = np.linspace(0.0, 1.5, 301)
rAfine = branchA_ratio(zfine)
imax = np.argmax(rAfine)
print(f"peak ratio  = {rAfine[imax]:.4f}  at z = {zfine[imax]:.3f}  "
      f"(= +{100*(rAfine[imax]-1):.1f}% bump)")
for zc in [0.2, 0.3, 0.4, 0.5]:
    print(f"  a0(z={zc:.1f})/a0(0) = {branchA_ratio(zc):.4f}  "
          f"(+{100*(branchA_ratio(zc)-1):.1f}%)")

print()
print("="*78)
print("BTFR OFFSET  dlog10(v) at fixed M_b  [and percent in v]")
print("  sign: <0 => BELOW z=0 BTFR (LOW v);  =0 => ON;  >0 => ABOVE")
print("="*78)
print(f"{'z':>5} | {'A dlogv':>9} {'A %v':>8} | {'B dlogv':>9} {'B %v':>8} | {'C dlogv':>9}")
print("-"*78)
for z in zs:
    dA = dlogv(branchA_ratio(z)); pA = (10**dA - 1)*100
    dB = dlogv(branchB_ratio(z)); pB = (10**dB - 1)*100
    dC = 0.0
    print(f"{z:>5.1f} | {dA:>+9.4f} {pA:>+7.2f}% | {dB:>+9.4f} {pB:>+7.2f}% | {dC:>+9.4f}")

print()
print("="*78)
print("BTFR OFFSET  dlog10(M_b) at fixed v  [mass shift]")
print("="*78)
print(f"{'z':>5} | {'A dlogMb':>9} | {'B dlogMb':>9} | {'C dlogMb':>9}")
print("-"*78)
for z in zs:
    print(f"{z:>5.1f} | {dlogMb(branchA_ratio(z)):>+9.4f} | "
          f"{dlogMb(branchB_ratio(z)):>+9.4f} | {0.0:>+9.4f}")

# --- headline numbers requested: z=1,2,3 Branch A both footings ---
print()
print("="*78)
print("HEADLINE -- BRANCH A predicted BTFR offset at z=1,2,3 (BOTH footings)")
print("  NOTE: the RATIO a0(z)/a0(0) is footing-INDEPENDENT (a0(0) cancels),")
print("  so dlog10(v) is IDENTICAL for both footings. Absolute a0 differs.")
print("="*78)
for z in [1.0, 2.0, 3.0]:
    rA = branchA_ratio(z)
    dA = dlogv(rA); pA = (10**dA - 1)*100
    print(f"  z={z:.0f}:  a0(z)/a0(0)={rA:.4f}  dlog10(v)={dA:+.4f} dex "
          f"({pA:+.2f}% in v)")
    print(f"        canonical a0(z)={a0_canon*rA:.3e},  alt a0(z)={a0_alt*rA:.3e}")

# a0(3)/a0(0) sanity vs prompt's 0.737
print()
print(f"SANITY: Branch A a0(3)/a0(0) = {branchA_ratio(3.0):.4f}  (prompt states 0.737)")

# prove-by-moving-the-number: toggle w to LCDM (w=-1) => ratio must ->1
print()
print("="*78)
print("PROVE-BY-MOVING: set w0=-1, wa=0 (LCDM) => Branch A ratio must be 1.0")
print("="*78)
_w0, _wa = w0, wa
w0, wa = -1.0, 0.0
for z in [1.0, 3.0]:
    print(f"  z={z:.0f}:  a0(z)/a0(0) = {branchA_ratio(z):.6f}  (dlogv={dlogv(branchA_ratio(z)):+.5f})")
w0, wa = _w0, _wa
print("  => branch A DISSOLVES into C when w->-1 (offset is the DE-departure hostage).")
