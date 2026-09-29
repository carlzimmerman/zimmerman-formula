#!/usr/bin/env python3
"""f03_volume_law_ddim.py -- the Verlinde-type volume-law (elastic dark-energy medium) reading, re-derived in D = d+1 spacetime dimensions.

Source of the steps: arXiv:1611.02269 (opened; sections 1.4, 4.1-4.4).  The paper states its scaling relation 'in d spacetime
dimensions' (his d is our D): Sigma_D^2 = a0 Sigma_B/(8 pi G (D-1)) and a_M = (D-3)/((D-2)(D-1)) a0, = a0/6 at D = 4.  This script does not take that
from the paper: it redoes every step symbolically in D and checks that the paper's printed D-dependence follows, then converts to
the record's variables (spatial d, Z = c H/a0_deep).  a0 there is the de Sitter surface gravity c H, which is H in every D (f01 C-kdS).

Steps (each labelled DETERMINED = fixed by Gauss law / horizon thermodynamics / geometry, or PREMISE = one of the paper's heuristic identifications):
  1 volume law:  S_DE(r) = V(r)/V0, V0 = V(L)/S_dS, S_dS = A(L)/4G   [DETERMINED once the volume-law premise is granted]  -> V0 = 4 G L/(D-1),
                 S_DE(r) = (r/L) A(r)/4G in every D.
  2 Newton potential in D dims (f01):  Phi = -8 pi G M/((D-2) Omega r^(D-3)).  [DETERMINED]
  3 removed entropy:  dS_M/dr = Phi dA/dr /(4G) = -2 pi M  (D-independent Bekenstein form).  [DETERMINED given the paper's eq. 4.26 premise]
  4 displacement u = Phi L (PREMISE: horizon shift), V*_M = -u A, V*_M/V_M = (D-1)/(D-2).  [PREMISE]
  5 elastic inclusion identity  int eps^2 dV = N V0 over the exterior  [DETERMINED, D-independent; checked symbolically]
  6 Sigma_D = a0 eps/(8 pi G) [PREMISE: strain <-> apparent density]; Gauss: Sigma = ((D-2)/(D-3)) g/(8 pi G) for both B and D [PREMISE for D].
Result: g_D^2 = a0 g_B (D-3)/((D-2)(D-1)) ;  Z_V(d) = a0/a_M = d(d-1)/(d-2)  (d = D-1 spatial), = 6 at d = 3.
Controls: (i) dropping the (D-1)/(D-2) displacement factor gives a different D-dependence (the wrong-step mutation), (ii) D = 4 reproduces 6,
(iii) d = 2 (D = 3): Newton potential is logarithmic, a_M -> 0 (Z_V -> infinity), (iv) Z_V(d) versus the record's Z_d = 8 sqrt(pi/(d(d-1))) never coincide at an integer d.
Exit 0 = all checks as stated.
"""
import sys
import math
import sympy as sp
from scipy.optimize import brentq

OK = []
def check(name, cond):
    OK.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

r, L, G, M, a0, Om, Dd = sp.symbols('r L G M a0 Omega D', positive=True)   # Dd = spacetime dimension D
N_, r0 = sp.symbols('N r0', positive=True)

A = Om * r**(Dd - 2)
V = Om * r**(Dd - 1) / (Dd - 1)

print("1  volume law")
SdS = A.subs(r, L) / (4 * G)
V0 = sp.simplify(V.subs(r, L) / SdS)
check("1a  V0 = V(L)/S_dS = 4 G L/(D-1)", sp.simplify(V0 - 4 * G * L / (Dd - 1)) == 0)
SDE = V / V0
check("1b  S_DE(r) = (r/L) A(r)/(4G) in every D (volume law overtakes area law exactly at r = L)", sp.simplify(SDE - (r / L) * A / (4 * G)) == 0)

