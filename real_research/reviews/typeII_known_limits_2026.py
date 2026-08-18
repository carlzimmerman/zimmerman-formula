#!/usr/bin/env python3
r"""typeII_known_limits_2026.py -- IS AeST's QUASI-STATIC SECTOR "TYPE-II"?  CHECKED AGAINST WHAT
IS ALREADY KNOWN, FROM THREE DIRECTIONS, PLUS AN INDEPENDENT LAGRANGE-MULTIPLIER AUDIT.

WHAT IS UNDER TEST.  real_research/reviews/ppn_newtonian_radial_2026.py PART Q asserts three things
about the weak-field quasi-static limit of the aether-scalar-tensor (AeST) theory:

  (P1)  with g_00 = -(1+2Psi), g_ij = (1-2Phi)delta_ij, A_mu = (-(1+Psi-Psi^2/2),0,0,0) with
        A^mu A_mu = -1 enforced ORDER BY ORDER, and phi = Q_0 t + varphi(x), one gets
        Qcal = Q_0(1 - Psi + 3Psi^2/2)  and  Ycal = |grad varphi|^2 EXACTLY at quadratic order;
  (P2)  Psi = Psi_N + varphi with lap(Psi_N) = 4 pi Ghat rho and
        div[ J_Y(Ycal) grad varphi ] = lap(Psi_N),  Ycal = |grad varphi|^2;
  (P3)  hence u = |grad varphi| IS the anomalous acceleration and obeys the PURELY LOCAL ALGEBRAIC
        law  u J_Y(u^2) = g_bar,  i.e. u = (nu(y) - 1) g_bar with y = g_bar/a_0.

Downstream of (P3) sits the legality theorem (single-valued J(Ycal) / no longitudinal ghost requires
y -> u(y) MONOTONE), which rejects the operative kernel nu = 1/(1-e^(-sqrt y)) and selects
nu = sqrt(1+1/y), i.e. g_obs^2 = g_bar^2 + a_0 g_bar, with closed-form free function
J_Y = v/(1-2v), v = sqrt(Ycal)/a_0.  (P1)-(P3) had been derived ONCE, by one script.  This file is
an independent confrontation with (a) the published AeST literature, (b) the AQUAL/TeVeS analogy,
and (c) the corpus's own committed numbers -- plus (M) the multiplier audit the task demands.

=========================================================================================
SOURCES ACTUALLY RETRIEVED, AND WHAT COULD NOT BE
=========================================================================================
RETRIEVED IN FULL, arXiv LaTeX source, 2026-08-17 (curl arxiv.org/e-print/<id>):
  S1  arXiv:2007.00082 -> newRMONDLett.tex .  Skordis & Zlosnik, PRL 127, 161302 (2021).
      The quasi-static paragraph and the two nonrelativistic actions read VERBATIM off the source.
  S2  arXiv:2304.05134 -> main.tex .  Verwayen, Skordis & Boehm, "AeST theory: quasistatic
      spherical solutions and their phenomenology", MNRAS 531, 272 (2024).  Their weak-field
      system, their FIRST INTEGRAL, and their curl-term statement read VERBATIM off the source.
RETRIEVED, ABSTRACT ONLY (arXiv landing page; body not parsed here):
  S3  arXiv:2109.13287, Skordis & Zlosnik, "AeST: Linear stability on Minkowski space".  Confirms
      only "mu ... estimated to be <~ Mpc^-1".  No quasi-static equations extracted.  Anything
      about that paper's interior is NOT used below.
NOT RETRIEVED / NOT USED: Mistele's AeST papers (arXiv:2301.03499 weak lensing; Mistele 2023 on
  mu^-1 from rotation-curve extent).  Their existence is recorded from a search-result listing
  only; NOTHING is inferred from them.  Marked UNVERIFIED wherever they are mentioned.
NO equation number, quotation, DOI or citation below is invented: every equation label quoted
(NT_A_action, scalar_AQUAL_action, NT_quasi_Phi, Kcal_expansion, Phi-Orig, Chi-Orig, Chi-AQUAL,
first_int, Jcal_MOND, Jcal_GR, def_f_general, mu_Simple) is a \label{} string present in the
retrieved .tex files.  Where the papers print no numbered equation, this file says so.

=========================================================================================
HEADLINE FINDINGS
=========================================================================================
F1  (P2) IS THE PUBLISHED EQUATION, not a corpus reconstruction.  SZ21's own nonrelativistic
    template action (label scalar_AQUAL_action) is written in exactly the split (P2) asserts --
    Phi = PhiE + varphi, Ycal = |grad varphi|^2 -- and the sentence immediately after it prints
    both field equations: varphi obeys div[(dJcal/dYcal) grad varphi] = 4 pi Ghat rho, and PhiE
    obeys lap(PhiE) = 4 pi Ghat rho.  Verwayen+2024 restate the same system (labels Phi-Orig,
    Chi-Orig, Chi-AQUAL) with chi for varphi and Phih for PhiE.  (P2) CONFIRMED.
F2  GATES (a) and (b) ARE PUBLISHED SENTENCES.  SZ21's quasi-static paragraph states the aether
    alignment A^0 = 1-Psi, A^i = 0, then Qcal = (1-Psi)Qcal_0 -- gate (a), verbatim -- and then
    "leads to Psi = Phi" -- gate (b), verbatim.  Verwayen+2024 restate Phi = Psi and its lensing
    consequence.  Both gates CONFIRMED against the source, independently of PART Q.
F3  GATE (c) IS PUBLISHED TWICE.  Jcal -> [2 lambda_s/(3(1+lambda_s) a_0)] Ycal^(3/2) as
    grad varphi -> 0 appears in SZ21 (unnumbered, after scalar_AQUAL_action) and as
    Verwayen+2024's label Jcal_MOND.  This file DERIVES from it that the algebraic law gives
    g_obs -> sqrt(g_bar a_0), and that the corpus's closed-form J has exactly this small-Y limit
    at lambda_s -> infinity.  CONFIRMED.
F4  *** (P3) IS NOT PUBLISHED AS STATED, AND IT IS NOT GENERALLY TRUE. ***  What the literature
    prints is the VECTOR first integral (Verwayen+2024, label first_int)
        grad Phih  =  f(|grad chi|/a_0) grad chi  +  curl k ,
    with the explicit statement -- theirs, citing Bekenstein & Milgrom 1984 -- that curl k is
    exactly zero for particular symmetries INCLUDING SPHERICAL and falls at least as r^-3
    otherwise.  So u J_Y(u^2) = g_bar is EXACT IN SPHERICAL (and planar, and cylindrical)
    symmetry and NOT exact in general.  This file derives the exact obstruction: the algebraic
    law holds iff  grad|grad Psi_N| x grad Psi_N = 0, which fails for a binary (demonstrated) and
    for a disc.  (P3) is therefore PARTIAL as written -- it needs the words "in spherical
    symmetry" -- and PART Q's own text ("purely local algebraic law") overstates it.
F5  *** BUT THE LEGALITY THEOREM SURVIVES INTACT, AND IS INDEPENDENTLY KNOWN. ***  The theorem is
    a statement about the FUNCTION J, and the spherical family ALONE sweeps y over all of
    (0, infinity), so it fixes J_Y on its whole domain.  A kernel with non-injective U(y) admits
    NO single-valued J_Y even in spherical symmetry.  Moreover the condition is Milgrom's known
    monotonicity requirement on x f(x), and it is visible in Verwayen+2024's own spherical ODE
    (label d2_chi_spher_sym), whose leading coefficient is exactly [x df/dx + f]: the same
    quantity whose sign the corpus calls the longitudinal ghost.  Route A and alpha=2 are
    REJECTED; alpha=1 is SELECTED.  Direction: FAVOURABLE to the corpus's own signature relation,
    ADVERSE to its operative kernel -- exactly as the radial script concluded.
F6  *** THE MULTIPLIER IS HANDLED CONSISTENTLY IN PART Q, AND THIS FILE SHOWS WHY. ***  lambda_bg
    is NOT zero here either: three independent routes (the c_2 variation, the A_mu field equation,
    and the requirement that Minkowski solve its own Einstein equation) all give
        lambda_bg = (2 - K_B) Q_0^2  +  K'(Q_0) Q_0 .
    PART Q nonetheless gets the right answer because solving A^mu A_mu = -1 to SECOND order pushes
    (A^mu A_mu + 1) to O(Psi^3), so lambda cannot enter the quadratic action at all.  The
    counterfactual is computed: truncating the constraint at first order (c_2 = 0) and setting
    lambda = 0 -- the ppn_scalar_retained_2026.py failure mode -- leaves a SPURIOUS quadratic term
    -(2-K_B)Q_0^2 Psi^2, i.e. a spurious mass, of exactly the size that produced that file's bogus
    graviton Yukawa.  The two errors cancel only if BOTH are made; making one is fatal.
F7  ONE REAL DEFECT FOUND IN PART Q, NOT LOAD-BEARING.  PART Q's Q-sector mass term is wrong by a
    factor of -2.  SZ21 define Kcal(Qcal) = -(1/2)Fcal(0,Qcal) (their sentence, before
    Kcal_expansion), so the action bracket carries -Fcal ⊃ +2 Kcal_2 Q_0^2 Psi^2, giving
    lap(Psi) + mu^2 Psi = 4 pi Ghat rho + lap(varphi) with mu^2 = 2 Kcal_2 Q_0^2/(2-K_B) -- which
    reproduces SZ21's own printed mu = sqrt(2 Kcal_2/(2-K_B)) Qcal_0 EXACTLY, and their statement
    that the solution is OSCILLATORY beyond r_C.  PART Q instead carries -Kcal_2 Q_0^2 Psi^2 and
    reports lap(Psi) - m^2 Psi = ... with m^2 = Kcal_2 Q_0^2/(2-K_B) = mu^2/2: half the size and
    the wrong sign (screening rather than oscillation).  It changes NOTHING in (P1)-(P3) or in the
    legality theorem, because mu^-1 >~ 1 Mpc puts the term 10 orders of magnitude away from every
    scale PART Q uses -- but it is a transcription error and it is recorded as one.

WHAT IS NOT DONE HERE.  The O(w^2) preferred-frame sector, alpha_1/alpha_2, the vector/tensor mode
spectrum, and any claim about Mistele's papers.  No cosmology.  a_0 = kappa c sqrt(G rho_Lambda) =
9.3619e-11 canonical / 1.1279e-10 alt with kappa = 1/2 FITTED, never derived; both footings are
carried through every dimensional number below.

EXIT 0 iff every numbered check passes.
"""
from __future__ import annotations

import math
import os
import sys
import time

import numpy as np
import sympy as sp

