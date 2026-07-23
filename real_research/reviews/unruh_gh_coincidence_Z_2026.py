#!/usr/bin/env python3
"""
UNRUH / GIBBONS-HAWKING HORIZON-COINCIDENCE ACCOUNTING OF Z  (2026-07-23)
========================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA.  a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3) = 5.78881...,  equivalently a0 = (c/2) sqrt(G rho_DE).

ROLE OF THIS SCRIPT (thermodynamic angle, reasoned from the mechanism's OWN premises):
set a0 where the Unruh temperature of the Rindler horizon meets the de Sitter
Gibbons-Hawking temperature, derive the FORM a0 ~ c H_Lambda (FORCED), locate EXACTLY
where Z enters, and ask whether the Unruh/GH thermodynamics FIXES the coefficient or
leaves the normalization (kappa = 1/2) FREE.  Every factor is checked with sympy; the
assertions are written to FAIL if any factor is mis-stated ("prove by moving the number").

PRIOR WALL (tested here, not relitigated): kappa = 1/2 is provably unforceable by
ghost-freedom+unitarity+holography; the SPARC/RAR is non-diagnostic; the period-ring and
CKN-dof doors are shut.  This script asks the ONE thermodynamic question left: does the
Unruh<->GH horizon-coincidence / horizon-AREA-dof weighting force Z where the bulk EFT
arguments could not?

HONESTY: a0's value, Z, and the sign are POSITED, not derived; nu(y)=sqrt(1+1/y) is
Milgrom-1999's kernel (the framework's distinctive content is the cH_Lambda/Z coefficient
+ the modified-inertia completion).  This re-derives the wall with a SHARPER thermodynamic
reason.  It is NOT a Z derivation, NOT 'theory closed', NOT a TOE claim.  Exit 0 = ran.
"""
import sympy as sp

FAIL = []
def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)

# exact symbols (positive reals)
c, G, H, rho, hbar, kB, a, pi = sp.symbols('c G H rho hbar kB a pi', positive=True)
PI = sp.pi
Zf = float(sp.sqrt(sp.Rational(32, 3) * PI))

print("=" * 82)
print("UNRUH/GH HORIZON-COINCIDENCE ACCOUNTING OF Z = sqrt(32 pi/3) = %.5f" % Zf)
print("=" * 82)

# ---------------------------------------------------------------------------
# PART 1 -- the naive horizon-coincidence: T_Unruh(a0) = T_GH  ->  a0 = cH, Z=1
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 1  Unruh temp of the Rindler horizon = Gibbons-Hawking temp  ->  a0 = cH  (Z=1)")
print("-" * 82)
# Unruh:  kB T_U = hbar a /(2 pi c)     (proper accel a, Rindler horizon at c^2/a)
# GH   :  kB T_GH = hbar H /(2 pi)      (de Sitter horizon at R_dS = c/H)
T_U  = hbar * a / (2 * PI * c * kB)
T_GH = hbar * H / (2 * PI * kB)
a0_naive = sp.solve(sp.Eq(T_U, T_GH), a)[0]
print(f"  T_U(a)  = hbar a /(2 pi c kB) ;  T_GH = hbar H /(2 pi kB)")
print(f"  T_U(a0) = T_GH  =>  a0 = {a0_naive}   =>  Z = cH/a0 = {sp.simplify(c*H/a0_naive)}")
check("temperature coincidence T_U(a0)=T_GH forces a0 = cH exactly (the FORM a0 ~ cH_Lambda)",
      sp.simplify(a0_naive - c * H) == 0)
check("=> the NAIVE Unruh/GH coincidence gives Z = 1 (NOT sqrt(32pi/3))",
      sp.simplify(c * H / a0_naive - 1) == 0)
print("  RESULT: the horizon-coincidence FORCES the FORM (a0 proportional to c H_Lambda) but")
print("  the pure TEMPERATURE match gives Z=1.  The 8pi/3 and the 2 are absent -- T_GH is a")
print("  SURFACE quantity (T_GH ~ H directly); no Friedmann coupling and no 1/2 appear.")

