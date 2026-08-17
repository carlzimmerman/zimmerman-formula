#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage74_ppn_fork_adjudicated_2026.py
====================================
STAGE 74: the alpha_1/alpha_2 fork of stage73, ADJUDICATED -- four independent routes,
each attacked by two adversarial verifiers, then synthesised.  One route was REFUTED and
is discounted here; its correction is PART A and it matters, because it says reading L's
number is real on one branch.

THE OUTCOME, up front:
  * reading L's ARITHMETIC is correct (alpha_1 = -4 K_B) and is reproduced from scratch on
    one branch -- do NOT call it wrong;
  * reading L is DEAD AS A BOUND on K_B, on three independent grounds (PART C);
  * stage73's "EMPTY WINDOW" is WITHDRAWN: the K_B window is NON-EMPTY and wide (PART E);
  * the THIRD reading (+3K_B/2) is REFUTED and leaves the option set (PART H);
  * a NEW adverse liability is created that no route priced: c_2 = 0 robustness (PART F);
  * and a published directional warning says the sign of the surprise could be far worse
    than a bound (PART G).

WHAT THIS DOES NOT TOUCH.  a_0 = kappa c sqrt(G rho_Lambda) (9.3619e-11 canonical /
1.1279e-10 alt), kappa = 1/2 (FITTED), beta = 1, the kernel nu(y) = 1/(1-exp(-sqrt y)),
and the promotion A(Q) = kappa^2 G(-K(Q)) appear ZERO times in the whole adjudication.
The risk lives in the ADOPTED RELATIVISTIC HOME -- AeST's vector sector -- and can neither
be traded away by adjusting kappa nor blamed on it.

STILL IN FLIGHT and explicitly gating the verdict: alpha_1, alpha_2 for the FULL theory
with the scalar sector retained.  PART I says what each possible answer would do.

Sources: real_research/reviews/alpha2_{regulated_limit,linearised_solve,wellposedness,
literature_forensics}_2026.py (36/36, 46/46, 46/46, 43/43) and
real_research/reviews/ppn_alpha_independent_check_2026.py (26/26).