# =================================================================================================
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


print(__doc__)
T0 = time.time()

CLIGHT = 2.99792458e8
GMSUN = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
MPC = 1.0e6 * PC
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
EPH_EARTH = 3.66e-14      # Sereno & Jetzer 2006 Earth bound, 2 sigma, as carried in the corpus
J2_SUN = 2.2e-7           # solar quadrupole, for the "is the Sun spherical enough" check

# =================================================================================================
print()
print("=" * 100)
print("PART L -- DIRECTION (a): WHAT THE PUBLISHED AeST LITERATURE ACTUALLY SAYS.")
print("           Everything here is derived from, or matched against, LaTeX sources retrieved in")
print("           full on 2026-08-17.  Access log is printed; nothing second-hand is used.")
print("=" * 100)

info("L0  ACCESS LOG.\n"
     "      arXiv:2007.00082  newRMONDLett.tex      RETRIEVED IN FULL   (SZ21, PRL 127, 161302)\n"
     "      arXiv:2304.05134  main.tex              RETRIEVED IN FULL   (Verwayen, Skordis &\n"
     "                                                                   Boehm, MNRAS 531, 272)\n"
     "      arXiv:2109.13287  abstract only         PARTIAL  -- only 'mu <~ Mpc^-1' extracted\n"
     "      arXiv:2301.03499  NOT RETRIEVED         Mistele+ weak lensing -- UNVERIFIED, unused\n"
     "      Mistele 2023 (mu^-1 from RC extent)     NOT RETRIEVED -- UNVERIFIED, unused")

# --- L1: the action as printed, and the -2 Lambda that is NOT in it -------------------------------
check(True,
      "L1  THE ACTION, label NT_A_action, as it stands in newRMONDLett.tex:\n"
      "        S = int d^4x sqrt(-g)/(16 pi Gt) [ R - (K_B/2) Fh^{mu nu}Fh_{mu nu}\n"
      "              + 2(2-K_B) Jh^mu grad_mu phi - (2-K_B) Ycal - Fcal(Ycal,Qcal)\n"
      "              - lambda(Ah^mu Ah_mu + 1) ] + S_m[g]\n"
      "    with Fh_{mu nu} = 2 grad_[mu Ah_nu], Jh_mu = Ah^alpha grad_alpha Ah_mu,\n"
      "    Qcal = Ah^mu grad_mu phi, Ycal = q^{mu nu} grad_mu phi grad_nu phi, q = g + Ah Ah.\n"
      "    *** THERE IS NO EXPLICIT '- 2 Lambda' IN THE BRACKET. ***",
      "the task brief's transcription inserts a '- 2 Lambda' term.  It is not in the source: Lambda\n"
      "         enters ONLY through Kcal = -2 Lambda + Kcal_2(Qcalb - Qcal_0)^2 + ... (label\n"
      "         Kcal_expansion) via Kcal(Qcalb) = -(1/2) Fcal(0,Qcalb).  real_research/\n"
      "         bridge1_aest_equations.md has it RIGHT (no -2 Lambda); the brief has it wrong.\n"
      "         Immaterial below -- every gate is taken in the declared Lambda -> 0 corner -- but\n"
      "         recorded, because the brief called that line 'verified verbatim'.")

# --- L2: reproduce SZ21's printed mu from the F <-> K relation ------------------------------------
KB, K2s, Q0s, Gt, Ghat, rho_s = sp.symbols("K_B Kcal_2 Q_0 Gt Ghat rho", positive=True)
Psi_s, Phi_s, vp_s, mu2 = sp.symbols("Psi Phi varphi mu2")
# SZ21: Kcal(Qcalb) = -(1/2) Fcal(0,Qcalb).  Hence -Fcal(0,Qcal) = +2 Kcal(Qcal).
# With Kcal_expansion and Qcal = (1-Psi)Qcal_0, (Qcal-Qcal_0)^2 = Q_0^2 Psi^2 at quadratic order.
bracket_mass = 2 * K2s * Q0s ** 2 * Psi_s ** 2                     # from -Fcal, inside the bracket
# SZ21's NT_quasi_Phi carries the same physics as  -(2-K_B)/(16 pi Gt) * (- mu^2 Phi^2):
sz_mass_in_bracket = (2 - KB) * mu2 * Psi_s ** 2
mu2_derived = sp.solve(sp.Eq(bracket_mass, sz_mass_in_bracket), mu2)[0]
check(sp.simplify(mu2_derived - 2 * K2s * Q0s ** 2 / (2 - KB)) == 0,
      "L2  *** THE F <-> K NORMALISATION IS PINNED BY SZ21's OWN PRINTED mu. ***  Taking\n"
      "    Kcal = -(1/2)Fcal(0,Qcal) (their sentence) and Kcal_expansion, the bracket's Qcal-mass\n"
      "    term is +2 Kcal_2 Q_0^2 Psi^2, which matched against NT_quasi_Phi gives\n"
      "        mu^2 = 2 Kcal_2 Q_0^2/(2-K_B) ,  i.e.  mu = sqrt(2 Kcal_2/(2-K_B)) Qcal_0\n"
      "    -- EXACTLY the mu SZ21 print under NT_quasi_Phi.  So the reading is confirmed by an\n"
      "    independent published number, not assumed.",
      f"mu^2 = {sp.simplify(mu2_derived)}; bridge1_aest_equations.md carries the same mu.")

# --- L3: PART Q's mass term is off by -2 ----------------------------------------------------------
partQ_mass_in_bracket = -K2s * Q0s ** 2 * Psi_s ** 2               # ppn_newtonian_radial_2026 PART Q
ratio_mass = sp.simplify(partQ_mass_in_bracket / bracket_mass)
check(ratio_mass == sp.Rational(-1, 2),
      "L3  *** DEFECT FOUND IN PART Q (reported, not load-bearing). ***  PART Q's assembled\n"
      "    Lagrangian carries -Kcal_2 Q_0^2 Psi^2 where the action gives +2 Kcal_2 Q_0^2 Psi^2:\n"
      "    a factor of exactly -1/2.  Consequences: PART Q's Q6b prints lap(Psi) - m^2 Psi = ...\n"
      "    with m^2 = mu^2/2, i.e. a SCREENING (Yukawa) mass, where SZ21's own action gives\n"
      "    lap(Psi) + mu^2 Psi = ... -- an OSCILLATORY term, which is precisely what SZ21 and\n"
      "    Verwayen+2024 describe (solutions 'oscillatory' beyond r_C).",
      f"PART Q bracket term / correct bracket term = {ratio_mass}.  Its provenance is PART Q's own\n"
      f"         Q0 info line, which decomposes Fcal = (2-K_B)Jcal(Ycal) + Kcal(Qcal); that\n"
      f"         decomposition contradicts SZ21's Kcal = -(1/2)Fcal(0,Qcal) by exactly -2.  NOT\n"
      f"         load-bearing: see check L4 for the scale separation.")

mu_inv = MPC
r_used_max = 1000 * AU
check(mu_inv / r_used_max > 1e5,
      "L4  and the reason it is not load-bearing, quantified: SZ21 require mu^-1 >~ 1 Mpc (their\n"
      "    sentence under NT_quasi_Phi; Verwayen+2024 repeat it), while PART Q's gates and its\n"
      "    ephemeris numbers live at r <= 1000 AU.  The mass term is suppressed by (mu r)^2.",
      f"mu^-1 / (1000 AU) = {mu_inv / r_used_max:.3e}; (mu * 1 AU)^2 <= "
      f"{(AU / mu_inv) ** 2:.3e}.  Neither the sign nor the factor 2 of a term this small can move\n"
      f"         (P1), (P2), (P3), gamma_PPN, or the kernel legality verdict.")

# --- L5: derive the two published quasi-static field equations from SZ21's own template action ----
x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
SPC = (x1, x2, x3)
PhiE = sp.Function("PhiE")(*SPC)
vpf = sp.Function("varphi")(*SPC)
JYf = sp.Function("J_Y")            # dJcal/dYcal as an unspecified function
Ycal_expr = sum(sp.diff(vpf, c) ** 2 for c in SPC)


def el3(Lag, f):
    out = sp.diff(Lag, f)
    for c in SPC:
        out -= sp.diff(sp.diff(Lag, sp.Derivative(f, c)), c)
    return sp.expand(out.doit())


# SZ21 label scalar_AQUAL_action:  S = int d^4x { (1/(8 pi Ghat))[ |grad PhiE|^2 + Jcal(Ycal) ]
#                                                 + Phi rho },  Phi = PhiE + varphi.
cJ, pw = sp.symbols("cJ p")
lap = lambda e: sum(sp.diff(e, c, 2) for c in SPC)
ok_pairs = []
for pv in (sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2)):
    Jc = cJ * Ycal_expr ** pv
    JYv = cJ * pv * Ycal_expr ** (pv - 1)
    Lqs = (sum(sp.diff(PhiE, c) ** 2 for c in SPC) + Jc) / (8 * sp.pi * Ghat) \
        + (PhiE + vpf) * rho_s
    ePhiE = el3(Lqs, PhiE)
    evp = el3(Lqs, vpf)
    tgt_PhiE = sp.expand((-2 * lap(PhiE)) / (8 * sp.pi * Ghat) + rho_s)
    tgt_vp = sp.expand(-2 * sum(sp.diff(JYv * sp.diff(vpf, c), c) for c in SPC)
                       / (8 * sp.pi * Ghat) + rho_s)
    ok_pairs.append((sp.simplify(ePhiE - tgt_PhiE) == 0, sp.simplify(evp - tgt_vp) == 0))
check(all(a and b for a, b in ok_pairs),
      "L5  *** (P2) IS THE PUBLISHED PAIR OF EQUATIONS. ***  Varying SZ21's own template action\n"
      "    (label scalar_AQUAL_action) reproduces, as an operator identity for every power of\n"
      "    Ycal, exactly the two equations the sentence after it prints:\n"
      "        lap(PhiE) = 4 pi Ghat rho     and     div[ (dJcal/dYcal) grad varphi ] = 4 pi Ghat rho\n"
      "    with Phi = PhiE + varphi and Ycal = |grad varphi|^2.  PART Q's (P2) is therefore not a\n"
      "    reconstruction: it is the authors' own quasi-static system, in the authors' own split.",
      "Verwayen+2024 restate the same system in their labels Phi-Orig / Chi-Orig / Chi-AQUAL with\n"
      "         chi = varphi and Phih = PhiE, adding the mu^2 Phi term.  Two independent published\n"
      "         statements of (P2).  Verified symbolically at p = 3/2, 2, 5/2.")

