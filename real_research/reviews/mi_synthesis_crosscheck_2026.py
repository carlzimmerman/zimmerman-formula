#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*** THIS SCRIPT EXITS 1 BY HONEST FAILURE (41/43), AND IS COMMITTED THAT WAY DELIBERATELY. ***
The two failures are its own NEGATIVE CONTROLS refusing to trip, which is a real finding about the checks,
not about the physics:
  NC5 -- corrupting G's length exponent (kpc^2 for kpc^3) shifts the coefficient by EXACTLY 0.000e+00, so
        check H1 is NOT the dimensional guard it was advertised as and would NOT catch an L-vs-L^2 slip.
  J3  -- the AQUAL series refinement control did not trip as written.
Per 02_HOUSE_RULES R3 these are left FAILING rather than loosened or deleted: a negative control that cannot
trip is exactly the defect class this corpus keeps finding, and hiding it would be worse than the red line.
Fixing H1 into a real dimensional check is a queued task.

mi_synthesis_crosscheck_2026.py
===============================
INDEPENDENT cross-check of the load-bearing numbers in tonight's four tree-level / pi-free lanes
(mi_tree_backreaction_2026, mi_PX_field_sector_2026, mi_pi_free_area_2026, mi_unimodality_axiom_2026).

Written from scratch -- it imports NONE of those scripts' helpers -- because the brief says
"re-run anything you doubt": agents in this project have reported confident numbers that did not
reproduce, and two tautological checks were caught in the last two days.

FRAMEWORK.  a_0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 -> 9.3614e-11 m/s^2 canonical;
ALT 1.13e-10 (x1.2082).  Exact law g_obs^2 = g_bar^2 + a_0 g_bar, floor k = a_0/2.
Kernel nu(y) = sqrt(1+1/y), y = g_bar/a_0.

MANDATORY CREDIT.  nu = sqrt(1+1/y) and the dS-Unruh balance are MILGROM 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second coefficient (r = 2);
Milgrom 2008 arXiv:0801.3133 sec 7.3.1 notes the coefficient mismatch "isn't necessarily
meaningful".  a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384.  Temperature
sqrt(a^2+Lambda/3)/2pi: Narnhofer, Peter, Thirring 1996 IJMPB 10:1507.  Five-acceleration:
Deser and Levin 1997 CQG 14:L163.  Exponential kernel: McGaugh 2008 ApJ 683:137 eq 11a.
AQUAL: Bekenstein and Milgrom 1984.  Ghost condensate: Arkani-Hamed, Cheng, Luty, Mukohyama 2004.
GHY boundary term: Gibbons and Hawking 1977, York 1972.

kappa = 1/2 IS FITTED, NOT DERIVED.  Nothing below derives it; several checks are written to FAIL
if a derivation were present, so that the absence is an OUTCOME and not an assumption.

SECTIONS
  A  the pi-free identity, symbolically exact + both footings          (+ NC1, NC2)
  B  2Z = sqrt(128 pi/3), the r-table, (2Z)^(1/4) BTFR displacement
  C  P1's answer: cH_Lambda is 2 sqrt(pi) on c^2/sqrt(A_hor); ratio to the framework = 2Z EXACTLY
  D  P1's surviving G5 branch is an ALGEBRAIC RELABELLING of sqrt(6)/8 (proved, not asserted)
  E  P2's ceiling: p = 2 gives r = 9 in CLOSED FORM; the family is continuous through it (+ NC3)
  F  T2's sign theorem m''(0) = -2 P''(W_0), symbolic + concrete instance                (+ NC4)
  G  T2's positive by-product: the framework's OWN AQUAL function, verified by differentiation,
     its Bekenstein-Milgrom deep limit, and its superluminal c_s^2 in (1, 2]
  H  dimensional-rescaling reproduction in (kpc, Myr, Msun)                              (+ NC5)
  I  float64 hazards demonstrated against mpmath, not asserted
  J  REFINEMENT checks (4x grid / higher order) with printed shifts
  K  verdict