# ---------------------------------------------------------------------------
# PART 2 -- the framework value needs the DENSITY reading; where 8pi/3 and 2 enter
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 2  The framework a0 = (c/2)sqrt(G rho_DE):  Z = 2 sqrt(8pi/3).  Factor autopsy.")
print("-" * 82)
# de Sitter Friedmann: H^2 = (8 pi G/3) rho_DE  ->  cH = c sqrt(8pi/3) sqrt(G rho)
friedmann = sp.Eq(H**2, sp.Rational(8, 3) * PI * G * rho)
H_of_rho = sp.sqrt(sp.Rational(8, 3) * PI * G * rho)          # positive root
a0_frame = (c / 2) * sp.sqrt(G * rho)                          # the POSITED density/collapse a0
Z_frame  = sp.simplify(c * H_of_rho / a0_frame)               # cH / a0
print(f"  Friedmann (de Sitter): H = sqrt(8pi/3) sqrt(G rho)  ->  cH = c sqrt(8pi/3) sqrt(G rho)")
print(f"  framework a0 = (c/2) sqrt(G rho)  (density / collapse reading, NOT a temperature)")
print(f"  Z = cH/a0 = {Z_frame} = {float(Z_frame):.5f}")
check("Z = cH/a0 = 2 sqrt(8pi/3) exactly", sp.simplify(Z_frame - 2 * sp.sqrt(sp.Rational(8, 3) * PI)) == 0)
check("Z^2 = 32 pi/3 = 4 * (8pi/3) exactly",
      sp.simplify(Z_frame**2 - sp.Rational(32, 3) * PI) == 0 and
      sp.simplify(Z_frame**2 - 4 * sp.Rational(8, 3) * PI) == 0)
# the a0/(cH) ratio, decomposed
ratio = sp.simplify(a0_frame / (c * H_of_rho))                # = 1/Z
print(f"\n  a0/(cH) = 1/Z = {ratio} = (1/2) * sqrt(3/(8pi))")
check("a0/(cH) = (1/2) sqrt(3/(8pi))  (the '2' sits OUTSIDE the Friedmann sqrt)",
      sp.simplify(ratio - sp.Rational(1, 2) * sp.sqrt(3 / (8 * PI))) == 0)
print("  DECOMPOSITION of Z = 2 * sqrt(8pi/3):")
print("    * sqrt(8pi/3)  = the Friedmann/Einstein conversion H <-> sqrt(G rho).  It appears")
print("      ONLY because a0 is read off the vacuum-energy DENSITY (a VOLUME quantity), not")
print("      off T_GH (a SURFACE quantity).  '8pi'=Einstein coupling, '3'=Friedmann 3.")
print("    * the outer 2  = the (c/2) surface-gravity / Schwarzschild prefactor  (kappa=1/2).")
print("  => the ENTIRE gap between the thermodynamic Z=1 (Part 1) and Z=5.79 is: (a) swap the")
print("     SURFACE temperature reading for the VOLUME density reading [buys sqrt(8pi/3)], then")
print("     (b) impose the Schwarzschild 1/2 [buys the 2].  Neither step is a temperature match.")

# ---------------------------------------------------------------------------
# PART 3 -- does horizon-AREA / dof weighting FORCE Z?  (the task's proposed lever)
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 3  Horizon-AREA / holographic-dof weighting: does it force Z? (bare area-law test)")
print("-" * 82)
# bare area-law equipartition:  M c^2 = (1/2) N kB T,  N = A/l_P^2 = 4 pi r^2 c^3/(hbar G),
# T = hbar a/(2 pi c kB).  Solve for a.
M, r = sp.symbols('M r', positive=True)
lP2 = hbar * G / c**3
N = 4 * PI * r**2 / lP2
a_area = sp.solve(sp.Eq(M * c**2, sp.Rational(1, 2) * N * kB * (hbar * a / (2 * PI * c * kB))), a)[0]
print(f"  M c^2 = (1/2) N kB T,  N = A/l_P^2,  T = hbar a/(2 pi c kB)  =>  a = {sp.simplify(a_area)}")
check("bare area-law holographic equipartition -> a = G M / r^2 = NEWTON (NO a0 at all)",
      sp.simplify(a_area - G * M / r**2) == 0)