print("\n2-3  potential and removed entropy")
Phi = -8 * sp.pi * G * M / ((Dd - 2) * Om * r**(Dd - 3))
# D-dim Poisson: lap Phi = 8 pi G (D-3) rho/(D-2) with point source ; flux of grad Phi through S^(D-2) = 8 pi G (D-3) M/(D-2)
flux = sp.simplify(sp.diff(Phi, r) * Om * r**(Dd - 2))
check("2   Phi = -8 pi G M/((D-2) Omega r^(D-3)) has flux 8 pi G (D-3) M/(D-2), the D-dim weak-field Gauss law (f01: lap Phi = 8 pi G (d-2) rho/(d-1), d = D-1)",
      sp.simplify(flux - 8 * sp.pi * G * (Dd - 3) * M / (Dd - 2)) == 0)
dSM = sp.simplify(Phi * sp.diff(A, r) / (4 * G))
check("3   dS_M/dr = Phi (dA/dr)/(4G) = -2 pi M, independent of r AND of D (the Bekenstein form S_M = -2 pi M r)", sp.simplify(dSM + 2 * sp.pi * M) == 0)
SM = -2 * sp.pi * M * r
VM = sp.simplify(-SM * V0)
check("3b  V_M = -S_M V0 = 8 pi G M r L/(D-1)", sp.simplify(VM - 8 * sp.pi * G * M * r * L / (Dd - 1)) == 0)

print("\n4  displacement premise u = Phi L")
u = Phi * L
VMstar = sp.simplify(-u * A)
check("4a  V*_M = -u A = 8 pi G M r L/(D-2)", sp.simplify(VMstar - 8 * sp.pi * G * M * r * L / (Dd - 2)) == 0)
check("4b  V*_M/V_M = (D-1)/(D-2)  (paper's eq. 4.37)", sp.simplify(VMstar / VM - (Dd - 1) / (Dd - 2)) == 0)

print("\n5  elastic inclusion")
V0star = V0 * (Dd - 1) / (Dd - 2)
uu = -N_ * V0star / A
eps = sp.simplify(sp.diff(uu, r))
check("5a  eps = u' = N V0/V(r) exactly (the (D-1)/(D-2) is what makes the strain at the inclusion boundary equal 1)", sp.simplify(eps - N_ * V0 / V) == 0)
Vv, V1 = sp.symbols('Vv V1', positive=True)
check("5b0 dV/dr = A(r) (so int eps^2 A dr = int eps^2 dV)", sp.simplify(sp.diff(V, r) - A) == 0)
eps_of_V = N_ * V0 / Vv                                     # eps = N V0/V (5a)
exterior = sp.integrate(eps_of_V**2, (Vv, V1, sp.oo))
check("5b  int eps^2 dV over the exterior of the inclusion = N V0 when V(r0) = N V0, for every D (paper's eq. 4.44)",
      sp.simplify(exterior.subs(V1, N_ * V0) - N_ * V0) == 0)
print("     (mutation: without the (D-1)/(D-2) factor the strain at the boundary is not 1:  eps V/(N V0) =", sp.simplify(sp.diff(-N_ * V0 / A, r) * V / (N_ * V0)), ")")
check("5c  mutation: u = -N V0/A (no displacement factor) gives boundary strain (D-2)/(D-1), which is never 1: the factor (D-1)/(D-2) is what the premise u = Phi L supplies",
      sp.simplify(sp.diff(-N_ * V0 / A, r) * V / (N_ * V0) - (Dd - 2) / (Dd - 1)) == 0)

