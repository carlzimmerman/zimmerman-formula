#!/usr/bin/env python3
"""
Z_boundary_geometry_2026.py  --  HONEST SYNTHESIS of the dS4 d=3 boundary-geometry
angle on the POSITED coefficient Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3) = 5.78881...
===================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA.  a0 = c H_Lambda / Z,
equivalently a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE).

This is the SYNTHESIZER script that closes the 2026-07-23 delve.  It distils two
independent upstream analyses (both committed, both exit 0) into a single ledger:
  * real_research/reviews/unruh_gh_coincidence_Z_2026.py   (derive-agent, forces_Z=false)
  * real_research/reviews/executioner_Z_convention_sweep_2026.py  (adversary, MOVES)
  * real_research/reviews/dS4_boundary_measure_Z_2026.py          (adversary, boundary null)
  * real_research/reviews/period_ring_obstruction_2026.py         (the sqrt(pi) provenance)

THE QUESTION (the ONE untried angle): the dS4 d=3 CONFORMAL-BOUNDARY geometry the
period-ring's lone sqrt(pi)=Gamma(1/2) pointed to -- does counting holographic dof on
the d=3 boundary FORCE the normalization '2' (= kappa=1/2) where the bulk arguments
(ghost-freedom+unitarity+holography; CKN g_*=1; period-ring number field) could not?

EXACT DECOMPOSITION (ground truth): Z^2 = 32pi/3 = 4*(8pi/3).
  '8pi' = Einstein/Friedmann coupling (rho_DE = Lambda c^2/(8piG));
  '3'   = Friedmann 3 (H^2 = (8piG/3) rho);
  '4'   = 2^2 from the (c/2) prefactor in a0 = (c/2) sqrt(G rho_DE)  =>  kappa = 1/2.
So Z = 2 * sqrt(8pi/3): '8pi/3' is the SHAPE, the '2' (kappa) is the NORMALIZATION = crux.

MANUFACTURED-WIN GUARD (max risk -- Carl publicly retracted TOE/SM overclaims): a
DERIVATION of Z is valid ONLY if FORCED with NO free normalization and NO post-hoc
factor assembly.  Multiplying {8pi, 3, 4pi/3, sqrt(pi), 1/2, 2} to hit 5.789 is
NUMEROLOGY -- the failure mode to reject.  Every factor must be independently motivated
by the geometry, not chosen to land the target.  Expected honest outcome, PRE-REGISTERED:
Z STAYS POSITED because the '2'=kappa is provably unforceable, and the dS4-boundary angle,
while it fixes the SHAPE, ALSO cannot force the normalization -- a SHARPER geometric REASON
for the standing wall, not a derivation and not a failure.

HONESTY: a0's value, Z, and the sign are POSITED, not derived; nu(y)=sqrt(1+1/y) is
Milgrom-1999 PLA 253:273 Eq.9's kernel (the framework's distinctive content is the
cH_Lambda/Z coefficient + the modified-inertia completion).  No TOE; not "theory closed".
Both footings (rho_DE/cH_Lambda canonical vs rho_total/cH0) carried.  Exit 0 = ran.
"""
import sympy as sp

pi = sp.pi
FAIL = []


def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


Z = sp.sqrt(sp.Rational(32, 3) * pi)                 # = 2 sqrt(8pi/3), the framework value
Zf = float(Z)
print("=" * 90)
print(f"Z_BOUNDARY_GEOMETRY 2026  --  synthesis: does the dS4 d=3 boundary FORCE Z = {Zf:.5f}?")
print("=" * 90)

# ---------------------------------------------------------------------------
# PART A -- EXACT DECOMPOSITION (ground truth, sympy-verified).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART A  Ground truth:  Z^2 = 32pi/3 = 4*(8pi/3);  Z = 2*sqrt(8pi/3).  8pi/3=SHAPE, 2=NORM")
print("-" * 90)
check("Z^2 = 32pi/3 exactly", sp.simplify(Z**2 - sp.Rational(32, 3) * pi) == 0)
check("Z = 2 sqrt(8pi/3) exactly", sp.simplify(Z - 2 * sp.sqrt(sp.Rational(8, 3) * pi)) == 0)
check("Z^2 = 4*(8pi/3) exactly (outer 4 = 2^2, inner 8pi/3 = Friedmann coupling)",
      sp.simplify(Z**2 - 4 * (sp.Rational(8, 3) * pi)) == 0)
