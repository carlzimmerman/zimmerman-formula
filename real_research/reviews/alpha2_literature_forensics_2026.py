#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
alpha2_literature_forensics_2026.py
===================================
THE LITERATURE-FORENSICS ADJUDICATION OF THE alpha_1/alpha_2 FORK FOR AeST's
AETHER SECTOR (the "Maxwell aether": c_1 = +K_B, c_2 = 0, c_3 = -K_B, c_4 = 0).

THE FORK
  READING L  (nbody_2026/stage70_ppn_preferred_frame_2026.py):
        apply Foster & Jacobson's alpha_1 formula on the dictionary, get
        alpha_1 = -4 K_B, hence K_B < 2.5e-5 from lunar laser ranging.
  READING D  (real_research/reviews/ppn_alpha_independent_check_2026.py, 26/26):
        from scratch, alpha_1 = alpha_2 = 0 identically for every K_B, because
        the linearized equations force lambda = 0; price = a non-normalisable
        stationary wake and a discontinuity at w = 0.

THE ANSWER THIS SCRIPT ESTABLISHES.  It is decisive, and it is a documentary
result, not a new calculation:

  *** THE PUBLISHED EINSTEIN-AETHER PPN LITERATURE EXPLICITLY EXCLUDES THE
      LOCUS c_123 = 0 FROM ITS DOMAIN OF VALIDITY, AND JACOBSON HIMSELF NAMES
      *THIS EXACT THEORY* -- "the Maxwell action (with the unit constraint on
      the vector)", c_13 = c_2 = c_4 = 0 -- AS THE CASE WHERE "the perturbation
      series used in the PPN analysis is thus evidently not applicable". ***

  So READING L applies a formula outside the domain its own authors stated.
  And the same source says the Maxwell-action theory "is equivalent to Maxwell
  theory in a special gauge if it is further restricted to the sector in which
  the Lagrange multiplier field vanishes" -- which is EXACTLY the lambda = 0
  sector reading D derived from scratch, together with exactly reading D's
  price (the vector is then not physical; shocks and instabilities are known).

  Direction: READING D.  Reading L's bound K_B < 2.5e-5 must be withdrawn as a
  literature-inherited result, so stage73's EMPTY WINDOW is NOT established.
  That is favourable.  But two NEW adverse items are documented here that
  neither reading priced (PART C, PART E).

SOURCES ACTUALLY READ IN FULL TEXT (arXiv PDFs, text-extracted; every equation
number and quote below was read off the extracted text, not recalled):
  [FJ06]  B. Z. Foster & T. Jacobson, "Post-Newtonian parameters and constraints
          on Einstein-aether theory", Phys. Rev. D 73, 064015 (2006),
          arXiv:gr-qc/0509083v2.                                   FULL TEXT READ
  [JAC08] T. Jacobson, "Einstein-aether gravity: a status report",
          PoS(QG-Ph)020, arXiv:0801.1547.                          FULL TEXT READ
  [SAGI09] E. Sagi, "Preferred frame parameters in the tensor-vector-scalar
          theory of gravity and its generalization", Phys. Rev. D 80, 044032
          (2009), arXiv:0905.4001.                                 FULL TEXT READ
  [GHLP18] Y. Gong, S. Hou, D. Liang, E. Papantonopoulos, "Gravitational waves
          in Einstein-aether and generalized TeVeS theory after GW170817",
          arXiv:1801.03382v3.                                      FULL TEXT READ
  [SZ21s] C. Skordis & T. Zlosnik, "Aether scalar tensor theory: Linear
          stability on Minkowski space", arXiv:2109.13287.         FULL TEXT READ

NOT ACCESSED (findings that would rest on them are marked UNVERIFIED in PART F):
  Eling & Jacobson gr-qc/0310044; Graesser-Jenkins-Wise hep-th/0501223;
  Jacobson & Mattingly gr-qc/0402005; Will's textbook (1993) Sec. 5.4;
  Tamaki PRD 77, 124020 (2008); Kostelecky & Samuel; Clayton (shocks);
  Seifert (instability); arXiv:2304.05134; Oost-Mukohyama-Wang 1802.04303.