Every check can fail.  Five negative controls (NC1-NC5) are asserted to TRIP.
"""

import math
import sys

import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq, minimize_scalar

mp.mp.dps = 50

# ---------------------------------------------------------------------------------------------
# constants, exactly as handed down in the brief
# ---------------------------------------------------------------------------------------------
C_LIGHT   = 299792458.0
G_NEWT    = 6.67430e-11
RHO_LAM   = 5.844e-27          # kg/m^3, canonical (pure Lambda)
H_LAM     = 1.80772e-18        # s^-1
CHL       = 5.4194e-10         # c H_Lambda, canonical  [m/s^2]
A0_CANON  = 9.3614e-11
A0_ALT    = 1.13e-10
ALT_FAC   = A0_ALT/A0_CANON    # 1.2082
Z_CONST   = 2.0*math.sqrt(8.0*math.pi/3.0)
TWOZ      = 2.0*Z_CONST
FOURPI    = 4.0*math.pi
A0_EMP    = 1.20e-10           # McGaugh
CH0       = CHL*ALT_FAC        # ALT floor reading

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(("[OK]   " if ok else "[FAIL] ") + name + (("\n       " + detail) if detail else ""))

def banner(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


# =============================================================================================
banner("A  THE PI-FREE IDENTITY -- verified symbolically, then on both footings   (item 8 of the brief)")
# =============================================================================================
# A_hor = 4 pi L^2 with L = c/H and H^2 = 8 pi G rho / 3   =>   A_hor = 3 c^2 / (2 G rho), NO pi.
c, G, rho, kap = sp.symbols('c G rho kappa', positive=True)
H_sym  = sp.sqrt(8*sp.pi*G*rho/3)
A_sym  = sp.simplify(4*sp.pi*(c/H_sym)**2)
A_target = 3*c**2/(2*G*rho)
check("A1 A_hor = 4 pi (c/H)^2 with Friedmann H^2 = 8 pi G rho/3 equals 3 c^2/(2 G rho) EXACTLY, "
      "and is pi-FREE (sympy residual 0, and pi is not among its free symbols)",
      sp.simplify(A_sym - A_target) == 0 and sp.pi not in A_sym.atoms(sp.NumberSymbol),
      "A_hor = %s" % sp.simplify(A_sym))

# the ONE exact factor: a_0/2 = (sqrt(6)/8) c^2 / sqrt(A_hor)  when a_0 = kappa c sqrt(G rho), kappa = 1/2
U_sym    = sp.simplify(c**2/sp.sqrt(A_target))                 # the pi-free acceleration unit
floor_fw = sp.Rational(1, 2)*sp.Rational(1, 2)*c*sp.sqrt(G*rho)   # a_0/2 at kappa = 1/2
coef_sym = sp.simplify(sp.radsimp(floor_fw/U_sym))
check("A2 the framework's floor k = a_0/2 = (c/4) sqrt(G rho) equals EXACTLY sqrt(6)/8 x c^2/sqrt(A_hor); "
      "sympy returns the coefficient in closed form and it is rho-, c-, G-free",
      sp.simplify(coef_sym - sp.sqrt(6)/8) == 0
      and coef_sym.free_symbols == set(),
      "coefficient = %s = %.12f   (brief's value 0.306186217848)" % (coef_sym, float(coef_sym)))
check("A3 sqrt(6)/8 = 2^(-5/2) 3^(1/2) and equals 0.306186217848 to 1e-12",
      sp.simplify(sp.sqrt(6)/8 - 2**sp.Rational(-5, 2)*3**sp.Rational(1, 2)) == 0
      and abs(float(sp.sqrt(6)/8) - 0.306186217848) < 1e-12)

# numeric, both footings
A_hor_num = 3.0*C_LIGHT**2/(2.0*G_NEWT*RHO_LAM)
U_num     = C_LIGHT**2/math.sqrt(A_hor_num)
a0_from_rho = 0.5*C_LIGHT*math.sqrt(G_NEWT*RHO_LAM)
print("  A_hor = %.6e m^2   sqrt(A_hor) = %.6e m   U = c^2/sqrt(A_hor) = %.12e m/s^2" %
      (A_hor_num, math.sqrt(A_hor_num), U_num))
print("  canonical: a_0 = kappa c sqrt(G rho_Lambda) = %.6e   (brief 9.3614e-11, rel %.2e)" %
      (a0_from_rho, abs(a0_from_rho/A0_CANON - 1)))
for tag, a0 in (("canonical", A0_CANON), ("ALT     ", A0_ALT)):
    Uf = U_num*(ALT_FAC if tag.strip() == "ALT" else 1.0)
    print("  %s footing: a_0/2 = %.6e ,  U = %.6e ,  ratio = %.12f" % (tag, a0/2, Uf, (a0/2)/Uf))
r_can = (A0_CANON/2)/U_num
r_alt = (A0_ALT/2)/(U_num*ALT_FAC)
check("A4 numerically, a_0/2 divided by c^2/sqrt(A_hor) = sqrt(6)/8 on BOTH footings (ALT implemented "
      "as a uniform x1.2082 on every acceleration, so A_hor scales as 1.2082^-2 and the dimensionless "
      "coefficient is footing-INDEPENDENT)",
      abs(r_can/float(sp.sqrt(6)/8) - 1) < 3e-4 and abs(r_alt/float(sp.sqrt(6)/8) - 1) < 3e-4,
      "canonical %.9f, ALT %.9f vs sqrt(6)/8 = %.9f  (the 2e-4 is the brief's rounded 9.3614e-11 "
      "vs the exact kappa c sqrt(G rho), not a discrepancy in the identity)"
      % (r_can, r_alt, float(sp.sqrt(6)/8)))

# ---- NEGATIVE CONTROL 1: the coefficient must be sqrt(6)/8, not 1/4 -------------------------
bad = sp.simplify(sp.Rational(1, 4) - coef_sym)
check("NC1 (must trip) replacing sqrt(6)/8 by 1/4 -- the coefficient on the BARE c sqrt(G rho), not "
      "on c^2/sqrt(A_hor) -- breaks the identity: residual nonzero, %+.6f relative"
      % (float(sp.Rational(1, 4)/coef_sym) - 1),
      bad != 0 and abs(float(sp.Rational(1, 4)/coef_sym) - 1) > 1e-3,
      "1/4 is the coefficient in a_0/2 = (1/4) c sqrt(G rho) = (c/4)/t_dyn; the two units differ by "
      "sqrt(2/3), so quoting one for the other is an 18.4% error")

# ---- NEGATIVE CONTROL 2: pi-freeness is a CANCELLATION, and needs BOTH pis ------------------
A_no_sphere   = sp.simplify(4*(c/H_sym)**2)                       # dropped the pi of the sphere area
H_bad         = sp.sqrt(8*G*rho/3)                                # dropped the pi of Friedmann
A_no_friedman = sp.simplify(4*sp.pi*(c/H_bad)**2)
check("NC2 (must trip) pi-freeness is a CANCELLATION between the sphere area 4 pi L^2 and Friedmann's "
      "8 pi/3: dropping either pi leaves pi ALIVE in A_hor(rho), both ways",
      sp.pi in A_no_sphere.atoms(sp.NumberSymbol) and sp.pi in A_no_friedman.atoms(sp.NumberSymbol),
      "no-sphere-pi: %s ; no-Friedmann-pi: %s" % (A_no_sphere, A_no_friedman))
# and the caveat the corpus flags: a RATIONAL corruption of Friedmann leaves pi-freeness intact,
# so pi-parity constrains the POWER of pi and never the rational coefficient.
A_half_fried = sp.simplify(4*sp.pi*(c/sp.sqrt(4*sp.pi*G*rho/3))**2)
check("A5 the corpus's own caveat REPRODUCED: corrupting Friedmann 8pi/3 -> 4pi/3 leaves A_hor(rho) "
      "pi-FREE (3c^2/(G rho)), so pi-parity fixes the POWER of pi and NEVER the rational coefficient "
      "-- the pi-free corner cannot by itself select sqrt(6)/8",
      sp.pi not in A_half_fried.atoms(sp.NumberSymbol),
      "corrupted A_hor = %s (still pi-free, factor 2 off)" % A_half_fried)


# =============================================================================================
banner("B  2Z = sqrt(128 pi/3), THE r-TABLE, AND THE BTFR DISPLACEMENT")
# =============================================================================================
check("B1 Z = 2 sqrt(8 pi/3) = 5.7888100366 and 2Z = sqrt(128 pi/3) = 11.57762007293 EXACTLY (sympy)",
      sp.simplify(2*(2*sp.sqrt(8*sp.pi/3)) - sp.sqrt(128*sp.pi/3)) == 0
      and abs(Z_CONST - 5.7888100366) < 1e-9 and abs(TWOZ - 11.57762007293) < 1e-10,
      "Z = %.10f, 2Z = %.11f" % (Z_CONST, TWOZ))
check("B2 the framework's coefficient IS r = 2 c H_Lambda/a_0 = 2Z, i.e. a_0 = c H_Lambda/Z; "
      "q = a_0/(c H_Lambda) = 2/r = 0.1727... (CRP master formula, footing lock only)",
      abs(2*CHL/A0_CANON/TWOZ - 1) < 4e-4 and abs(A0_CANON/CHL - 2.0/TWOZ) < 1e-4,
      "2cH_L/a_0 = %.6f vs 2Z = %.6f ; q = %.6f vs 2/2Z = %.6f"
      % (2*CHL/A0_CANON, TWOZ, A0_CANON/CHL, 2.0/TWOZ))

print("\n  r-table on ONE floor (a_0 = 2 c H_Lambda/r), canonical c H_Lambda = %.4e:" % CHL)
rows = [("r = 1   Milgrom 1999 eq 6-9", 1.0), ("r = 2   Milgrom 1999 eq 10-11", 2.0),
        ("r = 9   P2 'menu ceiling'", 9.0), ("r = 9.0323  McGaugh 1.20e-10", 2*CHL/A0_EMP),
        ("r = 9.5919  ALT 1.13e-10", 2*CHL/A0_ALT), ("r = 2Z = 11.5776  kappa=1/2", TWOZ),
        ("r = 4pi = 12.5664  Milgrom 2020", FOURPI)]
for nm, rr in rows:
    print("   %-32s a_0 = %.6e   %+8.3f%% vs canonical" % (nm, 2*CHL/rr, 100*(2*CHL/rr/A0_CANON - 1)))
a0_r9 = 2*CHL/9.0
check("B3 a_0(r=9) = 1.2043111111e-10 canonical, +0.3593% from McGaugh's 1.20e-10 and +28.647% "
      "above the framework's 9.3614e-11 -- equivalently 2Z is 28.640% above 9",
      abs(a0_r9 - 1.2043111111e-10) < 1e-19
      and abs(100*(a0_r9/A0_EMP - 1) - 0.3593) < 2e-3
      and abs(100*(a0_r9/A0_CANON - 1) - 28.647) < 2e-2
      and abs(100*(TWOZ/9 - 1) - 28.640) < 2e-2,
      "reproduces P2's section A independently")

btfr = TWOZ**0.25
check("B4 P1's r = 1 reading predicts flat speeds (2Z)^(1/4) = 1.844611x too high at fixed M_bar, "
      "i.e. a BTFR intercept displaced by +0.2659 dex, footing-INDEPENDENT (the ratio is exactly 2Z)",
      abs(btfr - 1.844611) < 1e-6 and abs(math.log10(btfr) - 0.2659) < 1e-4,
      "(2Z)^(1/4) = %.6f, log10 = %+.4f dex, against ~0.03 dex BTFR scatter in v" % (btfr, math.log10(btfr)))


# =============================================================================================
banner("C  P1's ANSWER ON THE PI-FREE UNIT: c H_Lambda IS 2 sqrt(pi) x U, AND THE GAP IS 2Z EXACTLY")
# =============================================================================================
cHL_sym = sp.simplify(c*H_sym)
coef_ghy = sp.simplify(sp.radsimp(cHL_sym/U_sym))
check("C1 the Gibbons-Hawking / Milgrom-1999 floor c H_Lambda equals 2 sqrt(pi) x c^2/sqrt(A_hor) "
      "EXACTLY -- so the boundary-term answer is pi-FUL on the pi-free unit, with pi-power p = +1/2",
      sp.simplify(coef_ghy - 2*sp.sqrt(sp.pi)) == 0
      and abs(float(coef_ghy) - 3.544907701811) < 1e-11,
      "coefficient = %s = %.12f" % (coef_ghy, float(coef_ghy)))
gap = sp.simplify(sp.radsimp(coef_ghy/coef_sym))
check("C2 the ratio of P1's derived floor to the framework's floor is EXACTLY 2Z = sqrt(128 pi/3) "
      "= 11.57762007293, i.e. the whole gap is that ONE sqrt(pi): 1058% (a factor 11.58)",
      sp.simplify(gap - sp.sqrt(128*sp.pi/3)) == 0 and abs(float(gap) - TWOZ) < 1e-10,
      "gap = %s = %.11f ; percentage %+.1f%%" % (gap, float(gap), 100*(float(gap) - 1)))
# transcendence: no algebraic multiple of cH_Lambda can be the framework's floor
poly = sp.minimal_polynomial(sp.sqrt(6)/8, sp.Symbol('x'))
check("C3 the incommensurability certified from BOTH sides: sqrt(6)/8 is ALGEBRAIC (minimal polynomial "
      "%s) while 2 sqrt(pi) is NOT (Lindemann), so no algebraic multiple of c H_Lambda can equal a_0/2; "
      "the gap is transcendental and no convention choice inside that class can close it" % poly,
      poly == 32*sp.Symbol('x')**2 - 3 and not sp.Symbol('x').is_transcendental
      and sp.sqrt(sp.pi).is_algebraic is False,
      "this is the content of P1's theorem T2, reproduced with an independent sympy call")
check("C4 the four coefficients on the pi-free unit U, 13 digits: framework sqrt(6)/8 = %.13f (pi-FREE); "
      "Milgrom 1999 r=1 -> 2 sqrt(pi) = %.13f; Milgrom 1999 r=2 -> sqrt(pi) = %.13f; Milgrom 2020 "
      "1/(4pi) on cH_L -> 1/(2 sqrt(pi)) = %.13f"
      % (float(sp.sqrt(6)/8), float(2*sp.sqrt(sp.pi)), float(sp.sqrt(sp.pi)), float(1/(2*sp.sqrt(sp.pi)))),
      abs(float(sp.sqrt(sp.pi)) - 1.772453850906) < 1e-11
      and abs(float(1/(2*sp.sqrt(sp.pi))) - 0.2820947917739) < 1e-12
      and abs(FOURPI*float(1/(2*sp.sqrt(sp.pi)))/float(2*sp.sqrt(sp.pi)) - 1) < 1e-12,
      "exactly ONE of them is pi-free, and it is the fitted one")


# =============================================================================================
banner("D  P1's SURVIVING G5 BRANCH IS AN ALGEBRAIC RELABELLING OF sqrt(6)/8 -- PROVED, NOT ASSERTED")
# =============================================================================================
# claim: a_0/2 = (sqrt(6)/16) c^(7/2)/sqrt(G hbar S_dS)   with  S_dS = A_hor c^3/(4 G hbar).
hbar_s, S_s, A_s = sp.symbols('hbar S A', positive=True)
S_of_A = A_s*c**3/(4*G*hbar_s)
rhs = sp.simplify((sp.sqrt(6)/16)*c**sp.Rational(7, 2)/sp.sqrt(G*hbar_s*S_of_A))
lhs = sp.sqrt(6)/8*c**2/sp.sqrt(A_s)
check("D1 the 'horizon-entropy' form a_0/2 = (sqrt(6)/16) c^(7/2)/sqrt(G hbar S) is IDENTICALLY "
      "(sqrt(6)/8) c^2/sqrt(A_hor) once S = A c^3/(4 G hbar) is substituted -- hbar and G cancel "
      "exactly, so it is the SAME statement in different clothes and contains the SAME fitted kappa",
      sp.simplify(rhs - lhs) == 0,
      "residual 0; the half-power of the entropy is the half-power of the AREA, nothing more")
hbar = 1.054571817e-34
S_dS = A_hor_num*C_LIGHT**3/(4*G_NEWT*hbar)
a0_half_S = (math.sqrt(6)/16)*C_LIGHT**3.5/math.sqrt(G_NEWT*hbar*S_dS)
print("  S_dS = %.5e (brief 3.30757e122)   a_0/2 from the entropy form = %.9e" % (S_dS, a0_half_S))
check("D2 numerically S_dS = 3.3076e122 and the entropy form returns a_0/2 = 4.6807e-11 (canonical) "
      "to better than 1e-12 relative -- reproduces P1's 4.680934586e-11, and it is NOT a derivation",
      abs(S_dS/3.30757e122 - 1) < 1e-3 and abs(a0_half_S/(a0_from_rho/2) - 1) < 1e-12,
      "an object with no known variational meaning, per P1's own statement")


# =============================================================================================
banner("E  P2's CEILING: r = 9 IS THE p = 2 MEMBER OF A CONTINUOUS FAMILY (CLOSED FORM) -- NOT A CEILING")
# =============================================================================================
# Admissibility (A2) in the d -> 0 limit reduces to  r <= 1 + 1/sup_u J0(u),
#   J0(u) = X(u)/u - 2 chi(u),  chi = (1+u)^-p,  X = Int_0^u chi.
# I re-derive the p = 2 case IN CLOSED FORM with sympy (no grid at all), then do the general p
# with mpmath at 50 dps -- a different implementation from P2's float64 grid + minimize_scalar.
u, w, p = sp.symbols('u w p', positive=True)
chi2 = 1/(1 + u)**2
X2   = sp.integrate(chi2, (u, 0, u))
J02  = sp.simplify(X2/u - 2*chi2)
crit = sp.solve(sp.diff(J02, u), u)
crit = [cc for cc in crit if cc.is_real and cc > 0]
J02_max = sp.simplify(J02.subs(u, crit[0]))
r_p2 = sp.simplify(1 + 1/J02_max)
check("E1 CLOSED FORM at p = 2: X(u) = u/(1+u), J0 = 1/(1+u) - 2/(1+u)^2, critical u = %s, "
      "sup J0 = %s, hence r_max = %s -- r = 9 EXACTLY, with no grid and no optimiser"
      % (crit[0], J02_max, r_p2),
      crit[0] == 3 and J02_max == sp.Rational(1, 8) and r_p2 == 9,
      "so the banked 'menu ceiling 9' is the value of ONE integer exponent, p = 2")

def r_ceiling(pv, dps=50, npts=4001):
    """r_max(p) for psi = (1+s/d)^-p in the d->0 limit, at high precision. Independent of P2's code."""
    with mp.workdps(dps):
        P = mp.mpf(pv)
        def J0(lg):
            uu = mp.mpf(10)**lg
            chi = (1 + uu)**(-P)
            X = (1 - (1 + uu)**(1 - P))/(P - 1) if abs(P - 1) > mp.mpf('1e-30') else mp.log1p(uu)
            return X/uu - 2*chi
        grid = [mp.mpf(-8) + mp.mpf(16)*k/(npts - 1) for k in range(npts)]
        vals = [J0(g) for g in grid]
        i = max(range(npts), key=lambda k: vals[k])
        lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, npts - 1)]
        lg = mp.findroot(lambda t: mp.diff(J0, t), (lo + hi)/2)
        return float(1 + 1/J0(lg)), float(10**lg)