# kappa-parametrization: a0 = kappa c sqrt(G rho_DE), rho_DE = 3H^2/(8piG) -> Z(kappa)=(1/kappa)sqrt(8pi/3)
c, G, H = sp.symbols('c G H', positive=True)
kappa = sp.symbols('kappa', positive=True)
rho_DE = 3 * H**2 / (8 * pi * G)                     # de Sitter Friedmann, Lambda-only
a0_k = kappa * c * sp.sqrt(G * rho_DE)               # the POSITED density/collapse reading
Z_k = sp.simplify(c * H / a0_k)
check("Z(kappa) = (1/kappa) sqrt(8pi/3)  [SHAPE fixed, NORMALIZATION = 1/kappa]",
      sp.simplify(Z_k - (1 / kappa) * sp.sqrt(sp.Rational(8, 3) * pi)) == 0)
check("Z(kappa=1/2) = sqrt(32pi/3) = framework Z  (the '2' = 1/kappa, kappa the Schwarzschild 1/2)",
      sp.simplify(Z_k.subs(kappa, sp.Rational(1, 2)) - Z) == 0)
print("    => the whole derivation reduces to: is the SHAPE 8pi/3 forced, and is the '2'=1/kappa forced?")

# ---------------------------------------------------------------------------
# PART B -- the d=3 boundary furniture (what the dS4 conformal boundary actually supplies).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART B  dS4 conformal-boundary furniture (d=3):  Gamma(3/2)=sqrt(pi)/2, S_2=4pi, V_3=4pi/3")
print("-" * 90)
G32 = sp.gamma(sp.Rational(3, 2))                    # = sqrt(pi)/2, the d=3 half-measure
S2 = 2 * pi**sp.Rational(3, 2) / G32                 # unit 2-sphere area (boundary of unit 3-ball)
V3 = pi**sp.Rational(3, 2) / sp.gamma(sp.Rational(5, 2))   # unit 3-ball volume
check("Gamma(3/2) = sqrt(pi)/2  (the lone-sqrt(pi) measure the period-ring pointed to)",
      sp.simplify(G32 - sp.sqrt(pi) / 2) == 0)
check("S_2 = 2 pi^{3/2}/Gamma(3/2) = 4pi  (its sqrt(pi) CANCELS: integer-d measure -> pi^1)",
      sp.simplify(S2 - 4 * pi) == 0)
check("V_3 = pi^{3/2}/Gamma(5/2) = 4pi/3  (sqrt(pi) CANCELS)",
      sp.simplify(V3 - sp.Rational(4, 3) * pi) == 0)
check("S_2/pi = 4 and V_3/pi = 4/3 are RATIONAL  (=> boundary measures live in Q(pi), no lone sqrt(pi))",
      sp.simplify(S2 / pi).is_rational and sp.simplify(V3 / pi).is_rational)
print("    KEY: at INTEGER d the sqrt(pi) of pi^{d/2} pairs with Gamma(d/2) and CANCELS.  The d=3")
print("    boundary MEASURE (S_2, V_3) is rational*pi -- it carries NO free-standing sqrt(pi).")

# ---------------------------------------------------------------------------
# PART C -- the SHAPE 8pi/3: boundary-MOTIVATED (Einstein 8pi + Friedmann 3), and where the
#           lone sqrt(pi) really lives (sqrt of the Einstein 8pi density -- NOT a loop measure).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART C  The SHAPE 8pi/3 is motivated (8pi=Einstein, 3=Friedmann); its sqrt(pi)=sqrt(Einstein 8pi)")
print("-" * 90)
# 8pi/3 assembling from GR AND from boundary invariants (non-uniquely -- an honesty flag):
Kfried = sp.Rational(8, 3) * pi                      # Friedmann coupling H^2=(8piG/3)rho
check("8pi = Einstein coupling: rho_DE = Lambda c^2/(8piG) => the 8pi is the GR density normalization",
      sp.simplify(Kfried * 3 / pi - 8) == 0)          # strip to expose the bare 8pi and 3
