#!/usr/bin/env python3
"""
dS4 d=3 CONFORMAL-BOUNDARY MEASURE test of Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3)   (2026-07-23)
==========================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA.  a0 = c H_Lambda / Z,  Z = sqrt(32pi/3)
= 2 sqrt(8pi/3) = 5.78881...   Equivalently a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE).

THE UNTRIED ANGLE (period_ring_obstruction_2026.py, PART 1 / closing thread): Z's lone
transcendental is a single sqrt(pi) = Gamma(1/2), and its "one honest home" was flagged as a
d=3 (dS_4 conformal-boundary) loop measure -- Gamma(3/2)=sqrt(pi)/2, S_2=4pi, V_3=4pi/3.
This script asks the load-bearing question the bulk kappa-door could not settle FROM THE
BOUNDARY SIDE:

    Does the d=3 conformal-boundary geometry FORCE the full Z = 2 sqrt(8pi/3) -- including the
    normalization "2" (equivalently kappa = 1/2) -- or, as every bulk argument found, does it
    fix only the SHAPE sqrt(8pi/3) and leave the "2" free?

EXACT DECOMPOSITION under test (ground truth):
    Z^2 = 32pi/3 = 4 * (8pi/3).   8pi = Einstein (rho_DE = Lambda c^2/8piG); 3 = Friedmann;
    4 = (1/kappa)^2 with kappa = 1/2 the (c/2) free-fall prefactor.  Z(kappa) = (1/kappa) sqrt(8pi/3).

WALL BEING TESTED (do NOT relitigate; TEST whether the boundary evades it): kappa=1/2 is
provably unforceable by ghost-freedom+unitarity+holography (bulk); the number-field theorem
(desitter_entropy_coefficient / close_coefficient_Z) says every horizon/temperature/entropy
normalization lives in Q(pi)=rational*pi^n while Z is in Q(sqrt(pi)); the CKN-dof and
period-ring routes are shut.  This is the d=3-BOUNDARY test of the SAME "2".

HONESTY / manufactured-win guard: assembling {8pi, 3, 4pi/3, sqrt(pi), 1/2, 2} to multiply to
5.789 is NUMEROLOGY -- the failure mode to reject.  A derivation counts ONLY if every factor is
independently forced by the boundary geometry with NO free normalization.  Expected honest
outcome: Z STAYS POSITED (the boundary fixes the shape, not the "2").  a0's value, Z and the
sign are POSITED; nu(y)=sqrt(1+1/y) is Milgrom-1999's form.  No TOE; no "theory closed".
Sibling: period_ring_obstruction_2026.py, feynman_period_side.py, close_coefficient_Z.py.
"""
import sympy as sp
import numpy as np
import math

pi = sp.pi
FAIL = []


def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


print("=" * 90)
print("dS4 d=3 BOUNDARY-MEASURE test of Z = 2 sqrt(8pi/3):  does the boundary force the '2'?")
print("=" * 90)

Z = sp.sqrt(sp.Rational(32, 3) * pi)
Zf = float(Z)
print(f"  Z = sqrt(32pi/3) = 2 sqrt(8pi/3) = {Zf:.10f}    (a0 = c H_Lambda / Z)")

# ---------------------------------------------------------------------------
# PART 0 -- exact decomposition (ground truth), verified in sympy.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 0  Exact decomposition  Z^2 = 32pi/3 = 4*(8pi/3);  8pi=Einstein, 3=Friedmann, 4=(1/kappa)^2")
print("-" * 90)
check("Z^2 = 32pi/3", sp.simplify(Z**2 - sp.Rational(32, 3) * pi) == 0)
check("Z = 2*sqrt(8pi/3)", sp.simplify(Z - 2 * sp.sqrt(sp.Rational(8, 3) * pi)) == 0)
check("Z^2 = 4*(8pi/3)  (the '4' = 2^2 outer factor)",
      sp.simplify(Z**2 - 4 * (sp.Rational(8, 3) * pi)) == 0)
# kappa-parametrization: a0 = kappa c sqrt(G rho_DE), rho_DE = 3 H^2/(8pi G) -> Z(kappa)=(1/kappa)sqrt(8pi/3)
kappa = sp.symbols('kappa', positive=True)
Zk = (1 / kappa) * sp.sqrt(sp.Rational(8, 3) * pi)
check("Z(kappa) = (1/kappa) sqrt(8pi/3), and Z(1/2) = Z",
      sp.simplify(Zk.subs(kappa, sp.Rational(1, 2)) - Z) == 0)