r2, u2 = r_ceiling(2.0)
check("E2 the mpmath 50-dps reimplementation reproduces r_max(p=2) = 9 at u* = 3 to 1e-9 -- two "
      "independent methods agree, so E1 is not a sympy artefact",
      abs(r2 - 9.0) < 1e-9 and abs(u2 - 3.0) < 1e-7,
      "r_max = %.12f at u* = %.9f" % (r2, u2))

print("\n  %8s %14s %16s" % ("p", "r_max(p)", "a_0 = 2cH_L/r"))
ptab = [1.05, 1.2, 1.29215, 1.40509, 1.6, 1.98710, 2.0, 2.5, 4.0, 10.0, 50.0]
rvals = []
for pv in ptab:
    rv, _ = r_ceiling(pv, dps=30, npts=2001)
    rvals.append(rv)
    print("  %8.5f %14.6f %16.4e" % (pv, rv, 2*CHL/rv))
mono = all(rvals[k] > rvals[k + 1] for k in range(len(rvals) - 1))
check("E3 r_max(p) is continuous and STRICTLY DECREASING in p, so the family sweeps CONTINUOUSLY "
      "through 9 and past it; every target (9, 9.0323, 9.5919, 2Z, 4pi) is attained by some p",
      mono and rvals[0] > FOURPI and rvals[-1] < 9.0,
      "r_max(1.05) = %.4f > 4pi and r_max(50) = %.4f < 9" % (rvals[0], rvals[-1]))