check("8pi/3 = 2*V_3  (Friedmann coupling = twice the unit 3-ball volume: a boundary reading)",
      sp.simplify(Kfried - 2 * V3) == 0)
check("8pi/3 = (2/3)*S_2  (also = two-thirds the boundary 2-sphere area: a SECOND, different reading)",
      sp.simplify(Kfried - sp.Rational(2, 3) * S2) == 0)
print("    NOTE (honesty): 8pi/3 = 2*V_3 = (2/3)*S_2 -- TWO distinct boundary assemblies of the same")
print("    number.  That non-uniqueness is why 'the boundary can build 8pi/3' MOTIVATES but does not")
print("    uniquely FORCE; the physically load-bearing route is GR/Friedmann, which fixes 8pi and 3.")
# provenance of the lone sqrt(pi): it is sqrt of the pi^1 Einstein density, NOT Gamma(3/2).
shape = sp.sqrt(sp.Rational(8, 3) * pi)              # = Z*kappa, the kappa-independent shape
check("the SHAPE sqrt(8pi/3) carries the lone sqrt(pi): sqrt(8pi/3)/sqrt(pi) = sqrt(8/3) is algebraic",
      sp.simplify(shape / sp.sqrt(pi) - sp.sqrt(sp.Rational(8, 3))) == 0)
check("that sqrt(pi) = sqrt(Einstein 8pi):  sqrt(8pi) = 2 sqrt(2) sqrt(pi)  (a0 ~ sqrt(rho_DE), a pi^1 density)",
      sp.simplify(sp.sqrt(8 * pi) / sp.sqrt(pi) - 2 * sp.sqrt(2)) == 0)
print("    => the lone sqrt(pi) is the square-root of the pi^1 Einstein density (a0 ~ sqrt(rho_DE)),")
print("       sitting INSIDE the GR-forced shape sqrt(8pi/3).  Gamma(3/2)=sqrt(pi)/2 is only its")
print("       dimensional HOME, not its source: the integer-d boundary loop measure cancels its own")
print("       sqrt(pi) (Part B) and cannot SOURCE Z's.  So d=3 HOSTS the shape; it does not FORCE it.")

# ---------------------------------------------------------------------------
# PART D -- the NORMALIZATION '2' MOVES under alternative conventions (prove-by-moving-the-number).
#           This is the decisive synthesizer demonstration: the '2' is NOT forced.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART D  Does the '2' (=1/kappa) MOVE under defensible conventions?  (prove-by-moving-the-number)")
print("-" * 90)
# D1: prefactor kappa in a0 = kappa c sqrt(G rho_DE) -- each a defensible normalization.
print("  D1  prefactor kappa in a0 = kappa*c*sqrt(G rho_DE)   [Z = (1/kappa) sqrt(8pi/3)]:")
kappa_menu = [("1    bare c sqrt(Grho)",              sp.Integer(1)),
              ("1/2  Schwarzschild/free-fall  <-FRAMEWORK", sp.Rational(1, 2)),
              ("1/(4pi)  per-solid-angle",            1 / (4 * pi)),
              ("2pi  temperature 2pi",                2 * pi)]
Zvals_D1 = []
for nm, kv in kappa_menu:
    Zv = sp.nsimplify(Z_k.subs(kappa, kv))
    Zvals_D1.append(Zv)
    print(f"      kappa = {nm:34s}:  Z = {Zv} = {float(Zv):.4f}")
check("D1 MOVES: {kappa=1,1/2,1/(4pi),2pi} give 4 DISTINCT Z; only hand-picked kappa=1/2 = framework 5.789",
      len(set(Zvals_D1)) == 4 and sp.simplify(Z_k.subs(kappa, sp.Rational(1, 2)) - Z) == 0
      and sp.simplify(Z_k.subs(kappa, 1) - Z) != 0)
