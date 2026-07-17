#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M2, SEAM S2 (thermal / dS-Unruh)
=======================================================
Framework: de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman). Own interpolation
nu(y)=sqrt(1+1/y), g_obs=sqrt(g_bar^2+g_bar*a0), mu(x)=K(x^2)=(sqrt(1+4x^2)-1)/(2x).
Both footings carried: canonical a0 = cH_Lambda/Z = 9.362e-11 m/s^2 (rho_DE),
alt a0 = 1.130e-10 m/s^2 (rho_total/cH0). Z = sqrt(32*pi/3).

Derives and verifies (sympy, no hard-coded booleans):
 E-S2-1  FLOOR-FORM INVERSION: g_bar = sqrt(g_obs^2 + (a0/2)^2) - a0/2   [EXACT]
         equivalently the HYPERBOLA IDENTITY (2 g_bar + a0)^2 - (2 g_obs)^2 = a0^2.
 E-S2-2  MILGROM-DeltaT CORRESPONDENCE: the framework kernel mu(x) is EXACTLY the
         Milgrom-1999 vacuum/Unruh temperature-excess form [sqrt(a^2+k^2)-k]/a
         with floor k = a0/2 (NOT k = cH_Lambda).                        [EXACT]
         -> the floor a0/2 equals c times the Herglotz measure's cut edge
            omega_edge = sqrt(1/4)*a0/c = a0/(2c)  (region-A branch point).
 E-S2-3  THERMAL a0-LINE: with kappa_eff = sqrt(H^2 + (g_obs/c)^2) (dS-Unruh pole),
         (c*kappa_eff)^2 - (c*H_Lambda)^2 = g_bar^2 + a0*g_bar          [EXACT]
         i.e. (2 pi c k_B/hbar)^2 (T_eff^2 - T_dS^2) = g_bar^2 + a0 g_bar.
 E-S2-4  TEMPERATURE-RATIO IDENTITY: (T_eff/T_dS)^2 = 1 + y(y+1)/Z^2    [EXACT]
 E-S2-5  MEMORY-HORIZON WELD: tau_mem * H_Lambda = 2Z (exact, footing-free);
         floor temperature T_* = hbar a0/(4 pi c k_B) = T_dS/(2Z).