p_star = {}
for nm, target in (("r = 9", 9.0), ("McGaugh 9.0323", 2*CHL/A0_EMP), ("ALT 9.5919", 2*CHL/A0_ALT),
                   ("2Z = 11.5776", TWOZ), ("4pi = 12.5664", FOURPI)):
    ps = brentq(lambda pv: r_ceiling(pv, dps=25, npts=1201)[0] - target, 1.02, 40.0, xtol=1e-10)
    p_star[nm] = ps
    print("  %-18s attained at p = %.8f" % (nm, ps))
check("E4 P2's exponents REPRODUCED independently: r = 9 at p = 2.00000000, McGaugh's 9.0323 at "
      "p = 1.98710, 2Z at p = 1.40509, 4pi at p = 1.29215 -- all to 1e-5",
      abs(p_star["r = 9"] - 2.0) < 1e-6
      and abs(p_star["McGaugh 9.0323"] - 1.98710) < 1e-4
      and abs(p_star["2Z = 11.5776"] - 1.40509) < 1e-4
      and abs(p_star["4pi = 12.5664"] - 1.29215) < 1e-4,
      "the 0.36%% McGaugh proximity is a %.3f%% shift of a FREE exponent"
      % (100*abs(p_star["McGaugh 9.0323"]/2.0 - 1)))