print("  => AREA-law dof counting reproduces Newton and contains NO a0.  So horizon-AREA/dof")
print("     weighting does not even PRODUCE a0, let alone FORCE its coefficient.  a0 requires the")
print("     VOLUME/density ingredient (Part 2) -- exactly the non-thermodynamic posit.")
# horizon-coincidence geometry restated as an area ratio (shows 32pi/3 is the target, not a law)
print("\n  Horizon-coincidence geometry (the '~5.79 de Sitter radii' picture):")
print("    at a=a0 the Rindler horizon sits at  c^2/a0 = Z * R_dS  (Z de Sitter radii);")
print("    the transverse AREA ratio (c^2/a0)^2 / R_dS^2 = Z^2 = 32pi/3.")
check("Rindler-horizon-at-a0 sits at c^2/a0 = Z * R_dS (with R_dS=c/H, a0=cH/Z)",
      sp.simplify((c**2 / (c * H / (2 * sp.sqrt(sp.Rational(8,3)*PI)))) / (c / H)
                  - 2 * sp.sqrt(sp.Rational(8, 3) * PI)) == 0)
print("    But '32pi/3' here is just Z^2 RESTATED; no independent thermodynamic principle sets")
print("    the area ratio to 32pi/3.  Requiring it = 32pi/3 IS assuming the answer.  NOT forced.")

# ---------------------------------------------------------------------------
# PART 4 -- the thermodynamic O(1) MENU: which horizon number actually lands a0?
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 4  The horizon-thermodynamics O(1) menu on cH -- and which one FITS the data")
print("-" * 82)
import math
C = 2.99792458e8; MPC = 3.0857e22; H0 = 67.4e3 / MPC; A0_OBS = 1.2e-10; cH0 = C * H0
OMDE = 0.685; HL = H0 * math.sqrt(OMDE); cHL = C * HL      # H_Lambda (canonical pure-Lambda footing)
menu = [
    ("2cH_Lambda dS-Unruh temperature",       0.5,        "a0=2cH       (prior-doc reading; ~9-11x)"),
    ("T_U(a0)=T_GH temperature coincidence",  1.0,        "a0=cH        (Part 1; SURFACE match)"),
    ("enclosed critical-mass surface gravity", 2.0,       "a0=cH/2      (g=(4pi/3)Grho R_H=cH/2)"),
    ("Gibbons-Hawking temperature (Milgrom)",  2*math.pi, "2pi a0=cH    (1110.2580; BEST FIT)"),
    ("Verlinde de Sitter VOLUME entropy",      6.0,       "a0~cH/6      (contested)"),
    ("FRAMEWORK  Z=2 sqrt(8pi/3)",             Zf,        "a0=(c/2)sqrt(Grho) (geometric, not O(1))"),
]
print(f"  BOTH FOOTINGS carried:  cH0 = {cH0:.3e} (H0/total),  cH_Lambda = {cHL:.3e} (canonical).")
print(f"   {'route':<40}{'Z':>8}{'a0=cH0/Z':>11}{'/obs':>7}{'a0=cHL/Z':>11}{'/obs':>7}")
for name, Zr, note in menu:
    print(f"   {name:<40}{Zr:>8.3f}{cH0/Zr:>11.2e}{cH0/Zr/A0_OBS:>6.2f}x{cHL/Zr:>11.2e}{cHL/Zr/A0_OBS:>6.2f}x")