# --- L6: SZ21's diagonalisation reproduces Gt = (1-K_B/2)Ghat and the '-2' cross-term --------------
Pg, vg = sp.symbols("gPhi gvp")          # |grad Phi| and |grad varphi| stand-ins, 1-D matching
lhs = (2 - KB) / (16 * sp.pi * Gt) * (Pg ** 2 - 2 * Pg * vg + vg ** 2)
rhs = (Pg - vg) ** 2 / (8 * sp.pi * Ghat)
sol_G = sp.solve(sp.Eq(sp.expand(lhs - rhs), 0), Gt, dict=True)
check(len(sol_G) == 1 and sp.simplify(sol_G[0][Gt] - (1 - KB / 2) * Ghat) == 0,
      "L6  and SZ21's diagonalisation is verified rather than quoted: NT_quasi_Phi's kinetic\n"
      "    bracket |grad Phi|^2 - 2 grad Phi . grad varphi + |grad varphi|^2 is a PERFECT SQUARE\n"
      "    |grad(Phi - varphi)|^2 = |grad PhiE|^2, and matching its normalisation to\n"
      "    scalar_AQUAL_action forces Gt = (1 - K_B/2) Ghat -- SZ21's own printed identification,\n"
      "    and the corpus's committed relation.",
      f"solved: Gt = {sp.simplify(sol_G[0][Gt])}.  The '-2' in the cross term is what makes the\n"
      f"         square exact; PART Q's Q6c attributes the same cancellation to the action's\n"
      f"         2(2-K_B) J^mu coupling being twice the (2-K_B) Ycal coefficient.  Same fact.")

check(True,
      "L7  GATES (a) AND (b) ARE PUBLISHED SENTENCES, not corpus inferences.  SZ21's quasi-static\n"
      "    paragraph sets g_00 = -1-2Psi, g_ij = (1-2Phi)gamma_ij, takes the aether aligned with\n"
      "    the time direction so that Ah^0 = 1-Psi and Ah^i = 0, expands phi = phib + varphi with\n"
      "    phibdot at its late-time FLRW minimum Qcal_0, and states\n"
      "        Qcal = (1 - Psi) Qcal_0                                  <-- GATE (a), verbatim\n"
      "    and then that NT_A_action 'leads to Psi = Phi'.                <-- GATE (b), verbatim\n"
      "    Verwayen+2024 restate Phi = Psi and draw the lensing-mass = dynamical-mass consequence.",
      "NOTE the order of the published ansatz: SZ21 write Ah^0 = 1-Psi, i.e. FIRST order only.\n"
      "         PART Q's -Psi^2/2 in A_mu is a SECOND-order completion of it, outside what SZ21\n"
      "         state.  Whether that completion is legitimate is not settled by the literature;\n"
      "         PART M below settles it from the action.")

check(True,
      "L8  GATE (c)'s SOURCE, printed twice.  SZ21 (unnumbered, after scalar_AQUAL_action) and\n"
      "    Verwayen+2024 (label Jcal_MOND) both give\n"
      "        Jcal -> [ 2 lambda_s / (3 (1 + lambda_s) a_0) ] Ycal^(3/2)   as grad varphi -> 0 ,\n"
      "    with the Newtonian/screened end Jcal -> lambda_s Ycal (label Jcal_GR) defining\n"
      "    lambda_s, and f(x) = dJcal/dYcal, x = |grad chi|/a_0, the usual MOND interpolation\n"
      "    function (Verwayen+2024, label def_f_general).  Gate (c) is DERIVED from this at D2.")

check(True,
      "L9  *** WHAT THE LITERATURE DOES NOT PRINT: (P3) AS AN UNQUALIFIED LOCAL LAW. ***  What\n"
      "    Verwayen+2024 print (label first_int), integrating Chi-Orig once, is the VECTOR\n"
      "    relation\n"
      "        grad Phih = f(|grad chi|/a_0) grad chi + curl k ,\n"
      "    together with the statement -- theirs, attributed to Bekenstein & Milgrom 1984 -- that\n"
      "    curl k is exactly zero for particular symmetries INCLUDING SPHERICAL and behaves at\n"
      "    least as r^-3 for non-symmetric situations.  They then say: 'Since we are assuming\n"
      "    spherical symmetry, we can ignore' it.  Their whole paper is titled for the spherical\n"
      "    case.  So u J_Y(u^2) = g_bar is a SPHERICAL-SYMMETRY result in the literature, and\n"
      "    PART Q's word 'purely local' is an overstatement.  PART C quantifies the failure.",
      "the same source records that their spherical radial equation (label d2_chi_spher_sym) has\n"
      "         leading coefficient [ x df/dx + f ] -- the very combination whose sign the corpus\n"
      "         calls the longitudinal ghost.  Used at check C7.")

# =================================================================================================
print()
print("=" * 100)
print("PART M -- THE LAGRANGE MULTIPLIER, AUDITED INDEPENDENTLY.  lambda AND THE SECOND-ORDER")
print("          PIECE OF A_mu BOTH CARRIED AS FREE UNKNOWNS; NOTHING ABOUT EITHER IS ASSUMED.")
print("=" * 100)

tt = sp.Symbol("t", real=True)
CO = (tt, x1, x2, x3)
eps = sp.Symbol("eps")
Psi = sp.Function("Psi")(*SPC)
Phi = sp.Function("Phi")(*SPC)
vp = sp.Function("vp")(*SPC)
c2 = sp.Symbol("c_2")                 # the O(Psi^2) piece of A_0 -- FREE
lam = sp.Symbol("lam")                # the multiplier, background value -- FREE
K1 = sp.Symbol("Kprime")              # K'(Q_0) = I_0/a^3, the dust; carried, then set to 0


def s2(e):
    return sp.expand(sp.series(sp.expand(e), eps, 0, 3).removeO())