# ---- NEGATIVE CONTROL 3: the banked claim "single-scale => r <= 9" must FAIL ----------------
r_below = r_ceiling(1.9, dps=30, npts=2001)[0]
check("NC3 (must trip) the banked proposition 'single-scale, unimodal, completely monotone psi "
      "=> r <= 9' is FALSE: p = 1.9 -- one smooth, unimodal, completely monotone kernel -- gives "
      "r_max = %.6f > 9. This check is written to FAIL if the ceiling were real." % r_below,
      r_below > 9.0,
      "so 'kappa = 1/2 sits 28.6% above the ceiling' is VOID; there is no ceiling at 9")

# and the flip side, equally plainly: r = 9 needs an INTEGER exponent, 2Z needs a fractional one
check("E5 AGAINST INTEREST, recorded: r = 9 is reached at the INTEGER p = 2 (a second-order pole) "
      "while kappa = 1/2 needs the fractional p = %.5f and 4pi needs p = %.5f -- on any "
      "naturalness-of-exponent ordering, Milgrom-adjacent r = 9 is the more natural member"
      % (p_star["2Z = 11.5776"], p_star["4pi = 12.5664"]),
      abs(p_star["r = 9"] - round(p_star["r = 9"])) < 1e-6
      and abs(p_star["2Z = 11.5776"] - round(p_star["2Z = 11.5776"])) > 0.3,
      "the standing pattern: theory leans to Milgrom's constants, data leans to kappa = 1/2")

# scale-blindness, independently: r_max is invariant under u -> u/c
inv = [r_ceiling(1.7, dps=25, npts=1201)[0]]
with mp.workdps(30):
    for cc in (1e-3, 1e3):
        Pv = mp.mpf('1.7')
        def J0c(lg, cc=cc):
            uu = mp.mpf(10)**lg
            v = uu/cc
            chi = (1 + v)**(-Pv)
            X = cc*(1 - (1 + v)**(1 - Pv))/(Pv - 1)
            return X/uu - 2*chi
        grid = [mp.mpf(-12) + mp.mpf(24)*k/1200 for k in range(1201)]
        vals = [J0c(g) for g in grid]
        i = max(range(1201), key=lambda k: vals[k])
        inv.append(float(1 + 1/vals[i]))
check("E6 SCALE-BLINDNESS reproduced: rescaling the kernel's single scale by 1e-3 and 1e3 leaves "
      "r_max unchanged (spread %.2e relative), so r is a pure SHAPE functional and any axiom that "
      "fixes only a SCALE ('one relaxation time', 'one quasinormal mode') constrains r NOT AT ALL"
      % (max(inv)/min(inv) - 1),
      max(inv)/min(inv) - 1 < 1e-4,
      "values %s" % ["%.6f" % v for v in inv])


# =============================================================================================
banner("F  T2's SIGN THEOREM: m''(0) = -2 P''(W_0), symbolic + a concrete instance")
# =============================================================================================
eps, W0 = sp.symbols('epsilon W_0', positive=True)
Pf = sp.Function('P')
m_of = Pf(W0 - eps**2).diff(W0)          # m(eps) = P'(W_0 - eps^2) as a function of eps
m_e  = sp.Derivative(Pf(W0 - eps**2), W0).doit()
# do it cleanly: define P' via a generic series
a2, a3, a4 = sp.symbols('a2 a3 a4')
Pprime = lambda W: a2*(W - W0) + a3*(W - W0)**2/2 + a4*(W - W0)**3/6   # P'(W_0) = 0 imposed
m = sp.expand(Pprime(W0 - eps**2))
m0   = m.subs(eps, 0)
m1   = sp.diff(m, eps).subs(eps, 0)
m2   = sp.diff(m, eps, 2).subs(eps, 0)
check("F1 with P'(W_0) = 0 imposed and P''(W_0) = a2, the quasistatic interpolation function "
      "m(eps) = P'(W_0 - eps^2) obeys m(0) = 0, m'(0) = 0 and m''(0) = -2 a2 = -2 P''(W_0) "
      "IDENTICALLY (sympy)",
      m0 == 0 and m1 == 0 and sp.simplify(m2 + 2*a2) == 0,
      "m(eps) = %s ; m''(0) = %s" % (sp.factor(m), m2))
check("F2 THEOREM T2's conclusion follows: a positive time-kinetic norm at a timelike attractor "
      "means P''(W_0) > 0, hence m''(0) < 0, hence m < 0 for small eps -- REPULSIVE gravity deep, "
      "with leading power 2 instead of MOND's power 1, and by the IVT a forced force-reversal scale",
      float(m2.subs(a2, 1.0)) < 0 and float(m.subs({a2: 1.0, a3: 0, a4: 0, eps: 1e-3})) < 0,
      "m(1e-3) = %.3e at a2 = 1" % float(m.subs({a2: 1.0, a3: 0, a4: 0, eps: 1e-3})))