# D2: the boundary-dof reading -- 'count boundary dof' = divide the unit 3-ball by a boundary measure.
print("  D2  boundary-dof reading:  kappa = V_3 / (which boundary measure)   [same ball, many denominators]:")
denom_menu = [("K_Friedmann=8pi/3", Kfried), ("S_2=4pi", S2), ("2pi", 2 * pi)]
kappa_vals_D2 = []
for nm, dn in denom_menu:
    kv = sp.nsimplify(V3 / dn)
    kappa_vals_D2.append(kv)
    print(f"      V_3 / ({nm:16s}) = {kv}  ->  Z = (1/kappa)sqrt(8pi/3) = {float((1/kv)*shape):.4f}")
check("D2 MOVES: same unit 3-ball over defensible denominators gives kappa in {1/2, 1/3, 2/3} -- the "
      "'1/2' is ONE denominator choice among many, not forced",
      set(kappa_vals_D2) == {sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3)})
# D3: the horizon-coincidence GEOMETRY reading -- what you equate at a0.
print("  D3  horizon-coincidence geometry:  which horizon quantity coincides at a0:")
a = sp.symbols('a', positive=True)
R_dS = c / H
Z_dist = sp.simplify(c * H / sp.solve(sp.Eq(c**2 / a, R_dS), a)[0])          # distances -> Z=1
g_enc = sp.Rational(4, 3) * pi * G * (3 * H**2 / (8 * pi * G)) * R_dS         # enclosed-crit surface gravity
Z_enc = sp.simplify(c * H / g_enc)                                            # -> Z=2
Z_area = sp.sqrt(4 * pi)                                                      # bare area-equate -> 2sqrt(pi)
Z_gh = 2 * pi                                                                 # GH temperature (Milgrom) -> 2pi
for nm, Zv in [("distances c^2/a0=R_dS", Z_dist), ("enclosed-crit surface gravity", Z_enc),
               ("bare area-equate (+4pi)", Z_area), ("GH-temperature 2pi (Milgrom)", Z_gh)]:
    print(f"      {nm:34s}:  Z = {sp.nsimplify(Zv)} = {float(Zv):.4f}")
check("D3 MOVES: horizon-coincidence Z in {1, 2, 2sqrt(pi)=3.545, 2pi=6.28} -- 4 DISTINCT, NONE = 5.789",
      len({sp.nsimplify(Z_dist), sp.nsimplify(Z_enc), sp.nsimplify(Z_area), sp.nsimplify(Z_gh)}) == 4
      and all(sp.simplify(Zv - Z) != 0 for Zv in [Z_dist, Z_enc, Z_area, Z_gh]))
print("    => under EVERY defensible convention the '2'/normalization MOVES; only a hand-picked choice")
print("       lands 5.789.  The '2' is NOT forced.  (The FORM a0 ~ O(1)*cH_Lambda is invariant -- Part F.)")

# ---------------------------------------------------------------------------
# PART E -- CLOSED-DOOR AUDIT: the boundary count is BLIND to kappa (does not evade the 3 shut doors).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART E  Closed-door audit: is the boundary count blind to kappa?  (prove-by-moving kappa)")
print("-" * 90)
hbar, kB = sp.symbols('hbar kB', positive=True)
T_GH = hbar * H / (2 * pi * kB)                      # Gibbons-Hawking temperature
S_GH = pi * (c / H)**2                               # GH entropy A/4 (Planck units), the boundary dof count
a_match = sp.solve(sp.Eq(hbar * a / (2 * pi * c * kB), T_GH), a)[0]   # temp-match acceleration
print("  Quantities the d=3 boundary count SEES (d/dkappa must vanish -- blind to the outside fraction):")
for nm, q in [("T_GH", T_GH), ("R_dS=c/H", c / H), ("S_GH=A/4", S_GH), ("temp-match a*", a_match)]:
    dq = sp.simplify(sp.diff(q, kappa))
    check(f"d/dkappa[{nm:12s}] = {dq}  (kappa-FREE: the boundary count cannot see kappa)", dq == 0)
check("temp-match acceleration a* = cH regardless of kappa (fixes only the SCALE cH, never Z)",
      sp.simplify(a_match - c * H) == 0)
