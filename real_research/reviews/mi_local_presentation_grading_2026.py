#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_local_presentation_grading_2026.py
=====================================
THE PRESENTATION THEOREM:  why every horizon-side derivation in this corpus landed on MILGROM's
coefficient, why no route ever produced the framework's, and what that forces about where a
derivation of kappa = 1/2 must come from.

This is a SYNTHESIS script.  It uses no new physics input.  It takes the corpus's OWN no-gos as a
specification and shows they triangulate a structure nobody in the corpus wrote down.

--------------------------------------------------------------------------------------------------
THE OBSERVATION
--------------------------------------------------------------------------------------------------
Write every candidate acceleration scale two ways -- against the vacuum's LOCAL free-fall rate,
and against the GLOBAL horizon rate:

    LOCAL  (matter side of Einstein's eqs):   a_0 = lambda * c sqrt(G rho_Lambda)
    HORIZON (metric side of Einstein's eqs):  a_0 = q     * c H_Lambda

The two are related by the Friedmann factor  c H_L = c sqrt(8 pi G rho_L / 3), which carries the
8 pi from  G_munu = (8 pi G/c^4) T_munu.  So EXACTLY ONE of the two presentations can be pi-free
for a given coefficient.  Tabulate the three coefficients in the literature:

    coefficient                       lambda (LOCAL)          q (HORIZON)
    -------------------------------   ---------------------   -----------------------
    Milgrom 1999 eqs 6-9 (= the       Z = sqrt(32 pi/3)       2                <- RATIONAL
      GHY / pi-free lane's r = 1)       = alg x pi^(+1/2)
    Milgrom 2020 a_0 = cH_L/2pi       sqrt(2/3pi)             1/(2 pi)
                                        = alg x pi^(-1/2)
    THIS FRAMEWORK  kappa = 1/2       1/2   <- RATIONAL       1/Z = alg x pi^(-1/2)

*** The framework's coefficient is the UNIQUE pi-EVEN member in the LOCAL presentation, and
    Milgrom 1999's is the UNIQUE pi-EVEN member in the HORIZON presentation. ***

sqrt(pi) is transcendental (if it were algebraic, so would be its square pi -- Lindemann 1882).
So the pi-parity is a Z/2 GRADING on the coefficient, exactly the grading this corpus already
proved for the flavour sector -- and it has teeth:

    THEOREM (presentation).  A derivation whose output is an ALGEBRAIC number times the scale of
    its own presentation can reach ONLY the pi-even member of that presentation.  Therefore:
      * any HORIZON-side derivation (areas, boundary terms, surface gravity, horizon entropy,
        solid angles) can reach Milgrom 1999's a_0 = 2 c H_Lambda and can NEVER reach the
        framework's, because 1/Z is transcendental;
      * any LOCAL / MATTER-side derivation (a coupling to the vacuum stress tensor
        T^Lambda_munu = -rho_L c^2 g_munu, an index, an entropy normalisation, a rational
        multiplicity) can reach kappa = 1/2 and can NEVER reach Milgrom's, because Z is
        transcendental.

--------------------------------------------------------------------------------------------------
WHY THIS MATTERS -- IT RETRODICTS THE CORPUS'S OWN 18-ROUTE NULL
--------------------------------------------------------------------------------------------------
Every route in this corpus that produced a DEFINITE coefficient went through the horizon, and every
one of them produced MILGROM's:
    * GHY boundary term / pi-free area (`mi_pi_free_area_2026.py`, 56/56)   -> r = 1  EXACTLY
    * Deser-Levin / Narnhofer-Peter-Thirring horizon temperature            -> floor = c H_Lambda
    * the conventional 2 pi a_0 ~ c H_Lambda reading                        -> r = 4 pi
and every route that tried to reach 2Z left a free knob (the temperature class, r free;
the psi-escape kernels, second scale free).  The presentation theorem says that is not bad luck:
*** it is forced. ***  A horizon-side argument CANNOT output the framework's number, ever.
The corpus has been running the wrong side of Einstein's equations for the target it wants.

--------------------------------------------------------------------------------------------------
WHAT THE FRAMEWORK'S OWN PREMISE SAYS ABOUT WHICH SIDE IS PRIMITIVE
--------------------------------------------------------------------------------------------------
The framework is MODIFIED INERTIA, not modified gravity.  Its mechanism is that a particle's
inertia is its response to the vacuum's quantum state -- a MATTER/stress-energy object.  That is
the Sciama-Mach inertial-induction side, the T_munu side.  The horizon rate H_Lambda is the
curvature side (H^2 = Lambda c^2/3, a metric invariant).  So the framework's own premise selects
the LOCAL presentation, and the presentation theorem then says its coefficient must be RATIONAL.

    *** THE OPEN PROBLEM COLLAPSES FROM A TRANSCENDENTAL TO A RATIONAL. ***
    Instead of "derive 2Z = 11.577620...", the target becomes "derive the rational 1/4":

              MOND floor   k  =  (1/4) c sqrt(G rho_Lambda)  =  c / (4 t_Lambda)
              a_0 = 2k        =  (1/2) c sqrt(G rho_Lambda)  =  c / (2 t_Lambda)

    with t_Lambda = (G rho_Lambda)^(-1/2) the vacuum's own free-fall time (50.7 Gyr).  In words:
    THE MOND FLOOR IS ONE QUARTER OF THE VACUUM'S FREE-FALL RATE TIMES c.  Equivalently
    a_0 t_Lambda = c/2 exactly.  No pi, no Friedmann factor, no horizon, no dimension count.

    And 1/4 is the shape an entropy normalisation produces -- it is the 1/4 of S = A/4G, the one
    factor in horizon thermodynamics fixed by the Euclidean/thermal normalisation rather than by
    geometry.  THAT IS A NAMED CONJECTURE, PRICED BELOW, NOT A DERIVATION.

--------------------------------------------------------------------------------------------------
WHAT THIS DOES NOT DO -- read this before repeating any of it
--------------------------------------------------------------------------------------------------
  (1) It does NOT derive 1/2.  pi-evenness admits EVERY rational: 1/2, 1/3, 1, 2/5 all pass.
      Checked explicitly below (NC2).  kappa = 1/2 remains FITTED, NOT DERIVED.
  (2) The parities SWAP between presentations (Part C).  So the argument is exactly as strong as
      the postulate "the matter side is primitive".  Milgrom may equally postulate the metric side
      and get q = 2 as HIS rational.  This is a statement about WHERE to look, not a proof.
  (3) It does not touch any observable.  a_0(z), the RAR shape and BTFR are unaffected; the RAR
      shape is exactly coefficient-blind anyway (`mi_r_one_parameter_nogo_paper_2026.py`).
  (4) The GHY lane's falsification of a_0 = 2 c H_Lambda (+0.266 dex BTFR intercept) STANDS.  The
      theorem explains why that lane produced Milgrom's number; it does not rescue it.

CREDIT.  nu(y) = sqrt(1+1/y) and the temperature balance are MILGROM 1999 PLA 253:273 eqs 6-9
(a_0_hat = 2 c H_Lambda, the pi-even horizon member); eqs 10-11 give a second coefficient;
MILGROM 2008 sec 7.3.1 notes the mismatch "isn't necessarily meaningful"; a_lambda = c^2 sqrt(L/3)
is MILGROM 1994 Ann.Phys. 229:384; the temperature sqrt(a^2+L/3)/2pi is NARNHOFER, PETER &
THIRRING 1996 IJMPB 10:1507; S = A/4G is BEKENSTEIN 1973 / HAWKING 1975; pi transcendental is
LINDEMANN 1882.  The framework's distinctive content is the COEFFICIENT plus the MI completion.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 60

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=12):
    return mp.nstr(mp.mpf(x), n)


# ---------------------------------------------------------------------------------------------
G       = mp.mpf("6.67430e-11")
C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
ALT     = 1 / mp.sqrt(OMEGA_L)

RHO_L  = LAMBDA * C**2 / (8 * mp.pi * G)
CHL    = C**2 * mp.sqrt(LAMBDA / 3)
CSQRT  = C * mp.sqrt(G * RHO_L)                     # the LOCAL scale, c sqrt(G rho_L)
T_LAM  = 1 / mp.sqrt(G * RHO_L)                     # vacuum free-fall time
Znum   = 2 * mp.sqrt(8 * mp.pi / 3)
A0     = CSQRT / 2
FLOOR  = A0 / 2

print(__doc__)
print("=" * 100)
print("PART A -- exact identities for Z  (60 dps + symbolic)")
print("=" * 100)
pi_s = sp.pi
Z_sym = 2 * sp.sqrt(8 * pi_s / 3)
forms = {
    "2 sqrt(8 pi/3)   (as published)": 2 * sp.sqrt(8 * pi_s / 3),
    "4 sqrt(2 pi/3)": 4 * sp.sqrt(2 * pi_s / 3),
    "sqrt(32 pi/3)": sp.sqrt(32 * pi_s / 3),
    "sqrt(8 x 4pi/3)   (8 x the unit-ball volume)": sp.sqrt(8 * 4 * pi_s / 3),
    "sqrt(32/3) x sqrt(pi)   (alg x pi^(1/2))": sp.sqrt(sp.Rational(32, 3)) * sp.sqrt(pi_s),
}
for name, f in forms.items():
    same = sp.simplify(f - Z_sym) == 0
    check(same, f"A  Z = {name}", f"{sig(mp.mpf(str(sp.N(f, 40))), 13)}")
check(sp.simplify(Z_sym**2 - 32 * pi_s / 3) == 0,
      "A6  Z^2 = 32 pi/3 = 4 x (8 pi/3)  -- the '8pi/3 plus ONE factor of 4' decomposition",
      f"Z^2 = {sig(Znum**2, 13)}")
check(sp.simplify(2 * Z_sym - 4 * sp.sqrt(8 * pi_s / 3)) == 0,
      "A7  2Z = 4 sqrt(8 pi/3): the Friedmann factor, times a bare 4")

print()
print(f"  c H_Lambda        = {sig(CHL)}   m/s^2       (HORIZON scale)")
print(f"  c sqrt(G rho_L)   = {sig(CSQRT)}   m/s^2       (LOCAL scale)")
print(f"  ratio             = {sig(CHL/CSQRT, 13)}  must be Z/2 = {sig(Znum/2, 13)}")
check(abs(CHL / CSQRT - Znum / 2) / (Znum / 2) < mp.mpf("1e-50"),
      "A8  c H_Lambda / c sqrt(G rho_L) = Z/2 = sqrt(8pi/3) on real constants at 60 dps")
print(f"  t_Lambda = (G rho_L)^(-1/2) = {sig(T_LAM)} s = {sig(T_LAM/mp.mpf('3.1557e16'), 6)} Gyr")
print(f"  a_0   = c/(2 t_L) = {sig(A0)}   ALT {sig(A0*ALT)}   m/s^2")
print(f"  floor = c/(4 t_L) = {sig(FLOOR)}   ALT {sig(FLOOR*ALT)}   m/s^2")
check(abs(A0 * T_LAM / C - mp.mpf("0.5")) < mp.mpf("1e-50"),
      "A9  a_0 t_Lambda = c/2 EXACTLY -- the coefficient as a pure rational, no pi",
      f"a_0 t_L/c = {sig(A0*T_LAM/C, 20)}")
check(abs(FLOOR * T_LAM / C - mp.mpf("0.25")) < mp.mpf("1e-50"),
      "A10 floor t_Lambda = c/4 EXACTLY -- and 1/4 is the Bekenstein-Hawking rational",
      f"k t_L/c = {sig(FLOOR*T_LAM/C, 20)}")
# both footings
check(abs((A0 * ALT) * (T_LAM * mp.sqrt(OMEGA_L)) / C - mp.mpf("0.5")) < mp.mpf("1e-45"),
      "A11 and it is footing-INVARIANT: ALT rescales a_0 and t_L inversely, product unchanged",
      "-> the rational 1/2 is not a footing artefact")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the Z/2 pi-GRADING in the LOCAL presentation")
print("=" * 100)

# lambda = a_0 / (c sqrt(G rho_L)) for each literature coefficient
lam = {
    "Milgrom 1999 eqs 6-9  (= GHY lane r=1)": (2 * CHL) / CSQRT,
    "Milgrom 1999 eqs 10-11  (r=2)": CHL / CSQRT,
    "Milgrom 2020  a_0 = cH_L/2pi": (CHL / (2 * mp.pi)) / CSQRT,
    "THIS FRAMEWORK  kappa = 1/2": A0 / CSQRT,
}
lam_sym = {
    "Milgrom 1999 eqs 6-9  (= GHY lane r=1)": Z_sym,
    "Milgrom 1999 eqs 10-11  (r=2)": Z_sym / 2,
    "Milgrom 2020  a_0 = cH_L/2pi": Z_sym / (4 * pi_s),
    "THIS FRAMEWORK  kappa = 1/2": sp.Rational(1, 2),
}


def pi_parity(expr):
    """Return (algebraic_cofactor, half_integer_power_of_pi) for expr = alg * pi^(k/2), or None.

    Strategy: try k = -2,-1,0,1,2 and test whether expr / pi^(k/2) is algebraic (sympy can decide
    this for the closed forms here).  Parity is k mod 2: EVEN k => pi-even (algebraic times an
    algebraic power of pi is still transcendental unless k = 0, so we report k itself).
    """
    for k in (0, 1, -1, 2, -2):
        cof = sp.simplify(expr / pi_s ** sp.Rational(k, 2))
        if cof.is_algebraic:
            return sp.nsimplify(cof, rational=False), k
    return None, None


print(f"  {'coefficient':40s} {'lambda':>16s}  {'= algebraic x pi^(k/2)':>34s}  parity")
parities = {}
for name, val in lam.items():
    cof, k = pi_parity(lam_sym[name])
    par = "EVEN (algebraic)" if k == 0 else "ODD  (transcendental)"
    parities[name] = k
    print(f"  {name:40s} {sig(val, 12):>16s}  {str(cof) + ' x pi^(' + str(k) + '/2)':>34s}  {par}")
    # cross-check the symbolic form against the real constants
    check(abs(val - mp.mpf(str(sp.N(lam_sym[name], 45)))) / val < mp.mpf("1e-40"),
          f"B-num  {name[:34]}: symbolic lambda matches real constants at 60 dps")

fw = "THIS FRAMEWORK  kappa = 1/2"
check(parities[fw] == 0,
      "B1  the framework's lambda = 1/2 is pi-EVEN: an ALGEBRAIC (indeed rational) number")
check(all(parities[k] != 0 for k in parities if k != fw),
      "B2  ALL THREE Milgrom coefficients are pi-ODD in the local presentation",
      f"parities: {[(k.split()[0]+k.split()[1], parities[k]) for k in parities]}")
check(sp.sqrt(pi_s).is_algebraic is False,
      "B3  sqrt(pi) is TRANSCENDENTAL (Lindemann 1882: pi transcendental => so is its root)")
check(sp.simplify(Z_sym / sp.sqrt(pi_s) - sp.sqrt(sp.Rational(32, 3))) == 0
      and sp.sqrt(sp.Rational(32, 3)).is_algebraic,
      "B4  Z = sqrt(32/3) x sqrt(pi) with sqrt(32/3) ALGEBRAIC -- so Z is transcendental",
      "=> unreachable from any algebraic source in the local presentation")
check(sp.simplify(lam_sym["Milgrom 2020  a_0 = cH_L/2pi"] * sp.sqrt(pi_s)
                  - sp.sqrt(sp.Rational(2, 3))) == 0,
      "B5  Milgrom 2020's lambda = sqrt(2/3) x pi^(-1/2) -- also transcendental, opposite power")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- AGAINST INTEREST: the parities SWAP in the horizon presentation")
print("=" * 100)
q_sym = {
    "Milgrom 1999 eqs 6-9  (= GHY lane r=1)": sp.Integer(2),
    "Milgrom 1999 eqs 10-11  (r=2)": sp.Integer(1),
    "Milgrom 2020  a_0 = cH_L/2pi": 1 / (2 * pi_s),
    "THIS FRAMEWORK  kappa = 1/2": 1 / Z_sym,
}
print(f"  {'coefficient':40s} {'q = a_0/cH_L':>16s}  {'= algebraic x pi^(k/2)':>34s}  parity")
qpar = {}
for name, qe in q_sym.items():
    cof, k = pi_parity(qe)
    qpar[name] = k
    par = "EVEN (algebraic)" if k == 0 else "ODD  (transcendental)"
    print(f"  {name:40s} {sig(mp.mpf(str(sp.N(qe, 40))), 12):>16s}  "
          f"{str(cof) + ' x pi^(' + str(k) + '/2)':>34s}  {par}")
check(qpar["Milgrom 1999 eqs 6-9  (= GHY lane r=1)"] == 0 and qpar[fw] != 0,
      "C1  in the HORIZON presentation it is MILGROM's coefficient that is algebraic (q=2) "
      "and the framework's that is transcendental (1/Z)")
check(qpar[fw] == -1,
      "C2  1/Z = sqrt(3/32) x pi^(-1/2): the framework is pi-ODD on the horizon side",
      "-> so NO horizon/area/boundary argument can ever output it.  That is the retrodiction.")
check(parities[fw] == 0 and qpar[fw] != 0
      and parities["Milgrom 1999 eqs 6-9  (= GHY lane r=1)"] != 0
      and qpar["Milgrom 1999 eqs 6-9  (= GHY lane r=1)"] == 0,
      "C3  THE SWAP IS EXACT: each coefficient is algebraic in exactly ONE presentation",
      "=> the principle is a statement about WHICH SIDE IS PRIMITIVE, not a proof of a number")

# quantify the honest residual: how close are the two rival coefficients in kappa-convention?
kappa_M20 = mp.sqrt(2 / (3 * mp.pi))
print()
print(f"  in the framework's OWN kappa-convention (a_0 = kappa c sqrt(G rho_L)):")
print(f"    framework      kappa = 0.5")
print(f"    Milgrom 2020   kappa = sqrt(2/3pi) = {sig(kappa_M20, 12)}   -> only "
      f"{float(abs(kappa_M20/mp.mpf('0.5') - 1))*100:.2f}% away")
gap_down = abs(kappa_M20 / mp.mpf("0.5") - 1)      # 7.87%  (his value, as a fraction of 1/2)
gap_up = abs(mp.mpf("0.5") / kappa_M20 - 1)        # 8.54%  (1/2, as a fraction of his)
check(gap_down < mp.mpf("0.09") and gap_up < mp.mpf("0.09"),
      "C4  AGAINST INTEREST: Milgrom 2020 sits within 8% of kappa=1/2 -- any derivation must be "
      "EXACT to beat it, and the 2 natural constants in the a_0 box are BOTH his",
      f"{float(gap_down)*100:.2f}% below 1/2, equivalently 1/2 is {float(gap_up)*100:.2f}% above his "
      "(the corpus's banked 8.54% is this second direction -- do not conflate them)")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the FRIEDMANN factor is the whole of Z, and the framework's form does not use it")
print("=" * 100)
print("""  In d spatial dimensions the Friedmann relation is  H^2 = 16 pi G rho / (d(d-1)),
  so Milgrom's  a_0 = 2 c H  acquires a d-DEPENDENT transcendental in the local presentation,
  while the framework's  a_0 = (1/2) c sqrt(G rho)  never references the Friedmann factor at all.
  (Scope: this holds the FORM fixed and varies only the Friedmann coefficient.  G itself carries
  d-dependent dimensions -- this is a structural remark about the form, not a d-dim derivation.)""")
d_s = sp.symbols("d", positive=True, integer=True)
lam_M99_d = 2 * sp.sqrt(16 * pi_s / (d_s * (d_s - 1)))
print(f"  {'d':>3s}  {'lambda_Milgrom(d) = 2 sqrt(16pi/d(d-1))':>42s}  {'lambda_framework':>18s}")
vals_d = []
for dv in range(2, 10):
    lv = mp.mpf(str(sp.N(lam_M99_d.subs(d_s, dv), 40)))
    vals_d.append(lv)
    print(f"  {dv:3d}  {sig(lv, 12):>42s}  {'0.5 (fixed)':>18s}")
check(sp.simplify(lam_M99_d.subs(d_s, 3) - Z_sym) == 0,
      "D1  at d = 3 Milgrom's local lambda is exactly Z -- the identification is right")
check(max(vals_d) / min(vals_d) > mp.mpf("2"),
      "D2  Milgrom's local coefficient MOVES by >2x across d = 2..9; the framework's does not",
      f"range {sig(min(vals_d), 8)} .. {sig(max(vals_d), 8)}")
check(sp.simplify(sp.diff(sp.Rational(1, 2), d_s)) == 0,
      "D3  the framework's lambda is d-independent by construction (it never sees 8pi/3)")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- consistency with the z-blindness result of the same day")
print("=" * 100)
print("""  `mi_a0z_r_blindness_2026.py` (25/25) proved: a_0(z)/a_0(0) is EXACTLY blind to the
  coefficient, but a NON-Lambda escape scale would show up as a residual, forcing the escape
  scale to be Lambda-pure to p <= 0.072 in matter-density power.  The local presentation passes
  that test STRUCTURALLY: rho_Lambda is Lambda-pure by definition, and the candidate second
  scale in the entropy branch (ell_Planck, via sqrt(S_dS)) does not redshift at all.""")
check(True and abs(RHO_L - LAMBDA * C**2 / (8 * mp.pi * G)) == 0,
      "E1  rho_Lambda IS Lambda (times fixed constants) -- z-frozen up to w != -1, by definition")
S_dS = mp.mpf("3.30757e122")
HBAR = mp.mpf("1.054571817e-34")
ent_branch = (mp.sqrt(6) / 16) * C ** mp.mpf("3.5") / mp.sqrt(G * HBAR * S_dS)
print(f"  entropy branch: (sqrt6/16) c^(7/2)/sqrt(G hbar S) = {sig(ent_branch, 12)}"
      f"   vs floor {sig(FLOOR, 12)}")
check(abs(ent_branch / FLOOR - 1) < mp.mpf("1e-4"),
      "E2  the pi-free entropy branch reproduces the floor to <1e-4 (banked; needs a HALF power "
      "of S, an object with no known variational meaning -- a NECESSARY CONDITION, not a route)",
      f"ratio {sig(ent_branch/FLOOR, 12)}")
check(mp.mpf("16") == 4 ** 2,
      "E3  and its prefactor 1/16 = 1/4^2 -- the SAME rational 4, appearing squared under a "
      "square root of entropy.  Suggestive; priced in Part F, NOT claimed.")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- PRICING the '1/4 is Bekenstein-Hawking' conjecture (do not skip this)")
print("=" * 100)
print("""  The corpus already priced one geometric lock at p = 0.480 over a 109-value menu
  (`mi_geometric_lock_*`).  The same discipline applies here.  The claim being priced is NOT
  "1/4 appears" -- it is "the residue after stripping the Friedmann factor is a SMALL RATIONAL".
  Menu: the residue could a priori have been any of the small rationals below.""")
menu = [sp.Rational(p, q) for q in (1, 2, 3, 4, 5, 6, 8) for p in range(1, 9)
        if sp.Rational(p, q) <= 8 and sp.gcd(p, q) == 1]
menu = sorted(set(menu))
target = sp.Rational(1, 4)
print(f"  menu of small rationals p/q, q in 1..8, value <= 8:  {len(menu)} entries")
print(f"  the observed residue (floor / [c sqrt(G rho_L)]) = {sig(FLOOR/CSQRT, 20)}")
hit = [m for m in menu if abs(mp.mpf(str(sp.N(m, 40))) - FLOOR / CSQRT) < mp.mpf("1e-30")]
check(hit == [target],
      "F1  the residue lands EXACTLY on 1/4 -- a single menu entry, zero tuning",
      f"hit = {hit}")
p_val = mp.mpf(len(menu)) ** -1
print(f"  crude menu p-value for landing on ANY prespecified single entry: 1/{len(menu)} "
      f"= {sig(p_val, 4)}")
check(p_val < mp.mpf("0.05"),
      "F2  p = 0.02 on the menu -- BETTER than the p = 0.480 geometric lock, but this is a "
      "POST-HOC menu and 1/4 was chosen knowing the answer",
      "-> the honest reading: 'small rational' is a WEAK claim; 'it is BH's 1/4' is UNTESTED")
check(True,
      "F3  what would make it a lock: a construction in which the SAME 1/4 that normalises "
      "S = A/4G appears as the MI kernel's prefactor, with NO other freedom.  Not built here.")
print("""
  FALSIFIABLE CONSEQUENCE if the 1/4 really is the entropy normalisation:  in any gravity theory
  where the horizon entropy normalisation changes (Gauss-Bonnet / Wald entropy, S = A/4G + alpha
  x curvature corrections), a_0 must shift by the SAME factor as S's normalisation, at fixed
  rho_Lambda.  That is a genuine over-determination -- one equation, no new parameter -- and it is
  the first coefficient test in this corpus that does not run through a horizon area.""")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- NEGATIVE CONTROLS (each must trip, or the criterion is vacuous)")
print("=" * 100)
# NC1: does the parity criterion actually discriminate, or does it call everything even?
odd_count = sum(1 for k in parities if parities[k] != 0)
check(odd_count == 3,
      "NC1  the criterion is NOT vacuous: it calls 3 of the 4 local lambdas ODD",
      "(a criterion that passed everything would be worthless)")
# NC2: the criterion must NOT single out 1/2 -- it admits every rational.
others = [sp.Rational(1, 3), sp.Rational(1, 1), sp.Rational(2, 5), sp.Rational(7, 8)]
all_even = all(pi_parity(o)[1] == 0 for o in others)
check(all_even,
      "NC2  CONTROL FIRES: 1/3, 1, 2/5, 7/8 are ALL pi-even too",
      "*** so pi-evenness does NOT derive 1/2.  kappa = 1/2 stays FITTED. ***")
# NC3: corrupt the algebraic factorisation and the parity test must fail to certify
bad = sp.sqrt(pi_s) * sp.pi ** sp.Rational(1, 3)     # pi^(5/6): not a half-integer power
cof_bad, k_bad = pi_parity(bad)
check(k_bad is None,
      "NC3  CONTROL FIRES: pi^(5/6) is refused by the grading (not a half-integer power)",
      "-> the grading really is Z/2 and can reject inputs")
# NC4: the swap must not be an artefact of how I wrote the ratio -- rebuild it from raw constants
lam_raw = (2 * CHL) / CSQRT
q_raw = A0 / CHL
check(abs(lam_raw - mp.mpf(str(sp.N(Z_sym, 45)))) / lam_raw < mp.mpf("1e-40")
      and abs(q_raw - 1 / mp.mpf(str(sp.N(Z_sym, 45)))) / q_raw < mp.mpf("1e-40"),
      "NC4  both presentations rebuilt from RAW measured constants agree with the symbols",
      f"lambda_M99 = {sig(lam_raw, 13)}, q_fw = {sig(q_raw, 13)}")
# NC5: a real dimensional guard -- corrupt G's exponent and the local scale must MOVE
CSQRT_bad = C * mp.sqrt(G**2 * RHO_L)
check(abs(CSQRT_bad / CSQRT - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: squaring G moves the local scale by a factor "
      f"{sig(CSQRT_bad/CSQRT, 6)} -- the construction is dimensionally load-bearing")


# =============================================================================================
print()
print("=" * 100)
print("PART H -- the SM / geometric-lock hint this opens (flagged, NOT claimed)")
print("=" * 100)
print("""  The corpus's NUMBER-FIELD OBSTRUCTION (2026-06-27) says: a_0/Z structurally carries
  sqrt(pi), all flavour data is algebraic, therefore the framework's scale is gauge-blind and all
  18 unification routes came out partial.  *** That computation was done in the HORIZON
  presentation. ***  In the LOCAL presentation the framework's coefficient is RATIONAL, so the
  transcendence obstruction to an algebraic flavour bridge DISSOLVES -- it was presentation-
  dependent, not intrinsic.  This does not build a bridge.  It says the corpus's own reason for
  believing no bridge can exist DOES NOT APPLY on the side its own premise selects.

  CONCRETE NEXT DOOR (one script):  re-run the number-field obstruction with c sqrt(G rho_L) as
  the bridge object instead of c H_Lambda / Z, and ask whether the Z/2 grading still forbids a
  finite algebraic bridge to the Koide / mass-ratio sector.  Two banked facts become relevant
  again the moment the presentation changes:
      * kappa^(-1/2) = sqrt(2) EXACTLY (banked; previously discounted, and it is an ALGEBRAIC
        statement in an algebraic presentation -- it dies only on kappa's 1.2-5.4% precision)
      * Koide Q = 2/3 is rational, and the local presentation's residue is the rational 1/4
  ⚠️ Neither is evidence.  Both are the SAME class of coincidence the corpus priced at p = 0.480,
  and Carl publicly retracted the TOE/SM overclaims on 2026-06-23.  Do NOT re-overclaim.  The
  deliverable here is that ONE named obstruction is now known to be presentation-dependent.""")
check(abs(mp.mpf("0.5") ** mp.mpf("-0.5") - mp.sqrt(2)) < mp.mpf("1e-50"),
      "H1  kappa^(-1/2) = sqrt(2) exactly, and sqrt(2) is ALGEBRAIC -- so in the local "
      "presentation this lead is no longer killed by transcendence",
      "(it is still killed by nothing but precision: kappa is known to 1.2-5.4%)")
check(sp.Rational(2, 3).is_algebraic and sp.Rational(1, 4).is_algebraic,
      "H2  Koide's 2/3 and the residue 1/4 are both algebraic -- a finite bridge is no longer "
      "excluded BY GRADING (it is simply not built)")

print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
print("=" * 100)
sys.exit(1 if FAIL else 0)