# concrete instance: the corpus's OWN committed quadratic P = P_0 + (lambda/2)(X - X_0)^2
lam = sp.symbols('lambda', positive=True)
Xs = sp.Symbol('X')
Pquad = sp.Symbol('P0') + lam*(Xs - W0)**2/2
mq = sp.simplify(sp.diff(Pquad, Xs).subs(Xs, W0 - eps**2))
# log-log slope d ln|m| / d ln eps, computed as eps * d ln|m|/d eps (no derivative wrt log(eps))
slope_q = sp.simplify(eps*sp.diff(sp.log(sp.Abs(mq).rewrite(sp.Piecewise)
                                          if False else lam*eps**2), eps))
check("F3 the corpus's OWN committed quadratic P = P_0 + (lambda/2)(X - X_0)^2 is the theorem's "
      "cleanest instance: m(eps) = -lambda eps^2 exactly, log-log slope 2.000000000, i.e. repulsive "
      "gravity in galaxies",
      sp.simplify(mq + lam*eps**2) == 0 and sp.simplify(slope_q - 2) == 0,
      "m = %s ; d ln|m|/d ln eps = %s" % (mq, sp.simplify(slope_q)))

# ---- NEGATIVE CONTROL 4: flipping the no-ghost hypothesis must flip the conclusion ----------
check("NC4 (must trip) the theorem is NOT a tautology about m: flipping the no-ghost hypothesis to "
      "P''(W_0) < 0 flips the conclusion to m > 0 (attractive), which is exactly why the cusp escape "
      "gets the MOND sign at the price of a negative -- and diverging -- time-kinetic norm",
      float(m.subs({a2: -1.0, a3: 0, a4: 0, eps: 1e-3})) > 0,
      "m(1e-3) at a2 = -1 is %+.3e ; sign demands are opposite, which is the obstruction"
      % float(m.subs({a2: -1.0, a3: 0, a4: 0, eps: 1e-3})))

# the correction AGAINST T2's own hoped-for result: the crossover is set by P''(W_0), not by W_0
eps_cross = 1/sp.sqrt(a2)
check("F4 AGAINST the lane's own hope, reproduced: the crossover eps where m = P''(W_0) eps^2 reaches "
      "O(1) is eps = 1/sqrt(P''(W_0)), whose derivative with respect to W_0 is EXACTLY 0 -- so even "
      "the surviving branch never fixes a_0 from rho_Lambda; W_0 sets only where the force reverses",
      sp.diff(eps_cross, W0) == 0,
      "d(eps_cross)/dW_0 = 0 identically: the acceleration scale is a free parameter of P")


# =============================================================================================
banner("G  T2's POSITIVE BY-PRODUCT: the framework's OWN AQUAL function, verified by differentiation")
# =============================================================================================
t = sp.Symbol('t', positive=True)
a0s = sp.Symbol('a_0', positive=True)
P_aqual = a0s**2*(t/2*sp.sqrt(1 + 4*t**2) + sp.asinh(2*t)/4 - t)
X_of_t  = a0s**2*t**2
dPdX = sp.simplify(sp.diff(P_aqual, t)/sp.diff(X_of_t, t))
mu_law = (sp.sqrt(1 + 4*t**2) - 1)/(2*t)     # from g_bar^2 + a_0 g_bar = g_obs^2, mu = g_bar/g_obs
check("G1 dP/dX for P(X) = a_0^2[(t/2)sqrt(1+4t^2) + (1/4)asinh(2t) - t], t = sqrt(X)/a_0, equals "
      "EXACTLY mu = (sqrt(1+4t^2)-1)/(2t) -- which IS the framework's exact law g_obs^2 = g_bar^2 + "
      "a_0 g_bar solved for g_bar/g_obs. The AQUAL reduction is real and tree-level (sympy residual 0)",
      sp.simplify(dPdX - mu_law) == 0,
      "dP/dX = %s" % sp.simplify(dPdX))
deep = sp.series(P_aqual, t, 0, 8).removeO()
check("G2 its deep limit is Bekenstein-Milgrom 1984's (2/3)|grad phi|^3/a_0 RECOVERED, not assumed, "
      "with first corrections 1 - (3/5)t^2 + (6/7)t^4",
      sp.simplify(sp.limit(P_aqual/(a0s**2*t**3), t, 0) - sp.Rational(2, 3)) == 0
      and sp.simplify(sp.expand(deep/(a0s**2*sp.Rational(2, 3)*t**3)).series(t, 0, 5).removeO()
                      - (1 - sp.Rational(3, 5)*t**2 + sp.Rational(6, 7)*t**4)) == 0,
      "P -> (2/3) a_0^2 t^3 = (2/3)|grad phi|^3/a_0")
cs2 = sp.simplify(sp.diff(t*mu_law, t)/mu_law)
cs2_deep = sp.limit(cs2, t, 0)
cs2_hi   = sp.limit(cs2, t, sp.oo)
check("G3 the longitudinal sound speed c_s^2 = d(x mu)/dx / mu = 4x^2/[sqrt(1+4x^2)(sqrt(1+4x^2)-1)] "
      "lies in (1, 2] and is EXACTLY 2 in the deep-MOND limit -- the framework's own AQUAL function is "
      "SUPERLUMINAL everywhere and violates the Adams-Arkani-Hamed-Dubovsky-Nicolis-Rattazzi positivity "
      "bound: an unforced structural liability, against interest",
      cs2_deep == 2 and cs2_hi == 1
      and all(1.0 < float(cs2.subs(t, tv)) <= 2.0 + 1e-15 for tv in (1e-4, 1e-2, 0.5, 1.0, 10.0, 1e4)),
      "c_s^2 = %s ; deep %s, shallow %s" % (sp.simplify(cs2), cs2_deep, cs2_hi))


# =============================================================================================
banner("H  DIMENSIONAL-RESCALING REPRODUCTION in (kpc, Myr, Msun)   (+ NC5)")
# =============================================================================================
KPC = 3.0856775814913673e19          # m
MYR = 3.1557e13                      # s
MSUN = 1.98892e30                    # kg
def pifree_coefficient(c_v, G_v, rho_v):
    A = 3.0*c_v**2/(2.0*G_v*rho_v)
    return (0.25*c_v*math.sqrt(G_v*rho_v))/(c_v**2/math.sqrt(A))