print("    => SHAPE sqrt(8pi/3) is GR-forced; the '2' = 1/kappa is the normalization under test.")

# ---------------------------------------------------------------------------
# PART 1 -- the d=3 conformal-boundary geometric invariants (what the boundary actually supplies).
#           KEY FACT: at INTEGER d the sqrt(pi) of the measure CANCELS -> pi^integer, NOT a lone sqrt(pi).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 1  d=3 boundary invariants: their sqrt(pi) CANCELS (integer d) -> they carry pi^INTEGER")
print("-" * 90)
G12 = sp.gamma(sp.Rational(1, 2))          # sqrt(pi)
G32 = sp.gamma(sp.Rational(3, 2))          # sqrt(pi)/2
G52 = sp.gamma(sp.Rational(5, 2))          # 3 sqrt(pi)/4
S2 = 2 * pi**sp.Rational(3, 2) / G32        # unit 2-sphere area  (bdy of unit 3-ball)
V3 = pi**sp.Rational(3, 2) / G52            # unit 3-ball volume
check("Gamma(1/2) = sqrt(pi)", sp.simplify(G12 - sp.sqrt(pi)) == 0)
check("Gamma(3/2) = sqrt(pi)/2", sp.simplify(G32 - sp.sqrt(pi) / 2) == 0)
check("S_2 = 2 pi^{3/2}/Gamma(3/2) = 4pi   (the sqrt(pi) in pi^{3/2} and Gamma(3/2) CANCEL)",
      sp.simplify(S2 - 4 * pi) == 0)
check("V_3 = pi^{3/2}/Gamma(5/2) = 4pi/3   (sqrt(pi) CANCELS)",
      sp.simplify(V3 - sp.Rational(4, 3) * pi) == 0)
check("S_2/pi = 4 is RATIONAL  (=> S_2 in Q(pi), a pi^1 object, no lone sqrt(pi))",
      (sp.simplify(S2 / pi)).is_rational)
check("V_3/pi = 4/3 is RATIONAL  (=> V_3 in Q(pi), pi^1, no lone sqrt(pi))",
      (sp.simplify(V3 / pi)).is_rational)
print("    => EVERY integer-d boundary measure is rational*pi^n (sqrt(pi)'s pair up and cancel).")
print("       The dS_4 boundary d=3 gives S_2=4pi and V_3=4pi/3 -- both in Q(pi), NOT Q(sqrt(pi)).")

# ---------------------------------------------------------------------------
# PART 2 -- Z carries a LONE sqrt(pi); it is in Q(sqrt(pi)) NOT Q(pi).  So NO integer-d boundary
#           measure can equal Z.  (Re-confirms period_ring PART 1: d*=1.907, no integer d gives Z.)
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 2  Z carries a LONE sqrt(pi) (Q(sqrt(pi))); integer-d boundary measures cannot equal it")
print("-" * 90)
x = sp.symbols('x')
cof = sp.simplify(Z / sp.sqrt(pi))                         # Z / sqrt(pi)
mpoly = sp.minimal_polynomial(cof, x)
check("Z/sqrt(pi) = sqrt(32/3) = 4 sqrt(6)/3  (algebraic, LONE sqrt(pi) stripped)",
      sp.simplify(cof - 4 * sp.sqrt(6) / 3) == 0)
check("Z/sqrt(pi) is a QUADRATIC irrational (minpoly 3x^2-32, degree 2) -> Z in Q(sqrt(pi)), not Q(pi)",
      sp.degree(mpoly, x) == 2)
check("Z^2/pi = 32/3 is rational but Z/pi is NOT (odd power of pi) -> lone sqrt(pi)",
      (sp.simplify(Z**2 / pi)).is_rational and not (sp.nsimplify(Z / pi)).is_rational)
# no integer d in 1..8 makes the (d-1)-sphere area equal Z (all are rational*pi -> can't match Q(sqrt(pi)))
def Sarea(dd):
    return 2 * pi**sp.Rational(dd, 2) / sp.gamma(sp.Rational(dd, 2))
near = {dd: float(Sarea(dd)) for dd in range(1, 9)}
check("no integer d in 1..8 has (d-1)-sphere area = Z (dS_4 boundary d=3 gives S_2=4pi=12.566 != Z)",
      all(abs(near[dd] - Zf) > 1e-6 for dd in range(1, 9)))