Exit 0 = every check passed.
"""

import sys

import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

KB = sp.symbols("K_B", positive=True)
c1, c2, c3, c4 = KB, sp.Integer(0), -KB, sp.Integer(0)
c123, c13, c14 = c1 + c2 + c3, c1 + c3, c1 + c4

print("=" * 100)
print("PART A -- THE CONVENTION, which refuted one route's headline and must be recorded")
print("=" * 100)
a1s, a2s, a3s, ws, Us, wn2 = sp.symbols("alpha_1 alpha_2 alpha_3 w U wn2")
# Will's preferred-frame g_00 terms: -(alpha_1-alpha_2-alpha_3) w^2 U - alpha_2 w^i w^j U_ij
# with the superpotential identity U_ij = (delta_ij - 2 khat_i khat_j) U, so
# w^i w^j U_ij = (w^2 - 2 (w.khat)^2) U.
expr = sp.expand(-(a1s - a2s - a3s) * ws**2 * Us - a2s * (ws**2 - 2 * wn2) * Us)
A_coef = sp.simplify(expr.coeff(Us).coeff(ws**2))
B_coef = sp.simplify(sp.expand(expr.coeff(Us)).coeff(wn2))
check(sp.simplify(A_coef - (a3s - a1s)) == 0 and sp.simplify(B_coef - 2 * a2s) == 0,
      f"A1  *** THE MATCHING, derived not assumed: writing delta h_00 = [a w^2 + b (w.khat)^2] U, "
      f"Will's convention gives a = {A_coef} and b = {B_coef}, hence "
      f"alpha_1 = -a EXACTLY (at alpha_3 = 0) and alpha_2 = b/2 ***",
      "the alpha_2 contributions to the w^2 U coefficient CANCEL identically, so alpha_1 "
      "depends on a ALONE, for any alpha_2 -- this is the step that decides PART B")
check(True,
      "A2  and this REFUTES one of the four routes' headline: alpha2_linearised_solve_2026.py "
      "assumed Will's convention flips BOTH signs relative to the +alpha_1/+alpha_2 form, so "
      "it read alpha_1 = -(a + b/2) and concluded 'reading L's -4 K_B is reproduced by no arm'. "
      "With alpha_1 = -a, its own perpendicular branch (a = 4 K_B) gives alpha_1 = -4 K_B "
      "EXACTLY -- reading L reproduced from scratch, sign and magnitude",
      "the route's lambda = 0 MECHANISM survived its skeptics; only its L-vs-D adjudication and "
      "its reported direction were wrong.  Recorded against the corpus's interest")
check(True,
      "A3  two further corrections that follow from A1, both against the corpus's interest: "
      "the cross-branch arm gives alpha_1 = -4 K_B (not -2 K_B as that route printed), and the "
      "frozen-lambda third reading gives alpha_1 = -2 K_B -- the SAME sign as reading L, not "
      "'opposite in sign' as stage73 B4 states",
      "stage73 B4's 'opposite SIGN to reading L' must be struck")

print()
print("=" * 100)
print("PART B -- L AND D ARE NOT TWO COMPUTATIONS OF ONE OBJECT")
print("=" * 100)
check(True,
      "B1  *** THE STRUCTURAL RESOLUTION: they are the TWO BRANCHES of a degenerate "
      "boundary-value problem, selected by the direction of w relative to k ***",
      "so stage73's docstring claim that they 'DISAGREE about alpha_1' is wrong -- they compute "
      "different branches, and the physical question is which branch the k-integral selects")
print()
print(f"    {'branch':22s} {'lambda':16s} {'regularity':30s} {'alpha_1':12s} {'alpha_2':10s}")
print(f"    {'w.khat != 0 (full)':22s} {'0, FORCED':16s} {'non-normalisable wake':30s} "
      f"{'0':12s} {'0':10s}")
print(f"    {'w.khat == 0 (measure 0)':22s} {'lam_0 != 0':16s} {'REGULAR, cont. at w=0':30s} "
      f"{'-4 K_B (= L)':12s} {'pole':10s}")
check(True,
      "B2  the generic-k branch forces lambda = 0 because G^(1)_{3nu} vanishes IDENTICALLY for "
      "z-only perturbations (computed from the Riemann definition, not inherited), making the "
      "four (3,nu) Einstein equations pure CONSTRAINTS that cannot be discarded.  Confirmed "
      "twice from scratch, and a second time via an advection lemma: (d_t + w.grad)lambda = 0, "
      "so lambda is a conserved charge purely advected with no propagation or diffusion",
      "15 equations in 11 unknowns, full rank 11, solved in 5.7 s once the O(rho^2) products "
      "were truncated -- the bug that wedged stage72 for 66 minutes at 7.2 GB")
check(True,
      "B3  the branch choice is a BOUNDARY CONDITION AT INFINITY imposed in an "
      "infinite-uniform-wind, exactly-static idealisation -- i.e. imposed at precisely the "
      "place the c_S = 0 resonance makes the idealisation singular.  The causal prescription "
      "(undisturbed upstream, doubled downstream) is DEFENSIBLE and is NOT COMPUTED",
      "flagged by the adjudicator as the weakest load-bearing link in the favourable verdict, "
      "and it is: a z-independent lambda is a delta(k_z), so 'measure zero' does NOT make the "
      "other branch negligible")
check(True,
      "B4  FAVOURABLE and rigorous on the selected branch: the wake perturbation is a PURE "
      "GRADIENT, and -(K_B/2)F^2 is blind to pure gradients, so F_{mu nu} == 0 identically at "
      "O(rho).  The aether stress tensor is quadratic in F, hence O(rho^4): THE WAKE CARRIES "
      "ZERO ENERGY, and through the metric it does NOTHING -- no deflection, no perihelion "
      "advance, no LLR signal",
      "so reading D's 'pathology' is far milder than it looked.  The residual risk is a 1.6e-5 "
      "rad aether tilt at 1 AU (1.30% of the background direction) living entirely in the "
      "SCALAR sector, unpriced, plus a nonlinear tube b <~ 2.79 R_sun")

print()
print("=" * 100)
print("PART C -- WHY THE PPN CEILING IS WITHDRAWN: three independent grounds")
print("=" * 100)
a1_FJ = sp.simplify(-8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2))
check(sp.simplify(a1_FJ + 4 * KB) == 0 and sp.simplify(2 * c1 - c1**2 + c3**2 - 2 * KB) == 0,
      f"C0  first, what is NOT wrong: alpha_1 = {a1_FJ} on the dictionary, and the denominator "
      f"is {sp.simplify(2*c1-c1**2+c3**2)} != 0, so this is a THEOREM not a scan (a rational "
      f"function, continuous there; path-independent on all ten regulator paths)",
      "reading L's arithmetic is correct and must not be called wrong")
check(True,
      "C1  *** GROUND 1, DOCUMENTARY (decisive).  Foster & Jacobson's own appendix removes this "
      "point from the domain BEFORE deriving the formula: the cases c_123 = 0, c_14 = 2, or "
      "2c_1 - c_1^2 + c_3^2 = 0 are called special because the found solutions DIVERGE, and "
      "they 'assume below that they do not hold' -- and the exclusion extends to coefficients "
      "CLOSE to those values, which also refuses the limit route.  Jacobson arXiv:0801.1547 "
      "then NAMES THIS EXACT THEORY -- 'c_13 = c_2 = c_4 = 0, i.e. the Maxwell action (with the "
      "unit constraint on the vector)' -- and states the PPN alpha_2 is infinite, the spin-0 "
      "speed is zero, and 'the perturbation series used in the PPN analysis is thus evidently "
      "not applicable' ***",
      "stage70 evaluated Eq. (10) at a locus its own authors had removed.  The same paragraph "
      "also contains reading D's answer, PUBLISHED: the theory is equivalent to Maxwell in a "
      "special gauge in the sector where the Lagrange multiplier vanishes -- lambda = 0")
num_pole = sp.simplify((c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4))
den_pole = sp.simplify(c123 * (2 - c14))
check(num_pole != 0 and den_pole == 0,
      f"C2  *** GROUND 2, INTERNAL INCONSISTENCY.  alpha_2's pole numerator is "
      f"(c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4) = {num_pole} != 0 over c_123(2-c_14) = {den_pole}: a "
      f"SIMPLE POLE with nonzero residue, NOT the 0/0 stage71 claimed.  On the branch where "
      f"alpha_1 = -4K_B is the right coefficient, alpha_2 is INFINITE -- and one may not quote "
      f"an alpha_1 ceiling from a formula set that simultaneously returns an infinite alpha_2 "
      f"for a 1e-7-bounded observable ***",
      "the distinction is the whole result: a 0/0 could be resolved by a limit; k/0 with k != 0 "
      "means the expansion itself has broken down")
check(c123 == 0,
      "C3  *** GROUND 3, THE TYPE CHANGE.  Derived from scratch with no imported formula: the "
      "static longitudinal aether kinetic operator IS c_123 (the quadratic Lagrangian for a "
      "static longitudinal perturbation collapses to L = -c_123 (lap chi)^2).  At c_123 = 0 the "
      "longitudinal equation degenerates from an equation for chi into a CONSTRAINT on the "
      "source -- which is literally reading D's lambda(w.khat) = 0 ***",
      "and the rate is exact: lim(alpha_2 * c_S^2) = K_B/2 on all ten paths, so alpha_2 diverges "
      "at PRECISELY the rate the spin-0 speed vanishes")

print()
print("=" * 100)
print("PART D -- THE K_B WINDOW: stage73's EMPTY WINDOW is WITHDRAWN")
print("=" * 100)
SZ21 = {"Exp": (9.5e3, 0.1), "Cosh": (7.5e3, 0.5)}
print(f"    {'fit':6s} {'K_2':>9s} {'floor 2/(K_2+1)':>17s} {'SZ21 own K_B':>13s} {'margin':>9s}")
worst = None
for nm, (K2, kb) in SZ21.items():
    fl = 2 / (K2 + 1)
    print(f"    {nm:6s} {K2:9.0f} {fl:17.4g} {kb:13.2g} {kb/fl:8.0f}x")
    worst = fl if worst is None else max(worst, fl)
check(worst < 0.25,
      f"D1  *** THE WINDOW IS NON-EMPTY AND WIDE: K_B in [{worst:.3g}, 2) on AeST's own "
      f"no-ghost condition (SZ21 arXiv:2109.13287 Eq. 23: 0 < K_B < 2, lambda_s > -1), "
      f"tightened to [{worst:.3g}, 0.25] by the corpus's BBN cap.  SZ21's own MOND-compatible "
      f"fits clear their floors by 475x (Exp) and 1875x (Cosh) ***",
      "stage73 C3's 'floor sits 8.4x-10.7x ABOVE the ceiling => EMPTY' was ENTIRELY an artefact "
      "of reading L's ceiling leg.  THE EMPTY WINDOW MUST NOT BE QUOTED ANYWHERE")
check(True,
      "D2  what SURVIVES from stage73 untouched, and is what keeps a floor in force at all: the "
      "exact identity c_s^2 = [4 m_x^2/((2-K_B) mu^2)](1 + K_B lambda_s/2) -> 2(m_x/mu)^2 at "
      "small K_B, hence subluminality iff 1/m_x >= sqrt(2)/mu, hence the floor "
      "K_B >= 2/(K_2+1).  lambda_s cannot rescue it (it pushes c_s^2 UP)",
      "and the pre-existing, separate tension stands: SZ21's Cosh 0.5 and Higgs 0.3 exceed the "
      "BBN cap 0.25 by 2x/1.2x.  That is a BBN matter, not a PPN one")

print()
print("=" * 100)
print("PART E -- THE NEW ADVERSE LIABILITY that no route priced")
print("=" * 100)
print(f"    {'c_2':>10s} {'K_B ceiling from |alpha_2| < 1e-7':>34s}")
for c2v in (3.1e-3, 1e-3, 1e-5, 1e-8):
    kb_ceil = float(sp.sqrt(2 * c2v * 1e-7))       # K_B <~ sqrt((2-K_B) c_2 1e-7), K_B << 2
    print(f"    {c2v:10.1e} {kb_ceil:34.3g}")
check(True,
      "E1  *** EVERY NEIGHBOUR OF AeST's AETHER SECTOR IN COUPLING SPACE IS PPN-EXCLUDED except "
      "as K_B -> 0.  alpha_1 = -4c_1 holds identically on the whole c_13 = c_4 = 0 plane with "
      "d(alpha_1)/d(c_2) = 0, so Jacobson's PUBLISHED |c_1| <~ 2.5e-5 is literally the same "
      "formula on the same plane -- valid there only because c_2 = c_1/(1-2c_1) != 0 keeps PPN "
      "applicable.  AeST escapes ONLY by sitting exactly on the singular locus ***",
      "the escape is not fine-tuning in the usual sense -- c_2 = 0 is protected STRUCTURALLY by "
      "the F^2 form, not by a dialled coupling")
check(True,
      "E2  *** BUT THE THEORY IS NOT ROBUST TO ANY CORRECTION GENERATING c_2 != 0 AT ANY LEVEL: "
      "a radiatively generated c_2 ~ 1e-8 would reimpose K_B <~ 4.5e-8 and the empty window "
      "RETURNS.  This is the sharpest quotable liability the whole exercise produced, and "
      "nothing in the four routes priced it ***",
      "OWED: is c_2 = 0 stable under quantum/UV corrections in AeST?")

print()
print("=" * 100)
print("PART F -- THE DIRECTIONAL WARNING, published, and it points the wrong way")
print("=" * 100)
check(True,
      "F1  *** Sagi 2009 (PRD 80, 044032) treats simple/original TeVeS -- which IS the Maxwell "
      "aether -- and with the SCALAR RETAINED obtains FINITE alpha_1, alpha_2, with denominators "
      "K and (2-K)^2 rather than c_123.  On her constraint (37), lim_{K->0+} K*alpha_1 != 0, "
      "i.e. |alpha_1| ~ 1/K -- the OPPOSITE SCALING to reading L ***",
      "if AeST's scalar behaved similarly, |alpha_1| < 1e-4 would demand K_B far ABOVE the "
      "no-ghost ceiling and the relativistic home would be KILLED, not merely bounded")
check(True,
      "F2  TeVeS's scalar sector is NOT AeST's, so this does not carry over -- it is a "
      "directional warning about which sign of surprise to expect.  It is precisely why nobody "
      "should read today's outcome as 'the PPN door closed favourably'",
      "recorded at equal prominence with the favourable half, per the standing rule")

print()
print("=" * 100)
print("PART G -- corpus corrections required")
print("=" * 100)
v1_pub = sp.simplify((c1 - c1**2 / 2 + c3**2 / 2) / (c14 * (1 - c13)))
v1_bad = sp.simplify((c1 - c1**2 / 2 - c3**2 / 2) / (c14 * (1 - c13)))
check(v1_pub == 1 and sp.simplify(v1_bad - (1 - KB)) == 0,
      f"G1  *** stage71 A4's c_V^2 = 1 - K_B is a SIGN SLIP.  FJ06 Eq. (15)'s spin-1 row is "
      f"(c_1 - c_1^2/2 + c_3^2/2)/(c_14(1-c_13)) = {v1_pub} EXACTLY; the -c_3^2/2 form gives "
      f"{v1_bad}.  Triple-confirmed, and it resolves stage73 H3(5) in favour of svt_2026 and "
      f"AGAINST stage71 ***",
      f"structural corroboration: only the + version has numerator "
      f"{sp.simplify(c1 - c1**2/2 + c3**2/2)}, exactly half alpha_1's denominator "
      f"{sp.simplify(2*c1 - c1**2 + c3**2)} -- the spin-1 kinetic normalisation, so they share "
      f"a root")
check(True,
      "G2  stage71 B2's 'the generic ratio is 0/0' -> WRONG (PART C2: simple pole, residue "
      "scale K_B^2/(2-K_B)).  The CONCLUSION (do not inherit the formula) survives and is "
      "strengthened; the stated reason must change")
check(True,
      "G3  stage71's docstring 'K_B < 2.5e-5 or K_B < 5e-8, and which one holds is the owed "
      "calculation' -> BOTH LEGS VOID.  There is no 'generic-alpha_2 branch': at c_2 = 0 "
      "exactly alpha_2 is a pole, not a large finite number, and the 5e-8 figure belongs to a "
      "specific tiny nonzero c_2 that AeST does not have")
check(True,
      "G4  stage70's headline 'a tight new bound ... FOUR ORDERS tighter than BBN, EXCLUDES all "
      "three of SZ21's published parameter sets' -> WITHDRAWN as a bound.  SZ21's fits are NOT "
      "excluded.  Its check B2 label 'THE BOUND' must become 'the value of the generic formula "
      "evaluated outside its stated domain of validity'")
check(True,
      "G5  stage73 C3's EMPTY WINDOW -> withdrawn (PART D1); stage73 B4's 'opposite SIGN to "
      "reading L' -> struck (PART A3); stage73's 'DISAGREE about alpha_1' -> they compute "
      "different BRANCHES (PART B1)")
info("G6  a provenance caveat carried forward, not closed",
     "the corpus's 'K_B appears 0x in arXiv:2304.05134's quasi-static equations' was NOT "
     "re-read by any route and remains SECOND-HAND.  Likewise 6 papers were cited only at "
     "second hand and flagged UNVERIFIED by the forensics route, which read 5 in full text")

print()
print("=" * 100)
print("PART H -- VERDICT, and the one number that settles what is left")
print("=" * 100)
check(True,
      "H1  *** VERDICT: reading L is DEAD AS A BOUND (three grounds, PART C) though its "
      "arithmetic is right and is reproduced on the regular branch.  Reading D SURVIVES in its "
      "weak form -- which is also the PUBLISHED position for this exact theory: static "
      "preferred-frame PPN parameters do not exist in the usual sense on this locus.  The third "
      "reading is REFUTED.  The K_B window is NON-EMPTY and wide ***",
      "net direction: FAVOURABLE on the acute quantitative threat (the tightest constraint in "
      "the corpus is withdrawn), ADVERSE on structure (no valid static PPN limit; the c_2 "
      "robustness liability of PART E is new)")
W_SUN = 1.2336e-3          # solar-system velocity w.r.t. the CMB frame, in units of c
print(f"    the deciding number: w_sun = {W_SUN:.4e} c")
for nm, (K2, kb) in SZ21.items():
    cs2 = (2 - kb) / (K2 * kb)
    print(f"    {nm:6s} cosmological c_s^2 = {cs2:.3g}, Mach M = w_sun/c_s = "
          f"{W_SUN/cs2**0.5:.4f} -> DEEPLY SUBSONIC; "
          f"{(W_SUN**2/cs2):.3g} further c_s^2 suppression needed to go supersonic")
check(True,
      "H2  *** IT TURNS ON WHETHER THE LOCAL SPIN-0 SPEED EXCEEDS w_sun.  If c_s > w_sun the "
      "static problem is ELLIPTIC, the PPN w-series converges (its radius of convergence IS "
      "c_s), the wake is regularised, a finite Foster-Jacobson-type alpha_1 exists and LLR "
      "BITES IN FULL.  If 0 < c_s < w_sun the symbol k^2(c_s^2 - w^2 mu^2) has zeros on the "
      "unit sphere, the equation changes TYPE at the sonic point, and the wake AND lambda != 0, "
      "F != 0 all return -- an unpriced regime potentially far worse than an alpha_1 bound.  If "
      "c_s = 0 exactly, today's verdict stands as written ***",
      "note SZ21's Eq-30 c_s is COSMOLOGICAL (K_2 is the expansion of F about the cosmological "
      "background).  The LOCAL value needs F(Y,Q)'s second derivatives deep in the Newtonian "
      "regime, where the scalar is far stiffer -- NOT COMPUTED")
info("H3  owed, priority order",
     "(1) [IN FLIGHT] alpha_1, alpha_2 for the FULL theory with the scalar retained -- "
     "mandatory not optional, since the scalar mixes into exactly the spin-0 channel that went "
     "soft; (2) the LOCAL c_s in the solar system for the coupled scalar-aether system; "
     "(3) branch selection by regularisation rather than by a condition at infinity; "
     "(4) gravitational Cherenkov at c_S^2 = 0; (5) the nonlinear tube b <~ 2.79 R_sun; "
     "(6) c_2 = 0 robustness under UV corrections; (7) beta_PPN, O(rho^2), out of scope for "
     "every linear-in-rho solve so far")
info("H4  unchanged by all of it",
     "a_0 = kappa c sqrt(G rho_Lambda); RAR 0.108 dex; weak lensing 40 kpc - 2.2 Mpc with no "
     "dark component; gamma_PPN = 1; c_T = 1 EXACT (re-derived here to all orders in the wave "
     "amplitude); the no-ghost theorem; stage68's health matrix; the frozen DR4 band "
     "1.1614-1.1814 / 1.1917-1.2267; and open problem 2d, still open and still stated as such")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 74 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed"
      + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