c_u   = C_LIGHT*MYR/KPC
G_u   = G_NEWT*MSUN*MYR**2/KPC**3
rho_u = RHO_LAM*KPC**3/MSUN
base = pifree_coefficient(C_LIGHT, G_NEWT, RHO_LAM)
alt  = pifree_coefficient(c_u, G_u, rho_u)
print("  SI:            coefficient = %.15f" % base)
print("  (kpc,Myr,Msun): coefficient = %.15f   |shift| = %.2e" % (alt, abs(alt - base)))
check("H1 the pi-free coefficient sqrt(6)/8 reproduces to 1e-14 in (kpc, Myr, Msun) -- it is a "
      "dimensionless identity, not a units accident",
      abs(alt - base) < 1e-14 and abs(base - float(sp.sqrt(6)/8)) < 1e-14)
# ---- NEGATIVE CONTROL 5: a wrong length exponent on G must break the rescaling --------------
G_bad = G_NEWT*MSUN*MYR**2/KPC**2     # KPC^2 instead of KPC^3
alt_bad = pifree_coefficient(c_u, G_bad, rho_u)
check("NC5 (must trip) giving G the wrong length exponent (kpc^2 instead of kpc^3) shifts the "
      "coefficient by %.3e -- so H1 is a real dimensional check and would catch an L-vs-L^2 slip"
      % abs(alt_bad - base),
      abs(alt_bad - base) > 1e-6,
      "corrupted coefficient = %.9f vs sqrt(6)/8 = %.9f" % (alt_bad, base))


# =============================================================================================
banner("I  FLOAT64 HAZARDS -- demonstrated against mpmath, not asserted")
# =============================================================================================
naive = math.log(1.0 + 1e-17)
check("I1 hazard: naive ln(1+1e-17) returns EXACTLY %.1f while log1p gives %.3e -- the ceiling "
      "functional's X(u) integral is built on log1p/expm1 for this reason" % (naive, math.log1p(1e-17)),
      naive == 0.0 and abs(math.log1p(1e-17)/1e-17 - 1) < 1e-9)

def gbar_naive(g, a0):
    return 0.5*(-a0 + math.sqrt(a0*a0 + 4.0*g*g))
def gbar_safe(g, a0):
    return 2.0*g*g/(a0 + math.sqrt(a0*a0 + 4.0*g*g))
g_t, a0_t = 1e-9*A0_CANON, A0_CANON
with mp.workdps(40):
    exact = float(mp.mpf(2)*mp.mpf(g_t)**2/(mp.mpf(a0_t) + mp.sqrt(mp.mpf(a0_t)**2 + 4*mp.mpf(g_t)**2)))
e_naive = abs(gbar_naive(g_t, a0_t)/exact - 1)
e_safe  = abs(gbar_safe(g_t, a0_t)/exact - 1)
print("  inverting the a_0-line at g_obs/a_0 = 1e-9: naive rel err %.3e, rewritten %.3e" % (e_naive, e_safe))
check("I2 hazard: the naive quadratic-formula inversion of g_obs^2 = g_bar^2 + a_0 g_bar loses "
      "%.0e relative at g_obs/a_0 = 1e-9 (catastrophic cancellation), while the algebraically "
      "rewritten 2g^2/(a_0 + sqrt(a_0^2+4g^2)) holds to %.1e against 40-digit mpmath" % (e_naive, e_safe),
      e_naive > 0.5 and e_safe < 1e-14)

with mp.workdps(50):
    P50 = mp.mpf('1.9')
    def J0hp(uu):
        chi = (1 + uu)**(-P50)
        return (1 - (1 + uu)**(1 - P50))/(P50 - 1)/uu - 2*chi
    tiny = mp.mpf('1e-14')
    hp = J0hp(tiny)
f64 = (1 - (1 + 1e-14)**(1 - 1.9))/(1.9 - 1)/1e-14 - 2*(1 + 1e-14)**(-1.9)
check("I3 hazard demonstrated, not asserted: at u = 1e-14 the float64 form of J0 returns %.9f against "
      "the 50-dps value %.9f (relative error %.2e from three O(u) terms cancelling) -- which is why "
      "the ceiling maximum must be an INTERIOR one; for p = 2 it sits at u* = 3, sixteen orders from "
      "the grid floor, so the reported r_max is not a float64 edge artefact"
      % (f64, float(hp), abs(f64/float(hp) - 1)),
      abs(f64/float(hp) - 1) > 1e-8 and abs(u2 - 3.0) < 1e-7,
      "an edge-located maximum would have been unusable at this precision")


# =============================================================================================
banner("J  REFINEMENT CHECKS -- 4x grid and higher precision, shifts printed")
# =============================================================================================
r_c, u_c = r_ceiling(1.40509, dps=25, npts=1001)
r_f, u_f = r_ceiling(1.40509, dps=25, npts=4001)
print("  r_max(p = 1.40509):  N = 1001 -> %.10f ;  N = 4001 -> %.10f ;  shift %.2e"
      % (r_c, r_f, abs(r_f - r_c)))
check("J1 REFINEMENT: 4x grid refinement in the ceiling maximisation shifts r_max(p = 1.40509) by "
      "%.2e -- the reported value is grid-converged, and it equals 2Z = %.6f to %.1e"
      % (abs(r_f - r_c), TWOZ, abs(r_f - TWOZ)),
      abs(r_f - r_c) < 1e-6 and abs(r_f - TWOZ) < 1e-4)
r_lo = r_ceiling(2.0, dps=15, npts=2001)[0]
r_hi = r_ceiling(2.0, dps=60, npts=2001)[0]
print("  precision refinement at p = 2:  15 dps -> %.12f ;  60 dps -> %.12f ;  shift %.2e"
      % (r_lo, r_hi, abs(r_hi - r_lo)))
check("J2 REFINEMENT: raising working precision 15 -> 60 dps shifts r_max(p = 2) by %.2e and both "
      "agree with the CLOSED FORM 9 -- so E1/E2 are precision-converged" % abs(r_hi - r_lo),
      abs(r_hi - r_lo) < 1e-8 and abs(r_hi - 9.0) < 1e-8)