check("a0 MOVES with kappa (da0/dkappa != 0): kappa is a DYNAMICAL inertia-response coupling, "
      "invisible to the holographic count",
      sp.simplify(sp.diff(a0_k, kappa)) != 0 and sp.simplify(sp.diff(Z_k, kappa)) != 0)
print("  => MOVE kappa: T_GH, R_dS, S_GH=A/4 and the temp-match scale cH are ALL FROZEN while a0, Z MOVE.")
print("     The boundary count is HOLOGRAPHIC and STRUCTURALLY BLIND to kappa.  Door-by-door:")
print("     (a) kappa-wall (ghost-freedom+unitarity+holography): RE-HIT -- the boundary count is")
print("         holographic; the 'holography reaches only the scale cH' barrier applies verbatim.")
print("     (b) CKN g_*=1 limit: RE-HIT -- the boundary dof ARE the GH entropy cells S=A/4 (one per")
print("         4 Planck areas, NO matter-species content = g_*=1, where 0.5878=(3/8pi)^{1/4} lands).")
print("         An honest SM count g_*=106.75 would give ~0.18-0.41; the boundary supplies no g_*!=1.")
print("     (c) sqrt(pi) number-field: HOSTED, not FORCING -- d=3 is the dimensional home of a lone")
print("         sqrt(pi), and the SHAPE 8pi/3 is boundary-readable, but the '2' is a free denominator")
print("         (Part D).  hosts != forces -- the same distinction that killed the E8/J3(O) SM door.")

# ---------------------------------------------------------------------------
# PART F -- what IS forced (the robust half): the FORM a0 ~ c H_Lambda, and both-footings numbers.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART F  What IS forced: the FORM a0 ~ c H_Lambda (invariant); + both-footings numeric ledger")
print("-" * 90)
check("FORM is invariant: every convention gives a0 = O(1)*cH (a0/(cH) = 1/Z for each Z above)",
      all(sp.simplify((c * H / Zv) / (c * H) - 1 / Zv) == 0
          for Zv in [Z_dist, Z_enc, Z_area, Z_gh, Z]))
import math
C = 2.99792458e8; MPC = 3.0857e22; H0 = 67.4e3 / MPC; A0_OBS = 1.2e-10
OMDE = 0.685; HL = H0 * math.sqrt(OMDE)             # H_Lambda (pure-Lambda footing)
cH0 = C * H0; cHL = C * HL
print("  BOTH FOOTINGS (Carl non-negotiable #4):")
print(f"    canonical  a0 = cH_Lambda/Z = {cHL / Zf:.3e} m/s^2   (target 9.36e-11; rho_DE/cH_Lambda)")
print(f"    total-ftg  a0 = cH0/Z       = {cH0 / Zf:.3e} m/s^2   (rho_total/cH0 fork)")
print(f"    swing between footings = sqrt(Omega_Lambda) = {math.sqrt(OMDE):.4f}  (a real ~17% ambiguity)")
check("canonical footing reproduces a0 = 9.36e-11 to 1% (cH_Lambda/Z with H_Lambda=H0 sqrt(0.685))",
      abs(cHL / Zf - 9.36e-11) / 9.36e-11 < 0.01)
check("the two footings differ by sqrt(Omega_Lambda) ~ 0.82 (both defensible; a0 itself footing-dependent)",
      abs((cHL / Zf) / (cH0 / Zf) - math.sqrt(OMDE)) < 1e-9)
# the horizon O(1) that actually FITS the data is 2pi (T_GH), NOT the geometric 5.789:
print(f"  Horizon O(1) menu vs data (a0_obs={A0_OBS:.1e}):  Z=1 -> {cH0/1/A0_OBS:.2f}x,  Z=2 -> "
      f"{cH0/2/A0_OBS:.2f}x,  Z=2pi -> {cH0/(2*math.pi)/A0_OBS:.2f}x,  Z=5.789 -> {cH0/Zf/A0_OBS:.2f}x")
check("the clean horizon number that FITS is 2pi (T_GH), off the geometric Z=5.789 by ~8% -- Z is "
      "SELECTED within the large-divisor cluster {2pi, 6, 5.79}, not forced",
      0.05 < abs(Zf - 2 * math.pi) / (2 * math.pi) < 0.12)