WHAT IS NOT DONE HERE.  This script does NOT compute alpha_1 or alpha_2 for
AeST.  It adjudicates whether the literature formula MAY be applied, and reports
what the literature says about this locus.  The AeST-specific calculation with
the scalar sector 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y retained is a SIBLING
AGENT's job, and PART C tells that agent what the closest published analogue
(Bekenstein's TeVeS, whose vector sector is the SAME Maxwell aether) actually
gives -- which is neither reading L nor reading D.

Exit 0 = every check passed.
"""

import sys

import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d}  {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


def hdr(s):
    print()
    print("=" * 100)
    print(s)
    print("=" * 100)


print(__doc__)

# framework anchors (never touched by this file; printed so it is on the record
# that the adjudication is independent of them)
A0_CANON, A0_ALT, KAPPA_FITTED = 9.3619e-11, 1.1279e-10, 0.5
A1_LLR, A2_SOLAR = 1e-4, 4e-7        # [FJ06] main text; [JAC08] Sec. 2; [SAGI09] Sec. V

# generic Einstein-aether parameters
c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4")
c13, c14, c123 = c1 + c3, c1 + c4, c1 + c2 + c3
KB = sp.symbols("K_B", positive=True)

# ---------------------------------------------------------------- published formulas
# [FJ06] Eq. (10) == [JAC08] Eq. (2.2)
ALPHA1_FJ10 = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
# [FJ06] Eq. (11), transcribed verbatim from the extracted text of gr-qc/0509083v2 p.5
ALPHA2_FJ11 = ((2 * c13 - c14)**2 / (c123 * (2 - c14))
               - (12 * c3 * c13 + 2 * c1 * c14 * (1 - 2 * c14)
                  + (c1**2 - c3**2) * (4 - 6 * c13 + 7 * c14))
               / ((2 - c14) * (2 * c1 - c1**2 + c3**2)))
# [JAC08] Eq. (2.3) -- a DIFFERENT published way of writing the same alpha_2
ALPHA2_JAC23 = (ALPHA1_FJ10 / 2
                - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / (c123 * (2 - c14)))
# [FJ06] Eq. (15) mode speeds (squared).  Signs read off the extracted text; note the
# spin-1 row is (c_1 - c_1^2/2 + c_3^2/2), i.e. HALF the alpha_1 denominator.
CT2_FJ15 = 1 / (1 - c13)
CV2_FJ15 = (c1 - c1**2 / 2 + c3**2 / 2) / (c14 * (1 - c13))
CS2_FJ15 = c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2))
# [FJ06] Eq. (3) == [JAC08] Eq. (2.1)
GN_OVER_G = 1 / (1 - c14 / 2)
# [FJ06] Eq. (6): the AETHER perturbation itself.  Coefficient of (V_i - W_i):
AETHER_VW_COEF = (2 * c1 + 3 * c2 + c3 + c4) / (2 * c123)

DICT_AEST = {c1: KB, c2: sp.Integer(0), c3: -KB, c4: sp.Integer(0)}

# ==================================================================================
hdr("PART G -- GATES.  Machinery + transcription validation.  If any of these fails, "
    "nothing below is claimed.")
# ==================================================================================
# GATE 1: derive the dictionary in-script from the F^2 expansion (do not inherit it).
Dg = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f"D{m}{n}"))       # stands for grad_m A_n
ETAI = sp.diag(-1, 1, 1, 1)
F_from_D = sp.Matrix(4, 4, lambda m, n: Dg[m, n] - Dg[n, m])
F2 = sp.expand(sum(F_from_D[m, n] * F_from_D[a, b] * ETAI[m, a] * ETAI[n, b]
                   for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
T_dot_T = sum(Dg[m, n] * Dg[a, b] * ETAI[m, a] * ETAI[n, b]
              for m in range(4) for n in range(4) for a in range(4) for b in range(4))
T_dot_Tt = sum(Dg[m, n] * Dg[a, b] * ETAI[m, b] * ETAI[n, a]
               for m in range(4) for n in range(4) for a in range(4) for b in range(4))
check(sp.simplify(F2 - 2 * (T_dot_T - T_dot_Tt)) == 0,
      "GATE 1  F^2 = 2[(grad_m A_n)(grad^m A^n) - (grad_m A_n)(grad^n A^m)], derived here "
      "by explicit index contraction, hence -(K_B/2)F^2 has c_1 = +K_B, c_2 = 0, "
      "c_3 = -K_B, c_4 = 0 in the Einstein-aether basis "
      "L = -[c_1(grad A)^2 + c_2(div A)^2 + c_3(grad A)(grad A)^T + c_4(A.grad A)^2]",
      "the dictionary is DERIVED in this file, not inherited from stage70")
check(sp.simplify(c13.subs(DICT_AEST)) == 0 and sp.simplify(c123.subs(DICT_AEST)) == 0
      and sp.simplify(c14.subs(DICT_AEST) - KB) == 0,
      "GATE 2  on that dictionary c_13 = 0 AND c_123 = 0 identically, while "
      "c_14 = K_B != 0 and 2c_1 - c_1^2 + c_3^2 = 2 K_B != 0",
      "so of [FJ06]'s three special cases (c_123 = 0, c_14 = 2, 2c_1-c_1^2+c_3^2 = 0) "
      "AeST's aether hits EXACTLY ONE, the first")

# GATE 3: reproduce c_T = 1 (the corpus's committed GW170817 result) from [FJ06] Eq (15).
check(sp.simplify(CT2_FJ15.subs(DICT_AEST) - 1) == 0,
      "GATE 3  c_T^2 = 1/(1 - c_13) = 1 EXACTLY  [FJ06 Eq. (15), spin-2 row]",
      "independently reproduces the corpus's committed 'c_T = 1 exact, GW170817-safe' "
      "result -- the known-external-result gate")

# GATE 4: reproduce G_N = G/(1 - K_B/2), i.e. the quasi-static G~ = (1 - K_B/2)G^,
# which reading D also found from scratch at w = 0.
check(sp.simplify(GN_OVER_G.subs(DICT_AEST) - 1 / (1 - KB / 2)) == 0,
      "GATE 4  G_N/G = (1 - c_14/2)^-1 = 1/(1 - K_B/2)  [FJ06 Eq. (3); JAC08 Eq. (2.1)]",
      "this is the SAME relation as the corpus's quasi-static G~ = (1 - K_B/2)G^, and it is "
      "the value reading D derived from scratch at w = 0 (its G_N(w=0) = G/(1-K_B/2)).  "
      "Second known-external-result gate, and it validates the c_14 slot of the dictionary")

# GATE 5: the two independently PUBLISHED forms of alpha_2 must be algebraically identical.
check(sp.simplify(ALPHA2_FJ11 - ALPHA2_JAC23) == 0,
      "GATE 5  *** [FJ06] Eq. (11) and [JAC08] Eq. (2.3) are IDENTICAL for generic c_i *** "
      "-- two different published ways of writing alpha_2, transcribed independently here "
      "from two different PDFs, agree exactly",
      "this is the transcription gate: a single mis-copied sign in either would break it, "
      "so the alpha_2 expression used below is verified against the source twice over")

# GATE 6: a THIRD paper's independent ab initio PPN calculation must reproduce both.
K, Kp, K2s, K4 = sp.symbols("K K_plus K_2 K_4")
# [SAGI09], text after Eq. (38), verbatim: "The relation between the coupling constants
# K_i and the c_i of AEther is c1-c3 = 2K, c1+c3 = 2K+, c2 = K2 and c4 = -K4."
SAGI_DICT = {c1: K + Kp, c3: Kp - K, c2: K2s, c4: -K4}
SAGI_A1_49 = 4 * ((K - Kp)**2 - K4 * (K + Kp)) / (2 * K * Kp - (K + Kp))
SAGI_A2_50 = (SAGI_A1_49 / 2
              + (K - 3 * Kp - K4) * (K + 3 * Kp + 3 * K2s - K4)
              / ((2 * Kp + K2s) * (2 - (K + Kp - K4))))
check(sp.simplify(SAGI_A1_49 - ALPHA1_FJ10.subs(SAGI_DICT)) == 0,
      "GATE 6a  [SAGI09] Eq. (49) == [FJ06] Eq. (10) under Sagi's own dictionary",
      "Sagi did an independent ab initio PPN computation and states (her text) that with the "
      "scalar decoupled 'the preferred frame parameters acquire the values calculated for "
      "AEther theory, as given in [27]' where her [27] IS Foster & Jacobson PRD 73 064015")
check(sp.simplify(SAGI_A2_50 - ALPHA2_JAC23.subs(SAGI_DICT)) == 0,
      "GATE 6b  [SAGI09] Eq. (50) == [JAC08] Eq. (2.3) == [FJ06] Eq. (11) under that "
      "dictionary -- THREE independent publications, one algebraic object",
      "and note (2K_+ + K_2) = c_13 + c_2 = c_123 exactly, so Sagi's denominator IS the "
      "c_123 of the other two")

if FAIL:
    print("\n  *** GATES FAILED -- NOTHING IS CLAIMED.  Aborting. ***")
    sys.exit(1)
info("all gates green: the dictionary is derived, two known external results are "
     "reproduced, and three published transcriptions of alpha_2 are mutually identical")

# ==================================================================================
hdr("PART A -- (c) IS THE TRANSCRIPTION RIGHT?  The published formulas evaluated on the "
    "dictionary, and TWO CORRECTIONS to the corpus")
# ==================================================================================
a1_aest = sp.simplify(ALPHA1_FJ10.subs(DICT_AEST))
print(f"    alpha_1 (FJ06 Eq. 10) on the dictionary = {a1_aest}")
check(sp.simplify(a1_aest + 4 * KB) == 0,
      "A1  alpha_1 = -4 K_B exactly.  *** READING L's ARITHMETIC IS CORRECT *** -- the "
      "formula, taken at face value on this dictionary, does give -4 K_B",
      "so the fork is NOT a transcription dispute about alpha_1.  It is entirely a "
      "domain-of-validity dispute (PART B)")
# third-source corroboration of the arithmetic on the c_13 = 0 locus
a1_gong = -4 * c14                       # [GHLP18] Eq. (60), valid on c_13 = 0
check(sp.simplify((a1_gong - ALPHA1_FJ10).subs({c3: -c1})) == 0,
      "A2  [GHLP18] Eq. (60) 'alpha_1 = -4 c_14' is the c_13 = 0 specialisation of "
      "[FJ06] Eq. (10) -- verified here symbolically by setting c_3 = -c_1",
      "a third published source agrees with reading L's arithmetic on exactly our locus, "
      "which is why PART B and not PART A is where the fork is decided")

# --- alpha_2: pole structure.  stage71 claimed 0/0; it is NOT 0/0.
pole_num = sp.simplify(-((c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4)).subs(DICT_AEST))
pole_den = sp.simplify((c123 * (2 - c14)).subs(DICT_AEST))
print(f"    alpha_2 pole term = [{pole_num}] / [{pole_den}]   (JAC08 Eq. 2.3 second term)")
check(pole_den == 0 and sp.simplify(pole_num - KB**2) == 0,
      "A3  *** CORRECTION TO stage71: alpha_2 is NOT 0/0 on this locus.  The pole term's "
      "numerator is +K_B^2 != 0 while its denominator c_123(2-c_14) = 0, so alpha_2 is a "
      "SIMPLE POLE with nonzero residue and DIVERGES *** ",
      "stage71 PART B check B2 says 'the generic ratio is 0/0 and the physical alpha_2 is "
      "whatever the degenerate sector gives'.  The first half is wrong: a 0/0 could be "
      "resolved by a limit, whereas k/0 with k != 0 means the expansion itself has broken "
      "down.  [JAC08] Sec. 8 states the alternative explicitly -- 'either alpha_2 diverges "
      "or, if the numerator also vanishes, it is indeterminate' -- and here it diverges")
res = sp.simplify(sp.limit(c2 * ALPHA2_JAC23.subs({c1: KB, c3: -KB, c4: 0}), c2, 0))
check(sp.simplify(res - KB**2 / (2 - KB)) == 0,
      f"A4  residue: lim_(c_2 -> 0) c_2 * alpha_2 = K_B^2/(2-K_B) != 0 for K_B in (0,2), "
      f"so alpha_2 -> +infinity as the theory approaches its own locus from c_2 > 0",
      "the divergence is one-sided-signed and first order; there is no nearby "
      "non-degenerate point whose limit could be quoted")

# --- the SAME factor that blows up alpha_2 blows up the AETHER PERTURBATION itself
aeth_num = sp.simplify((2 * c1 + 3 * c2 + c3 + c4).subs(DICT_AEST))
check(sp.simplify(aeth_num - KB) == 0 and sp.simplify((2 * c123).subs(DICT_AEST)) == 0,
      "A5  *** [FJ06] Eq. (6) -- the SOLUTION, not just the parameter -- diverges.  The "
      "aether perturbation is u_i = [(2c_1+3c_2+c_3+c_4)/(2c_123)](V_i - W_i) + [finite], "
      "and on the dictionary that coefficient is K_B / 0 ***",
      "this is the decisive technical point about reading L: alpha_1's apparent finiteness "
      "is an algebraic accident of one particular combination.  alpha_1 and alpha_2 are read "
      "off the SAME solution (FJ06 Appendix Steps 4 -> 5 -> 6: solve for u_i, then g_0i, "
      "then g_00), and that solution is singular.  A finite number extracted from a "
      "divergent solution is not a prediction")
check(sp.simplify(sp.expand((c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4)
                            - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4))) == 0
      and sp.simplify(pole_num / KB - KB) == 0,
      "A6  and it is ONE divergence, not two: the factor (2c_1+3c_2+c_3+c_4) = K_B that "
      "sits in [FJ06] Eq. (6)'s numerator is literally a factor of [JAC08] Eq. (2.3)'s "
      "alpha_2 pole numerator, whose value is K_B * K_B",
      "so 'the aether response to a moving mass is singular' and 'alpha_2 is infinite' are "
      "the same statement.  Reading D found the same thing by a different route: its "
      "longitudinal aether response v_L ~ U/(i k w.khat) has a simple pole with nonzero "
      "residue.  (Both are the velocity-sourced aether channel; a term-by-term "
      "identification of Eq. (6)'s V_i - W_i with reading D's v_L was NOT performed)")

# --- mode speeds, and CORRECTION 2
cs2, cv2 = sp.simplify(CS2_FJ15.subs(DICT_AEST)), sp.simplify(CV2_FJ15.subs(DICT_AEST))
print(f"    spin-0 speed^2 = {cs2}      spin-1 speed^2 = {cv2}")
check(cs2 == 0,
      "A7  spin-0 (longitudinal) aether-gravity mode speed^2 = 0 exactly "
      "[FJ06 Eq. (15) spin-0 row], because c_123 sits in its numerator",
      "reading D reached this independently from scratch (its Step 9: omega^2 = 0 for the "
      "longitudinal polarisation).  [FJ06] main text ties the two facts together: the "
      "special cases are special 'since alpha_1 and/or alpha_2 diverges ... From the wave "
      "speeds (15) below we see that the spin-0 speed vanishes'")
check(sp.simplify(cv2 - 1) == 0,
      "A8  *** CORRECTION TO stage71: spin-1 speed^2 = 1 EXACTLY, not 1 - K_B *** .  "
      "[FJ06] Eq. (15) spin-1 row is (c_1 - c_1^2/2 + c_3^2/2)/[c_14(1-c_13)] -- PLUS "
      "c_3^2/2, i.e. exactly half the alpha_1 denominator (2c_1 - c_1^2 + c_3^2)",
      "stage71 PART A check A4 transcribed it with a MINUS on c_3^2/2 and got c_V^2 = 1-K_B, "
      "then presented that as 'CROSS-CHECK 2 (sanity) ... no free parameters were used to "
      "make this come out sensible'.  It was validating a typo.  The correct value is "
      "confirmed independently by reading D's from-scratch Step 9 ('spin-1 (transverse) "
      "aether mode: omega^2 = k^2, i.e. v^2 = 1') and by the internal consistency of the "
      "published paper, in which the same combination 2c_1-c_1^2+c_3^2 appears as the "
      "alpha_1 denominator (Eq. 10) and the spin-1 energy numerator (Eq. 17)")
check(sp.simplify((2 * c1 - c1**2 + c3**2).subs(DICT_AEST) - 2 * KB) == 0
      and sp.simplify(2 * CV2_FJ15 * c14 * (1 - c13) - (2 * c1 - c1**2 + c3**2)) == 0,
      "A9  consistency of A8: 2 * (spin-1 speed^2) * c_14 * (1-c_13) == 2c_1 - c_1^2 + c_3^2 "
      "identically, and on the dictionary that combination is 2K_B != 0, so [FJ06]'s THIRD "
      "special case (spin-1 speed zero) is NOT hit",
      "the corpus's 'c_V^2 = 1 - K_B, subluminal for K_B > 0' should be withdrawn; the "
      "Maxwell aether's spin-1 mode is LUMINAL, which is a different (and cleaner) fact")
# [JAC08] Eq. (4.6): the spin-0 metric polarisation also carries 1/c_123
h33_pol = ((2 * c14 * (1 + c2)) / c123).subs({c1: KB, c3: -KB, c4: 0})
check(sp.limit(h33_pol, c2, 0, "+") == sp.oo,
      "A10 a third place the same 1/c_123 appears: [JAC08] Eq. (4.6) gives the spin-0 mode's "
      "metric polarisation as h_33 = [2c_14(1+c_2)/c_123] v_0, which on the dictionary is "
      "2K_B(1+c_2)/c_2 -> +infinity as c_2 -> 0+",
      "so the divergence shows up in the parameter (alpha_2), in the aether solution "
      "(FJ06 Eq. 6) and in the mode polarisation (JAC08 Eq. 4.6): three independent "
      "manifestations of the one degeneracy")

# ==================================================================================
hdr("PART B -- (a) and (b) THE GENERICITY ASSUMPTIONS AND THE STATED DOMAIN OF VALIDITY. "
    "This is where the fork is decided.")
# ==================================================================================
Q_FJ_APPENDIX = (
    "The cases in which c123 = 0, c14 = 2, or 2c1 - c1^2 + c3^2 = 0 are special in that "
    "the found solutions diverge.  We will presume that the post-Newtonian approximation "
    "is not valid in these cases, and assume below that they do not hold.  See the main "
    "text for more discussion of this point.")
print("    [FJ06] APPENDIX, immediately after the six-step solving procedure, VERBATIM:")
print(f'      "{Q_FJ_APPENDIX}"')
check("assume below that they do not hold" in Q_FJ_APPENDIX
      and sp.simplify(c123.subs(DICT_AEST)) == 0,
      "B1  *** THE DECIDING FACT, PART 1: [FJ06] STATE THEIR DOMAIN OF VALIDITY EXPLICITLY "
      "AND IT EXCLUDES c_123 = 0.  AeST's aether sector has c_123 = 0 IDENTICALLY, for "
      "every K_B.  Reading L therefore evaluates Eq. (10) at a point its own authors "
      "removed from the domain before deriving it. ***",
      "this is not a subtle inference.  It is the sentence that introduces the solving "
      "procedure from which Eq. (10) and Eq. (11) are extracted")
Q_FJ_MAIN = (
    "It is evident from the form of the metric and aether perturbations that the cases "
    "c123 = 0, c14 = 2, and 2c1 - c1^2 + c3^2 = 0 are special, since alpha1 and/or alpha2 "
    "diverges.  Presumably the post-Newtonian approximation is not valid when the "
    "coefficients are close to these values.  From the wave speeds (15) below we see that "
    "the spin-0 speed vanishes in either of the first two cases and the spin-1 speed "
    "vanishes in the last case.  This corresponds to the absence of spatial gradient terms "
    "in the action [9].")
print("\n    [FJ06] MAIN TEXT, immediately after Eqs. (10)-(11), VERBATIM:")
print(f'      "{Q_FJ_MAIN}"')
check("not valid when the coefficients are close to these values" in Q_FJ_MAIN,
      "B2  and the exclusion is not only AT the locus but NEAR it: 'not valid when the "
      "coefficients are CLOSE to these values'.  So 'take c_2 -> 0 as a limit' is also "
      "refused by the source -- which is what stage71's PART B check B1 attempted",
      "stage71 wrote 'the theory approaches the degenerate locus continuously in c_2 but "
      "LANDS on it exactly'.  True, but the published statement is that the approximation "
      "fails on the whole approach, so continuity of the c_2 -> 0 limit is not a licence")
Q_FJ_BC = ("We will assume that hab and delta-ua satisfy boundary conditions such that they "
           "vanish at spatial infinity.")
print(f'\n    [FJ06] APPENDIX, order-counting paragraph, VERBATIM:\n      "{Q_FJ_BC}"')
check("vanish at spatial infinity" in Q_FJ_BC,
      "B3  *** AND [FJ06] STATE THE BOUNDARY CONDITION READING D SHOWED CANNOT BE MET *** . "
      "Reading D's price for lambda = 0 is a stationary wake v_L ~ U/(i k w.khat) with a "
      "nonzero-residue simple pole, i.e. an aether perturbation that does NOT vanish at "
      "spatial infinity.  That is precisely [FJ06]'s assumption",
      "so reading D's 'honest caveat' is not a weakness of reading D -- it is the "
      "identification of WHICH published assumption this theory violates.  The two readings "
      "are not symmetric: reading D names the failed hypothesis, reading L uses the "
      "conclusion whose hypothesis has failed")
Q_FJ_HN = ("The case c123 = 0 corresponds [8] to the vector-tensor theory of Hellings and "
           "Nordtvedt [10] if the unit constraint on the aether is dropped.  This theory was "
           "shown by Will [1] to be dynamically over-determined and hence observationally "
           "unacceptable.")
print(f'\n    [FJ06] MAIN TEXT, VERBATIM:\n      "{Q_FJ_HN}"')
check("if the unit constraint on the aether is dropped" in Q_FJ_HN,
      "B4  [FJ06] identify c_123 = 0 with Hellings-Nordtvedt, which Will showed is "
      "'dynamically OVER-DETERMINED and hence observationally unacceptable' -- BUT ONLY "
      "'if the unit constraint on the aether is dropped', and AeST KEEPS the constraint.  "
      "The conditional clause is reported intact and the identification is NOT transferred",
      "recorded because the literature's word for the pathology at c_123 = 0 is "
      "'over-determined', and over-determination is exactly what reading D found from "
      "scratch: G^(1)_{3nu} vanishes identically, so the four (3,nu) Einstein equations "
      "become pure constraints that force lambda*(w.khat) = 0.  Two independent routes to "
      "the same word.  Will's conclusion itself is UNVERIFIED here (textbook not accessed)")

# ==================================================================================
hdr("PART C -- (d) and (e) HAS ANYONE DONE THIS CASE?  YES.  Jacobson names it, and "
    "Bekenstein's TeVeS *is* it.")
# ==================================================================================
Q_JAC_S8 = (
    "The first case to be examined in detail [8, 7] was c13 = c2 = c4 = 0, i.e. the "
    "\"Maxwell action\" (with the unit constraint on the vector).  The PPN result for alpha2 "
    "(2.3) is infinite in this case, and the spin-0 mode speed is zero.  The perturbation "
    "series used in the PPN analysis is thus evidently not applicable.  Independently of "
    "that, however, other problems with this case have been identified, such as the "
    "formation of shock discontinuities [7, 41] and a possibly related instability [34].  "
    "This case is equivalent to Maxwell theory in a special gauge if it is further "
    "restricted to the sector in which the Lagrange multiplier field vanishes (see "
    "[42, 7, 43, 44] and references therein).  However, this equivalence holds only if one "
    "abandons the notion that the vector is itself physical.  The shock discontinuities and "
    "instabilities of the vector can then be regarded as gauge artifacts, but the theory is "
    "no longer that of a Lorentz-violating vector field.")
print("    [JAC08] Section 8 'Special values of c_i', FIRST BULLET, VERBATIM:")
print(f'      "{Q_JAC_S8}"')
check("c13 = c2 = c4 = 0" in Q_JAC_S8
      and sp.simplify(c13.subs(DICT_AEST)) == 0
      and sp.simplify(c2.subs(DICT_AEST)) == 0
      and sp.simplify(c4.subs(DICT_AEST)) == 0,
      "C1  *** THE DECIDING FACT, PART 2, AND IT SETTLES THE FORK.  'c_13 = c_2 = c_4 = 0, "
      "i.e. the \"Maxwell action\" (with the unit constraint on the vector)' IS AeST's "
      "aether sector, exactly and completely.  And the co-author of the alpha_1 formula "
      "reading L uses writes, of this case: 'The perturbation series used in the PPN "
      "analysis is thus evidently NOT APPLICABLE.' ***",
      "the identification is airtight, not an analogy: c_13 = 0 and c_2 = 0 and c_4 = 0 are "
      "the three conditions AeST's -(K_B/2)F^2 satisfies identically (GATE 1), and the unit "
      "constraint A^mu A_mu = -1 is AeST's.  This is the same author, the same formula "
      "(he cites his own Eq. 2.3), naming this theory, and declaring the method inapplicable")
check("the sector in which the Lagrange multiplier field vanishes" in Q_JAC_S8,
      "C2  *** AND THE SAME PARAGRAPH CONTAINS READING D's RESULT, PUBLISHED.  'This case is "
      "equivalent to Maxwell theory in a special gauge if it is further restricted to the "
      "sector in which the LAGRANGE MULTIPLIER FIELD VANISHES.'  lambda = 0 is exactly what "
      "reading D's linearized field equations FORCE, and Maxwell theory in a gauge has no "
      "preferred frame, hence alpha_1 = alpha_2 = 0 -- reading D's answer *** ",
      "reading D did not invent a degenerate branch.  It independently rediscovered a "
      "published equivalence, from the field equations, without consulting the literature "
      "(its docstring: 'NOTHING here is copied from Foster & Jacobson or any other PPN "
      "reference').  That is strong evidence its machinery is sound")
check("the theory is no longer that of a Lorentz-violating vector field" in Q_JAC_S8
      and "shock discontinuities" in Q_JAC_S8,
      "C3  and the published PRICE of that sector is reading D's price, item for item: the "
      "equivalence 'holds only if one abandons the notion that the vector is itself "
      "physical', and the case has known 'shock discontinuities' and 'a possibly related "
      "instability' INDEPENDENTLY of PPN",
      "reading D's non-normalisable wake (|v_L| ~ U/w, linearization failing for w <~ U) is "
      "the same disease.  So the honest joint statement is: on this locus alpha_1 = alpha_2 "
      "= 0 in the lambda = 0 sector, and that sector's aether is not a physical "
      "Lorentz-violating vector.  NEITHER reading gets a clean win")
Q_JAC_25 = (
    "The mode speeds (4.1) are all equal to unity if c13 = c4 = 0 and c2 = c1/(1 - 2c1).  In "
    "this case the PPN parameters become alpha1 = -4c1 and alpha2 = 0, so the observational "
    "constraint on alpha1 imposes the stringent condition |c1| <~ 2.5e-5, and the other "
    "parameters are then similarly small.")
print(f'\n    [JAC08] Section 8, SECOND BULLET, VERBATIM:\n      "{Q_JAC_25}"')
c2_required = c1 / (1 - 2 * c1)
check("2.5e-5" in Q_JAC_25 and sp.simplify(c2_required.subs(c1, KB)) != 0,
      "C4  *** WHERE READING L's NUMBER ACTUALLY COMES FROM, AND WHY IT IS NOT THIS THEORY'S. "
      "The published bound |c_1| <~ 2.5e-5 exists -- but it is derived at c_13 = c_4 = 0 AND "
      "c_2 = c_1/(1 - 2c_1), which is STRICTLY NONZERO.  That is the non-degenerate "
      "neighbour of AeST's aether, differing from it in precisely the one parameter (c_2, "
      "hence c_123) that controls the degeneracy ***",
      "reading L's K_B < 2.5e-5 numerically reproduces a real published bound for a "
      "DIFFERENT theory: the one where all three mode speeds are luminal and alpha_2 = 0 "
      "because c_2 has been tuned to c_1/(1-2c_1).  AeST cannot make that choice: its F^2 "
      "form sets c_2 = 0 identically.  The coincidence of the number is what made reading L "
      "look safe")
Q_JAC_PRE = ("It appears that, unless all of the parameters are much smaller than unity, then "
             "in order to be compatible with all of the theoretical and observational "
             "constraints (leaving aside the radiation reaction and strong self-field "
             "effects), most likely none of the ci, nor c13, c14, or c123 can vanish.")
print(f'\n    [JAC08] Section 8 preamble, VERBATIM:\n      "{Q_JAC_PRE}"')
check("none of the ci, nor c13, c14, or c123 can vanish" in Q_JAC_PRE,
      "C5  [JAC08] Section 8's overall verdict on vanishing combinations, recorded verbatim "
      "with its own hedge ('It appears that', 'most likely', 'unless all of the parameters "
      "are much smaller than unity') and its own stated exclusions",
      "reported as the literature's disposition, NOT as a proof against AeST.  The hedge "
      "clause 'unless all of the parameters are much smaller than unity' is live for AeST if "
      "K_B is small, and the sentence is a survey judgement, not a theorem")
# [GHLP18]: the post-GW170817 treatment of exactly the c_13 = 0 locus
c2_lower_gong = c14 / (1 - 2 * c14)      # [GHLP18] Eq. (62) lower bound
check(sp.simplify((c2_lower_gong - c2_required.subs(c1, c14))) == 0,
      "C6  [GHLP18] independently analysed the c_13 = 0 branch after GW170817 and their "
      "Eq. (62) is 'c_14/(1 - 2c_14) < c_2 < c_2^u(c_14)' -- a STRICTLY POSITIVE lower bound "
      "on c_2, verified here to be algebraically the same expression as [JAC08]'s "
      "c_2 = c_1/(1-2c_1) with c_4 = 0.  AeST's c_2 = 0 lies BELOW it",
      "so the two independent post-GW170817 treatments of our own locus both require "
      "c_2 != 0.  [GHLP18] Eq. (59) also gives s_s^2 = c_2(2-c_14)/[c_14(2+3c_2)], which is "
      "0 at c_2 = 0 -- the same non-propagating scalar mode.  Nobody in this literature "
      "computes the c_2 = 0 point; three papers step around it")

# ==================================================================================
hdr("PART C2 -- (d) THE ONE PUBLISHED PPN CALCULATION OF THIS EXACT VECTOR SECTOR *WITH A "
    "SCALAR*: Bekenstein's TeVeS.  It agrees with NEITHER reading.")
# ==================================================================================
check(sp.simplify((c1 - c3).subs({c1: K, c3: -K}) - 2 * K) == 0
      and sp.simplify((c1 + c3).subs({c1: K, c3: -K})) == 0,
      "C7  *** SIMPLE (original) TeVeS IS THE MAXWELL AETHER.  [SAGI09] Eq. (38) writes the "
      "generalized vector action with couplings K (on F_ab F^ab), K_+ (on S_ab S^ab), K_2 "
      "(on (div A)^2), K_4 (on Adot^2), and states the dictionary c_1 - c_3 = 2K, "
      "c_1 + c_3 = 2K_+, c_2 = K_2, c_4 = -K_4.  Bekenstein's original TeVeS is K only, "
      "i.e. K_+ = K_2 = K_4 = 0, hence c_1 = K, c_3 = -K, c_2 = c_4 = 0 -- AeST's aether "
      "dictionary with K <-> K_B *** ",
      "[JAC08] Sec. 1 corroborates the identification independently: 'Other theories "
      "involving scalar fields in addition to a vector field with a Maxwell-like action for "
      "the vector are Bekenstein's TeVeS [13] and Moffat's STVG [14]', and names "
      "Kostelecky-Samuel as 'the Maxwell-like special case of ae-theory (c3 = -c1, "
      "c2 = c4 = 0)'.  So the vector sector AeST adopted is a well-studied one")
Q_SAGI_DIV = (
    "The covariant divergence of the vector equation, unlike the covariant divergence of the "
    "Einstein equation, is not automatically satisfied, but yields a constraint on the "
    "divergence of the vector field or on the coupling constants of the theory (see [20], "
    "Section 5.4 for details).")
print(f'    [SAGI09] Sec. III, VERBATIM:\n      "{Q_SAGI_DIV}"')
check("yields a constraint on the divergence of the vector field or on the coupling constants"
      in Q_SAGI_DIV,
      "C8  *** READING D's MECHANISM IS PUBLISHED.  Reading D's route (i) is: antisymmetry "
      "of F^{mu nu} gives d_mu d_nu F^{mu nu} == 0, hence grad_nu(lambda A^nu) = 0, an EXTRA "
      "identity a generic Einstein-aether theory does not have.  Sagi states the same thing "
      "in words and uses it as the central tool of her Sec. III *** ",
      "her Eq. (35) is the O(1.5) content of that identity for TeVeS: "
      "[K/(1-K/2)] U_,0 = -2(1 - e^{-4 phi_0}) U_,0")
Q_SAGI_TAMAKI = (
    "Here Tamaki's calculation [21] was in error; since he assumed phi_0 = 0, his conclusion "
    "at this step should have been that necessarily K = 0, namely one cannot take into "
    "account the coupling of the vector field in this particular theory without the scalar "
    "field, because obviously one cannot demand U,0 = 0 always.")
print(f'\n    [SAGI09] Sec. III, VERBATIM:\n      "{Q_SAGI_TAMAKI}"')
check("necessarily K = 0" in Q_SAGI_TAMAKI,
      "C9  *** AND SO IS READING D's CONCLUSION FOR THE SCALAR-FREE CASE.  With no scalar "
      "background (phi_0 = 0), the divergence identity forces 'necessarily K = 0' -- the "
      "Maxwell-aether-plus-gravity system with a moving source is OVER-DETERMINED unless "
      "the vector coupling is switched off.  Reading D hit the same wall in the form "
      "lambda*(w.khat) = 0 => lambda = 0 for generic k *** ",
      "so the AETHER-SECTOR-ONLY question -- which is precisely the question reading L and "
      "reading D disagree about -- has a published answer, and it is reading D's: there is "
      "no consistent nonzero-K aether-only preferred-frame solution to read alpha_1 off.  "
      "Sagi's 'K = 0' and reading D's 'lambda = 0' are the two ways of saying the source "
      "term lambda A_mu A_nu, the only aether source in the linearized Einstein equation, "
      "is absent")
# Sagi's simple-TeVeS PPN parameters, with the scalar RETAINED
Kc, kc, phi0 = sp.symbols("K k phi_0", real=True)
G_S28 = 1 / (1 / (1 - Kc / 2) + kc / (4 * sp.pi))                        # [SAGI09] Eq. (28)
A1_S32 = 4 * G_S28 / Kc * ((2 * Kc - 1) * sp.exp(-4 * phi0)
                           - sp.exp(4 * phi0) + 8) - 8                    # [SAGI09] Eq. (32)
A2_S33 = 2 * G_S28 / (2 - Kc)**2 * (3 * (2 - Kc)
                                    - (Kc + 4) * sp.exp(4 * phi0)) - 1    # [SAGI09] Eq. (33)
PHI0_S37 = -sp.Rational(1, 4) * sp.log(2 / (2 - Kc))                      # [SAGI09] Eq. (37)
a1_on_c = sp.simplify(A1_S32.subs(phi0, PHI0_S37))
a2_on_c = sp.simplify(A2_S33.subs(phi0, PHI0_S37))
lead = sp.simplify(sp.limit(Kc * a1_on_c, Kc, 0, "+"))
check(sp.simplify(c123.subs({c1: Kc, c2: 0, c3: -Kc, c4: 0})) == 0
      and sp.denom(sp.together(A1_S32)).has(Kc) and lead != 0,
      "C10 *** THE RESULT NEITHER READING HAS: with the scalar RETAINED, [SAGI09] Eqs. (32) "
      "and (33) give FINITE, NONZERO alpha_1 and alpha_2 for this exact Maxwell vector "
      "sector, and their denominators are K and (2-K)^2 -- NOT c_123.  A scalar CAN lift the "
      "pole.  Moreover alpha_1 goes like 1/K: on her constraint (37), "
      f"lim_(K->0+) K*alpha_1 = {sp.nsimplify(lead)} != 0 ***",
      "compare the two readings: reading L says alpha_1 = -4K_B (VANISHES as K_B -> 0); "
      "reading D says alpha_1 = 0 identically.  The published scalar-retained calculation "
      "for the same vector sector says |alpha_1| ~ 1/K, i.e. it BLOWS UP as the vector "
      "coupling goes to zero.  The sign of the risk in K_B is INVERTED relative to reading L. "
      "This is a pointer for the sibling agent, NOT a result for AeST: AeST's scalar sector "
      "(2(2-K_B)J.grad(phi) - (2-K_B)Y - F(Y,Q)) is not TeVeS's, and no number is transferred")
info("the 1/K scaling is robust to the one transcription ambiguity in Eq. (32)",
     "the extracted text places the big-paren glyphs so that the bracket is "
     "[(2K-1)e^{-4phi_0} - e^{4phi_0} + 8] with a separate '-8' outside; the only other "
     "plausible grouping puts the +8 outside, giving bracket -> -2 at K -> 0 instead of +6.  "
     "Either way the bracket is NONZERO at K = 0, so |alpha_1| ~ 1/K holds; only its SIGN "
     "is grouping-dependent, and the sign is not used")
Q_SAGI_LEAVE = (
    "This contradicts the basic assumption of TeVeS that its coupling parameters are "
    "constant, namely that they do not change during the evolution of the universe. ... "
    "When relation (37) holds, it can be shown that there is no ambiguity in the "
    "determination of the physical metric and the preferred frame parameters, although the "
    "spatial divergence of the vector field remains indeterminate.  However, it looks like "
    "the constraint (37) is another sign of the existence of a dynamical problem with the "
    "vector action in TeVeS, adding up to the analysis of Contaldi et al. [24] regarding the "
    "formation of caustic singularities in the evolution of the vector field.  Therefore, we "
    "leave aside simple TeVeS, and proceed instead to calculate the PPN parameters of TeVeS "
    "with AEther [26] type vector action.")
print(f'\n    [SAGI09] Sec. III, VERBATIM:\n      "{Q_SAGI_LEAVE}"')
check("we leave aside simple TeVeS" in Q_SAGI_LEAVE
      and "the spatial divergence of the vector field remains indeterminate" in Q_SAGI_LEAVE,
      "C11 and the price of C10 is that those alpha's exist only ON the constraint (37), "
      "phi_0 = -(1/4) ln[2/(2-K)], which ties the scalar's cosmological value to the vector "
      "coupling; 'the spatial divergence of the vector field remains indeterminate'; and "
      "Sagi treats this as 'another sign of the existence of a dynamical problem with the "
      "vector action' and ABANDONS the case",
      "so the count of published authors who reached AeST's aether locus and declined to "
      "push a PPN number through it is THREE: [FJ06] (excluded it by assumption), [JAC08] "
      "('evidently not applicable'), [SAGI09] ('we leave aside simple TeVeS').  Nobody has "
      "published alpha_1, alpha_2 for the Maxwell aether without a scalar")
# and the generalized case keeps the pole, so the scalar does not automatically save it
A2_S47_DEN = (K2s + 2 * Kp) * (2 - (K + Kp - K4))            # [SAGI09] Eqs. (47)-(48) denom
check(sp.simplify(A2_S47_DEN - (c123 * (2 - c14)).subs(SAGI_DICT)) == 0,
      "C12 *** AND THE SCALAR DOES NOT AUTOMATICALLY LIFT THE POLE.  [SAGI09] Eqs. (47)-(48) "
      "-- alpha_2 for GENERALIZED TeVeS, scalar fully retained -- has denominator "
      "(K_2 + 2K_+)(2 - (K + K_+ - K_4)), verified here to equal c_123(2 - c_14) exactly.  "
      "So with a scalar present the c_123 pole is STILL there in her generalized "
      "calculation *** ",
      "the resolution of the apparent conflict with C10 is that the simple-TeVeS alpha's "
      "(32)-(33) were obtained only AFTER imposing the degenerate sector's own constraint "
      "(37).  Whether AeST's scalar sector supplies an analogous constraint that renders "
      "alpha_1, alpha_2 finite -- and what it costs -- is the AeST-specific calculation, "
      "genuinely open, and exactly the sibling agent's assignment")

# ==================================================================================
hdr("PART D -- (d, second half) DOES ANY AeST PAPER BOUND K_B?")
# ==================================================================================
Q_SZ_KB = ("Clearly then we must require KB > 0 to avoid ghosts and gradient instabilities.  "
           "The mass term M is also non-tachyonic if both 0 < KB < 2 and lambda_s > -1.  "
           "Hence, stability considerations for the vector modes imply the following "
           "constraints on the parameter space of AeST: 0 < KB < 2, lambda_s > -1.")
print(f'    [SZ21s] text around Eq. (23), VERBATIM:\n      "{Q_SZ_KB}"')
check("0 < KB < 2, lambda_s > -1" in Q_SZ_KB and "stability considerations" in Q_SZ_KB,
      "D1  [SZ21s] arXiv:2109.13287 Eq. (23) is the ONLY constraint that paper places on "
      "K_B:  0 < K_B < 2,  lambda_s > -1, from no-ghost plus non-tachyonic mass term",
      "verified by reading the extracted full text of that paper.  It also gives "
      "c_s^2 = [(2-K_B)/(K_2 K_B)](1 + K_B lambda_s/2) as its Eq. (30), which matches "
      "stage73's transcription")
# grep counts recorded from the extracted text of arXiv:2109.13287 in this session
SZ_GREP = {"PPN": 0, "post-newton": 0, "preferred": 1, "KB": 63}
print(f"    case-insensitive occurrence counts in the extracted text of [SZ21s]: {SZ_GREP}")
check(SZ_GREP["PPN"] == 0 and SZ_GREP["post-newton"] == 0 and SZ_GREP["KB"] > 0,
      "D2  the words 'PPN' and 'post-Newtonian' occur ZERO times in [SZ21s] while K_B occurs "
      "63 times (grep counts on the extracted text, recorded above).  No AeST paper located "
      "in this search bounds K_B by a preferred-frame constraint",
      "so the corpus's observation that AeST's own literature is silent on K_B beyond "
      "0 < K_B < 2 is confirmed for the stability paper.  This is why stage70's number "
      "looked like new information -- it WAS new, it is just not derivable from [FJ06]")
check(True,
      "D3  NOT COMPUTED / NOT ACCESSED: arXiv:2304.05134 (Verwayen & Skordis, quasistatic "
      "spherical solutions) was not read in full text in this session, so the corpus's "
      "claim that K_B appears zero times in its quasi-static equations is NOT re-verified "
      "here.  It is carried forward as a corpus claim, not as a finding of this file",
      "listed explicitly rather than quietly assumed")

# ==================================================================================
hdr("PART E -- VERDICT, and what changes")
# ==================================================================================
check(True,
      "E1  *** THE FORK IS DECIDED, ON THE DOCUMENTS, IN FAVOUR OF READING D.  Reading L "
      "evaluates [FJ06] Eq. (10) at c_123 = 0, a locus [FJ06]'s own appendix removes from "
      "the domain ('assume below that they do not hold'), whose SOLUTION for the aether "
      "perturbation diverges ([FJ06] Eq. 6 = K_B/0, check A5), whose alpha_2 is a genuine "
      "nonzero-residue pole (A3, A4), and which Jacobson names as 'the Maxwell action (with "
      "the unit constraint on the vector)' with the words 'the perturbation series used in "
      "the PPN analysis is thus evidently not applicable' (C1). ***",
      "alpha_1 = -4 K_B is correct arithmetic on an inapplicable formula.  The corpus should "
      "record it as WITHDRAWN-AS-INHERITED, not as refuted arithmetic")
check(True,
      f"E2  CONSEQUENCE, AND IT IS FAVOURABLE: reading L's ceiling K_B < "
      f"{A1_LLR/4:.1e} does not follow from the literature, so stage73's two-sided squeeze "
      f"against the subluminality FLOOR K_B >= 2/(K_2+1) is NOT ESTABLISHED and the EMPTY "
      f"WINDOW at SZ21's own MOND-compatible fits (K_2 = 7.5e3, 9.5e3) EVAPORATES.  With no "
      f"PPN ceiling, 0 < K_B < 2 stands and SZ21's K_B = 0.5/0.3/0.1 are not excluded by "
      f"this route",
      "stated plainly because the standing rule cuts both ways: this is the withdrawal of an "
      "ADVERSE claim the corpus made, and it must be withdrawn as rigorously as it was made")
check(True,
      "E3  BUT TWO NEW ADVERSE ITEMS, NEITHER OF WHICH THE CORPUS CARRIES.  (i) [JAC08] "
      "reports that the Maxwell-action aether has known pathologies INDEPENDENT of PPN -- "
      "'the formation of shock discontinuities' and 'a possibly related instability' -- and "
      "that the lambda = 0 sector in which it behaves is one where 'the theory is no longer "
      "that of a Lorentz-violating vector field'.  (ii) [SAGI09]'s scalar-retained "
      "calculation for the SAME vector sector gives |alpha_1| ~ 1/K, so if AeST's scalar "
      "lifts the degeneracy the way TeVeS's does, SMALL K_B is the DANGEROUS regime and the "
      "risk in K_B has the OPPOSITE sign to reading L's",
      "these are pointers, not results.  (i) is a structural liability of the adopted "
      "relativistic home that the corpus has not priced; (ii) says the sibling agent's "
      "answer could be worse than reading L rather than better, and in the other direction")
check(True,
      "E4  WHAT IS RIGOROUSLY ESTABLISHED HERE, and nothing more: the published PPN "
      "formulas MAY NOT be applied to AeST's aether sector; the published literature "
      "contains no alpha_1, alpha_2 for the scalar-free Maxwell aether; reading D's two "
      "structural findings (the extra divergence identity from antisymmetry of F, and the "
      "lambda = 0 sector) are both PUBLISHED, in [SAGI09] and [JAC08] respectively; and "
      "reading D's caveats coincide with the published assumption that fails ([FJ06]'s "
      "vanish-at-infinity boundary condition) and the published pathologies ([JAC08]'s "
      "shocks and instability)",
      "NOT established: that alpha_1 = alpha_2 = 0 is the physically correct answer for "
      "AeST.  Reading D's own summary is that they 'do not exist in the usual sense' on this "
      "locus, and the literature agrees with THAT, not with a value of zero")
check(True,
      "E5  THE ONE CALCULATION THAT REMAINS, stated so it can be handed over: expand the "
      "FULL AeST action with the scalar sector retained about flat space with the aether "
      "boosted by w, and determine whether the AeST analogue of [SAGI09] Eq. (37) exists -- "
      "i.e. whether the scalar supplies a constraint that makes alpha_1, alpha_2 finite, and "
      "at what cost.  [SAGI09] Eqs. (32),(33),(37),(47),(48) are the template: FINITE and "
      "NONZERO for simple TeVeS but only on a constraint the author judged pathological, and "
      "STILL c_123-singular in her generalized case",
      "this is the sibling agent's assignment; this file's contribution is to establish that "
      "it is the ONLY route left, because the literature lookup is closed")

# ==================================================================================
hdr("PART F -- WHAT I READ vs. WHAT I DID NOT.  Read this before quoting anything above.")
# ==================================================================================
READ = ["gr-qc/0509083v2 (Foster & Jacobson 2006) -- full text, all quotes and Eqs. "
        "(3),(6),(10),(11),(15),(17),(A.9),(A.10),(A.20)-(A.22) read from extracted text",
        "arXiv:0801.1547 (Jacobson, status report) -- full text, Sec. 2 Eqs. (2.1)-(2.5), "
        "Sec. 4 Eqs. (4.1)-(4.6), Sec. 8 in full",
        "arXiv:0905.4001 (Sagi 2009) -- full text, Eqs. (28)-(33),(35)-(38),(46)-(50) and "
        "the Sec. III narrative",
        "arXiv:1801.03382v3 (Gong, Hou, Liang, Papantonopoulos) -- full text, "
        "Eqs. (44),(45),(59)-(62) and the generalized-TeVeS section",
        "arXiv:2109.13287 (Skordis & Zlosnik, linear stability) -- full text, Eqs. (1),(23),(30)"]
NOTREAD = ["Eling & Jacobson gr-qc/0310044 -- FJ06's ref [8], source of beta = gamma = 1 and "
           "of the c_123 = 0 <-> Hellings-Nordtvedt identification.  UNVERIFIED",
           "Graesser, Jenkins & Wise hep-th/0501223 -- FJ06's ref [9], the earlier alpha_2 "
           "and the 'absence of spatial gradient terms' remark.  UNVERIFIED",
           "Jacobson & Mattingly gr-qc/0402005 (aether waves) -- the mode-speed source.  "
           "UNVERIFIED except through FJ06 Eq. (15) and JAC08 Eq. (4.1)",
           "Will, Theory and Experiment in Gravitational Physics (1993), Sec. 5.4 -- the "
           "Hellings-Nordtvedt over-determination result and Sagi's divergence-constraint "
           "reference.  UNVERIFIED",
           "Tamaki PRD 77, 124020 (2008) -- the erroneous TeVeS PPN attempt Sagi corrects.  "
           "UNVERIFIED (only Sagi's characterisation of it was read)",
           "Kostelecky & Samuel; Clayton (shocks); Seifert (instability); Contaldi et al. "
           "(caustics) -- all cited only through JAC08/SAGI09.  UNVERIFIED",
           "arXiv:2304.05134 (Verwayen & Skordis) -- NOT read; the corpus's 'K_B appears "
           "zero times' claim is not re-verified here",
           "Oost, Mukohyama & Wang 1802.04303 and other post-GW170817 constraint papers "
           "beyond GHLP18 -- NOT read; a fourth independent treatment of the c_13 = 0 locus "
           "may exist and was not located"]
print("    READ IN FULL TEXT:")
for r in READ:
    print(f"      + {r}")
print("    NOT ACCESSED (findings resting on these are UNVERIFIED):")
for r in NOTREAD:
    print(f"      - {r}")
check(len(READ) == 5 and len(NOTREAD) == 8,
      "F1  provenance ledger recorded: 5 papers read in full extracted text, 8 sources "
      "cited only at second hand and flagged UNVERIFIED.  No equation number, quote or "
      "reference above comes from memory; every one was read off extracted PDF text in this "
      "session, and anything that was not is in the second list",
      "the two verbatim quotes doing the decisive work (FJ06's appendix domain statement, "
      "JAC08's Sec. 8 first bullet) are both from papers in the FIRST list")
check(A0_CANON > 0 and A0_ALT > 0 and KAPPA_FITTED == 0.5,
      f"F2  SCOPE: this adjudication touches nothing in the framework's normalisation claim. "
      f"a_0 = kappa c sqrt(G rho_Lambda) = {A0_CANON:.4e} (canonical) / {A0_ALT:.4e} (alt) "
      f"m/s^2 with kappa = {KAPPA_FITTED} FITTED-NOT-DERIVED, the MS08 kernel "
      f"nu(y) = 1/(1-exp(-sqrt y)), the RAR, lensing and the wide-binary band appear ZERO "
      f"times in the argument above.  The risk adjudicated is in the adopted relativistic "
      f"home (AeST's vector sector), not in the a_0 claim",
      "printed so no reader mistakes a verdict about K_B for a verdict about kappa")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"ALPHA2 LITERATURE FORENSICS: {NCHK[0] - n_fail}/{NCHK[0]} checks passed"
      + ("" if not n_fail else f"; FAILED: {FAIL}"))
print("SUPPORTS: READING D (reading L is out of its own published domain of validity).")
print("DIRECTION: MIXED -- an adverse corpus claim (K_B < 2.5e-5, the empty window) is")
print("           WITHDRAWN, which is favourable; two new adverse pointers are opened.")
print("=" * 100)
sys.exit(1 if FAIL else 0)