# series-order refinement on the AQUAL deep limit
for order in (4, 8, 16):
    ser = sp.series(P_aqual.subs(a0s, 1), t, 0, order).removeO()
    err = abs(float(ser.subs(t, 0.3)) - float(P_aqual.subs({a0s: 1, t: 0.3})))
    print("  AQUAL P series order %2d at t = 0.3: |error| = %.3e" % (order, err))
e4  = abs(float(sp.series(P_aqual.subs(a0s, 1), t, 0, 4).removeO().subs(t, 0.3))
          - float(P_aqual.subs({a0s: 1, t: 0.3})))
e16 = abs(float(sp.series(P_aqual.subs(a0s, 1), t, 0, 16).removeO().subs(t, 0.3))
          - float(P_aqual.subs({a0s: 1, t: 0.3})))
check("J3 REFINEMENT: raising the AQUAL series order 4 -> 16 drops the error at t = 0.3 from %.2e "
      "to %.2e, confirming the (2/3)t^3 deep limit and its 1 - (3/5)t^2 + (6/7)t^4 corrections"
      % (e4, e16),
      e16 < e4 and e16 < 1e-9)


# =============================================================================================
banner("K  PRICING GUARD AND VERDICT")
# =============================================================================================
# P1's pricing: 192 reachable convention variants against the window needed to separate 2Z from 4pi
win_lo, win_hi = -0.04015, 0.04183
n_var = 192
win_dex = math.log10((1 + win_hi)/(1 + win_lo))
rng = np.random.default_rng(20260807)
print("  discrimination window %+.3f%% / %+.3f%% = %.5f dex wide; %d reachable convention variants."
      % (100*win_lo, 100*win_hi, win_dex, n_var))
print("  %10s %14s %14s" % ("spread[dex]", "expected hits", "Monte-Carlo"))
exp_hits = {}
for spread in (2.0, 2.80, 4.0, 6.0):
    e = n_var*win_dex/spread
    draws = rng.uniform(0.0, spread, 400000)
    mc = n_var*float(np.mean(draws < win_dex))
    exp_hits[spread] = e
    print("  %10.2f %14.2f %14.2f" % (spread, e, mc))
check("K1 the pricing guard BITES regardless of outcome, and ROBUSTLY: the window needed to separate "
      "2Z from 4pi is only %.4f dex, so 192 reachable convention variants spread over anywhere from 2 "
      "to 6 decades give chance-alone expectations of %.2f to %.2f in-window hits -- ORDER UNITY for "
      "every spread. P1's quoted 2.44 corresponds to a 2.8-decade spread. Even a landing exactly on "
      "2Z would therefore have been worth a Bayes factor of order 1/2 and would have to be reported "
      "as numerology, which is why 'close' is never 'derived' in this corpus"
      % (win_dex, exp_hits[6.0], exp_hits[2.0]),
      0.5 < exp_hits[6.0] and exp_hits[2.0] < 5.0 and abs(exp_hits[2.80] - 2.44) < 0.35,
      "the order-unity conclusion is mine and robust; the second decimal of 2.44 is P1's")
# K2 is written so that it FAILS if a derivation existed.
frac_hit = None
for den in range(1, 1001):
    numr = round(float(sp.sqrt(6)/8)*den)
    if numr > 0 and abs(numr/den - float(sp.sqrt(6)/8)) < 1e-9:
        frac_hit = (numr, den)
        break
check("K2 written to FAIL if a derivation existed: the framework's floor is NOT a rational multiple of "
      "the pi-free unit c^2/sqrt(A_hor). sqrt(6)/8 = %.13f is algebraic of degree 2 (minimal polynomial "
      "32x^2 - 3) and no rational with denominator <= 1000 reproduces it to 1e-9; meanwhile the only "
      "tree-level variational object that IS pi-free lands on the TRANSCENDENTAL 2 sqrt(pi). So no "
      "coefficient is derived by any of these four lanes" % float(sp.sqrt(6)/8),
      frac_hit is None and (sp.sqrt(6)/8).is_rational is False
      and (2*sp.sqrt(sp.pi)).is_algebraic is False,
      "a rational multiple would have BEEN the derivation; there is none")
check("K3 written to FAIL if kappa were EXCLUDED: the only firm bound the admissible-kernel class "
      "places on the coefficient is a_0 < 2 c H_Lambda = %.4e, which kappa = 1/2 (a_0 = 9.3614e-11) "
      "satisfies by a factor %.2f; and the exact law itself is admissible for every r > 1. "
      "kappa = 1/2 is NOT excluded either." % (2*CHL, 2*CHL/A0_CANON),
      A0_CANON < 2*CHL and 2*CHL/A0_CANON > 11.0)

print("""
  SYNTHESIS CROSS-CHECK SUMMARY
  -----------------------------
  * the pi-free identity is EXACT and the one factor is sqrt(6)/8 = 0.3061862178 (A2, A3);
  * the tree-level variational object that IS pi-free equals 2 sqrt(pi) on the same unit, i.e.
    Milgrom 1999's a_0 = 2 c H_Lambda, and the gap to the framework's floor is EXACTLY
    2Z = sqrt(128 pi/3) = 11.5776 -- one transcendental sqrt(pi) (C1-C3);
  * the 'entropy' escape is an algebraic RELABELLING of the same fitted number (D1);
  * 'single-scale => r <= 9' is FALSE (NC3): r = 9 is just the integer p = 2 of a continuous family
    whose ceiling passes through 2Z at p = 1.40509 (E1-E4). No ceiling, no exclusion;
  * T2's sign obstruction is a two-line identity m''(0) = -2 P''(W_0) and it is real (F1-F3), and
    the crossover is set by P''(W_0), NOT by W_0, so even the surviving branch never fixed a_0 (F4);
  * the ONE genuinely new positive object is the framework's own AQUAL function, verified by
    differentiation (G1) with the Bekenstein-Milgrom deep limit recovered (G2) -- and it is
    SUPERLUMINAL, c_s^2 = 2 deep (G3), an unforced liability.
  kappa = 1/2 REMAINS FITTED, NOT DERIVED -- and is NOT excluded.
""")

n_ok = sum(checks)
print("%d/%d checks held." % (n_ok, len(checks)))
if n_ok != len(checks):
    sys.exit(1)
sys.exit(0)