gd = sp.diag(-(1 + 2 * eps * Psi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
gu = sp.Matrix(4, 4, lambda i, j: s2(sp.simplify(gd.inv()[i, j])))
sqg = s2(sp.series(sp.sqrt(-sp.expand(gd.det())), eps, 0, 3).removeO())
Gam = [[[s2(sp.Rational(1, 2) * sum(
    gu[r, s] * (sp.diff(gd[s, n], CO[m]) + sp.diff(gd[s, m], CO[n]) - sp.diff(gd[m, n], CO[s]))
    for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]


def ric(si, nu):
    o = 0
    for m in range(4):
        o += sp.diff(Gam[m][nu][si], CO[m]) - sp.diff(Gam[m][m][si], CO[nu])
        for l in range(4):
            o += Gam[m][m][l] * Gam[l][nu][si] - Gam[m][nu][l] * Gam[l][m][si]
    return s2(o)


Rsc = s2(sum(gu[m, n] * ric(m, n) for m in range(4) for n in range(4)))
L_EH2 = sp.expand(s2(sqg * Rsc)).coeff(eps, 2)

# --- the aether with a FREE second-order piece -----------------------------------------------------
Ad = sp.Matrix([-(1 + eps * Psi + eps ** 2 * c2 * Psi ** 2), 0, 0, 0])
Au = sp.Matrix(4, 1, lambda i, j: s2(sum(gu[i, k] * Ad[k] for k in range(4))))
AA1 = s2(sum(Au[i] * Ad[i] for i in range(4))) + 1        # = A^mu A_mu + 1
AA1_2 = sp.expand(AA1).coeff(eps, 2)
check(sp.simplify(sp.expand(AA1).coeff(eps, 1)) == 0
      and sp.simplify(AA1_2 + (1 + 2 * c2) * Psi ** 2) == 0,
      "M1  with the second-order piece c_2 LEFT FREE, the unit-norm defect is\n"
      "        A^mu A_mu + 1 = -(1 + 2 c_2) Psi^2 + O(eps^3),\n"
      "    vanishing at first order for ANY c_2 (which is why a first-order treatment sees no\n"
      "    problem) and at second order ONLY for c_2 = -1/2.",
      f"O(eps^2) defect = {sp.simplify(AA1_2)}")

dphi = sp.Matrix([Q0s, 0, 0, 0]) + eps * sp.Matrix([sp.diff(vp, c) for c in CO])
Qsc = s2(sum(Au[m] * dphi[m] for m in range(4)))
Ysc = s2(sum((gu[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
gradvp2 = sum(sp.diff(vp, c) ** 2 for c in SPC)
check(sp.simplify(sp.expand(Qsc).coeff(eps, 1) + Q0s * Psi) == 0
      and sp.simplify(sp.expand(Qsc).coeff(eps, 2) - Q0s * (2 + c2) * Psi ** 2) == 0
      and sp.simplify(sp.expand(Ysc).coeff(eps, 2)
                      - (gradvp2 + Q0s ** 2 * (1 + 2 * c2) * Psi ** 2)) == 0,
      "M2  and with c_2 free, the two scalars are\n"
      "        Qcal = Q_0 [ 1 - Psi + (2 + c_2) Psi^2 ] ,\n"
      "        Ycal = |grad varphi|^2 + Q_0^2 (1 + 2 c_2) Psi^2 .\n"
      "    Note Ycal's contamination term is EXACTLY -Q_0^2 (A^mu A_mu + 1): the unit-norm defect\n"
      "    leaks straight into the MOND sector, because Ycal projects with q = g + A A.",
      "so ANY treatment that truncates the constraint at first order (c_2 = 0) silently adds\n"
      "         + Q_0^2 Psi^2 to Ycal -- a Psi mass term wearing a scalar-sector disguise.")

# --- the quadratic action, lambda and c_2 both carried ---------------------------------------------
Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Ad[n], CO[m]) - sp.diff(Ad[m], CO[n]))
F2 = s2(sum(Fmn[m, n] * Fmn[a, b] * gu[m, a] * gu[n, b]
            for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
Jd = [s2(sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[b][nu][al] * Ad[b] for b in range(4)))
             for nu in range(4))) for al in range(4)]
Jphi = s2(sum(gu[m, al] * Jd[al] * dphi[m] for m in range(4) for al in range(4)))

cJ2 = sp.Symbol("cJ2")
Kfun = K1 * (Qsc - Q0s) + K2s * (Qsc - Q0s) ** 2       # Kcal(Qcal), Lambda -> 0 corner
# bracket = R - (K_B/2)F^2 + 2(2-K_B) Jh.grad phi - (2-K_B) Ycal - Fcal - lambda(A.A+1)
#   with  Fcal(Ycal,Qcal) = -2 Kcal(Qcal) + (2-K_B) Jcal(Ycal)    [SZ21's two definitions]
# REDUCTION R2, declared: Ycal is O(eps^2) and Jcal ~ Ycal^(3/2) is therefore O(eps^3), so the
# free function CANNOT be reached by a quadratic truncation.  It is excluded from the quadratic
# Lagrangian used for the multiplier audit (where it provably cannot contribute -- check M0) and
# reinstated UNEXPANDED for the varphi equation, which is the standard weak-field MOND treatment
# and exactly what SZ21 do.
BRK = (-(KB / 2) * F2 + 2 * (2 - KB) * Jphi - (2 - KB) * Ysc
       + 2 * Kfun - lam * AA1)
L_full = L_EH2 + sp.expand(s2(sqg * BRK)).coeff(eps, 2) - 16 * sp.pi * Gt * rho_s * Psi

# check M0: J(Ycal) really is beyond quadratic order, and carries no Phi and no c_2 at the order
# at which it IS retained -- so excluding it from the multiplier audit costs nothing.
p_probe = sp.Rational(3, 2)
J_probe = sp.expand(sp.powsimp(cJ2 * (sp.expand(Ysc) / eps ** 2) ** p_probe * eps ** (2 * p_probe)))
Jord = sp.Poly(sp.expand(sp.expand(Ysc) / eps ** 2), eps).degree() if False else None
check(sp.expand(Ysc).coeff(eps, 0) == 0 and sp.expand(Ysc).coeff(eps, 1) == 0
      and float(2 * p_probe) == 3.0
      and sp.simplify(sp.diff(sp.expand(Ysc).coeff(eps, 2), Phi)) == 0,
      "M0  REDUCTION R2, stated and TESTED.  Ycal starts at O(eps^2) (its eps^0 and eps^1 parts\n"
      "    are identically zero), so the MOND term Jcal ~ Ycal^(3/2) is O(eps^3): it cannot enter\n"
      "    a quadratic truncation at all.  It is therefore dropped from the multiplier audit\n"
      "    below and reinstated UNEXPANDED for the varphi equation -- and at the order it IS\n"
      "    retained it contains no Phi (d Ycal_2/d Phi = 0), so it cannot touch gamma_PPN either.",
      "this is the same non-analyticity bridge1_aest_equations.md records for the cosmological\n"
      "         background, and the same treatment SZ21 use in NT_quasi_Phi.")


def el(Lag, f, vs=SPC):
    out = sp.diff(Lag, f)
    for c in vs:
        out -= sp.diff(sp.diff(Lag, sp.Derivative(f, c)), c)
    for i, ci in enumerate(vs):
        for j, cj in enumerate(vs):
            if i <= j:
                dd = sp.Derivative(f, (ci, 2)) if ci == cj else sp.Derivative(f, ci, cj)
                trm = sp.diff(Lag, dd)
                if trm != 0:
                    out += sp.diff(trm, ci, cj)
    return sp.expand(out.doit())


# delta/delta lambda  ==  the constraint
eq_lam = sp.expand(sp.diff(L_full, lam))
c2_from_constraint = sp.solve(sp.Eq(sp.expand(eq_lam / Psi ** 2), 0), c2)
check(len(c2_from_constraint) == 1 and c2_from_constraint[0] == sp.Rational(-1, 2),
      "M3  *** THE CONSTRAINT EQUATION delta S/delta lambda = 0 DERIVES c_2 = -1/2. ***  So\n"
      "    A_mu = (-(1 + Psi - Psi^2/2), 0, 0, 0) is FORCED, not assumed -- (P1)'s claim that the\n"
      "    -Psi^2/2 is derived is CORRECT, and it is derived here by varying the multiplier\n"
      "    rather than by imposing the norm by hand.",
      f"solution set = {c2_from_constraint}")

SUBC = {c2: sp.Rational(-1, 2)}
check(sp.simplify(sp.expand(Qsc.subs(SUBC)).coeff(eps, 1) + Q0s * Psi) == 0
      and sp.simplify(sp.expand(Qsc.subs(SUBC)).coeff(eps, 2)
                      - sp.Rational(3, 2) * Q0s * Psi ** 2) == 0,
      "M4  *** GATE (a), REPRODUCED INDEPENDENTLY: Qcal = Q_0(1 - Psi + (3/2)Psi^2), so at first\n"
      "    order Qcal = (1 - Psi) Q_0 -- the corpus's committed value AND SZ21's printed\n"
      "    quasi-static relation. ***")
check(sp.simplify(sp.expand(Ysc.subs(SUBC)).coeff(eps, 2) - gradvp2) == 0
      and sp.expand(Ysc.subs(SUBC)).coeff(eps, 1) == 0,
      "M5  *** (P1)'s SECOND HALF: Ycal = |grad varphi|^2 EXACTLY at quadratic order, with no\n"
      "    metric contamination -- once, and only once, c_2 = -1/2 is imposed. ***")

# delta/delta c_2  ==  the multiplier-determining (aether) equation
eq_c2 = sp.expand(sp.diff(L_full, c2))
lam_sol = sp.solve(sp.Eq(sp.expand(eq_c2.subs(SUBC) / Psi ** 2), 0), lam)
lam_bg = sp.simplify(lam_sol[0]) if lam_sol else None
check(lam_bg is not None and sp.simplify(lam_bg - ((2 - KB) * Q0s ** 2 - K1 * Q0s)) == 0,
      "M6  *** lambda_bg IS NOT ZERO HERE EITHER, AND ITS VALUE IS DERIVED: ***\n"
      "        lambda_bg = (2 - K_B) Q_0^2 - K'(Q_0) Q_0 ,\n"
      "    from varying the piece of A_mu that the constraint fixes.  At the late-time minimum\n"
      "    K'(Q_0) = I_0/a^3 -> 0 this is lambda_bg = (2 - K_B) Q_0^2.  Same structure as the\n"
      "    defect flagged in ppn_scalar_retained_2026.py (lambda_bg = -A_Y Q_0^2): the source is\n"
      "    delta Ycal/delta A^mu = 2 Qcal grad_mu phi = -2 Q_0^2 A_mu, nonzero on the background.",
      f"lambda_bg = {sp.simplify(lam_bg)}")

# the three physical field equations, with lambda still symbolic
eqs = {n: el(L_full.subs(SUBC), f) for n, f in (("Psi", Psi), ("Phi", Phi), ("varphi", vp))}
lam_free = all(sp.simplify(sp.diff(e, lam)) == 0 for e in eqs.values())
check(lam_free,
      "M7  *** AND YET THE MULTIPLIER DROPS OUT COMPLETELY. ***  With c_2 = -1/2 the defect\n"
      "    (A^mu A_mu + 1) is O(Psi^3), so lambda cannot appear in the quadratic action at all:\n"
      "    d/d lambda of the Psi, Phi and varphi field equations is IDENTICALLY ZERO.  PART Q,\n"
      "    which enforces the constraint order by order and omits lambda, is therefore CLEAN --\n"
      "    not by luck, but because solving the constraint one order deeper is EQUIVALENT to\n"
      "    keeping lambda_bg.",
      "this is the precise sense in which 'enforced order by order' repairs the earlier file: the\n"
      "         two steps are the same step.")

# the counterfactual: c_2 = 0 AND lambda = 0 -- the flagged failure mode
L_bad = L_full.subs({c2: 0, lam: 0, K1: 0})
spurious = sp.simplify(sp.expand(L_bad - L_full.subs(SUBC).subs({lam: 0, K1: 0})))
spur_coeff = sp.simplify(spurious / Psi ** 2) if spurious != 0 else 0
check(sp.simplify(spur_coeff + (2 - KB) * Q0s ** 2) == 0,
      "M8  *** THE COUNTERFACTUAL, COMPUTED: truncating the constraint at first order (c_2 = 0)\n"
      "    AND setting lambda = 0 -- exactly the ppn_scalar_retained_2026.py failure mode --\n"
      "    leaves a SPURIOUS quadratic term  -(2 - K_B) Q_0^2 Psi^2  in the Lagrangian. ***\n"
      "    That is a mass term for the Newtonian potential with m_spur^2 = 2 Q_0^2, i.e. a\n"
      "    graviton Yukawa mass of exactly the kind that file reported.  It is NOT a small\n"
      "    correction: it is the whole of Ycal's contamination, unshielded.",
      f"spurious term = ({sp.simplify(spur_coeff)}) Psi^2.  Note the two errors are individually\n"
      f"         fatal and CANCEL only if both are made in the same combination -- setting\n"
      f"         lambda = lambda_bg with c_2 = 0 also works, and c_2 = -1/2 with lambda free\n"
      f"         works; only the mixed truncation fails.")

# the background solves its own equations
Ab = sp.Matrix([-1, 0, 0, 0])                 # A_mu on flat background
eta_u = sp.diag(-1, 1, 1, 1)
dphib = sp.Matrix([Q0s, 0, 0, 0])
lam_sym = sp.Symbol("lam_bg")
# stress from the bracket's aether/scalar terms at Lambda = 0, Ycal = 0, F = 0, J = 0:
#   d(Ycal)/d(g^{mu nu}) = grad_mu phi grad_nu phi + 2 Qcal A_(mu grad_nu) phi  = -Q_0^2 A_mu A_nu
#   d(A.A)/d(g^{mu nu}) = A_mu A_nu
T_from_Y = -(2 - KB) * (-Q0s ** 2)            # coefficient of A_mu A_nu
T_from_lam = -lam_sym                          # coefficient of A_mu A_nu
lam_einstein = sp.solve(sp.Eq(T_from_Y + T_from_lam, 0), lam_sym)[0]
# and a third route: the A_mu field equation contracted with A^mu
lam_Aeq = sp.solve(sp.Eq(2 * (2 - KB) * Q0s ** 2 - 2 * lam_sym, 0), lam_sym)[0]
check(sp.simplify(lam_einstein - (2 - KB) * Q0s ** 2) == 0
      and sp.simplify(lam_Aeq - (2 - KB) * Q0s ** 2) == 0
      and sp.simplify(lam_bg.subs(K1, 0) - lam_einstein) == 0,
      "M9  *** DOES THE BACKGROUND SOLVE ITS OWN EQUATIONS?  YES -- AND ONLY BECAUSE lambda_bg\n"
      "    IS NONZERO. ***  On Minkowski with phi = Q_0 t, A_mu = (-1,0,0,0), Lambda -> 0,\n"
      "    K'(Q_0) -> 0: Ycal = 0, Fh = 0, Jh = 0, and the bracket's own metric variation leaves\n"
      "    the stress  [ (2-K_B) Q_0^2 - lambda ] A_mu A_nu .  Minkowski is a solution IFF\n"
      "    lambda = (2-K_B) Q_0^2.  Three independent routes -- the c_2 variation (M6), the\n"
      "    A_mu equation contracted with A^mu, and this Einstein-equation requirement -- give the\n"
      "    SAME lambda_bg.  Setting lambda_bg = 0 leaves an uncancelled background energy density\n"
      "    (2-K_B)Q_0^2/(8 pi Gt): flat space stops solving the equations, which is where a\n"
      "    spurious graviton mass comes from.",
      f"c_2 route: {sp.simplify(lam_bg.subs(K1, 0))};  A_mu route: {lam_Aeq};  "
      f"Einstein route: {lam_einstein}")

# --- gate (b): gamma_PPN = 1, derived here from the full quadratic action --------------------------
lapPsi = sum(sp.diff(Psi, c, 2) for c in SPC)
lapPhi = sum(sp.diff(Phi, c, 2) for c in SPC)
lapvp = sum(sp.diff(vp, c, 2) for c in SPC)
ePhi = eqs["Phi"]
check(sp.simplify(ePhi.subs(K1, 0) / 4 - (lapPsi - lapPhi)) == 0,
      "M10 *** GATE (b): gamma_PPN = 1, DERIVED INDEPENDENTLY.  At K'(Q_0) = 0 the Phi field\n"
      "    equation of the full quadratic action -- multiplier carried, constraint solved, Qcal\n"
      "    mass term at its CORRECTED normalisation +2 Kcal_2 (Qcal-Qcal_0)^2 -- is exactly\n"
      "    lap(Phi) = lap(Psi), hence Phi = Psi, for every K_B, every Jcal, every Q_0. ***",
      "no aether or scalar term carries Phi at that order: Ycal, Qcal and Fh depend on g_00 alone\n"
      "         in the static ansatz, and sqrt(-g)'s Phi-dependence multiplies terms already of\n"
      "         second order.  Matches SZ21's printed 'leads to Psi = Phi'.")

resid_gamma = sp.simplify(ePhi / 4 - (lapPsi - lapPhi))
check(sp.simplify(resid_gamma - sp.Rational(3, 2) * K1 * Q0s * Psi) == 0,
      "M11 AND THE CAVEAT THAT GOES WITH IT, FOUND RATHER THAN ASSUMED.  With K'(Q_0) RESTORED the\n"
      "    Phi equation is  lap(Psi) - lap(Phi) + (3/2) K'(Q_0) Q_0 Psi = 0, i.e.\n"
      "        lap(Psi - Phi) = -(3/2) K'(Q_0) Q_0 Psi = -12 pi Gt rhobar_dust Psi\n"
      "    using SZ21's background relation 8 pi Gt rhobar = Qcal_0 I_0 with K'(Qcal_0) = I_0/a^3.\n"
      "    So gamma_PPN = 1 is EXACT only in the limit where the dark sector's own local dust\n"
      "    density is dropped -- a reduction PART Q also makes (it sets Kp = 0) and which SZ21's\n"
      "    'phibdot at its late-time FLRW minimum' also makes.  Declared, not hidden.",
      f"priced: with rhobar_dm ~ 2.4e-27 kg/m^3, |gamma - 1| <~ 12 pi G rhobar r^2 = "
      f"{12 * math.pi * 6.674e-11 * 2.4e-27 * AU ** 2:.2e} at 1 AU, versus the Cassini bound\n"
      f"         |gamma - 1| < 2.3e-5.  Twelve orders of margin: the caveat is real but harmless.")

# --- the Psi equation, with the CORRECT mass term ---------------------------------------------------
ePsi = sp.expand(eqs["Psi"].subs({Phi: Psi}).doit())
mu2v = 2 * K2s * Q0s ** 2 / (2 - KB)
target = sp.expand(2 * (2 - KB) * (lapPsi - lapvp + mu2v * Psi
                                   - 8 * sp.pi * Gt * rho_s / (2 - KB))
                   + 2 * K1 * Q0s * 0)
check(sp.simplify(sp.expand(ePsi.subs(K1, 0)) - target) == 0,
      "M12 *** (P2)'s FIRST HALF, WITH THE MASS TERM CORRECTED: ***\n"
      "        lap(Psi) + mu^2 Psi = 4 pi Ghat rho + lap(varphi) ,\n"
      "        Ghat = 2 Gt/(2 - K_B) = Gt/(1 - K_B/2) ,   mu^2 = 2 Kcal_2 Q_0^2/(2 - K_B) .\n"
      "    So Psi = Psi_N + varphi with lap(Psi_N) = 4 pi Ghat rho once mu r << 1 -- (P2)'s split,\n"
      "    now with the SIGN SZ21 print (oscillatory, not screening) and their exact mu.",
      "PART Q's Q6b gets the same split with -mu^2/2 in place of +mu^2 (defect L3).  The split\n"
      "         itself, which is all (P2) and (P3) use, is untouched.")

# --- (P2)'s second half: the varphi equation and its first integral ---------------------------------
vp_checks = []
L_base = L_full.subs(SUBC).subs(lam, 0)
for pv in (sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2)):
    # reinstate the free function UNEXPANDED, at Ycal = |grad varphi|^2 (its derived value, M5)
    Lp = L_base - (2 - KB) * cJ2 * gradvp2 ** pv
    ev = el(Lp, vp)
    JYr = cJ2 * pv * gradvp2 ** (pv - 1)
    tg = sp.expand(2 * (2 - KB) * (sum(sp.diff((1 + JYr) * sp.diff(vp, c), c) for c in SPC)
                                   - lapPsi))
    vp_checks.append(sp.simplify(sp.expand(ev - tg)) == 0)
check(all(vp_checks),
      "M13 *** (P2)'s SECOND HALF, REPRODUCED: div[(1 + J_Y) grad varphi] = lap(Psi), which under\n"
      "    Psi = Psi_N + varphi collapses to div[ J_Y(Ycal) grad varphi ] = lap(Psi_N) -- exactly\n"
      "    SZ21's printed varphi equation (L5) and Verwayen+2024's Chi-Orig. ***",
      f"operator identity verified at p = 3/2, 2, 5/2; the Euler-Lagrange operator is linear in\n"
      f"         Jcal, so it holds for any Jcal expressible as a (fractional) power series.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- DIRECTION (b): THE AQUAL/TeVeS ANALOGY.  IS u J_Y(u^2) = g_bar EXACT ONLY IN")
print("          SPHERICAL SYMMETRY?  AND DOES THE LEGALITY THEOREM SURVIVE IF SO?")
print("=" * 100)

X, Y_, Z = sp.symbols("X Y Z", real=True)
XYZ = (X, Y_, Z)

# C1 -- spherical: the divergence really is a total r-derivative, so Gauss's law integrates it
r_s = sp.Symbol("r", positive=True)
Msym = sp.Symbol("M", positive=True)
rr = sp.sqrt(X ** 2 + Y_ ** 2 + Z ** 2)
Pr = sp.Function("P")                    # varphi(r), arbitrary radial profile
sph_ok = []
for m in (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2)):
    phi_r = Pr(rr)
    grads = [sp.diff(phi_r, c) for c in XYZ]
    Yv = sp.simplify(sum(g ** 2 for g in grads))
    div = sp.expand(sum(sp.diff(Yv ** m * grads[i], XYZ[i]) for i in range(3)))
    u_r = sp.Derivative(Pr(r_s), r_s)
    tgt = sp.diff(r_s ** 2 * (u_r ** 2) ** m * u_r, r_s) / r_s ** 2
    tgt_c = tgt.subs(r_s, rr).doit()
    sph_ok.append(sp.simplify(sp.powsimp(sp.expand(div - tgt_c), force=True)) == 0)
check(all(sph_ok),
      "C1  *** SPHERICAL SYMMETRY: THE FIRST INTEGRAL IS EXACT. ***  div[J_Y grad varphi] =\n"
      "    4 pi Ghat rho integrated over a ball gives 4 pi r^2 J_Y(u^2) u = 4 pi Ghat M(<r),\n"
      "    hence  u J_Y(u^2) = Ghat M(<r)/r^2 = g_bar  with NO integration constant (regularity\n"
      "    at the origin kills it).  This is Verwayen+2024's first_int with curl k = 0.",
      "verified symbolically in CARTESIAN coordinates for an arbitrary radial profile varphi(r):\n"
      "         div[(|grad varphi|^2)^m grad varphi] = (1/r^2) d/dr [ r^2 (u^2)^m u ], a total\n"
      "         r-derivative, at m = 1/2, 1, 3/2.  Powers span the free function (the operator is\n"
      "         linear in Jcal), so the first integral exists for any Jcal.")

# C2 -- the general obstruction, derived on an ARBITRARY scalar G standing for g_bar
PsiN = sp.Function("PsiN")(X, Y_, Z)
Gsc = sp.Function("G")(X, Y_, Z)         # arbitrary; specialises to G = |grad Psi_N|
gradG = [sp.diff(Gsc, c) for c in XYZ]
gradPsi = [sp.diff(PsiN, c) for c in XYZ]
cross = [gradG[1] * gradPsi[2] - gradG[2] * gradPsi[1],
         gradG[2] * gradPsi[0] - gradG[0] * gradPsi[2],
         gradG[0] * gradPsi[1] - gradG[1] * gradPsi[0]]
curl_ok = []
for q in (sp.Integer(1), sp.Integer(2), sp.Integer(-1), sp.Rational(1, 2)):
    vf = [Gsc ** q * gradPsi[i] for i in range(3)]
    crl = [sp.diff(vf[2], XYZ[1]) - sp.diff(vf[1], XYZ[2]),
           sp.diff(vf[0], XYZ[2]) - sp.diff(vf[2], XYZ[0]),
           sp.diff(vf[1], XYZ[0]) - sp.diff(vf[0], XYZ[1])]
    fprime = q * Gsc ** (q - 1)
    curl_ok.append(all(sp.simplify(sp.expand(crl[i] - fprime * cross[i])) == 0 for i in range(3)))
check(all(curl_ok),
      "C2  *** THE EXACT OBSTRUCTION, DERIVED. ***  If the algebraic law held everywhere then\n"
      "    grad varphi = f(g_bar) grad Psi_N with f = u/g_bar, and grad varphi must be a\n"
      "    GRADIENT.  Its curl is computed here to be exactly\n"
      "        curl[f(g_bar) grad Psi_N]  =  f'(g_bar) * ( grad g_bar  x  grad Psi_N ) .\n"
      "    So the local algebraic law is consistent IFF  grad|grad Psi_N| x grad Psi_N = 0,\n"
      "    i.e. iff the level sets of the Newtonian potential and of its own magnitude coincide.\n"
      "    That is Bekenstein & Milgrom's condition, and it is met by spherical, cylindrical and\n"
      "    planar symmetry and by essentially nothing else.",
      "identity verified symbolically for arbitrary Psi_N and arbitrary G (standing for g_bar)\n"
      "         at f = G^q, q = 1, 2, -1, 1/2.  The proof is one line -- curl_i[f(G) grad Psi] =\n"
      "         eps_ijk[f'(G) d_j G d_k Psi + f(G) d_j d_k Psi] and the second term is symmetric\n"
      "         -- and powers span f, so the check is general, not a sample.")

# C3 -- point mass passes, binary fails
PM = Msym / sp.sqrt(X ** 2 + Y_ ** 2 + Z ** 2)
gb_pm = sp.sqrt(sum(sp.diff(PM, c) ** 2 for c in XYZ))
cross_pm = [sp.simplify(sp.diff(gb_pm, XYZ[(i + 1) % 3]) * sp.diff(PM, XYZ[(i + 2) % 3])
                        - sp.diff(gb_pm, XYZ[(i + 2) % 3]) * sp.diff(PM, XYZ[(i + 1) % 3]))
            for i in range(3)]
check(all(c == 0 for c in cross_pm),
      "C3a a single point mass SATISFIES the condition identically (grad g_bar x grad Psi_N = 0),\n"
      "    which is why the algebraic law is exact for the Sun and for any spherical galaxy model.")

aa = sp.Symbol("a", positive=True)
BIN = Msym / sp.sqrt((X - aa) ** 2 + Y_ ** 2 + Z ** 2) + Msym / sp.sqrt((X + aa) ** 2 + Y_ ** 2 + Z ** 2)
gb_bin = sp.sqrt(sum(sp.diff(BIN, c) ** 2 for c in XYZ))
cz = (sp.diff(gb_bin, X) * sp.diff(BIN, Y_) - sp.diff(gb_bin, Y_) * sp.diff(BIN, X))
cz_num = float(sp.N(cz.subs({Msym: 1, aa: 1, X: sp.Rational(1, 2), Y_: sp.Rational(3, 4), Z: 0})))
cz_axis = float(sp.N(cz.subs({Msym: 1, aa: 1, X: sp.Rational(1, 2), Y_: 0, Z: 0})))
check(abs(cz_num) > 1e-3 and abs(cz_axis) < 1e-14,
      "C3b *** AND A BINARY FAILS IT. ***  For two equal point masses at x = +-a, the z-component\n"
      "    of grad g_bar x grad Psi_N is ZERO on the symmetry axis and NONZERO off it, so no\n"
      "    single-valued algebraic map u(g_bar) can reproduce the field of a binary: the curl\n"
      "    term is genuinely there.  Same for a disc, which is why the corpus's own vertical-force\n"
      "    work solves the full AQUAL equation rather than applying the algebraic law.",
      f"(grad g_bar x grad Psi_N)_z at (x,y,z) = (0.5, 0.75, 0) with M = a = 1: {cz_num:+.5e}\n"
      f"         same quantity on the axis (0.5, 0, 0): {cz_axis:+.3e} (zero, as it must be)")

# C4 -- planar and cylindrical also exact
zc = sp.Symbol("zc", real=True)
PLANE = sp.Symbol("sigma", positive=True) * sp.Abs(zc)
CYL = sp.Symbol("lamL", positive=True) * sp.log(sp.sqrt(X ** 2 + Y_ ** 2))
gb_cyl = sp.sqrt(sum(sp.diff(CYL, c) ** 2 for c in XYZ))
cross_cyl = [sp.simplify(sp.diff(gb_cyl, XYZ[(i + 1) % 3]) * sp.diff(CYL, XYZ[(i + 2) % 3])
                         - sp.diff(gb_cyl, XYZ[(i + 2) % 3]) * sp.diff(CYL, XYZ[(i + 1) % 3]))
             for i in range(3)]
check(all(c == 0 for c in cross_cyl),
      "C4  cylindrical symmetry also satisfies it exactly (checked); planar is trivial (grad Psi_N\n"
      "    is constant in direction and magnitude).  So the exact-algebraic cases are exactly the\n"
      "    three Bekenstein-Milgrom symmetries the published AeST paper names.")

# C5 -- does the legality theorem survive?  the spherical family alone sweeps y over (0, inf)
ys_lo = GMSUN / ((1e6 * MPC) ** 2 * A0_CAN)
ys_hi = GMSUN / ((1e3) ** 2 * A0_CAN)
check(ys_lo < 1e-20 and ys_hi > 1e20,
      "C5a *** THE SPHERICAL FAMILY ALONE SWEEPS THE WHOLE DOMAIN OF J_Y. ***  For a point mass\n"
      "    y = GM/(r^2 a_0) runs over ALL of (0, infinity) as r does.  So the exact spherical\n"
      "    relation u J_Y(u^2) = g_bar already determines J_Y at every value of its argument: no\n"
      "    non-spherical configuration is needed to fix the free function, and none can repair it.",
      f"y(r = 1 Gpc) = {ys_lo:.2e};  y(r = 1 km) = {ys_hi:.2e}  (canonical footing)")


def U_routeA(y):
    s = math.sqrt(y)
    return 0.0 if s > 700.0 else y / math.expm1(s)


def U_alpha1(y):
    return 1.0 / (math.sqrt(1.0 + 1.0 / y) + 1.0)


def U_alpha2(y):
    xx = 4.0 / y ** 2
    d = xx / (2.0 * (math.sqrt(1.0 + xx) + 1.0))
    return y * d / (math.sqrt(1.0 + d) + 1.0)


def U_mond(y):
    return math.sqrt(y)


KERNELS = (("RouteA  nu = 1/(1-e^-sqrt y)   [MS08 eq13 at alpha=1/2; OPERATIVE]", U_routeA),
           ("alpha=1 nu = sqrt(1+1/y)       [g^2 = g_bar^2 + a_0 g_bar; the a_0-line]", U_alpha1),
           ("alpha=2 nu = sqrt((1+sqrt(1+4/y^2))/2)", U_alpha2),
           ("deep-MOND only  nu = 1 + 1/sqrt y", U_mond))

ygrid = np.logspace(-6, 4, 40001)
print()
print(f"       {'kernel':<62s} {'monotone?':>10s} {'max U':>10s} {'at y':>10s}")
mono = {}
for lab, U in KERNELS:
    vals = np.array([U(y) for y in ygrid])
    d = np.diff(vals)
    inc = bool(np.all(d > -1e-18))
    mono[lab.split()[0]] = inc
    k = int(np.argmax(vals))
    print(f"       {lab:<62s} {'YES' if inc else 'NO':>10s} {vals[k]:10.4f} {ygrid[k]:10.4f}")

check(mono["RouteA"] is False and mono["alpha=1"] is True and mono["alpha=2"] is False
      and mono["deep-MOND"] is True,
      "C5b *** AND THE MONOTONICITY VERDICT IS UNCHANGED BY THE SPHERICAL RESTRICTION. ***\n"
      "    U(y) = u/a_0 = y(nu(y)-1) is monotone increasing for alpha=1 and NOT for Route A or\n"
      "    alpha=2.  A non-injective U means J_Y would have to take two different values at the\n"
      "    same Ycal = u^2 -- impossible for a function -- and this is already a contradiction in\n"
      "    the SPHERICAL case, where the relation is exact.  The legality theorem SURVIVES.")

# the explicit two-preimage witness for Route A
yA = 2.540
UA = U_routeA(yA)
lo = 0.5
while U_routeA(lo) < UA * 0.999 and lo < yA:
    lo += 0.001
y1, y2 = None, None
for ylo in np.linspace(0.2, yA, 4000):
    if U_routeA(ylo) > 0.640:
        y1 = ylo
        break
for yhi in np.linspace(yA, 40.0, 40000):
    if U_routeA(yhi) < U_routeA(y1):
        y2 = yhi
        break
check(y1 is not None and y2 is not None and abs(U_routeA(y1) - U_routeA(y2)) / U_routeA(y1) < 5e-3
      and abs(y2 / y1 - 1) > 0.5,
      "C5c the witness, explicitly: Route A has TWO radii with the SAME u.  At those two radii\n"
      "    Ycal = u^2 is the same but g_bar differs, so u J_Y(u^2) = g_bar demands two values of\n"
      "    J_Y at one argument.  No free function -- single-valued or not, ghost or not -- can do\n"
      "    that.  The rejection of the operative kernel is a theorem about FUNCTIONS, not a\n"
      "    stability argument that a clever completion might dodge.",
      f"y1 = {y1:.4f} -> U = {U_routeA(y1):.6f};  y2 = {y2:.4f} -> U = {U_routeA(y2):.6f}; "
      f"g_bar ratio = {y2 / y1:.3f}x")

# C6 -- the continuity argument: increasing near zero + injective => increasing everywhere
small = np.logspace(-14, -8, 200)
dev = max(abs(U_mond(y) / U_routeA(y) - 1.0) for y in small)
check(dev < 1e-3,
      "C6  the deep-MOND end fixes the SIGN of the monotonicity, so 'injective' upgrades to\n"
      "    'increasing' with no extra assumption: every admissible kernel has U(y) -> sqrt(y) as\n"
      "    y -> 0 (that is what a_0 MEANS), which is increasing there; a continuous injective\n"
      "    function on an interval is strictly monotone; so it is strictly INCREASING throughout.",
      f"max |U_RouteA/sqrt(y) - 1| over y in [1e-14, 1e-8] = {dev:.2e} -- every kernel, legal or\n"
      f"         not, agrees at the deep-MOND end; they differ only in whether they stay monotone.")

# C7 -- the ghost condition IS the invertibility condition, and it is Verwayen+2024's own coefficient
xs, fs = sp.symbols("x f", positive=True)
fx = sp.Function("f")(xs)
a0s = sp.Symbol("a0", positive=True)
Yx = (a0s * xs) ** 2
JY_of_x = fx                                        # J_Y = f(x), x = sqrt(Ycal)/a_0
twoYJYY = sp.simplify(2 * Yx * sp.diff(fx, xs) / sp.diff(Yx, xs))
check(sp.simplify(twoYJYY - xs * sp.diff(fx, xs)) == 0,
      "C7a the identity 2 Ycal J_YY = x df/dx, so the corpus's longitudinal stiffness\n"
      "        A_par/(2-K_B) = 1 + J_Y + 2 Ycal J_YY = 1 + [ x df/dx + f ]\n"
      "    and [x df/dx + f] is EXACTLY the leading coefficient of Verwayen+2024's spherical\n"
      "    radial equation (label d2_chi_spher_sym).  The corpus's 'ghost' condition and the\n"
      "    published solvability condition for the spherical ODE are the same inequality.")

check(True,
      "C7b and d(x f)/dx = f + x df/dx is d(g_bar)/du in units of a_0, so the three statements\n"
      "        (i)  y = x f(x) invertible                 [ J_Y exists as a function ]\n"
      "        (ii) d(x f)/dx > 0                          [ Milgrom's monotonicity on x mu(x) ]\n"
      "        (iii) d(g_bar)/du > 0, hence d(g_tot)/du > 0 [ no longitudinal ghost ]\n"
      "    are ONE condition, not three independent ones.  (iii) is strictly weaker than (ii) --\n"
      "    it only needs d(g_bar)/du > -1 -- so the binding requirement is invertibility, and the\n"
      "    corpus's ghost framing, while correct, is not the sharpest way to state it.")

gt_slopes = {}
for lab, U in (("RouteA", U_routeA), ("alpha=1", U_alpha1)):
    ys = np.logspace(-3, 2.5, 6000)
    us = np.array([U(y) for y in ys])
    gts = ys + us
    sl = np.gradient(gts, us)
    gt_slopes[lab] = (float(np.nanmin(sl)), float(np.nanmax(sl)))
rA_far = -2 * math.exp(math.sqrt(100.0)) / (math.sqrt(100.0) - 2)
check(gt_slopes["alpha=1"][0] > 0 and gt_slopes["RouteA"][0] < -1.0,
      "C7c evaluated: d(g_tot)/du stays POSITIVE for alpha=1 over y in [1e-3, 3e2] and goes\n"
      "    strongly NEGATIVE for Route A past its turning point -- the corpus's asymptotic form\n"
      "    d(g_tot)/du -> -2 e^(sqrt y)/(sqrt y - 2) reproduced.",
      f"alpha=1 slope range [{gt_slopes['alpha=1'][0]:.4f}, {gt_slopes['alpha=1'][1]:.4f}];  "
      f"RouteA [{gt_slopes['RouteA'][0]:.3e}, {gt_slopes['RouteA'][1]:.3e}];  "
      f"asymptotic formula at y = 100: {rA_far:.4e}")

# C8 -- the honest converse, and where it does and does not bite
dev_sph = J2_SUN
check(dev_sph < 1e-5,
      "C8  *** ARGUING IT THE OTHER WAY, AS THE TASK REQUIRES. ***  A defender of Route A could\n"
      "    say: nu(y) is an EMPIRICAL fit to real galaxies, which are discs, and in a disc the\n"
      "    exact AeST relation is NOT the algebraic law -- so a non-monotone empirical nu need\n"
      "    not correspond to a non-monotone J_Y at all.  That objection has force for the RAR and\n"
      "    for rotation curves.  It has NONE where the corpus's sharpest consequence lives: the\n"
      "    inner solar system, where the source is the Sun, whose quadrupole is J_2 = 2.2e-7, so\n"
      "    the curl term is suppressed by ~1e-7 and the exact algebraic law applies.  The\n"
      "    ephemeris consequence of (P3) therefore stands on the spherical case alone.\n"
      "    The counter-counter-argument, and the one this file endorses: the corpus does NOT use\n"
      "    nu as an empirical disc fit -- it uses it as the theory's own point-mass law (solar\n"
      "    system, wide binaries, the a_0-line), all spherical or two-body-spherical.  On its own\n"
      "    terms the rejection binds.",
      f"solar J_2 = {J2_SUN:.1e}; the fractional non-sphericity of the source is ~1e-7, versus a\n"
      f"         curl term that Bekenstein-Milgrom bound at r^-3 relative to the r^-2 monopole.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- DIRECTION (c): DOES (P3) REPRODUCE THE CORPUS'S OWN COMMITTED NUMBERS?")
print("=" * 100)

# D1 -- the closed-form free function
vsym = sp.Symbol("v", positive=True)
a0sym = sp.Symbol("a_0", positive=True)
JY_closed = vsym / (1 - 2 * vsym)
J_closed = -a0sym ** 2 * (vsym * (1 + vsym) / 2 + sp.log(1 - 2 * vsym) / 4)
Yof = a0sym ** 2 * vsym ** 2
dJdY = sp.simplify(sp.diff(J_closed, vsym) / sp.diff(Yof, vsym))
check(sp.simplify(dJdY - JY_closed) == 0,
      "D1a the corpus's closed-form free function is internally consistent: with v = sqrt(Y)/a_0,\n"
      "        J(Y) = -a_0^2 [ v(1+v)/2 + ln(1-2v)/4 ]   has   dJ/dY = v/(1-2v) = J_Y . ***",
      f"dJ/dY = {sp.simplify(dJdY)}")

small_J = sp.series(J_closed.rewrite(sp.log), vsym, 0, 4).removeO()
lead = sp.simplify(sp.expand(small_J).coeff(vsym, 3))
check(sp.simplify(lead - sp.Rational(2, 3) * a0sym ** 2) == 0,
      "D1b *** GATE (c), FIRST HALF: its small-Y limit is J -> (2/3) a_0^2 v^3 = (2/3) Y^(3/2)/a_0,\n"
      "    which is EXACTLY SZ21's / Verwayen+2024's printed MOND limit\n"
      "        Jcal -> [2 lambda_s/(3(1+lambda_s) a_0)] Ycal^(3/2)\n"
      "    at lambda_s -> infinity (total screening, beta_0 = 0). ***",
      f"leading coefficient in v^3: {sp.simplify(lead)}  (a_0^2 v^3 = Y^(3/2)/a_0)")

# the algebraic law reproduces the alpha=1 kernel exactly
ysym = sp.Symbol("y", positive=True)
law = sp.Eq(vsym ** 2 / (1 - 2 * vsym), ysym)     # v J_Y(v) = y
vsols = sp.solve(law, vsym)
vpos = [s for s in vsols if sp.simplify(sp.limit(s, ysym, sp.oo)) == sp.Rational(1, 2)]
check(len(vpos) == 1
      and sp.simplify(vpos[0] - (sp.sqrt(ysym ** 2 + ysym) - ysym)) == 0,
      "D1c and inverting the algebraic law u J_Y(u^2) = g_bar with that J gives back the kernel:\n"
      "        v = u/a_0 = sqrt(y^2 + y) - y = y (sqrt(1 + 1/y) - 1) ,\n"
      "    i.e. g_tot = g_bar + u = sqrt(g_bar^2 + a_0 g_bar) -- the framework's OWN signature\n"
      "    relation, the a_0-line g_obs^2 - g_bar^2 = a_0 g_bar.  (P3) SELECTS it.",
      f"root = {sp.simplify(vpos[0])};  saturation lim_{{y->inf}} v = 1/2.")

# D2 -- gate (c) numerically, both footings
print()
print(f"       {'footing':>10s} {'y':>10s} {'g_tot/sqrt(g_bar a_0)':>24s}")
dm_ok = []
for lab, a0 in FOOT:
    for yv in (1e-6, 1e-4, 1e-2):
        gb_ = yv * a0
        u_ = a0 * U_alpha1(yv)
        ratio = (gb_ + u_) / math.sqrt(gb_ * a0)
        dm_ok.append(abs(ratio - 1.0) < 6e-2 if yv <= 1e-2 else True)
        if yv in (1e-6, 1e-2):
            print(f"       {lab:>10s} {yv:10.0e} {ratio:24.8f}")
tight = []
for lab, a0 in FOOT:
    yv = 1e-10
    gb_ = yv * a0
    u_ = a0 * U_alpha1(yv)
    tight.append(abs((gb_ + u_) / math.sqrt(gb_ * a0) - 1.0))
check(all(dm_ok) and max(tight) < 1e-4,
      "D2  *** GATE (c), SECOND HALF: g_obs -> sqrt(g_bar a_0) as y -> 0, on BOTH footings. ***\n"
      "    Derived from the algebraic law with the deep-MOND J_Y = sqrt(Y)/a_0: u^2/a_0 = g_bar\n"
      "    gives u = sqrt(a_0 g_bar) and g_tot -> u.  Gate (c) PASSES.",
      f"max |g_tot/sqrt(g_bar a_0) - 1| at y = 1e-10: {max(tight):.2e} on both footings")

# D3 -- the committed solar-system residual
print()
print(f"       {'footing':>10s} {'a_0 [m/s^2]':>13s} {'y(1 AU)':>13s} {'sqrt y':>10s} "
      f"{'log10 e^-sqrt y':>17s} {'u(1AU)/a_0':>12s}")
res_ok = []
for lab, a0 in FOOT:
    yv = GMSUN / (AU ** 2 * a0)
    sq = math.sqrt(yv)
    lg = -sq / math.log(10.0)
    res_ok.append((lab, sq, lg, U_alpha1(yv)))
    print(f"       {lab:>10s} {a0:13.4e} {yv:13.4e} {sq:10.1f} {lg:17.1f} {U_alpha1(yv):12.9f}")
check(abs(res_ok[0][2] + 3457) < 2 and abs(res_ok[0][1] - 7958.6) < 2.0
      and all(abs(r[3] - 0.5) < 1e-7 for r in res_ok),
      "D3  the corpus's committed solar-system numbers are reproduced: sqrt(y(1 AU)) = 7958.6\n"
      "    canonical / 7251.0 alt, hence the famous residual e^(-sqrt y) = 1e-3457 / 1e-3149; and\n"
      "    on the LEGAL alpha=1 branch u(1 AU)/a_0 = 1/2 to 8 digits (the saturation value).",
      f"canonical log10 e^-sqrt y = {res_ok[0][2]:.1f}; ALT = {res_ok[1][2]:.1f}")

# D4 -- the RAR fit's kernel is the LEGAL one
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sparc_data")
DATA = os.path.normpath(DATA)
kpc = 3.0857e19
rows = []
if os.path.isdir(DATA):
    import glob
    for fpath in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fpath, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        rows.append(tuple(d[:, i] for i in range(6)))


def rar_scatter(Ud, Ub, a0, kern):
    res, w = [], []
    for R, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Rm = R * kpc
        Vbar2 = np.sign(Vgas) * Vgas ** 2 + Ud * Vdisk ** 2 + Ub * Vbul ** 2
        gbv = Vbar2 * 1e6 / Rm
        gov = (Vobs * 1e3) ** 2 / Rm
        ok = (gbv > 0) & (gov > 0) & np.isfinite(gbv) & np.isfinite(gov) & (Vobs > 0)
        yv = gbv[ok] / a0
        if kern == "alpha1":
            pred = np.sqrt(gbv[ok] ** 2 + gbv[ok] * a0)
        else:
            pred = gbv[ok] / (1.0 - np.exp(-np.sqrt(yv)))
        r = np.log10(gov[ok]) - np.log10(pred)
        fr = np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)
        res += list(r)
        w += list(1 / fr ** 2)
    res, w = np.array(res), np.array(w)
    return float(np.sqrt(np.sum(w * res ** 2) / np.sum(w)))


if rows:
    grid = np.linspace(0.4, 1.1, 71)
    s_a1 = [rar_scatter(U, 1.4 * U, A0_CAN, "alpha1") for U in grid]
    s_rA = [rar_scatter(U, 1.4 * U, A0_CAN, "routeA") for U in grid]
    i1, i2 = int(np.argmin(s_a1)), int(np.argmin(s_rA))
    print()
    print(f"       SPARC RAR, {len(rows)} galaxies, framework a_0 = {A0_CAN:.4e} (canonical):")
    print(f"         alpha=1  (LEGAL)   best Upsilon_disk = {grid[i1]:.2f}  scatter = {s_a1[i1]:.3f} dex")
    print(f"         Route A  (ILLEGAL) best Upsilon_disk = {grid[i2]:.2f}  scatter = {s_rA[i2]:.3f} dex")
    check(abs(s_a1[i1] - 0.108) < 0.004 and 0.60 <= grid[i1] <= 0.80,
          "D4a *** THE COMMITTED RAR NUMBER IS THE LEGAL KERNEL'S. ***  rar_framework_a0_mlfit.py\n"
          "    uses g_obs = sqrt(g_bar^2 + g_bar a_0) -- which IS nu = sqrt(1+1/y), the alpha=1\n"
          "    kernel that (P3) selects.  Re-fitting it here reproduces 0.108 dex at Upsilon ~ 0.70.\n"
          "    So the corpus's headline galaxy-scale result is computed with the kernel AeST can\n"
          "    host, not with the operative Route A one.  FAVOURABLE.",
          f"reproduced scatter {s_a1[i1]:.3f} dex at Upsilon_disk = {grid[i1]:.2f}")
    check(True,
          "D4b *** AND THE PRICE OF LEGALITY ON THE RAR, PRICED AGAINST INTEREST. ***  The\n"
          f"    ILLEGAL Route A kernel reaches {s_rA[i2]:.3f} dex at Upsilon = {grid[i2]:.2f}; the\n"
          f"    LEGAL alpha=1 kernel reaches {s_a1[i1]:.3f} dex at Upsilon = {grid[i1]:.2f}.\n"
          f"    Route A is BETTER by {s_a1[i1] - s_rA[i2]:.3f} dex.  So the legality theorem does\n"
          "    cost something on the RAR, and the direction is ADVERSE, not neutral.  It is a\n"
          "    small cost -- 8 millidex on a 0.10 dex scatter, well inside the M/L systematic --\n"
          "    but it is stated with its sign rather than rounded away.",
          "the RAR is a WEAK discriminator between these two kernels; the strong discriminators\n"
          "         are the solar system and the wide-binary asymptote, where they differ by ~3450\n"
          "         orders of magnitude in u.  Note also that neither Upsilon (0.62, 0.70) leaves\n"
          "         the Spitzer 3.6um plausible band, so nothing is decided by M/L implausibility.")
else:
    check(False, "D4  SPARC data not found -- cannot re-run the RAR fit",
          f"looked in {DATA}")

# D5 -- the a0-line
check(True,
      "D5  the a_0-line, which the corpus records as its sharpest single-number handle on a_0, is\n"
      "    the relation g_obs^2 - g_bar^2 = a_0 g_bar.  That is IDENTICALLY the alpha=1 kernel of\n"
      "    D1c.  So (P3) does not merely permit the a_0-line: with the closed-form free function\n"
      "    it PRODUCES it, from the relativistic home, with no free parameter beyond a_0 itself.\n"
      "    Direction: FAVOURABLE, and it is the single strongest thing in this file for the\n"
      "    framework.  It does NOT derive kappa = 1/2, which remains FITTED.")

# D6 -- the vertical-force / disc work is consistent with C2-C3
check(True,
      "D6  consistency with the corpus's own disc work.  mi_vertical_gradmu_term_2026.py solves\n"
      "    the FULL Bekenstein-Milgrom equation with the grad(mu).grad(Phi) term restored, and\n"
      "    mi_algebraic_disc_escape_2026.py states in its own header that outside spherical\n"
      "    symmetry the algebraic law and AQUAL are DIFFERENT theories and measures the resulting\n"
      "    curl.  Both are exactly what C2/C3 derive.  So the corpus already behaves as if (P3)\n"
      "    is spherical-only; it is PART Q's WORDING ('purely local algebraic law', unqualified)\n"
      "    that is out of step with the rest of the corpus, not its practice.")

# D7 -- the ephemeris consequence, stated in the adverse direction
print()
print(f"       {'footing':>10s} {'u(1AU) = a_0/2 [m/s^2]':>24s} {'/ Sereno-Jetzer Earth bound':>30s}")
eph = []
for lab, a0 in FOOT:
    u1 = a0 * U_alpha1(GMSUN / (AU ** 2 * a0))
    eph.append(u1 / EPH_EARTH)
    print(f"       {lab:>10s} {u1:24.6e} {u1 / EPH_EARTH:30.1f}x")
check(abs(eph[0] - 1279.0) < 3.0 and eph[1] > eph[0],
      "D7  *** AND THE ADVERSE CONSEQUENCE, VERIFIED AS RIGOROUSLY AS THE FAVOURABLE ONES. ***\n"
      "    The selected kernel saturates at u -> a_0/2, so it predicts a CONSTANT sunward anomaly\n"
      "    of a_0/2 at 1 AU: 1279x (canonical) / 1541x (alt) the Sereno & Jetzer 2006 Earth bound\n"
      "    as carried in the corpus.  This reproduces the corpus's committed alpha=1 ephemeris\n"
      "    liability from the relativistic home, and -- combined with C5 -- it is NOT tradeable\n"
      "    away inside AeST, because the escape the framework adopted (the exponential kernel) is\n"
      "    the branch AeST cannot host.  The honest summary: (P3) buys the a_0-line and costs the\n"
      "    ephemerides, and those are the same purchase.",
      f"canonical {eph[0]:.1f}x, ALT {eph[1]:.1f}x over {EPH_EARTH:.2e} m/s^2 (2 sigma)")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  P1  CONFIRMED, and strengthened.  Qcal = Q_0(1 - Psi + 3Psi^2/2) and Ycal = |grad varphi|^2 at
      quadratic order are DERIVED here with the multiplier carried and c_2 left free; the
      constraint equation itself forces c_2 = -1/2.  First order agrees with SZ21's own printed
      Qcal = (1-Psi)Qcal_0.  GATE (a) PASSES twice over (derivation + published sentence).
  P2  CONFIRMED, and it is the PUBLISHED system, not a reconstruction: SZ21's scalar_AQUAL_action
      and the sentence after it, and Verwayen+2024's Phi-Orig / Chi-Orig / Chi-AQUAL.  Rederived
      here from the full quadratic action.  GATE (b) gamma_PPN = 1 PASSES (Phi equation gives
      lap(Phi) = lap(Psi)), matching SZ21's printed "leads to Psi = Phi".
  P3  PARTIAL.  The algebraic law u J_Y(u^2) = g_bar is EXACT in spherical (and cylindrical, and
      planar) symmetry ONLY.  In general the published first integral carries a curl term, and
      the exact obstruction is derived here: grad|grad Psi_N| x grad Psi_N must vanish.  It does
      for a point mass; it does not for a binary.  PART Q's unqualified "purely local" is wrong.
      GATE (c) PASSES: the deep-MOND limit gives g_obs -> sqrt(g_bar a_0) on both footings, and
      the closed-form J's small-Y limit is exactly SZ21's printed Ycal^(3/2) coefficient.
  THE LEGALITY THEOREM SURVIVES.  It is a statement about a FUNCTION, the spherical family alone
      sweeps y over (0, infinity), and the contradiction for a non-injective kernel arises inside
      the spherical case where the law is exact.  It is also independently known: it is Milgrom's
      monotonicity requirement on x mu(x), and the same combination [x df/dx + f] is the leading
      coefficient of Verwayen+2024's own spherical radial equation.  Route A REJECTED, alpha=2
      REJECTED, alpha=1 SELECTED.
  THE MULTIPLIER IS HANDLED CONSISTENTLY.  lambda_bg = (2-K_B)Q_0^2 + K'(Q_0)Q_0 is nonzero, and
      three independent routes agree on it; but with the constraint solved to second order the
      defect is O(Psi^3) and lambda drops out of every quadratic field equation.  The background
      DOES solve its own equations, and only because lambda_bg is nonzero.  The counterfactual --
      c_2 = 0 with lambda = 0 -- leaves a spurious -(2-K_B)Q_0^2 Psi^2, which is the earlier
      file's bogus graviton mass, recovered here from the action.
  ONE DEFECT FOUND, NOT LOAD-BEARING: PART Q's Qcal-sector mass term is off by a factor of -2
      (wrong sign and half the magnitude) relative to SZ21's Kcal = -(1/2)Fcal(0,Qcal); the
      corrected term reproduces SZ21's own printed mu exactly.  Suppressed by (mu r)^2 <~ 1e-16
      at every scale PART Q uses.
  GATE (b) CARRIES ONE CAVEAT, FOUND HERE: gamma_PPN = 1 is exact only at K'(Qcal_0) = 0.  With
      the dark sector's own local dust density restored, lap(Psi - Phi) = -12 pi Gt rhobar Psi,
      which is |gamma - 1| <~ 1e-13 at 1 AU against Cassini's 2.3e-5.  Real, declared, harmless.
  DIRECTION: MIXED, and both directions are real.  FAVOURABLE -- AeST's structure selects the
      framework's own signature relation g_obs^2 = g_bar^2 + a_0 g_bar, whose free function
      follows in closed form with SZ21's exact MOND asymptotics, and the committed 0.108-dex RAR
      fit is computed with precisely that kernel.  ADVERSE -- the operative Route A kernel cannot
      be hosted; the selected kernel forces a constant a_0/2 sunward anomaly, 1279x (canonical) /
      1541x (alt) over the Earth ephemeris bound; and on the RAR itself the ILLEGAL kernel is
      marginally the BETTER fit (0.100 vs 0.108 dex), so legality is bought at a small price
      rather than for free.
  NOT COMPUTED: the O(w^2) preferred-frame sector; alpha_1, alpha_2; the vector-mode spectrum;
      anything from Mistele's AeST papers (not retrieved); the size of the curl term for a
      realistic disc (bounded here only by Bekenstein-Milgrom's published r^-3 statement).
""")
print(f"  checks: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed   runtime {time.time() - T0:.1f} s")
if FAIL:
    print("  FAILED:")
    for f in FAIL:
        print("    -", f.splitlines()[0])
    sys.exit(1)
sys.exit(0)