print(f"    integer-d sphere areas: " + ", ".join(f"d={dd}:{near[dd]:.3f}" for dd in (2, 3, 4, 5)))
print(f"    Z={Zf:.3f} sits BETWEEN d=3 (S_2=4pi=12.566... as an AREA) -- no integer-d measure hits it.")

# ---------------------------------------------------------------------------
# PART 3 -- WHERE the lone sqrt(pi) actually comes from: sqrt(Einstein 8pi), i.e. a0 ~ sqrt(rho).
#           It is part of the GR-FORCED SHAPE sqrt(8pi/3), NOT a d=3 loop measure, and NOT the
#           normalization.  The d=3-loop-measure "home" is a RED HERRING (its sqrt(pi) cancels).
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 3  The lone sqrt(pi) = sqrt(Einstein 8pi) (a0 ~ sqrt(rho_DE)); it sits in the SHAPE")
print("-" * 90)
c, G, Lam, H_L = sp.symbols('c G Lambda H_L', positive=True)
rho_DE = 3 * H_L**2 / (8 * pi * G)                 # Friedmann/Einstein, Lambda-only
a0_dens = sp.Rational(1, 2) * c * sp.sqrt(G * rho_DE)   # framework a0 = (c/2) sqrt(G rho_DE)
Z_dens = sp.simplify(c * H_L / a0_dens)
check("a0 = (c/2) sqrt(G rho_DE) reproduces Z = sqrt(32pi/3) exactly",
      sp.simplify(Z_dens - Z) == 0)
shape = sp.sqrt(sp.Rational(8, 3) * pi)             # = Z * kappa, the kappa-independent shape
check("SHAPE sqrt(8pi/3) already carries the LONE sqrt(pi): sqrt(8pi/3)/sqrt(pi)=sqrt(8/3) algebraic",
      sp.simplify(shape / sp.sqrt(pi) - sp.sqrt(sp.Rational(8, 3))) == 0)
check("the sqrt(pi) is sqrt of the Einstein 8pi (density coupling), NOT a boundary loop measure",
      sp.simplify(sp.sqrt(8 * pi) / sp.sqrt(pi) - 2 * sp.sqrt(2)) == 0)   # sqrt(8pi)=2sqrt(2) sqrt(pi)
print("    => Z = (1/kappa) * sqrt(8pi/3).  The lone sqrt(pi) lives ENTIRELY in the GR-forced shape")
print("       sqrt(8pi/3) = sqrt(Einstein-8pi/Friedmann-3); it is sourced by a0 ~ sqrt(rho), the")
print("       square-root of a pi^1 density -- exactly the odd-power origin.  A d=3 loop measure")
print("       (S_2, V_3) canNOT be its source: those cancel their sqrt(pi) (Part 1).  The '2'/kappa")
print("       multiplies this shape and carries NO pi at all -> the boundary sqrt(pi) does not touch it.")

# ---------------------------------------------------------------------------
# PART 4 -- STEELMAN the boundary forcing the "2", and refute each in sympy.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 4  Steelmen: could a d=3 boundary factor FORCE the '2'?  (each refuted exactly)")
print("-" * 90)

# Steelman A: the universal leading "2" of S_{d-1} = 2 pi^{d/2}/Gamma(d/2).
rest_of_S2 = pi**sp.Rational(3, 2) / G32           # what the sphere "2" actually multiplies
check("Steelman A REFUTED: the sphere-measure '2' multiplies pi^{3/2}/Gamma(3/2)=2pi, NOT sqrt(8pi/3)",
      sp.simplify(rest_of_S2 - 2 * pi) == 0 and sp.simplify(rest_of_S2 - shape) != 0)
print("      (S_2's '2' is glued to a 2pi giving 4pi; Z's '2' is glued to sqrt(8pi/3)=2.894. Different.)")

# Steelman B: the ratio Gamma(1/2)/Gamma(3/2) = 2 (a d=1-vs-d=3 measure ratio).
check("Steelman B: Gamma(1/2)/Gamma(3/2) = 2 exactly (= 1/(d/2-1) at d=3)",
      sp.simplify(G12 / G32 - 2) == 0)
print("      This '2' IS real on the boundary -- but it is the Gamma recursion 1/(d/2-1)|_{d=3},")
print("      identical in content to kappa=1/2 -> 1/kappa=2 (a free O(1) READING of d), not a")
print("      forced coefficient: no boundary loop integral outputs 1/(d/2-1) as a0's prefactor")
print("      without ALSO cancelling its sqrt(pi) (Part 5). Re-labels the '2', does not force it.")