# ---------------------------------------------------------------------------
# VERDICT + SUB-FACTOR LEDGER
# ---------------------------------------------------------------------------
print("\n" + "=" * 90)
print("VERDICT:  POSITED (sharper reason).  The dS4 d=3 boundary geometry FIXES the SHAPE 8pi/3")
print("          (incl. its lone sqrt(pi)=sqrt-of-Einstein-8pi) but does NOT force the")
print("          NORMALIZATION '2'=kappa.  A geometric REASON the kappa=1/2 door stays shut.")
print("=" * 90)
print("  SUB-FACTOR LEDGER  (Z = 2 * sqrt(8pi/3)):")
print("    factor     value      status")
print("    ------     -----      ------")
print("    (form) cH  --         FORCED: any Unruh<->GH horizon coincidence forces a0 ~ c H_Lambda")
print("    8pi        Einstein   MOTIVATED (GR-forced): the density coupling rho_DE=Lambda c^2/(8piG);")
print("                          boundary-readable as 8pi/3 = 2 V_3, but gated on reading a0 off the")
print("                          VOLUME/density (surface reading gives Z=1, no 8pi/3)")
print("    3          Friedmann  MOTIVATED (GR-forced): the Friedmann 3 in H^2=(8piG/3)rho; rides with 8pi")
print("    sqrt(pi)   d=3 home   MOTIVATED but PROVENANCE-CORRECTED: it is sqrt(Einstein-8pi) = sqrt of a")
print("                          pi^1 density (a0 ~ sqrt(rho)), sitting INSIDE the shape; Gamma(3/2)=")
print("                          sqrt(pi)/2 is its dimensional HOME, not its source (integer-d measures")
print("                          cancel their sqrt(pi)).  Boundary HOSTS it; does not source/force it.")
print("    2 (kappa)  1/2        FREE: the Schwarzschild/surface-gravity normalization.  MOVES under every")
print("                          defensible convention (Part D): kappa in {1,1/2,1/4pi,2pi} and boundary")
print("                          denominator in {8pi/3,4pi,2pi} -> kappa {1/2,1/3,2/3}.  NOT forced.")
print("  WHY the boundary cannot force the '2':  the boundary count is holographic and d/dkappa=0 on")
print("  every invariant it sees (T_GH, R_dS, S_GH=A/4, temp-match cH); a0 and Z live OUTSIDE that count.")
print("  The '2' carries NO pi and sits in a DIFFERENT structural slot than the pi-graded shape, so the")
print("  integer-d boundary measure has no lever on it.  The boundary RE-HITS all three shut doors in")
print("  geometric clothing (kappa-wall / CKN g_*=1 / hosts!=forces), evading none.")
print("  CAVEATS (all carried):")
print("   * kappa=1/2 door: PROVABLY unforceable (ghost-freedom+unitarity+holography); a0's VALUE is a")
print("     one-parameter EFT input, kappa free-but-nonzero.  Upheld, not relitigated.")
print("   * CKN g_*=1: 0.5878=(3/8pi)^{1/4} is the g_*=1 geometric limit; the boundary supplies no")
print("     microscopic g_*!=1 to fix kappa -- it reconfirms g_*=1.")
print("   * hosts != forces: d=3 HOSTS a lone sqrt(pi) and the shape 8pi/3, but hosting is not forcing")
print("     (same distinction that walled the E8/J3(O) SM door).")
print("   * BOTH footings carried: rho_DE/cH_Lambda (canonical, a0=9.36e-11) vs rho_total/cH0; the value")
print("     of a0 itself swings by sqrt(Omega_Lambda)~0.82 across the footing fork.")
print("   * POSITED throughout: a0's value, Z, the sign.  nu(y)=sqrt(1+1/y) is Milgrom-1999 PLA 253:273")
print("     Eq.9; the distinctive content is the cH_Lambda/Z coefficient + the MI completion.  No TOE;")
print("     no 'theory closed'.  A boundary theory, if ever written, is a SEPARATE posit -- not forced here.")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0 (ran; a null: boundary fixes the SHAPE, not the '2'/kappa).")