print(f"   canonical framework a0 = cH_Lambda/Z = {cHL/Zf:.3e} m/s^2  (target 9.36e-11).")
print("   => the SMALL clean horizon O(1)s {1/2, 1, 2} overshoot a0 by 2.3-11x and are excluded.")
print("      The data-fitting cluster is the LARGE divisors {2pi=6.28, Verlinde 6, framework")
print("      5.79}, all within ~13% of observed a0 and MUTUALLY within ~8% -- data cannot")
print("      separate them.  The framework's 5.789 = geometric sqrt(32pi/3) is the SMALLEST of")
print("      that cluster: ~3.5% from the CONTESTED Verlinde 6, ~8% from the clean T_GH 2pi.")
print("      It is SELECTED within the large-divisor cluster, not FORCED by any clean route.")
check("small clean O(1)s {1,2} overshoot a0 (Z_data=cH0/a0 ~ 5.5, so 1 and 2 are far too small)",
      cH0 / A0_OBS > 4.0 and Zf > 2.5)
check("framework Z is ~8% below the clean T_GH value 2pi (0.05 < |Z-2pi|/2pi < 0.12)",
      0.05 < abs(Zf - 2 * math.pi) / (2 * math.pi) < 0.12)
check("framework Z is within ~3.5% of the CONTESTED Verlinde 6 (a known near-coincidence)",
      abs(Zf - 6.0) / 6.0 < 0.05)

# ---------------------------------------------------------------------------
# PART 5 -- does the d=3 dS4-BOUNDARY angle evade the kappa=1/2 wall?  (test, don't assume)
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 5  Boundary test: does the d=3 (dS4-boundary) geometry FORCE the normalization 2?")
print("-" * 82)
V3 = sp.Rational(4, 3) * PI          # unit 3-ball volume  (the '3' + a 4pi)
Kfried = sp.Rational(8, 3) * PI      # Friedmann coefficient
S2 = 4 * PI                          # unit 2-sphere area (dS4 boundary S_2)
G32 = sp.gamma(sp.Rational(3, 2))    # = sqrt(pi)/2, the d=3 half-measure
print(f"  d=3 boundary furniture:  V_3(ball)=4pi/3={float(V3):.4f},  S_2=4pi,  Gamma(3/2)=sqrt(pi)/2")
check("Gamma(3/2) = sqrt(pi)/2 (the lone-sqrt(pi) d=3 measure the period-ring pointed to)",
      sp.simplify(G32 - sp.sqrt(PI) / 2) == 0)
# the SUGGESTIVE identity: (ball volume)/(Friedmann coeff) = 1/2 = kappa
kappa_read = sp.simplify(V3 / Kfried)
print(f"  SUGGESTIVE:  V_3 / K_Friedmann = (4pi/3)/(8pi/3) = {kappa_read} = kappa  (the '1/2')")
check("(4pi/3)/(8pi/3) = 1/2 exactly  (ball-volume / Friedmann-coefficient = kappa)",
      kappa_read == sp.Rational(1, 2))
print("  So the boundary furniture REPRODUCES the shape: 8pi/3 (Friedmann), sqrt(pi)=2 Gamma(3/2)")
print("  (d=3 measure), and even the 1/2 as V_ball/K_Friedmann.  BUT this is an ASSEMBLY, not a")
print("  forcing: nothing makes the mechanism divide the ball volume by the Friedmann coefficient")
print("  rather than by (say) S_2=4pi or use V_ball raw.  The choice of DENOMINATOR is exactly")
print("  the free normalization kappa.  Verify the rival readings (same ball, different kappa):")
for denom_name, denom in [("K_Friedmann=8pi/3", Kfried), ("S_2=4pi", S2), ("2pi", 2*PI)]:
    print(f"      V_3 / ({denom_name}) = {sp.nsimplify(V3/denom)}")
check("SAME ball volume gives DIFFERENT kappa per denominator: V_3/(8pi/3)=1/2, V_3/(4pi)=1/3, "
      "V_3/(2pi)=2/3 (the normalization is a free choice of denominator)",
      sp.simplify(V3 / Kfried - sp.Rational(1, 2)) == 0 and
      sp.simplify(V3 / S2 - sp.Rational(1, 3)) == 0 and
      sp.simplify(V3 / (2 * PI) - sp.Rational(2, 3)) == 0)