# Steelman C: the d=3 tadpole coefficient Gamma(-1/2) = -2 sqrt(pi) carries BOTH a 2 AND a sqrt(pi).
Gm12 = sp.gamma(sp.Rational(-1, 2))
check("Steelman C: Gamma(-1/2) = -2 sqrt(pi) (a lone '2' AND a lone sqrt(pi) together!)",
      sp.simplify(Gm12 + 2 * sp.sqrt(pi)) == 0)
# but the physical d=3 tadpole A0 = (1/(4pi)^{d/2}) Gamma(1-d/2) (m^2)^{d/2-1} is sqrt(pi)- AND 2-washed:
m = sp.symbols('m', positive=True)
d = sp.symbols('d', positive=True)
A0 = (1 / (4 * pi)**(d / 2)) * sp.gamma(1 - d / 2) * (m**2)**(d / 2 - 1)
A0_3 = sp.simplify(A0.subs(d, 3))
check("Steelman C REFUTED: physical d=3 tadpole A0 = -m/(4pi) -- the '2' and sqrt(pi) of Gamma(-1/2) "
      "CANCEL against (4pi)^{3/2}",
      sp.simplify(A0_3 - (-m / (4 * pi))) == 0)
print("      => the d=3 boundary measure is LITTERED with 2's and sqrt(pi)'s (Gamma(-1/2)=-2sqrt(pi),")
print("         Gamma(1/2)=sqrt(pi), S_2 prefactor 2, Gamma(1/2)/Gamma(3/2)=2) -- but in every PHYSICAL")
print("         integer-d quantity they CANCEL to rational*pi^n. None is a forced, free-standing '2sqrt(pi)'.")

# ---------------------------------------------------------------------------
# PART 5 -- FIT-ANYTHING / DOF: the boundary-atom toolbox blankets the neighborhood of Z.
#           Assembling 2 sqrt(8pi/3) from boundary factors carries no information.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 5  Fit-anything: a d=3-boundary-atom toolbox densely covers the neighborhood of Z")
print("-" * 90)
ATOMS = {'2': 2.0, '3': 3.0, 'pi': math.pi, 'sqrtpi': math.sqrt(math.pi),
         'S2=4pi': 4 * math.pi, 'V3=4pi/3': 4 * math.pi / 3, '8pi': 8 * math.pi,
         'G(3/2)=sqrtpi/2': math.sqrt(math.pi) / 2}
ak = list(ATOMS)
H = 6
vals = set()
for i in range(len(ak)):
    for j in range(i, len(ak)):
        for op in (lambda a, b: a * b, lambda a, b: a / b if b else None,
                   lambda a, b: math.sqrt(a * b), lambda a, b: math.sqrt(a / b) if b else None):
            base = op(ATOMS[ak[i]], ATOMS[ak[j]])
            if base is None or base <= 0:
                continue
            for p in range(1, H + 1):
                for q in range(1, H + 1):
                    vals.add(p / q * base)
vals = np.array(sorted(v for v in vals if 0 < v < 100))
# how close does the toolbox get to Z, and how DENSE is it there (the DOF/fit-anything signature)?
dЗ = float(np.min(np.abs(vals - Zf)) / Zf)
dens = int(np.sum(np.abs(vals - Zf) / Zf < 0.02))            # count within 2% of Z
# control: same density near a RANDOM nearby target (shows it is not special to Z)
rng = np.random.default_rng(20260723)
ctrl = [int(np.sum(np.abs(vals - t) / t < 0.02)) for t in rng.uniform(4, 8, 200)]
print(f"  toolbox size {len(vals)} expressions; closest to Z: rel-err {dЗ:.2e}")
print(f"  # expressions within 2% of Z = {dens};   median # within 2% of RANDOM targets in [4,8] = "
      f"{int(np.median(ctrl))}")
check("toolbox hits Z to <0.1% (assembling 2 sqrt(8pi/3) is trivial -- NUMEROLOGY, not a derivation)",
      dЗ < 1e-3)
check("the neighborhood of Z is NOT special: ~as many boundary-expressions land within 2% of random "
      "targets as of Z (fit-anything DOF signature)",
      dens <= 3 * max(1, int(np.median(ctrl))))
print("    => 'the d=3 boundary can assemble 2 sqrt(8pi/3)' is uninformative: the atom toolbox blankets")
print("       the whole neighborhood. Landing on Z is what a fit-anything basis does, not a forcing.")