print("\n6  Tully-Fisher-type relation")
epsq = sp.simplify(sp.diff(VM, r) / A)                    # eps^2 = (1/A) dV_M/dr   (paper eq. 4.47)
SigD2 = sp.simplify((a0 / (8 * sp.pi * G))**2 * epsq)     # Sigma_D = a0 eps/(8 pi G)
SigB = M / A
check("6a  Sigma_D^2 = a0 Sigma_B/(8 pi G (D-1))  with a0 = 1/L  (paper eq. 1.5)", sp.simplify((SigD2 - a0 * SigB / (8 * sp.pi * G * (Dd - 1))).subs(L, 1 / a0)) == 0)
gB = sp.simplify(sp.diff(Phi, r))     # magnitude of the (inward) acceleration
check("6b  Gauss: g_B = 8 pi G (D-3)/(D-2) Sigma_B", sp.simplify(gB - 8 * sp.pi * G * (Dd - 3) / (Dd - 2) * SigB) == 0)
gD2 = sp.simplify(SigD2 * (8 * sp.pi * G * (Dd - 3) / (Dd - 2))**2)
aM_over_a0 = sp.simplify((gD2 / (gB * a0)).subs(L, 1 / a0))
check("6c  g_D^2 = a_M g_B with a_M/a0 = (D-3)/((D-2)(D-1))  (paper eq. 1.7); = 1/6 at D = 4", sp.simplify(aM_over_a0 - (Dd - 3) / ((Dd - 2) * (Dd - 1))) == 0 and aM_over_a0.subs(Dd, 4) == sp.Rational(1, 6))
d = sp.symbols('d', positive=True)
Zv = sp.simplify(1 / aM_over_a0.subs(Dd, d + 1))
check("6d  in spatial d: Z_V(d) = a0/a_M = d(d-1)/(d-2) = 2 dim SO(d)/(d-2); Z_V(3) = 6", sp.simplify(Zv - d * (d - 1) / (d - 2)) == 0 and Zv.subs(d, 3) == 6)

# ------------------------------------------------------------------ comparison with the record's d-dependences
print("\n  comparison (Z = cH/a0_deep;  kappa = Z_f,d/Z with Z_f,d = 4 sqrt(pi/(d(d-1))) the forced kernel):")
def Zf(dd): return 4 * math.sqrt(math.pi / (dd * (dd - 1)))
print(f"    {'d':>3}{'Z_V = d(d-1)/(d-2)':>22}{'record Z_d (kappa=1/2)':>26}{'kappa_V = Zf/Z_V':>20}{'N_V = 1/kappa_V':>18}")
for dd in (3, 4, 5, 6, 7, 8):
    zv = dd * (dd - 1) / (dd - 2)
    zr = 2 * Zf(dd)
    kv = Zf(dd) / zv
    print(f"    {dd:>3}{zv:>22.4f}{zr:>26.4f}{kv:>20.4f}{1 / kv:>18.4f}")
check("6e  at d = 3: Z_V = 6, record Z = 5.7888, kappa_V = 0.4824 (N = 2.073): the volume-law reading is close to, NOT equal to, kappa = 1/2",
      abs(Zf(3) / 6 - 0.48237) < 1e-4 and abs(6 / (2 * Zf(3)) - 1.0365) < 1e-3)
import numpy as np
f = lambda dd: dd * (dd - 1) / (dd - 2) - 8 * math.sqrt(math.pi / (dd * (dd - 1)))
grid = np.linspace(2.05, 30, 6000)
vals = [f(x) for x in grid]
roots = [brentq(f, grid[i], grid[i + 1]) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
print("    Z_V(d) - Z_d(record) changes sign only at d = " + ", ".join(f"{x:.4f}" for x in roots) + f"; minimum {min(vals):.4f} at d = {grid[int(np.argmin(vals))]:.3f}")
check("6f  the two crossings (%s) are non-integer, and Z_V > Z_d at every integer d >= 3 (and d = 2 is singular): no spatial dimension makes the derived volume-law Z equal the record's Z"
      % ", ".join(f"{x:.3f}" for x in roots), len(roots) == 2 and all(abs(x - round(x)) > 0.1 for x in roots) and all(f(k) > 0 for k in range(3, 40)))
check("6g  control d = 2 (D = 3): Newton potential is logarithmic, (D-3) -> 0 kills a_M: Z_V -> infinity", sp.limit(Zv, d, 2, '+') == sp.oo)
# grows with d vs record falls with d
check("6h  for d >= 4 the derived Z_V is non-decreasing (6, 6.67, 7.5, ...) while the record's Z_d = sqrt(32 pi/dim SO(d)) falls: opposite d-dependence",
      all(k * (k - 1) / (k - 2) >= (k - 1) * (k - 2) / (k - 3) - 1e-12 for k in range(5, 20)) and all(2 * Zf(k + 1) < 2 * Zf(k) for k in range(3, 20)))
print(f"\n  {sum(OK)}/{len(OK)} checks held.")
sys.exit(0 if all(OK) else 1)