print("  => the d=3 boundary angle FIXES THE SHAPE (8pi/3, sqrt(pi), the '3') but the")
print("     NORMALIZATION '2' remains a CHOICE OF DENOMINATOR = kappa.  The wall is NOT evaded;")
print("     it is re-expressed as 'which boundary volume ratio', still unforced.")

# ---------------------------------------------------------------------------
# PART 6 -- CLOSED-DOOR AUDIT: prove-by-moving kappa.  Does the boundary EVADE the 3 shut
#           doors (kappa unforceable / CKN g_*=1 / number-field) or RE-HIT them?
# ---------------------------------------------------------------------------
print("\n" + "-" * 82)
print("PART 6  CLOSED-DOOR AUDIT: kappa is INVISIBLE to the Unruh/GH/boundary count (prove-by-moving)")
print("-" * 82)
kap = sp.symbols('kappa', positive=True)
# kappa-parametrize the density reading:  a0 = kappa c sqrt(G rho_DE),  rho_DE = 3H^2/(8 pi G)
rho_DE_k = 3 * H**2 / (8 * PI * G)
a0_k = kap * c * sp.sqrt(G * rho_DE_k)
Z_k  = sp.simplify(c * H / a0_k)
print(f"  a0(kappa) = kappa c sqrt(G rho_DE) ;  Z(kappa) = cH/a0 = {sp.nsimplify(Z_k)}")
check("Z(kappa) = (1/kappa) sqrt(8pi/3): SHAPE fixed, NORMALIZATION = 1/kappa",
      sp.simplify(Z_k - (1/kap)*sp.sqrt(sp.Rational(8, 3)*PI)) == 0)
check("Z(kappa=1/2) = sqrt(32pi/3) = canonical Z",
      sp.simplify(Z_k.subs(kap, sp.Rational(1, 2)) - sp.sqrt(sp.Rational(32, 3)*PI)) == 0)
# What the Unruh/GH/boundary count SEES -- differentiate each w.r.t. kappa (all must be 0):
T_GH_q   = hbar * H / (2 * PI * kB)          # Gibbons-Hawking temperature
R_dS_q   = c / H                             # de Sitter horizon distance
S_GH_q   = PI * (c / H)**2                   # GH entropy A/4 (Planck units)
a_match  = sp.solve(sp.Eq(hbar * a / (2 * PI * c * kB), T_GH_q), a)[0]   # temp-match accel
print("  Quantities the count SEES (d/dkappa must vanish -- the count is blind to kappa):")
for nm, q in [("T_GH", T_GH_q), ("R_dS", R_dS_q), ("S_GH=A/4", S_GH_q), ("temp-match a*", a_match)]:
    dq = sp.simplify(sp.diff(q, kap))
    check(f"d/dkappa[{nm:12s}] = {dq}  (kappa-FREE)", dq == 0)
check("temp-match acceleration a* = cH regardless of kappa (fixes only the SCALE, never Z)",
      sp.simplify(a_match - c * H) == 0)
check("a0 MOVES with kappa (da0/dkappa != 0): kappa is a DYNAMICAL inertia-response coupling",
      sp.simplify(sp.diff(a0_k, kap)) != 0)