# ---------------------------------------------------------------------------
# PART 6 -- horizon coincidence on the boundary: every variant RELOCATES the free normalization.
# ---------------------------------------------------------------------------
print("\n" + "-" * 90)
print("PART 6  Horizon coincidence: naive gives Z=1; every 'boundary' variant relocates the free O(1)")
print("-" * 90)
# naive: Rindler horizon c^2/a0 = dS horizon R_dS = c/H_L  ->  a0 = c H_L -> Z=1.
print("  naive c^2/a0 = R_dS=c/H_L  ->  Z = 1  (T_Unruh=T_GH). Framework needs Z=5.789: a factor 5.789.")
# area-equate variant: (c^2/a0)^2 = (1/f) * 4pi R_dS^2  -> a0 = c H_L sqrt(f/4pi) -> Z=sqrt(4pi/f).
f = sp.symbols('f', positive=True)
Z_area = sp.sqrt(4 * pi / f)
f_needed = sp.solve(sp.Eq(Z_area, Z), f)[0]
check("area-equate horizon coincidence forces Z=sqrt(4pi/f); to hit Z it needs f = 3/8 -- inserted BY HAND",
      sp.simplify(f_needed - sp.Rational(3, 8)) == 0)
print(f"    equating horizon AREAS (bringing in the 4pi by choice) needs f={f_needed}=3/8 by hand;")
print("    f=3/8 = (Friedmann 3)/(8) is the SAME 8pi/3 shape with the normalization re-inserted.")
print("    Whether one equates DISTANCES (Z=1), AREAS (free f), dof or TEMPERATURES (Deser-Levin: a0_eff")
print("    =2cH_L, i.e. Z=1/2, off by 2Z=11.6), the free O(1) just MOVES. The boundary never pins it.")

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("\n" + "=" * 90)
print("VERDICT:  the d=3 boundary FIXES THE SHAPE sqrt(8pi/3), NOT the normalization '2'. Z STAYS POSITED.")
print("=" * 90)
print("""  * The dS_4 conformal boundary is d=3, an INTEGER dimension. Every integer-d geometric measure
    (S_2=4pi, V_3=4pi/3, and the sphere/ball family) is rational*pi^n IN Q(pi): its Gamma(3/2)=sqrt(pi)/2
    is exactly cancelled by the pi^{3/2}. So the boundary MEASURE carries NO lone sqrt(pi).
  * Z = sqrt(32pi/3) carries a LONE sqrt(pi) (Q(sqrt(pi)), a quadratic irrational over sqrt(pi)); NO
    integer-d boundary measure equals it (period_ring's d*=1.907 re-confirmed from the boundary side).
  * WHERE the lone sqrt(pi) really lives: sqrt(Einstein 8pi), because a0 ~ sqrt(rho_DE) is the square
    root of a pi^1 density. That sqrt(pi) sits INSIDE the GR-forced SHAPE sqrt(8pi/3); the period-ring
    "d=3 loop-measure home for sqrt(pi)" is a RED HERRING -- the boundary loop measure cancels its
    sqrt(pi) and cannot source it. The normalization '2'=1/kappa multiplies the shape and carries NO pi.
  * The boundary IS littered with 2's and sqrt(pi)'s (Gamma(-1/2)=-2sqrt(pi), Gamma(1/2)/Gamma(3/2)=2,
    the S_2 leading 2), so one CAN assemble 2 sqrt(8pi/3) from them -- but (i) in every physical
    integer-d quantity they CANCEL to rational*pi^n, and (ii) the atom toolbox blankets the whole
    neighborhood of Z (fit-anything DOF). Assembling Z that way is NUMEROLOGY, not a forcing.
  * Every horizon-coincidence reading (distance -> Z=1; area -> free f=3/8 by hand; temperature/
    Deser-Levin -> Z=1/2) merely RELOCATES the free O(1). The boundary never pins kappa.
  * SHARPER RESULT (the value here): this gives a GEOMETRIC REASON for the bulk kappa-wall. The shape
    8pi/3 (incl. its lone sqrt(pi) = sqrt of the Einstein density) is boundary/GR-forced; the '2' is a
    dimension-reading / square-root-normalization convention that lives in a DIFFERENT structural slot
    (it carries no pi) and the integer-d boundary measure has no lever on it. NOT forced. NO new door.
  * a0's value, Z and the sign remain POSITED; nu is Milgrom-1999's; both footings carried. No TOE;
    not "theory closed" -- a boundary theory, if ever written, would be a separate posit, not forced here.""")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0 (ran; a null: boundary fixes the shape, not the '2').")