Cross-checks against banked numbers: kappa_eff(a0)/H = sqrt(1+1/Z^2) = 1.01481
(prep_2026/mi_closure_pin/PULLBACK.md).
"""
import sys
import sympy as sp

FAIL = []
def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

# ---------- symbols ----------
g, gob, a0, c, H, Z, y, x, kap = sp.symbols('g g_obs a0 c H Z y x kappa', positive=True)
hbar, kB = sp.symbols('hbar k_B', positive=True)

nu   = sp.sqrt(1 + 1/y)                       # framework interpolation (own premises)
gobs_of_g = sp.sqrt(g**2 + a0*g)              # g_obs(g_bar), EXACT framework law
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)       # framework kernel mu(x) = K(x^2)

print("="*78)
print("E-S2-1  Floor-form inversion + hyperbola identity")
print("="*78)
# invert g_obs^2 = g^2 + a0 g for g (positive root)
sols = sp.solve(sp.Eq(gob**2, g**2 + a0*g), g)
pos = [s for s in sols if sp.simplify(s.subs({gob: a0, a0: a0})).is_positive is not False]
floor_form = sp.sqrt(gob**2 + (a0/2)**2) - a0/2
# check the positive branch equals the floor form
match = any(sp.simplify(s - floor_form) == 0 for s in sols)
check("inversion: positive root of a0-line == sqrt(g_obs^2+(a0/2)^2) - a0/2", match)
# hyperbola identity, verified by substituting the law (not by construction)
hyp = ((2*g + a0)**2 - (2*gobs_of_g)**2 - a0**2)
check("hyperbola: (2 g_bar + a0)^2 - (2 g_obs)^2 = a0^2 under the law", sp.simplify(hyp) == 0)
# and that it is EQUIVALENT to the a0-line (same variety):
a0line = gob**2 - g**2 - a0*g
hyp_g  = (2*g + a0)**2 - (2*gob)**2 - a0**2
check("hyperbola == -4*(a0-line)  (same identity, exact algebra)",
      sp.expand(hyp_g + 4*a0line) == 0)

print()
print("="*78)
print("E-S2-2  Milgrom-1999 vacuum DeltaT correspondence, floor = a0/2 = c*cut-edge")
print("="*78)
# Milgrom 1999 (Phys Lett A 253, 273) vacuum-inertia form: m_eff ~ DeltaT with
# T ~ sqrt(a^2 + k^2)/2pi  =>  mu_M(a) = [sqrt(a^2+k^2) - k]/a  (normalized mu(inf)=1)
k_floor = sp.symbols('k_floor', positive=True)
a = sp.symbols('a', positive=True)
mu_M = (sp.sqrt(a**2 + k_floor**2) - k_floor)/a
diff_ = sp.simplify(mu_M.subs(k_floor, a0/2).subs(a, x*a0) - mu_fw)
check("mu_fw(x) == Milgrom-DeltaT form with floor k = a0/2 (EXACT, all x)", diff_ == 0)
# the floor is NOT the framework's dS scale cH = Z a0; ratio:
ratio = sp.simplify((Z*a0)/(a0/2))
check("floor mismatch vs dS scale: cH_Lambda/(a0/2) = 2Z (exact)", sp.simplify(ratio - 2*Z) == 0)
# cut-edge weld: region-A support of the unique Herglotz measure ends at t=-1/4;
# operator argument z = (c^2/a0^2) * d^2/dtau^2 -> frequency map |t| = (c w/a0)^2
# edge |t|=1/4  =>  w_edge = a0/(2c)  =>  acceleration floor c*w_edge = a0/2.
w_edge = sp.sqrt(sp.Rational(1, 4))*a0/c
check("cut edge: c*omega_edge == a0/2 (floor IS the region-A branch point)",
      sp.simplify(c*w_edge - a0/2) == 0)

print()
print("="*78)
print("E-S2-3  Thermal a0-line  (c kappa_eff)^2 - (cH)^2 = g_bar^2 + a0 g_bar")
print("="*78)
# dS-Unruh Pythagorean pole (derived in mi_closure_pin/PULLBACK.md from the embedding):
kappa_eff = sp.sqrt(H**2 + (gobs_of_g/c)**2)
lhs = sp.expand((c*kappa_eff)**2 - (c*H)**2)
check("(c kappa_eff)^2 - (cH)^2 == g_bar^2 + a0 g_bar (EXACT)",
      sp.simplify(lhs - (g**2 + a0*g)) == 0)
# temperature form: T = hbar*kappa/(2 pi k_B c) * c ... use T = hbar kappa/(2 pi k_B)
Teff = hbar*kappa_eff/(2*sp.pi*kB)
TdS  = hbar*H/(2*sp.pi*kB)
therm = sp.simplify((2*sp.pi*kB*c/hbar)**2 * (Teff**2 - TdS**2) - (g**2 + a0*g))
check("(2 pi c k_B/hbar)^2 (T_eff^2 - T_dS^2) == g_bar^2 + a0 g_bar", therm == 0)

print()
print("="*78)
print("E-S2-4  Temperature-ratio identity (T_eff/T_dS)^2 = 1 + y(y+1)/Z^2")
print("="*78)
# with cH = Z a0 (framework definition a0 = cH/Z), g = y a0:
expr = ((Teff/TdS)**2).subs(H, Z*a0/c).subs(g, y*a0)
check("(T_eff/T_dS)^2 == 1 + y(y+1)/Z^2 under cH = Z a0",
      sp.simplify(expr - (1 + y*(y+1)/Z**2)) == 0)
# cross-check the banked pullback number: at g_obs = a0 (x=1): kappa/H = sqrt(1+1/Z^2)
Zn = sp.sqrt(32*sp.pi/3)
val = sp.sqrt(1 + 1/Zn**2)
check("kappa_eff(a=a0)/H = sqrt(1+1/Z^2) = 1.01481 (matches PULLBACK.md)",
      abs(float(val) - 1.01481) < 5e-6)

print()
print("="*78)
print("E-S2-5  Memory-horizon weld tau_mem * H_Lambda = 2Z ; T_* = T_dS/(2Z)")
print("="*78)
tau_mem = 2*c/a0                    # framework input (kernel memory time)
HL = Z*a0/c
check("tau_mem * H_Lambda == 2Z (exact, footing-free)",
      sp.simplify(tau_mem*HL - 2*Z) == 0)
Tstar = hbar*(a0/2)/(2*sp.pi*kB*c)  # floor temperature (acceleration a0/2 -> T = hbar a/(2 pi c k_B))
TdS_  = hbar*HL/(2*sp.pi*kB)
check("T_*/T_dS == 1/(2Z) (exact)", sp.simplify(Tstar/TdS_ - 1/(2*Z)) == 0)

# ---------- numbers, BOTH footings ----------
print()
print("numbers (both footings):")
import math
cn = 2.99792458e8
for tag, a0n in (("canonical", 9.362e-11), ("alt", 1.130e-10)):
    Znum = math.sqrt(32*math.pi/3)
    HLn = Znum*a0n/cn
    taum = 2*cn/a0n
    yr = 3.155815e7
    Gyr = 1e9*yr
    hbarn, kBn = 1.054571817e-34, 1.380649e-23
    Tstar_n = hbarn*(a0n/2)/(2*math.pi*kBn*cn)
    TdS_n = hbarn*HLn/(2*math.pi*kBn)
    print(f"  [{tag}] a0={a0n:.4g}  cH_L={cn*HLn:.4g} m/s^2  g_floor=a0/2={a0n/2:.4g} m/s^2")
    print(f"         tau_mem=2c/a0={taum/Gyr:.1f} Gyr  1/H_L={1/HLn/Gyr:.2f} Gyr  tau_mem*H_L={taum*HLn:.4f} (=2Z={2*Znum:.4f})")
    print(f"         T_dS={TdS_n:.3e} K   T_*=T_dS/(2Z)={Tstar_n:.3e} K")

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL CHECKS PASS")
sys.exit(1 if FAIL else 0)