check("Z MOVES with kappa (dZ/dkappa != 0)", sp.simplify(sp.diff(Z_k, kap)) != 0)
print("  => MOVE kappa: T_GH, R_dS, S_GH, and the temp-match acceleration cH are ALL FROZEN, while")
print("     a0 and Z MOVE.  The Unruh/GH/boundary count is a HOLOGRAPHIC count and is STRUCTURALLY")
print("     BLIND to the outside fraction kappa.  Now the three-door audit:")
print()
print("  (a) kappa-wall (ghost-freedom+unitarity+holography):  RE-HIT, not evaded.  The boundary")
print("      count is holographic; the prior 'holography reaches only the scale cH' barrier applies")
print("      verbatim -- above, the temp match yields a*=cH (kappa-free) and every horizon invariant")
print("      is d/dkappa=0.  Same wall, boundary clothes.")
print("  (b) CKN g_*=1 limit:  RE-HIT, not evaded.  The boundary 'dof' ARE the GH entropy cells")
print("      S=A/4 -- one per 4 Planck areas, carrying NO matter-species content = the g_*=1")
print("      (no-matter) limit at which 0.5878=(3/8pi)^{1/4} lands.  An honest SM count g_*=106.75")
print("      gives ~0.18-0.41.  The boundary supplies NO g_*!=1 to fix kappa; it RECONFIRMS g_*=1.")
print("  (c) sqrt(pi) number-field:  HOSTED, not FORCING.  d=3 is the natural HOME of a lone")
print("      sqrt(pi)=2 Gamma(3/2) and the SHAPE 8pi/3 IS boundary-derivable, but PART 5 showed the")
print("      normalization is a free denominator (1/2 vs 1/3 vs 2/3).  Hosting sqrt(pi) != forcing")
print("      the coefficient -- the same hosts!=forces distinction that killed the E8/J3(O) SM door.")
print("  AUDIT VERDICT: the boundary angle EVADES NONE of the three doors; it RE-HITS each in")
print("  geometric clothing -- a SHARPER REASON for the wall (SHAPE=geometry, boundary-derivable;")
print("  NORMALIZATION=dynamics, fit to a0), not a route around it.")

# ---------------------------------------------------------------------------
# VERDICT + sub-factor ledger
# ---------------------------------------------------------------------------
print("\n" + "=" * 82)
print("VERDICT: Z STAYS POSITED. Thermodynamics forces the FORM + the SHAPE-conditional-on-")
print("         -density, but NOT the normalization.  A sharper geometric REASON for the wall.")
print("=" * 82)
print("  SUB-FACTOR LEDGER (Z = 2 * sqrt(8pi/3)):")
print("    factor      value     status under Unruh/GH thermodynamics")
print("    ------      -----     ------------------------------------")
print("    (form) cH   --        FORCED: T_U(a0)=T_GH forces a0 ~ c H_Lambda (Z=1 at this stage)")
print("    8pi         Einstein  FIXED but CONDITIONAL: enters ONLY via the DENSITY (volume)")
print("                          reading of rho_DE; absent in the pure temperature (surface) match")
print("    3           Friedmann FIXED but CONDITIONAL: same -- the Friedmann '3' rides with 8pi")
print("    2 (kappa)   1/2       FREE: the Schwarzschild/surface-gravity normalization; the")
print("                          Unruh/GH menu offers {1,2,2pi,6}, none = 2 sqrt(8pi/3); the d=3")
print("                          boundary re-expresses it as a choice of denominator, still unforced")
print("  BOTTOM LINE:")
print("   * The Unruh<->GH horizon-coincidence FORCES a0 ~ c H_Lambda and, if one commits to the")
print("     de Sitter ENERGY-DENSITY (volume) reading, the SHAPE sqrt(8pi/3) (Friedmann).")
print("   * It does NOT force the coefficient: the naive TEMPERATURE match gives Z=1; reaching")
print("     Z=5.79 requires (a) surface->volume (buys sqrt(8pi/3)) and (b) the Schwarzschild 1/2")
print("     (buys the 2) -- neither is a thermodynamic identity.  The clean horizon O(1) that")
print("     FITS is 2pi (T_GH), off Z by ~8%.  kappa=1/2 stays FREE (prior wall upheld).")
print("   * The d=3 dS4-boundary angle does NOT evade the wall: it fixes the shape beautifully")
print("     (8pi/3, sqrt(pi)=2Gamma(3/2), the 3) but the '2' becomes 'which boundary-volume")
print("     ratio', i.e. the same unforced normalization.  This is a SHARPER statement of the")
print("     wall (a geometric REASON), NOT a derivation of Z and NOT a claim of closure.")
print("   * POSITED throughout: a0's value, Z, the sign; nu is Milgrom-1999's.  No TOE.")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0 (ran; not a verdict of derivation).")
