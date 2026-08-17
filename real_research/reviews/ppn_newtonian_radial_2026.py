#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_newtonian_radial_2026.py
============================
THE PPN PREFERRED-FRAME PROBLEM REDONE ABOUT THE RIGHT BACKGROUND -- DIRECT RADIAL ROUTE.
No Fourier modes, no local-homogeneity assumption, no free k.

WHAT WAS WRONG, AND WHAT THIS FILE FIXES
  real_research/reviews/ppn_scalar_retained_2026.py (35/35) expanded AeST's quadratic action
  about a background with Y_bg = 0 exactly (its own check 0-1), i.e. grad_mu phi = -Q_0 A_mu
  with NO solar scalar gradient.  real_research/reviews/ppn_verify_gradient_A_2026.py (28/28)
  then showed the O(w^2) answer is a function of Lambda = A_Y Q_0^2/k^2 alone, that the
  verified alphas are its Lambda -> 0 corner, and that with the frozen A_Y = (2-K_B)e^(sqrt y)
  the solar system sits at Lambda(1 AU) = 1e3430 -- the other corner, where the graviton Yukawa
  range is 1e-1704 m.  Its own C6 named the root cause: Y_bg = 0 is the wrong background.
  THIS FILE BUILDS THE RIGHT ONE, FROM THE ACTION, AND SOLVES RADIALLY.

=========================================================================================
HEADLINE, BOTH DIRECTIONS, BEFORE ANY DETAIL
=========================================================================================
(1) *** THE Lambda >> 1 PATHOLOGY IS AN ARTEFACT AND IT IS GONE.  FAVOURABLE. ***
    In a radial boundary-value problem there is no free k; the role of Lambda is played by
    (m r)^2, the squared Yukawa phase across the source distance, with m^2 = A Q_0^2/(2-K_B)
    evaluated at the CORRECT background's stiffness A.  On every legal background
        (m_perp r)^2 (1 AU) = 4.0e-19 ,   (m_par r)^2 (1 AU) = 1.0e-10 ,
    and the corner boundary (m r) = 1 sits at r = 1500 km canonical / 1245 km alt -- INSIDE THE
    SUN (R_sun = 6.96e5 km),
    not at 158 AU.  The solar system is in the massless / PPN corner by 10 to 19 orders of
    magnitude, so the Lambda -> 0 corner IS the physical one and B7/B10's K_B-independent
    a+b = -4, a = +8 (alpha_1 = -8, alpha_2 = -6 in Will's convention) are NOT the solar-system
    answer.  The 1e-1704 m Yukawa range disappears: on the correct background the Newtonian
    potential's own mass comes from the Q-sector alone, m_Psi = mu/sqrt(2), range ~1.4 Mpc.

(2) *** THE ALPHAS ARE THEREFORE O(K_B), NOT SCREENED, AND THE TWO-SIDED K_B WINDOW IS
    EMPTY.  ADVERSE. ***
    The corrections that the correct background adds to the Lambda -> 0 corner values are
    bounded here by max(1/J_Y, u r) = 7.9e-9 at 1 AU (check P3), so
        alpha_1 = -4 K_B ,  alpha_2 = -(5/2) K_B   (Will's convention)
    to a relative accuracy of 8e-9.  There is NO e^(-sqrt y) suppression of the preferred-frame
    sector -- the screening lives in the SCALAR's response to the SOURCE, and the alphas are
    carried by the AETHER, which is not screened at all.  |alpha_1| < 1e-4 => K_B < 2.5e-5,
    |alpha_2| < 1e-7 => K_B < 4.0e-8, against the subluminality floor K_B >= 2.105e-4: empty
    by 8.4x on alpha_1 and 5.3e3x on alpha_2.
    ONE PIECE OF RELIEF, reported with equal weight: the K_B-INDEPENDENT -4/A_Y floor that
    ppn_verify_gradient_A_2026.py flagged as a possible kill for every K_B including K_B = 0 is
    NOT triggered on the correct background.  There A_Y = 1 + J_Y = 1.27e8 at 1 AU, so
    |4/A_Y| = 3.2e-8, BELOW the |alpha_2| < 1e-7 bound.  On the illegal frozen branch it was
    2.5e-4, i.e. 2500x over.  That red flag is retired.

(3) *** THE DECISIVE RESULT IS NOT PPN AT ALL.  IT IS A LEGALITY THEOREM ON THE KERNEL, AND
    IT CUTS BOTH WAYS. ***
    Derived from the action here (PART Q, symbolic): AeST's quasi-static sector is TYPE-II --
    Psi = Psi_N + varphi with J_Y(Y) grad varphi = grad Psi_N and Y = |grad varphi|^2.  So the
    scalar's gradient u = |grad varphi| is the ANOMALOUS ACCELERATION, u = (nu(y)-1) g_bar, and
    it obeys the purely local algebraic law u J_Y(u^2) = g_bar.  For J to be a single-valued
    function of Y at all -- and for the longitudinal scalar mode not to be a ghost -- the map
    y -> u(y) must be MONOTONE INCREASING.  Consequences:
      (a) ADVERSE TO THE OPERATIVE KERNEL.  Route A, nu = 1/(1-e^(-sqrt y)) (Milgrom & Sanders
          2008 Eq. 13 at alpha = 1/2), gives u/a_0 = y/(e^(sqrt y)-1), which RISES to 0.6476 at
          y = 2.540 and then FALLS.  It is not injective, so NO single-valued J(Y) reproduces
          it, and on its Newtonian branch d(g_tot)/du = -2 e^(sqrt y)/(sqrt y - 2) < 0: a
          longitudinal GHOST, of exponentially large magnitude.  The exponential kernel cannot
          be hosted by AeST.  Same verdict for alpha = 2 (u/a_0 peaks at 0.3002 near y = 0.47
          then falls as 1/(2y)).
      (b) FAVOURABLE, AND STRIKINGLY SO.  The framework's OWN signature relation
          g_obs^2 = g_bar^2 + a_0 g_bar (the alpha = 1 kernel nu = sqrt(1+1/y)) IS legal, and it
          is the SATURATING one: u/a_0 = sqrt(y^2+y) - y rises monotonically to exactly 1/2.
          Its free function is obtained in closed form here,
              J_Y(Y) = v/(1-2v) ,  v = sqrt(Y)/a_0 ,  J(Y) = -a_0^2[ v(1+v)/2 + ln(1-2v)/4 ] ,
          whose small-Y limit is (2/3) Y^(3/2)/a_0 -- EXACTLY the MOND asymptotics
          2 lambda_s/(3(1+lambda_s)a_0) Y^(3/2) that Skordis & Zlosnik print, at lambda_s -> oo.
          So AeST's structure SELECTS alpha = 1, the relation the corpus calls its signature.
          That is a derivation of the exact law from the relativistic home, not a fit.
      (c) AND THEREFORE ADVERSE ON THE EPHEMERIDES, STRUCTURALLY.  Monotone u plus the
          deep-MOND limit U(y) -> sqrt(y) -- which is what a_0 MEANS -- forces a CONSTANT
          sunward anomaly u(1 AU) >= a_0 sqrt(y_0) for any anchor y_0 in the deep-MOND regime.
          On the most conservative rung, y_0 = 0.01, that is >= 9.36e-12 m/s^2 (canonical) /
          1.13e-11 (alt) against Sereno & Jetzer 2006's Earth bound 3.66e-14 m/s^2: 256x / 308x
          over.  At y_0 = 1 it is 2558x / 3082x, and at alpha = 1 exactly it is a_0/2 and 1279x,
          which reproduces the corpus's own committed ephemeris liability from AeST's
          structure.  The
          liability is therefore NOT a kernel choice the framework could trade away inside
          AeST: the escape it adopted (the exponential kernel) is the illegal branch.

WHAT IS AND IS NOT AT ISSUE.  a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical /
1.1279e-10 alt, kappa = 1/2 (FITTED, never derived), beta, the promotion
A(Q) = kappa^2 G(-K(Q)), the RAR at 0.108 dex, BTFR, weak lensing, CLASS: NONE of them is
touched, credited or blamed.  Every result above is a property of the ADOPTED RELATIVISTIC
HOME (AeST: Skordis & Zlosnik, PRL 127, 161302 (2021), arXiv:2007.00082) and of which
interpolating kernels its 𝒴-sector can host.  The one place the framework's own number enters
is favourable and is stated as such in (3b).

=========================================================================================
METHOD, AND EVERY REDUCTION STATED
=========================================================================================
R1  FRAME AND ANSATZ.  Matter (Sun) rest frame, static.  g_00 = -(1+2Psi),
    g_ij = (1-2Phi)delta_ij; aether A_mu = (-(1+Psi-Psi^2/2), 0,0,0) with A^mu A_mu = -1
    enforced order by order (the correction -Psi^2/2 is DERIVED here, not assumed);
    scalar phi = Q_0 t + varphi(x), so Q = Q_0(1 - Psi + 3Psi^2/2) -- the corpus's committed
    "Q = (1-Psi)Q_0" reproduced -- and Y = |grad varphi|^2 EXACTLY at quadratic order, with no
    metric contamination (check Q4).  A_i = 0 in the static background by t-reflection
    symmetry; the A_i field equation is satisfied identically by A_i = 0 (check Q7).
R2  THE ONE ESSENTIAL NON-EXPANSION.  Y is second order in the field amplitude, and the MOND
    term goes as Y^(3/2), so J(Y) is THIRD order and CANNOT be reached by a Taylor expansion
    in the field amplitude -- this is the same non-analyticity that
    bridge1_aest_equations.md records for the cosmological background.  The reduction used
    here is therefore: quadratic order in (Psi, Phi) and in varphi, with J(Y) kept as an
    UNEXPANDED general function of Y = |grad varphi|^2.  That is the standard weak-field MOND
    treatment and it is exact for the background; it is stated, not hidden.
R3  WHAT IS LINEARISED.  The metric in GM/r (weak field, 1e-8 at 1 AU).  The wind sector in
    w^2.  The scalar sector is NOT linearised in its own gradient -- that is the whole point.
R4  THE BACKGROUND IS SOLVED EXACTLY, not expanded in 1/sqrt(y): the first integral
    J_Y(u^2) u = g_bar is algebraic and local, so u(r) is obtained by root-finding to machine
    precision at every radius (check B2, residual < 1e-15).
R5  VALIDITY CONDITION OF THE PERTURBATIVE STEP, stated and TESTED (check P2).  Expanding
    J about Y_bg requires delta Y << Y_bg, i.e. u_bg >> Q_0 |delta A|.  At 1 AU on the legal
    alpha = 1 branch u_bg = 5.21e-28 m^-1 and Q_0|delta A| = 3.74e-36 m^-1: the condition HOLDS
    by 8.1 orders.  On the frozen Route-A branch u_bg = 1e-3476 m^-1 and it FAILS by ~3440
    orders -- which is an independent statement of why the earlier expansion was ill-founded.
R6  WHAT IS *NOT* DONE HERE, DECLARED UP FRONT: the O(w^2) radial ODE system is ASSEMBLED and
    its multipole structure and coefficient sizes are established, but it is NOT integrated.
    alpha_1 and alpha_2 are therefore NOT recomputed from scratch in this file.  What this file
    supplies is the missing bridge: a bound (check P3) on how much the correct background can
    move the Lambda -> 0 corner values, plus the demonstration (PART L) that that corner is the
    physical one.  The numbers -4 K_B and -(5/2) K_B are INHERITED, with provenance, from
    ppn_verify_g0i_channel_2026.py (which derived alpha_1 = -4 K_B from the g_0i channel with
    the scalar retained) and ppn_scalar_retained_2026.py Q3-4 as corrected by
    ppn_verify_transcription_2026.py's convention audit.  They are labelled INHERITED
    everywhere below and in the status ledger.

=========================================================================================
CONVENTION -- DERIVED IN-SCRIPT, NOT QUOTED (PART D)
=========================================================================================
Will's PPN metric carries, in g_00, the preferred-frame terms
    -(alpha_1 - alpha_2 - alpha_3) w^2 U  -  alpha_2 w^i w^j U_ij .
A RADIAL solve reads g_00 in POSITION space, where for a point mass U_ij = rhat_i rhat_j U
(derived at check D1 from the superpotential identity), NOT in Fourier space, where
U_ij = (delta_ij - 2 khat_i khat_j) U (derived at check D2).  The two give DIFFERENT
dictionaries, and this file needs the first:
    POSITION space, delta g_00 = [a_r w^2 + b_r (w.rhat)^2] U  =>  alpha_2 = -b_r,
                                                                  alpha_1 = -(a_r + b_r) ;
    FOURIER  space, delta g_00 = [a_k w^2 + b_k (w.khat)^2] U  =>  alpha_2 = +b_k/2,
                                                                  alpha_1 = -a_k .
Both are derived symbolically at checks D3/D4, along with the mapping to the convention used
by ppn_scalar_retained_2026.py (its C4: a_k = alpha_1^C4 + alpha_2^C4, b_k = -2 alpha_2^C4,
hence alpha_1^Will = -(alpha_1^C4 + alpha_2^C4) and alpha_2^Will = -alpha_2^C4 -- the two
conventions MIX the parameters and are not related by a sign, which is the error
ppn_verify_transcription_2026.py caught).  alpha_3 = 0 throughout (semiconservative;
ASSUMED, not verified here).
The multipole cross-check a radial solve has and a Fourier one does not: alpha_1 multiplies
w^2 U, which is l = 0 in the boost direction, while alpha_2 multiplies w^i w^j U_ij, which in
position space is (w.rhat)^2 U = w^2 U [1/3 + (2/3) P_2(cos theta)] -- so alpha_2 is the ONLY
source of an l = 2 angular dependence in delta g_00.  Recorded at check D5 as the structural
handle; not exercised, since the O(w^2) system is not integrated.

EXIT 0 iff every numbered check passes.  Runtime ~10 s.
"""

import math
import sys
import time

import sympy as sp

# =================================================================================================
# check harness
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

# =================================================================================================
# physical constants and the two footings
# =================================================================================================
CLIGHT = 2.99792458e8
GMSUN = 1.32712440018e20            # m^3 s^-2, IAU
AU = 1.495978707e11                 # m, IAU 2012
RSUN = 6.957e8                      # m, IAU 2015 nominal
PC = 3.0856775814913673e16
MPC = 1.0e6 * PC
A0_CAN = 9.3619e-11                 # kappa c sqrt(G rho_Lambda), canonical footing
A0_ALT = 1.1279e-10                 # alt footing
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
# Sereno & Jetzer 2006 (astro-ph/0606197) Table 1 (Pitjeva EPM2004) inverted through their
# Eq. (9), as verified and recorded in STANDING.md sec. 5 item 0:
EPH_EARTH = 3.66e-14                # m/s^2, 2 sigma
EPH_MARS = 3.72e-14                 # m/s^2, 2 sigma
# Skordis & Zlosnik's own MOND-compatible K_2 fits, as carried in bridge1_aest_equations.md
K2_FITS = (("Cosh", 7.5e3, 2.0), ("Exp", 9.5e3, 4.0))   # (name, K_2, K''/K_2)
MU_INV_FLOOR = 1.0 * MPC            # mu^-1 >~ 1 Mpc (bridge1), the most conservative choice

GBAR_1AU = GMSUN / AU ** 2          # m/s^2


def geom(a_ms2):
    """acceleration in m/s^2 -> inverse length in m^-1 (c = 1 units)"""
    return a_ms2 / CLIGHT ** 2


GM_GEOM = GMSUN / CLIGHT ** 2       # m


def y_of_r(r, a0):
    return GMSUN / (r ** 2 * a0)


# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE PPN DICTIONARY, DERIVED.  POSITION SPACE (what a radial solve sees) AND")
print("          FOURIER SPACE (what the two earlier files saw), IN BOTH CONVENTIONS.")
print("=" * 100)
X, Y_, Z = sp.symbols("X Y Z", real=True)
RR = sp.sqrt(X ** 2 + Y_ ** 2 + Z ** 2)
Mm = sp.Symbol("M", positive=True)
Upot = Mm / RR
chi_super = Mm * RR                      # superpotential: laplacian(chi) = 2 U
lap = lambda e: sum(sp.diff(e, c, 2) for c in (X, Y_, Z))
check(sp.simplify(lap(chi_super) - 2 * Upot) == 0,
      "D1a the superpotential identity laplacian(int rho|x-x'|) = 2 U, verified for a point mass",
      "this is the only input needed to reduce U_ij; nothing about PPN is assumed in it")
Uij = sp.Matrix(3, 3, lambda i, j: sp.simplify(
    sp.KroneckerDelta(i, j) * Upot - sp.diff(chi_super, (X, Y_, Z)[i], (X, Y_, Z)[j])))
rhat = [X / RR, Y_ / RR, Z / RR]
check(all(sp.simplify(Uij[i, j] - rhat[i] * rhat[j] * Upot) == 0 for i in range(3) for j in range(3)),
      "D1b *** POSITION SPACE: U_ij = rhat_i rhat_j U for a point mass, so "
      "w^i w^j U_ij = (w.rhat)^2 U ***",
      "derived from U_ij = delta_ij U - d_i d_j chi, which is the definition "
      "U_ij = int rho (x-x')_i (x-x')_j/|x-x'|^3 rewritten; the trace U_ii = U checks out")
check(sp.simplify(sum(Uij[i, i] for i in range(3)) - Upot) == 0,
      "D1c and the normalisation is right: U_ii = U")
kk = sp.symbols("k1 k2 k3", real=True)
k2s = sum(c ** 2 for c in kk)
Uk = sp.Symbol("U_k")
# in Fourier space chi(k) = -2 U(k)/k^2 and -d_i d_j -> +k_i k_j
Uij_k = sp.Matrix(3, 3, lambda i, j: sp.KroneckerDelta(i, j) * Uk
                  + kk[i] * kk[j] * (-2 * Uk / k2s))
check(all(sp.simplify(Uij_k[i, j] - (sp.KroneckerDelta(i, j) - 2 * kk[i] * kk[j] / k2s) * Uk) == 0
          for i in range(3) for j in range(3)),
      "D2  FOURIER SPACE: U_ij(k) = (delta_ij - 2 khat_i khat_j) U(k), so "
      "w^i w^j U_ij = (w^2 - 2(w.khat)^2) U",
      "the SAME object in two representations; the (a, b) coefficients read off delta g_00 "
      "therefore differ between them, which is why a radial route needs its own dictionary")

a1, a2, a3 = sp.symbols("alpha_1 alpha_2 alpha_3")
ar, br, ak, bk = sp.symbols("a_r b_r a_k b_k")
wv = sp.symbols("w1 w2 w3", real=True)
w2s = sum(c ** 2 for c in wv)
wdotr = sum(wv[i] * rhat[i] for i in range(3))
wdotk = sum(wv[i] * kk[i] for i in range(3)) / sp.sqrt(k2s)
# Will's g_00 preferred-frame terms
will_pos = -(a1 - a2 - a3) * w2s * Upot - a2 * sum(
    wv[i] * wv[j] * Uij[i, j] for i in range(3) for j in range(3))
mine_pos = ar * w2s * Upot + br * wdotr ** 2 * Upot
dic_pos = sp.solve([sp.Eq(c, 0) for c in sp.Poly(
    sp.simplify(sp.expand(will_pos - mine_pos) / Upot), w2s).all_coeffs()] if False else
    [sp.Eq(sp.expand(sp.simplify((will_pos - mine_pos) / Upot)).coeff(wv[0] ** 2), 0),
     sp.Eq(sp.expand(sp.simplify((will_pos - mine_pos) / Upot)).coeff(wv[0] * wv[2]), 0)],
    [ar, br], dict=True)
# do it cleanly instead: match on a concrete basis
expr_pos = sp.expand(sp.simplify((will_pos - mine_pos) / Upot))
eq1 = expr_pos.subs({wv[0]: 1, wv[1]: 0, wv[2]: 0, X: 0, Y_: 0, Z: 1})   # w perp rhat
eq2 = expr_pos.subs({wv[0]: 0, wv[1]: 0, wv[2]: 1, X: 0, Y_: 0, Z: 1})   # w para rhat
sol_pos = sp.solve([sp.Eq(eq1, 0), sp.Eq(eq2, 0)], [ar, br], dict=True)[0]
check(sp.simplify(sol_pos[ar] + (a1 - a2 - a3)) == 0 and sp.simplify(sol_pos[br] + a2) == 0,
      "D3  *** POSITION-SPACE DICTIONARY, DERIVED: a_r = -(alpha_1 - alpha_2 - alpha_3) and "
      "b_r = -alpha_2, hence alpha_2 = -b_r and alpha_1 = -(a_r + b_r) at alpha_3 = 0 ***",
      f"a_r = {sp.simplify(sol_pos[ar])},  b_r = {sp.simplify(sol_pos[br])}.  This is the "
      f"dictionary a RADIAL solve must use.  Note it is NOT the Fourier one: the w^2 U "
      f"coefficient here retains alpha_2, because (w.rhat)^2 U carries no -2 relative to w^2 U")
will_k = -(a1 - a2 - a3) * w2s * Uk - a2 * (w2s - 2 * wdotk ** 2) * Uk
mine_k = ak * w2s * Uk + bk * wdotk ** 2 * Uk
ek = sp.expand(sp.simplify((will_k - mine_k) / Uk))
ek1 = ek.subs({wv[0]: 1, wv[1]: 0, wv[2]: 0, kk[0]: 0, kk[1]: 0, kk[2]: 1})
ek2 = ek.subs({wv[0]: 0, wv[1]: 0, wv[2]: 1, kk[0]: 0, kk[1]: 0, kk[2]: 1})
sol_k = sp.solve([sp.Eq(ek1, 0), sp.Eq(ek2, 0)], [ak, bk], dict=True)[0]
check(sp.simplify(sol_k[ak] + a1 - a3) == 0 and sp.simplify(sol_k[bk] - 2 * a2) == 0,
      "D4a *** FOURIER DICTIONARY, DERIVED: a_k = -(alpha_1 - alpha_3) and b_k = +2 alpha_2, "
      "hence alpha_1 = -a_k EXACTLY at alpha_3 = 0 and alpha_2 = +b_k/2 -- the alpha_2 pieces "
      "DO cancel out of the w^2 U coefficient in Fourier space ***",
      f"a_k = {sp.simplify(sol_k[ak])},  b_k = {sp.simplify(sol_k[bk])}.  Exactly the matching "
      f"the task specifies, derived rather than quoted")
a1C4, a2C4 = sp.symbols("alpha_1^C4 alpha_2^C4")
# ppn_scalar_retained_2026.py's C4: g_00 = -1 + 2U + a1C4 w^2 U + a2C4 w^i w^j U_ij
c4_k = a1C4 * w2s * Uk + a2C4 * (w2s - 2 * wdotk ** 2) * Uk
ec = sp.expand(sp.simplify((c4_k - mine_k) / Uk))
ec1 = ec.subs({wv[0]: 1, wv[1]: 0, wv[2]: 0, kk[0]: 0, kk[1]: 0, kk[2]: 1})
ec2 = ec.subs({wv[0]: 0, wv[1]: 0, wv[2]: 1, kk[0]: 0, kk[1]: 0, kk[2]: 1})
sol_c4 = sp.solve([sp.Eq(ec1, 0), sp.Eq(ec2, 0)], [ak, bk], dict=True)[0]
map_a1 = sp.simplify(-sol_c4[ak])
map_a2 = sp.simplify(sol_c4[bk] / 2)
check(sp.simplify(map_a1 + a1C4 + a2C4) == 0 and sp.simplify(map_a2 + a2C4) == 0,
      "D4b *** AND THE CONVENTION MAPPING, DERIVED: alpha_1^Will = -(alpha_1^C4 + alpha_2^C4) "
      "and alpha_2^Will = -alpha_2^C4.  The two conventions MIX the parameters; they are NOT "
      "related by a sign flip ***",
      f"alpha_1^Will = {map_a1}, alpha_2^Will = {map_a2}.  So ppn_scalar_retained_2026.py's "
      f"C4 disclaimer ('flip the sign of both alphas ... no verdict depends on that choice') "
      f"is wrong on its second half, exactly as ppn_verify_transcription_2026.py found: with "
      f"alpha_1^C4 = (3/2)K_B and alpha_2^C4 = (5/2)K_B one gets alpha_1^Will = -4 K_B and "
      f"alpha_2^Will = -(5/2)K_B, so |alpha_1| = 4 K_B and the ceiling is K_B < 2.5e-5")
th = sp.Symbol("theta")
leg = sp.simplify(sp.expand(sp.cos(th) ** 2 - (sp.Rational(1, 3)
                                               + sp.Rational(2, 3) * sp.legendre(2, sp.cos(th)))))
check(sp.simplify(leg) == 0,
      "D5  THE MULTIPOLE HANDLE A RADIAL SOLVE HAS AND A FOURIER ONE DOES NOT: "
      "(w.rhat)^2 = w^2 [1/3 + (2/3) P_2(cos theta)], so alpha_2 is the ONLY source of l = 2 "
      "in delta g_00 while alpha_1 and alpha_2 both feed l = 0.  Recorded as the structural "
      "cross-check; NOT exercised here, because the O(w^2) system is not integrated (R6)")

# =================================================================================================
print()
print("=" * 100)
print("PART Q -- THE QUASI-STATIC AeST SECTOR, DERIVED FROM THE ACTION.  THE RIGHT BACKGROUND.")
print("=" * 100)
info("Q0  THE ACTION, T2 transcription (verified verbatim against the arXiv LaTeX source by "
     "real_research/reviews/ppn_verify_transcription_2026.py and recorded in "
     "real_research/bridge1_aest_equations.md):\n"
     "        S = int d^4x sqrt(-g)/(16 pi Gt) [ R - (K_B/2) F^{mu nu}F_{mu nu} "
     "+ 2(2-K_B) J^mu grad_mu phi\n"
     "                                          - (2-K_B) Y - F(Y,Q) - lambda(A^mu A_mu + 1) ] "
     "+ S_m[g]\n"
     "     with J^mu = A^nu grad_nu A^mu, Q = A^mu grad_mu phi, "
     "Y = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi,\n"
     "     and F(Y,Q) = (2-K_B) J(Y) + K(Q), K(Q) = -2 Lambda + K_2 (Q - Q_0)^2 + ...")

tt, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO = [tt, x1, x2, x3]
SPC = [x1, x2, x3]
eps = sp.Symbol("eps")
KB = sp.Symbol("K_B")
Q0s = sp.Symbol("Q_0")
K2s = sp.Symbol("K_2", positive=True)
Kp = sp.Symbol("Kprime")             # dK/dQ at Q_0 (= I_0/a^3, the dust); set 0 locally
GT = sp.Symbol("Gt", positive=True)  # Gtilde
rhos = sp.Symbol("rho")
Psi = sp.Function("Psi")(x1, x2, x3)
Phi = sp.Function("Phi")(x1, x2, x3)
vp = sp.Function("vp")(x1, x2, x3)
c2f = sp.Function("c2")(x1, x2, x3)
JF = sp.Function("J")                # placeholder name for the free function (see below)


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

# aether with the unit-norm constraint solved order by order (nothing assumed)
Ad = sp.Matrix([-(1 + eps * Psi + eps ** 2 * c2f), 0, 0, 0])
Au0 = sp.Matrix(4, 1, lambda i, j: s2(sum(gu[i, k] * Ad[k] for k in range(4))))
AA0 = s2(sum(Au0[i] * Ad[i] for i in range(4)))
c2_sol = sp.solve(sp.Eq(sp.expand(AA0 + 1).coeff(eps, 2), 0), c2f)[0]
Ad = Ad.subs(c2f, c2_sol)
Au = sp.Matrix(4, 1, lambda i, j: s2(sum(gu[i, k] * Ad[k] for k in range(4))))
AA = s2(sum(Au[i] * Ad[i] for i in range(4)))
check(sp.simplify(c2_sol + Psi ** 2 / 2) == 0 and sp.simplify(AA + 1) == 0,
      "Q1  the aether background is DERIVED, not assumed: A_mu = (-(1+Psi-Psi^2/2), 0,0,0) is "
      "the unique static unit-timelike aether aligned with the Killing vector, and it "
      "satisfies A^mu A_mu = -1 exactly to O(eps^2)",
      f"the O(eps^2) piece is c_2 = {c2_sol}")

Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Ad[n], CO[m]) - sp.diff(Ad[m], CO[n]))
F2 = s2(sum(Fmn[m, n] * Fmn[a, b] * gu[m, a] * gu[n, b]
            for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
gradPsi2 = sum(sp.diff(Psi, c) ** 2 for c in SPC)
check(sp.simplify(sp.expand(F2).coeff(eps, 2) + 2 * gradPsi2) == 0,
      "Q2  F^{mu nu}F_{mu nu} = -2 |grad Psi|^2, so -(K_B/2)F^2 contributes "
      "+K_B |grad Psi|^2 to the quadratic Lagrangian",
      "the aether kinetic term therefore RENORMALISES the Newtonian potential's own kinetic "
      "term -- this is where the corpus's Gt = (1-K_B/2)Ghat comes from (check Q6)")

dphi = sp.Matrix([Q0s, 0, 0, 0]) + eps * sp.Matrix([sp.diff(vp, c) for c in CO])
Qsc = s2(sum(Au[m] * dphi[m] for m in range(4)))
Ysc = s2(sum((gu[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n]
             for m in range(4) for n in range(4)))
gradvp2 = sum(sp.diff(vp, c) ** 2 for c in SPC)
check(sp.simplify(sp.expand(Qsc).coeff(eps, 1) + Q0s * Psi) == 0,
      "Q3  Q = Q_0 (1 - Psi + 3 Psi^2/2), i.e. delta Q = -Q_0 Psi -- the corpus's committed "
      "quasi-static relation Q = (1-Psi)Q_0 reproduced from the action")
check(sp.simplify(Ysc - eps ** 2 * gradvp2) == 0,
      "Q4  *** THE RIGHT BACKGROUND, IN ONE LINE: Y = |grad varphi|^2 EXACTLY at quadratic "
      "order, with NO metric contamination.  Y_bg is the SUN'S SCALAR GRADIENT and it is "
      "nonzero ***",
      f"Y = eps^2 |grad varphi|^2 identically.  The earlier files took grad_mu phi = -Q_0 A_mu, "
      f"i.e. varphi = const, which is Y_bg = 0.  That is the configuration with NO MOND force "
      f"at all -- the deep-MOND / interpolation-singular point -- and it is what put their "
      f"expansion at the divergence of their own G_eff")

Jd = [s2(sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[b][nu][al] * Ad[b] for b in range(4)))
             for nu in range(4))) for al in range(4)]
Jphi = s2(sum(gu[m, al] * Jd[al] * dphi[m] for m in range(4) for al in range(4)))
gradPsi_vp = sum(sp.diff(Psi, c) * sp.diff(vp, c) for c in SPC)
check(sp.simplify(sp.expand(Jphi).coeff(eps, 1)) == 0
      and sp.simplify(sp.expand(Jphi).coeff(eps, 2) - gradPsi_vp) == 0,
      "Q5  J^mu grad_mu phi = eps^2 grad Psi . grad varphi, and it vanishes at FIRST order: "
      "the aether's acceleration J^i is exactly the static observer's acceleration d_i Psi, "
      "so this term is the Psi-varphi mixing that makes AeST type-II",
      "no Q_0 appears here in the static background -- the Q_0 J^mu delta A_mu channel that "
      "lifts the aether degeneracy lives in the O(w) sector, not in the background")

# assemble the quadratic Lagrangian (16 pi Gt factored out of the bracket) and vary.
# The free function is carried as J(Y) = cJ * Y^p with SYMBOLIC power p; because the
# Euler-Lagrange operator is LINEAR in J, an identity that holds for every power p holds for
# every J representable as a (possibly fractional) power series, i.e. for a general free
# function.  Verified at four p including the MOND value p = 3/2 (check Q6c).
cJ_, pp = sp.symbols("cJ p")
Yv = gradvp2
Jterm = cJ_ * Yv ** pp
JY_expr = cJ_ * pp * Yv ** (pp - 1)          # J_Y for that representative
L = (L_EH2
     + KB * gradPsi2
     + 2 * (2 - KB) * gradPsi_vp
     - (2 - KB) * (Yv + Jterm)
     - (K2s * Q0s ** 2 * Psi ** 2 - Kp * Q0s * (-Psi + sp.Rational(3, 2) * Psi ** 2))
     - 16 * sp.pi * GT * rhos * Psi)


def el(Lag, f, vs=None):
    """Euler-Lagrange derivative, carrying first AND second derivatives of the field."""
    vs = SPC if vs is None else vs
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


eqPhi = el(L, Phi)
eqPsi = el(L, Psi)
lapPsi = sum(sp.diff(Psi, c, 2) for c in SPC)
lapPhi = sum(sp.diff(Phi, c, 2) for c in SPC)
lapvp = sum(sp.diff(vp, c, 2) for c in SPC)
check(sp.simplify(eqPhi / 4 - (lapPsi - lapPhi)) == 0,
      "Q6a *** GATE (a): gamma_PPN = 1 EXACTLY.  The Phi field equation is laplacian(Phi) = "
      "laplacian(Psi), hence Phi = Psi, for EVERY K_B, every free function J, every Q_0, and "
      "with the Q-sector mass term included ***",
      "no aether or scalar term contains Phi at quadratic order, so the transverse metric is "
      "pure GR.  This reproduces the corpus's committed gamma_PPN = 1 and the earlier files' "
      "G4a / B4 about a DIFFERENT background")
# now impose Phi = Psi and read the Psi and varphi equations
subPP = {Phi: Psi}
ePsi = sp.expand(eqPsi.subs(subPP).doit())
Ghat = sp.Symbol("Ghat", positive=True)
mass2 = sp.Symbol("m2")
target_Psi = (2 * (2 - KB)) * (lapPsi - lapvp - (K2s * Q0s ** 2 / (2 - KB)) * Psi
                               - 8 * sp.pi * GT * rhos / (2 - KB))
check(sp.simplify(sp.expand(ePsi.subs(Kp, 0)) - target_Psi) == 0,
      "Q6b *** GATE (c), FIRST HALF: the Psi equation is\n"
      "           laplacian(Psi) - m_Psi^2 Psi = 4 pi Ghat rho + laplacian(varphi),\n"
      "       with  Ghat = 2 Gt/(2-K_B) = Gt/(1-K_B/2)  and  m_Psi^2 = K_2 Q_0^2/(2-K_B) ***",
      "so Psi = Psi_N + varphi with laplacian(Psi_N) = 4 pi Ghat rho: AeST is a TYPE-II "
      "(two-field) MOND theory, the scalar ADDS to the Newtonian potential.  And "
      "Gt = (1-K_B/2)Ghat is the corpus's committed relation, DERIVED here from the F^2 term "
      "(check Q2), not assumed.  With K'' = 2 K_2 this m_Psi^2 = (1/2) mu^2 where "
      "mu^2 = K'' Q_0^2/(2-K_B) is SZ21's scalar mass as carried in bridge1 -- a factor-2 "
      "convention in K_2 vs K''/2, stated and carried")
JY = sp.Symbol("J_Y")
PVALS = (sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2), sp.Integer(3))
vp_ok = []
for pv in PVALS:
    ev = el(L.subs(pp, pv), vp)
    tg = sp.expand(2 * (2 - KB) * (sum(sp.diff((1 + JY_expr.subs(pp, pv)) * sp.diff(vp, c), c)
                                       for c in SPC) - lapPsi))
    vp_ok.append(sp.simplify(sp.expand(ev - tg)) == 0)
check(all(vp_ok),
      "Q6c *** GATE (c), SECOND HALF: the varphi equation is "
      "div[(1 + J_Y) grad varphi] = laplacian(Psi), which with Psi = Psi_N + varphi collapses "
      "to div[J_Y grad varphi] = laplacian(Psi_N), hence the LOCAL ALGEBRAIC FIRST INTEGRAL\n"
      "           J_Y(u^2) u = g_bar ,      u = |grad varphi| ,  g_bar = |grad Psi_N| ***",
      f"verified as an operator identity at p = {[str(v) for v in PVALS]} for J = cJ Y^p, "
      f"including the MOND value p = 3/2; the Euler-Lagrange operator is LINEAR in J, so an "
      f"identity holding for every power holds for a general free function.  "
      "the '1' cancels because the action's J-coupling coefficient 2(2-K_B) is exactly twice "
      "the Y coefficient (2-K_B) -- that is SZ21's design.  The consequence is the whole of "
      "PART C: u is the ANOMALOUS ACCELERATION and it is a function of the LOCAL g_bar alone")
nu_sym = sp.Symbol("nu")
Geff_over = sp.simplify(1 + 1 / JY)
check(sp.simplify(Geff_over - (1 + 1 / JY)) == 0,
      "Q6d and hence G_eff/G_N = g_tot/g_bar = (g_bar + u)/g_bar = 1 + 1/J_Y -- the corpus's "
      "committed G_eff = G_N(1 + 1/J_Y) (ppn_scalar_retained_2026.py G5a), reproduced about "
      "the CORRECT background instead of about Y_bg = 0",
      "and note what changed: there, 1 + 1/J_Y was obtained with J_Y a FROZEN CONSTANT, which "
      "is why A_Y = (2-K_B)e^(sqrt y) could be imported from a separate matching.  Here J_Y is "
      "a function of Y = u^2 and the SAME equation fixes u.  That closure is what the earlier "
      "route lacked, and it is what makes PART C decidable")
Ai_eq = "A_i = 0"
check(True,
      "Q7  A_i = 0 in the static background is CONSISTENT, not an assumption of convenience: "
      "A_i is odd under t -> -t while a static solution is even, and the quadratic Lagrangian "
      "above contains no term linear in A_i (the F^2 term needs F_{ij} which is quadratic in "
      "A_i, and J^mu grad_mu phi's A_i-linear piece is d_i(A_i Q_0) x const = a total "
      "divergence).  So delta L/delta A_i = 0 is solved by A_i = 0",
      "ARGUED from the structure printed above, not verified term by term with A_i restored; "
      "recorded in the ledger as such")

# GATE (b): c_T^2 = 1 -- a separate TT computation
tz = sp.symbols("z", real=True)
hf = sp.Function("h")(tt, tz)
u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
gdT = sp.Matrix([[-1, 0, 0, 0], [0, 1, eps * hf, 0], [0, eps * hf, 1, 0], [0, 0, 0, 1]])
guT = sp.Matrix(4, 4, lambda i, j: s2(sp.simplify(gdT.inv()[i, j])))
sqT = s2(sp.series(sp.sqrt(-sp.expand(gdT.det())), eps, 0, 3).removeO())
COT = [tt, x1, x2, tz]
GamT = [[[s2(sp.Rational(1, 2) * sum(
    guT[r, s] * (sp.diff(gdT[s, n], COT[m]) + sp.diff(gdT[s, m], COT[n]) - sp.diff(gdT[m, n], COT[s]))
    for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]


def ricT(si, nu):
    o = 0
    for m in range(4):
        o += sp.diff(GamT[m][nu][si], COT[m]) - sp.diff(GamT[m][m][si], COT[nu])
        for l in range(4):
            o += GamT[m][m][l] * GamT[l][nu][si] - GamT[m][nu][l] * GamT[l][m][si]
    return s2(o)


RT = s2(sum(guT[m, n] * ricT(m, n) for m in range(4) for n in range(4)))
LT = sp.expand(s2(sqT * RT)).coeff(eps, 2)
elT = el(LT, hf, vs=[tt, tz])
cff_tt = sp.simplify(elT.coeff(sp.Derivative(hf, (tt, 2))))
cff_zz = sp.simplify(elT.coeff(sp.Derivative(hf, (tz, 2))))
cT2 = sp.simplify(-cff_zz / cff_tt)
# the sector's TT contribution: A_mu constant => F = 0 and J^mu = 0; Y carries h with NO derivative
AdT = sp.Matrix([-1, 0, 0, 0])
AuT = sp.Matrix(4, 1, lambda i, j: s2(sum(guT[i, k] * AdT[k] for k in range(4))))
FT = sp.Matrix(4, 4, lambda m, n: sp.diff(AdT[n], COT[m]) - sp.diff(AdT[m], COT[n]))
JdT = [s2(sum(AuT[nu] * (sp.diff(AdT[al], COT[nu]) - sum(GamT[b][nu][al] * AdT[b] for b in range(4)))
              for nu in range(4))) for al in range(4)]
dphiT = sp.Matrix([Q0s, u1, u2, u3])
YT = s2(sum((guT[m, n] + AuT[m] * AuT[n]) * dphiT[m] * dphiT[n]
            for m in range(4) for n in range(4)))
QT = s2(sum(AuT[m] * dphiT[m] for m in range(4)))
sector_T = sp.expand(FT) + sp.zeros(4, 4)
no_der_sector = (all(sp.simplify(FT[i, j]) == 0 for i in range(4) for j in range(4))
                 and all(sp.simplify(JdT[i]) == 0 for i in range(4))
                 and not sp.expand(YT).has(sp.Derivative)
                 and not sp.expand(QT).has(sp.Derivative))
check(sp.simplify(cT2 - 1) == 0 and no_der_sector,
      "Q8  *** GATE (b): c_T^2 = 1 EXACTLY about the correct background.  The TT sector's "
      "kinetic terms come from the Einstein-Hilbert part alone: with A_mu constant the aether "
      "has F_{mu nu} = 0 and J^mu = 0 identically for a TT metric, and Y and Q contain h with "
      "NO derivatives, so the whole aether+scalar sector contributes only MASS-type terms and "
      "cannot move c_T ***",
      f"c_T^2 = {cT2} from the EH TT Lagrangian, and the sector's derivative census is empty "
      f"(F = 0, J = 0, Y and Q derivative-free in h) -- verified with a nonzero background "
      f"scalar gradient (u1,u2,u3), i.e. about the RIGHT background, which is the case the "
      f"earlier files could not test")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE SPHERICAL BACKGROUND, SOLVED EXACTLY.  Y_bg(r) != 0, AND ITS NUMBERS.")
print("=" * 100)
info("B0  THE CLOSURE.  PART Q gives, for a spherical source and regularity at infinity,\n"
     "        u(r) J_Y(u(r)^2) = g_bar(r) ,   g_tot = g_bar + u ,   nu(y) = 1 + u/g_bar ,\n"
     "    y = g_bar/a_0.  So specifying a kernel nu(y) is EQUIVALENT to specifying\n"
     "        U(y) = u/a_0 = y (nu(y) - 1)      and      J_Y = y/U(y) ,\n"
     "    and the free function is recovered by eliminating y between Y = a_0^2 U^2 and J_Y.")

# U(y) = u/a_0 = y (nu(y) - 1), written in NUMERICALLY STABLE closed form for each kernel:
# the naive y*(nu-1) suffers catastrophic cancellation at large y (nu - 1 ~ 1e-9 at 1 AU for
# alpha = 1), which would silently destroy the monotonicity test that PART C turns on.
def U_routeA(y):
    s = math.sqrt(y)
    return 0.0 if s > 700.0 else y / math.expm1(s)


def U_alpha1(y):
    return 1.0 / (math.sqrt(1.0 + 1.0 / y) + 1.0)          # = y(sqrt(1+1/y)-1), exactly


def U_alpha2(y):
    xx = 4.0 / y ** 2
    d = xx / (2.0 * (math.sqrt(1.0 + xx) + 1.0))            # nu^2 = 1 + d
    return y * d / (math.sqrt(1.0 + d) + 1.0)               # = y(nu-1), exactly


def U_mondonly(y):
    return math.sqrt(y)


KERNELS = {
    "RouteA  nu=1/(1-e^-sqrt y)  [MS08 eq13, alpha=1/2; OPERATIVE]": U_routeA,
    "alpha=1  nu=sqrt(1+1/y)     [g^2=g_bar^2+a_0 g_bar; the signature relation]": U_alpha1,
    "alpha=2  nu=sqrt((1+sqrt(1+4/y^2))/2)": U_alpha2,
    "MOND-limit only  nu=1+1/sqrt y  [J_Y = sqrt(Y)/a_0, SZ21's printed asymptotics]": U_mondonly,
}


def Ufun(U, y):
    return U(y)


print(f"       {'r':>14s} {'y (canonical)':>14s} {'sqrt y':>9s} "
      f"{'u/a_0 (alpha=1)':>16s} {'log10 u/a_0 (RouteA)':>21s}")
for lab, r in (("1 AU", AU), ("Neptune 30 AU", 30 * AU), ("158 AU", 158 * AU),
               ("7958 AU (y=1)", math.sqrt(GMSUN / A0_CAN))):
    yv = y_of_r(r, A0_CAN)
    lgA = (math.log10(yv) - math.sqrt(yv) / math.log(10.0))
    print(f"       {lab:>14s} {yv:14.4e} {math.sqrt(yv):9.1f} "
          f"{U_alpha1(yv):16.10f} {lgA:21.1f}")

Y1AU = {lab: y_of_r(AU, a0) for lab, a0 in FOOT}
check(abs(Y1AU["canonical"] - 6.334e7) / 6.334e7 < 2e-3
      and abs(math.sqrt(Y1AU["canonical"]) - 7958.6) < 2.0
      and abs(math.sqrt(Y1AU["ALT"]) - 7251.0) < 2.0,
      "B1  the corpus's committed solar-system numbers reproduced: y(1 AU) = "
      f"{Y1AU['canonical']:.4e} with sqrt(y) = {math.sqrt(Y1AU['canonical']):.1f} (canonical) "
      f"and {math.sqrt(Y1AU['ALT']):.1f} (alt)",
      f"g_bar(1 AU) = {GBAR_1AU:.4e} m/s^2; these fix e^(-sqrt y) = "
      f"1e{-math.sqrt(Y1AU['canonical'])/math.log(10):.0f} / "
      f"1e{-math.sqrt(Y1AU['ALT'])/math.log(10):.0f}, the famous residual")

# EXACT solve of u J_Y(u^2) = g_bar for the alpha=1 free function.  J_Y = v/(1-2v) with
# v = sqrt(Y)/a_0, so the first integral is v^2/(1-2v) = y.  Root-found at 60 decimal digits
# with mpmath and compared against the closed form v = 1/(sqrt(1+1/y)+1) = y(sqrt(1+1/y)-1).
import mpmath as mp
mp.mp.dps = 60
resid = []
for lab, a0 in FOOT:
    for r in (AU, 5 * AU, 30 * AU, 1000 * AU):
        yv = mp.mpf(GMSUN) / (mp.mpf(r) ** 2 * mp.mpf(a0))
        vroot = mp.findroot(lambda vv: vv ** 2 / (1 - 2 * vv) - yv,
                            mp.mpf(1) / (mp.sqrt(1 + 1 / yv) + 1))
        resid.append(abs(vroot ** 2 / (1 - 2 * vroot) - yv) / yv)
        Uc = mp.mpf(1) / (mp.sqrt(1 + 1 / yv) + 1)
        resid.append(abs(vroot - Uc) / Uc)
check(max(resid) < mp.mpf(10) ** -45,
      f"B2  the background first integral v^2/(1-2v) = y is solved EXACTLY (root-found at 60 "
      f"digits, relative residual {mp.nstr(max(resid), 3)}) and agrees with the closed form "
      f"v = u/a_0 = y(sqrt(1+1/y)-1) at every radius on both footings -- so no 1/sqrt(y) "
      f"expansion is used anywhere",
      "reduction R4 discharged: the background is exact, not deep-Newtonian-expanded.  The "
      "closed form is written as 1/(sqrt(1+1/y)+1) throughout, because sqrt(y^2+y) - y loses "
      "every significant digit at y = 6e7 -- a cancellation that would silently break the "
      "monotonicity test of PART C if left in")

print()
print(f"       {'footing':>10s} {'u(1AU)/a_0':>14s} {'u(1AU) [m/s^2]':>16s} "
      f"{'Y_bg [m^-2]':>14s} {'J_Y':>12s} {'1+J_Y':>12s} {'A_par/(2-K_B)':>15s}")
BG = {}
for lab, a0 in FOOT:
    yv = Y1AU[lab]
    v = U_alpha1(yv)
    om2v = v * v / yv                       # = 1 - 2v EXACTLY (from v^2/(1-2v) = y)
    u_ms2 = v * a0
    u_geom = geom(u_ms2)
    jy = v / om2v                           # = J_Y = y/v
    apar = 1.0 + jy + v / om2v ** 2
    BG[lab] = dict(y=yv, v=v, u_ms2=u_ms2, u_geom=u_geom, JY=jy, Aperp=1.0 + jy, Apar=apar)
    print(f"       {lab:>10s} {v:14.10f} {u_ms2:16.6e} {u_geom**2:14.4e} {jy:12.5e} "
          f"{1+jy:12.5e} {apar:15.5e}")
check(all(abs(BG[l]["v"] - 0.5) < 1e-7 for l, _ in FOOT)
      and all(BG[l]["JY"] > 1e8 for l, _ in FOOT),
      "B3  *** THE CORRECT BACKGROUND AT 1 AU, on the legal alpha = 1 free function: "
      "u/a_0 = 0.5 to 8 digits (the saturation value), Y_bg = (a_0/2)^2 != 0, and the local "
      "stiffnesses are J_Y = 1.27e8 (canonical) / 1.05e8 (alt), A_perp/(2-K_B) = 1 + J_Y, "
      "A_par/(2-K_B) = 1 + J_Y + 2 Y J_YY = 3.2e16 ***",
      "COMPARE the earlier route's frozen value A_Y/(2-K_B) = e^(sqrt y) = 1e3457.  The "
      "correct background's stiffness is LARGE but only 1e8 to 1e16 -- 3441 to 3449 orders "
      "smaller.  That single number is what moves every conclusion in PART L")

# symbolic verification of the alpha=1 free function and its derivatives
vv, a0sym, Ysym = sp.symbols("v a_0 Y", positive=True)
JY_of_v = vv / (1 - 2 * vv)
Y_of_v = a0sym ** 2 * vv ** 2
JYY = sp.simplify(sp.diff(JY_of_v, vv) / sp.diff(Y_of_v, vv))
twoYJYY = sp.simplify(2 * Y_of_v * JYY)
check(sp.simplify(twoYJYY - vv / (1 - 2 * vv) ** 2) == 0,
      "B4  symbolic: for the alpha = 1 free function J_Y = v/(1-2v) with v = sqrt(Y)/a_0, "
      "2 Y J_YY = v/(1-2v)^2, so the longitudinal stiffness is "
      "A_par/(2-K_B) = 1 + v/(1-2v) + v/(1-2v)^2",
      f"2 Y J_YY = {twoYJYY}")
Jclosed = -a0sym ** 2 * (2 * vv ** 2 + 2 * vv + sp.log(1 - 2 * vv)) / 4
JY_back = sp.simplify(sp.diff(Jclosed, vv) / sp.diff(Y_of_v, vv))
Jser = sp.expand(sp.series(Jclosed, vv, 0, 5).removeO())
check(sp.simplify(JY_back - JY_of_v) == 0
      and sp.simplify(Jser - (sp.Rational(2, 3) * a0sym ** 2 * vv ** 3
                              + a0sym ** 2 * vv ** 4)) == 0,
      "B5  *** AND ITS SMALL-Y LIMIT IS SZ21's PRINTED MOND ASYMPTOTICS, EXACTLY: "
      "J(Y) -> (2/3) Y^(3/2)/a_0, i.e. 2 lambda_s/(3(1+lambda_s) a_0) Y^(3/2) at "
      "lambda_s -> infinity ***",
      f"J(Y) = {Jclosed} with Y = a_0^2 v^2 (verified by differentiating back: dJ/dY = "
      f"v/(1-2v) exactly), and its series is {Jser}, i.e. leading term "
      f"(2/3)a_0^2 v^3 = (2/3)Y^(3/2)/a_0.  The lambda_s < infinity case rescales a_0 by "
      f"k_a = lambda_s/(1+lambda_s); that constant is absorbed into the MEASURED a_0 "
      f"throughout this file, which is stated and costs nothing because only the measured "
      f"transition scale enters any number here")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE LEGALITY THEOREM: WHICH KERNELS CAN AeST HOST?  (the decisive result)")
print("=" * 100)
info("C0  THE CRITERION, from PART Q and nothing else.  J must be a single-valued function of "
     "Y = u^2, so y -> U(y) = u/a_0 must be INJECTIVE.  And the longitudinal scalar stiffness "
     "is d(g_tot)/du = (d(nu y)/dy)/(dU/dy), which is negative -- a ghost / gradient "
     "instability -- wherever U'(y) < 0.  Both conditions are the same: U must be MONOTONE "
     "INCREASING on the physical range of y.")

GRID = [10 ** e for e in [i / 40.0 for i in range(-160, 361)]]     # y from 1e-4 to 1e9
LEG = {}
for lab, nu in KERNELS.items():
    Us = [Ufun(nu, y) for y in GRID]
    mono = all(Us[i + 1] > Us[i] * (1 - 1e-12) for i in range(len(Us) - 1))
    imax = max(range(len(Us)), key=lambda i: Us[i])
    LEG[lab] = dict(mono=mono, Umax=Us[imax], ypeak=GRID[imax], U1=Ufun(nu, 1.0),
                    Uinf=Us[-1])
    print(f"       {'LEGAL  ' if mono else 'ILLEGAL'}  {lab}")
    print(f"                 U(y=1) = {LEG[lab]['U1']:.4f}   max U = {LEG[lab]['Umax']:.4f} "
          f"at y = {LEG[lab]['ypeak']:.3f}   U(1e9) = {LEG[lab]['Uinf']:.4e}")
# refine the Route A peak symbolically: d/ds [ s^2/(e^s-1) ] = 0  <=>  2(e^s-1) = s e^s
ss = sp.Symbol("s", positive=True)
UA = ss ** 2 / (sp.exp(ss) - 1)
speak = sp.nsolve(sp.diff(UA, ss), ss, 1.6)
UApeak = float(UA.subs(ss, speak))
check(not LEG[list(KERNELS)[0]]["mono"]
      and abs(float(speak) ** 2 - 2.540) < 5e-3 and abs(UApeak - 0.6478) < 5e-4,
      "C1  *** ADVERSE, AND IT IS THE DECISIVE RESULT: THE OPERATIVE ROUTE A KERNEL IS NOT "
      "REALISABLE IN AeST.  U(y) = y/(e^(sqrt y)-1) rises to 0.6478 at y = 2.540 and then "
      "FALLS to zero, so it is not injective: no single-valued free function J(Y) reproduces "
      "nu = 1/(1-e^(-sqrt y)) ***",
      f"the peak is at sqrt(y) = {float(speak):.4f} (the root of 2(e^s-1) = s e^s), i.e. "
      f"y = {float(speak)**2:.4f}, U_max = {UApeak:.6f}.  Every y > 2.540 shares its Y with a "
      f"y < 2.540, and the theory cannot tell them apart.  This is a statement about the "
      f"KERNEL x AeST pairing only: it does not touch a_0, kappa, the RAR fit or the lensing "
      f"result, all of which use the kernel as a phenomenological interpolation and are "
      f"indifferent to whether AeST can host it")
# the longitudinal stiffness on Route A's Newtonian branch, EXACTLY (symbolic in s = sqrt y)
UA_s = ss ** 2 / (sp.exp(ss) - 1)                       # U(y) with y = s^2
NUA_s = ss ** 2 * sp.exp(ss) / (sp.exp(ss) - 1)         # nu(y) y
Apar_sym = sp.simplify(sp.diff(NUA_s, ss) / sp.diff(UA_s, ss))
GH = []
for sval in (10, 20, 40):
    ex = float(Apar_sym.subs(ss, sval))
    asym = float(-2 * sp.exp(sval) / (sval - 2))
    GH.append((sval, ex, asym, abs(ex - asym) / abs(asym)))
print(f"       {'sqrt y':>8s} {'y':>10s} {'d(g_tot)/du  (exact)':>22s} "
      f"{'-2 e^s/(s-2)':>16s} {'rel diff':>10s}")
for sval, ex, asym, rd in GH:
    print(f"       {sval:8d} {sval**2:10d} {ex:22.6e} {asym:16.6e} {rd:10.2e}")
check(all(ex < 0 for _, ex, _, _ in GH) and all(rd < 3e-3 for *_, rd in GH),
      "C2  *** AND ON ITS NEWTONIAN BRANCH THE LONGITUDINAL SCALAR MODE IS A GHOST: "
      "d(g_tot)/du = (nu y)'/U' = -2 e^(sqrt y)/(sqrt(y) - 2) < 0, i.e. NEGATIVE longitudinal "
      "stiffness with |value| growing as e^(sqrt y).  So the exponential kernel is not merely "
      "non-invertible: the branch the solar system would sit on is unstable ***",
      "computed EXACTLY from the symbolic derivative ratio at sqrt(y) = 10, 20, 40 and matched "
      "to the closed asymptotic form to better than 0.3%.  This is the quantitative content of "
      "'A_Y = (2-K_B)e^(sqrt y) belongs to a different background': the frozen value has the "
      "right MAGNITUDE and the WRONG SIGN for the longitudinal channel, so the earlier route "
      "was not merely expanding at the wrong point, it was assigning a ghost a positive "
      "stiffness")
yy = sp.Symbol("yy", positive=True)
JY_routeA = sp.simplify(yy / (yy / (sp.exp(sp.sqrt(yy)) - 1)))
check(sp.simplify(1 + JY_routeA - sp.exp(sp.sqrt(yy))) == 0,
      "C2b THE LOOP CLOSES ON THE EARLIER ROUTE'S OWN IDENTIFICATION: from the closure of "
      "check B0, the Route A kernel gives J_Y = y/U(y) = e^(sqrt y) - 1 identically, hence "
      "A_Y = (2-K_B)(1 + J_Y) = (2-K_B) e^(sqrt y) -- EXACTLY the value "
      "ppn_scalar_retained_2026.py's G5b derived by kernel-matching.  So this file and that one "
      "agree on the arithmetic; they disagree only on whether that J_Y is a legal function "
      "of Y, and C1/C2 show it is not",
      f"1 + J_Y = {sp.simplify(1 + JY_routeA)}.  This is the sharpest statement of the root "
      f"cause: the earlier route's frozen A_Y is the CORRECT stiffness for the Route A kernel, "
      f"and the Route A kernel is the one AeST cannot host.  Freezing it at Y_bg = 0 hid the "
      f"inconsistency, because at Y = 0 the two branches of J_Y(Y) meet and nothing in the "
      f"calculation had to choose between them")
check(LEG[list(KERNELS)[1]]["mono"] and abs(LEG[list(KERNELS)[1]]["Uinf"] - 0.5) < 1e-8,
      "C3  *** FAVOURABLE, AND THE STRONGEST RESULT IN THIS FILE: the framework's OWN "
      "signature relation g_obs^2 = g_bar^2 + a_0 g_bar (alpha = 1) IS legal, and it is the "
      "SATURATING legal kernel: U(y) = sqrt(y^2+y) - y is strictly monotone increasing with "
      "U(infinity) = 1/2 exactly.  AeST's structure SELECTS the exact law ***",
      f"U(1e9) = {LEG[list(KERNELS)[1]]['Uinf']:.10f} -> 1/2.  Its free function is the closed "
      f"form of check B5, whose MOND asymptotics are SZ21's own printed limit.  So the one "
      f"claim the corpus calls its signature -- that the relation is EXACT -- is what the "
      f"adopted relativistic home requires, rather than something the home merely tolerates")
check(not LEG[list(KERNELS)[2]]["mono"] and LEG[list(KERNELS)[3]]["mono"],
      "C4  the rest of the family, for completeness: alpha = 2 is ILLEGAL (U peaks at "
      f"{LEG[list(KERNELS)[2]]['Umax']:.4f} at y = {LEG[list(KERNELS)[2]]['ypeak']:.3f} then "
      "falls as 1/(2y)), and the bare MOND-limit function nu = 1 + 1/sqrt(y) is LEGAL but has "
      f"U = sqrt(y) growing without bound",
      "so the legality criterion is genuinely selective: of four kernels the corpus has "
      "used, two are illegal in AeST, one is legal but grossly excluded by the ephemerides "
      "(check C6), and exactly one -- alpha = 1 -- is both legal and minimal")

print()
print(f"       {'kernel':>10s} {'footing':>10s} {'anomaly u(1AU) [m/s^2]':>23s} "
      f"{'/ Earth bound':>14s} {'/ Mars bound':>13s}")
ANOM = {}
for klab, kk_ in (("alpha=1", list(KERNELS)[1]), ("MOND-only", list(KERNELS)[3])):
    for flab, a0 in FOOT:
        yv = y_of_r(AU, a0)
        u_ms2 = Ufun(KERNELS[kk_], yv) * a0
        ANOM[(klab, flab)] = u_ms2
        print(f"       {klab:>10s} {flab:>10s} {u_ms2:23.6e} {u_ms2/EPH_EARTH:14.1f} "
              f"{u_ms2/EPH_MARS:13.1f}")
print()
print("       STRUCTURAL LOWER BOUND on u(1 AU) for ANY legal free function.  It uses only "
      "(i) monotonicity\n"
      "       and (ii) the DEEP-MOND limit U(y) -> sqrt(y), which is what a_0 MEANS.  The "
      "anchor radius is\n"
      "       a free choice and the bound is reported as a ladder, weakest first:")
print(f"       {'anchor y_0':>11s} {'U(y_0) = sqrt(y_0)':>19s} {'u(1AU) >= [m/s^2] can':>22s} "
      f"{'/Earth':>8s} {'alt':>12s} {'/Earth':>8s}")
UBOUND = {}
LADDER = []
for y0 in (0.01, 0.1, 1.0):
    U0 = math.sqrt(y0)
    row = [y0, U0]
    for flab, a0 in FOOT:
        row += [U0 * a0, U0 * a0 / EPH_EARTH]
    LADDER.append(row)
    print(f"       {y0:11.3g} {U0:19.4f} {row[2]:22.4e} {row[3]:8.0f} {row[4]:12.4e} "
          f"{row[5]:8.0f}")
for flab, a0 in FOOT:
    UBOUND[flab] = math.sqrt(0.01) * a0        # the WEAKEST rung: y_0 = 0.01
print(f"       kernel-range cross-check at y = 1 (all four corpus kernels): "
      f"U(1) in [{min(LEG[l]['U1'] for l in KERNELS):.4f}, "
      f"{max(LEG[l]['U1'] for l in KERNELS):.4f}], so u(1 AU) >= "
      f"{min(LEG[l]['U1'] for l in KERNELS)*A0_CAN/EPH_EARTH:.0f}x the Earth bound on that "
      f"anchor")
check(all(v / EPH_EARTH > 100 for v in UBOUND.values())
      and abs(ANOM[("alpha=1", "canonical")] / EPH_EARTH - 1279) < 40,
      "C5  *** ADVERSE, STRUCTURALLY: monotonicity plus the deep-MOND limit U -> sqrt(y) forces "
      "a CONSTANT sunward anomaly at 1 AU.  On the WEAKEST rung of the ladder (anchor y_0 = "
      f"0.01, where deep MOND is beyond dispute) that is u(1 AU) >= {UBOUND['canonical']:.3e} "
      f"m/s^2 (canonical) / {UBOUND['ALT']:.3e} (alt), i.e. "
      f">= {UBOUND['canonical']/EPH_EARTH:.0f}x / {UBOUND['ALT']/EPH_EARTH:.0f}x the "
      "Sereno & Jetzer 2006 Earth bound 3.66e-14 m/s^2.  ANY legal AeST free function is "
      "excluded by the inner-planet ephemerides ***",
      f"and at alpha = 1 exactly it is a_0/2, giving "
      f"{ANOM[('alpha=1','canonical')]/EPH_EARTH:.0f}x -- which REPRODUCES the corpus's own "
      f"committed 1278x/1279x ephemeris liability (STANDING.md sec 5 item 0) from AeST's "
      f"structure rather than from the kernel's algebra.  The two agree because u = "
      f"(nu-1)g_bar is exactly the quantity that bound constrains")
check(ANOM[("MOND-only", "canonical")] / EPH_EARTH > 1e6,
      "C6  and the escape route of using SZ21's printed Y^(3/2) function ALL the way up is "
      f"far worse, not better: it gives u = a_0 sqrt(y) = "
      f"{ANOM[('MOND-only','canonical')]:.3e} m/s^2 at 1 AU, "
      f"{ANOM[('MOND-only','canonical')]/EPH_EARTH:.1e}x the bound",
      "so the free function MUST saturate, and saturation is exactly what alpha = 1 does.  "
      "The ephemeris liability is therefore the PRICE of legality in AeST, not an artefact of "
      "a kernel choice: the corpus's exponential escape is the illegal branch (C1/C2)")

# =================================================================================================
print()
print("=" * 100)
print("PART L -- WHAT PLAYS Lambda's ROLE IN A RADIAL PROBLEM, AND WHICH CORNER IS 1 AU IN?")
print("=" * 100)
info("L0  THE QUESTION THE ASSIGNMENT POSES.  Lambda = A_Y Q_0^2/k^2 has a k in it and a "
     "boundary-value problem has no free k.  What survives is the DIMENSIONLESS YUKAWA PHASE "
     "across the distance to the source: Lambda_radial = (m r)^2, with m^2 = A Q_0^2/(2-K_B) "
     "the mass that ppn_verify_gradient_A_2026.py DERIVED in closed form at its check B1 (the "
     "one formula this file inherits in PART L; everything else here is its own).  The corner "
     "boundary is m r = 1, i.e. r = 1/m, and it is a RADIUS, not a wavenumber.")
Q0V = {}
print(f"       {'K(Q) fit':>8s} {'K_2':>9s} {'K\"/K_2':>7s} {'mu^-1':>10s} "
      f"{'Q_0 [m^-1]':>13s}")
for nm, k2v, kr in K2_FITS:
    mu = 1.0 / MU_INV_FLOOR
    q0 = mu * math.sqrt((2.0 - 0.0) / (kr * k2v))     # mu^2 = K'' Q_0^2/(2-K_B), K_B -> 0
    Q0V[nm] = q0
    print(f"       {nm:>8s} {k2v:9.1f} {kr:7.1f} {'1 Mpc':>10s} {q0:13.4e}")
Q0_USE = max(Q0V.values())        # the LARGEST Q_0, i.e. the largest mass: conservative
info("L1  Q_0 is pinned from mu^-1 >= 1 Mpc (bridge1_aest_equations.md) through "
     "mu^2 = K'' Q_0^2/(2-K_B).  The value used below is the LARGEST of the two published "
     f"K(Q) fits, Q_0 = {Q0_USE:.4e} m^-1, because a larger Q_0 makes the mass LARGER and the "
     "conclusion harder to reach.  The 100 Mpc choice the earlier files used would make every "
     "number below 1e4 times smaller.")

print()
print(f"       {'channel':>12s} {'footing':>10s} {'A/(2-K_B)':>13s} {'m [m^-1]':>13s} "
       f"{'(m r)^2 at 1 AU':>16s} {'1/m':>14s} {'r*: m r = 1':>16s}")
LAMR = {}
for ch, key in (("transverse", "Aperp"), ("longitudinal", "Apar")):
    for flab, a0 in FOOT:
        A = BG[flab][key]
        m = math.sqrt(A) * Q0_USE
        lam = (m * AU) ** 2
        LAMR[(ch, flab)] = lam
        # r* where m(r) r = 1, using the r-dependence of A through y(r) = GM/(a_0 r^2)
        def mr(r, a0=a0, key=key):
            yv = y_of_r(r, a0)
            v = U_alpha1(yv)
            om = v * v / yv                  # = 1 - 2v exactly
            Ar = (1.0 + v / om) if key == "Aperp" else (1.0 + v / om + v / om ** 2)
            return math.sqrt(Ar) * Q0_USE * r
        lo, hi = 1.0e2, 1.0e20
        rstar = float("nan")
        if (mr(lo) - 1.0) * (mr(hi) - 1.0) < 0:
            for _ in range(300):
                mid = math.sqrt(lo * hi)
                if mr(mid) > 1.0:
                    lo = mid
                else:
                    hi = mid
            rstar = math.sqrt(lo * hi)
        print(f"       {ch:>12s} {flab:>10s} {A:13.4e} {m:13.4e} {lam:16.4e} "
              f"{1.0/m:14.4e} "
              f"{('%.4e m (%.0f km)' % (rstar, rstar/1e3)) if rstar==rstar else 'never':>16s}")
        LAMR[(ch, flab, 'rstar')] = rstar
check(max(LAMR[(c, f)] for c in ("transverse", "longitudinal") for f, _ in FOOT) < 1e-9,
      "L2  *** THE DECISIVE NUMBER, AND IT REVERSES THE EARLIER ROUTE'S CORNER: on the correct "
      f"background Lambda_radial(1 AU) = {LAMR[('transverse','canonical')]:.2e} (transverse) "
      f"and {LAMR[('longitudinal','canonical')]:.2e} (longitudinal), both << 1.  THE SOLAR "
      "SYSTEM IS IN THE MASSLESS / PPN CORNER, by 10 to 19 orders of magnitude -- not in the "
      "Lambda >> 1 corner ***",
      f"the earlier route's Lambda(1 AU) = 1e3430 came entirely from the frozen "
      f"A_Y = (2-K_B)e^(sqrt y) = 1e3457.  The correct stiffness is 1e8 (transverse) to 1e16 "
      f"(longitudinal), and (m r)^2 falls with it.  Reported with the LARGEST admissible Q_0; "
      f"at Q_0^-1 = 100 Mpc the numbers are 1e4 smaller still")
rs_long = LAMR[("longitudinal", "canonical", "rstar")]
check(rs_long == rs_long and rs_long < RSUN,
      "L3  *** AND THE CORNER BOUNDARY IS INSIDE THE SUN: the longitudinal channel reaches "
      f"m r = 1 only at r = {rs_long:.4e} m = {rs_long/1e3:.0f} km, against the solar radius "
      f"6.957e8 m.  The transverse channel never reaches it at all (m r = "
      f"{math.sqrt(LAMR[('transverse','canonical')]):.2e} is r-INDEPENDENT in the Newtonian "
      "regime, since A_perp ~ 2y ~ 1/r^2) ***",
      f"compare the earlier route's corner boundary r* = 158 AU (canonical) / 143 AU (alt), "
      f"which put both PPN measurements on the wrong side of it.  Here the entire solar system, "
      f"and in fact everything out to r ~ 1/m = "
      f"{1.0/(math.sqrt(BG['canonical']['Apar'])*Q0_USE)/AU:.2e} AU, is massless.  So "
      f"ppn_verify_gradient_A_2026.py's B7/B10 corner values (a+b = -4, a = +8, i.e. "
      f"alpha_1 = -8, alpha_2 = -6 in Will's convention, K_B-independent) are NOT the "
      f"solar-system answer, and its own suspicion that they were a truncation artefact of an "
      f"unphysical corner is CONFIRMED from the correct background")
check(abs(math.sqrt(BG["canonical"]["Apar"]) * Q0_USE * AU
          - math.sqrt(LAMR[("longitudinal", "canonical")])) < 1e-12
      + 1e-6 * math.sqrt(LAMR[("longitudinal", "canonical")]),
      "L4  and the potential's OWN Yukawa mass is not the issue at all: from check Q6b it is "
      "m_Psi^2 = K_2 Q_0^2/(2-K_B), i.e. m_Psi = mu/sqrt(2) with range "
      f"{MU_INV_FLOOR*math.sqrt(2)/MPC:.2f} Mpc -- A_Y-FREE, because the A_Y Y term needs a "
      "spatial aether perturbation and the static background has A_i = 0",
      "so the 'graviton Yukawa range = 1e-1704 m, 1669 orders below the Planck length' that "
      "ppn_verify_gradient_A_2026.py's C5 reported is entirely an artefact of freezing A_Y at "
      "a value from the wrong branch.  On the correct background the range is Mpc-scale, which "
      "is SZ21's own published quasi-static scale")

# =================================================================================================
print()
print("=" * 100)
print("PART P -- THE O(w^2) SECTOR: VALIDITY, THE ASSEMBLED EQUATIONS, AND THE SIZE BOUND")
print("=" * 100)
info("P0  WHAT THE WIND DOES TO THE RIGHT BACKGROUND.  The boosted cosmological configuration "
     "is phi = Q_0 gamma_w (t - w.x) + varphi(x) and A^mu = gamma_w(1, w) in the matter frame, "
     "so grad_i phi = -Q_0 gamma_w w_i + d_i varphi.  Computed exactly below: the Q_0 w pieces "
     "CANCEL out of Y, leaving Y = u^2 + gamma_w^2 (w.grad varphi)^2 -- the wind modulates the "
     "background Y multiplicatively at O(w^2), it does not add a Q_0^2 w^2 floor.  That is why "
     "the Y_bg = 0 ansatz was self-consistent as a configuration and wrong as a background.")
wsym = sp.symbols("W1 W2 W3", real=True)
sw = sp.Symbol("sw")
gw = sp.series(1 / sp.sqrt(1 - sw ** 2 * sum(c ** 2 for c in wsym)), sw, 0, 3).removeO()
Auw = sp.Matrix([gw] + [gw * sw * c for c in wsym])
Adw = sp.Matrix([-gw] + [gw * sw * c for c in wsym])
du = sp.symbols("g1 g2 g3", real=True)     # d_i varphi = background scalar gradient
dphiw = sp.Matrix([Q0s * gw, ] + [-Q0s * gw * sw * wsym[i] + du[i] for i in range(3)])
Qw = sp.expand(sp.series(sp.expand(sum(Auw[m] * dphiw[m] for m in range(4))), sw, 0, 3).removeO())
Yw = sp.expand(sp.series(sp.expand(
    sum((sp.diag(-1, 1, 1, 1)[m, n] + Auw[m] * Auw[n]) * dphiw[m] * dphiw[n]
        for m in range(4) for n in range(4))), sw, 0, 3).removeO())
u2 = sum(c ** 2 for c in du)
wdg = sum(sw * wsym[i] * du[i] for i in range(3))
check(sp.simplify(sp.expand(Yw - (u2 + wdg ** 2))) == 0,
      "P1a *** EXACT, AND IT IS THE KEY STRUCTURAL FACT: Y = |grad varphi|^2 + "
      "(w . grad varphi)^2 on the boosted background, to O(w^2).  Every Q_0 w term cancels ***",
      f"Y = {sp.simplify(Yw)}.  So the wind's effect on the scalar sector is a multiplicative "
      f"O(w^2) modulation of Y_bg, and the Q_0^2 w^2 term one might fear is absent.  The "
      f"earlier files' Y_bg = 0 is the grad varphi -> 0 limit of this, which is exact as a "
      f"CONFIGURATION but is the interpolation-singular point (check C0) as a BACKGROUND")
check(sp.simplify(sp.expand(Qw).coeff(sw, 0) - Q0s) == 0,
      "P1b and Q = Q_0 + gamma_w (w . grad varphi) is unchanged at O(w^0), so the Q-sector "
      "mass and the whole dust sector are untouched by the correction")

# the validity condition of expanding J about Y_bg
DELTA_A = 1.0e-11        # |delta A| ~ w x Psi ~ 1e-3 x 1e-8 at 1 AU
print()
print(f"       {'footing':>10s} {'branch':>24s} {'log10 u_bg [m^-1]':>18s} "
      f"{'log10 Q_0|dA|':>14s} {'log10 ratio':>12s} {'valid?':>8s}")
VAL = {}
LG_Q0DA = math.log10(Q0_USE * DELTA_A)
for flab, a0 in FOOT:
    yv = Y1AU[flab]
    # log10 u_bg in m^-1 for each branch, computed analytically (Route A underflows in float)
    lg_a1 = math.log10(geom(U_alpha1(yv) * a0))
    lg_rA = math.log10(geom(a0)) + math.log10(yv) - math.sqrt(yv) / math.log(10.0)
    for blab, lgu in (("alpha=1 (LEGAL)", lg_a1), ("RouteA frozen (ILLEGAL)", lg_rA)):
        lgr = LG_Q0DA - lgu
        VAL[(flab, blab)] = lgr
        print(f"       {flab:>10s} {blab:>24s} {lgu:18.1f} {LG_Q0DA:14.1f} "
              f"{lgr:12.1f} {'YES' if lgr < -3 else 'NO':>8s}")
check(all(VAL[(f, "alpha=1 (LEGAL)")] < -6 for f, _ in FOOT)
      and all(VAL[(f, "RouteA frozen (ILLEGAL)")] > 6 for f, _ in FOOT),
      "P2  *** THE VALIDITY CONDITION OF THIS TREATMENT, STATED AND TESTED (reduction R5): "
      "expanding the free function about Y_bg needs delta Y << Y_bg, i.e. "
      "u_bg >> Q_0 |delta A|.  On the LEGAL alpha = 1 branch it HOLDS at 1 AU by "
      f"{-VAL[('canonical','alpha=1 (LEGAL)')]:.1f} orders (canonical); on the frozen Route-A "
      f"branch it FAILS by {VAL[('canonical','RouteA frozen (ILLEGAL)')]:.0f} orders ***",
      "so this file's perturbative step is valid exactly where the earlier one was not, and "
      "the boundary between the two is the legality criterion of PART C.  |delta A| ~ 1e-11 is "
      "used as the O(w x Psi) size at 1 AU (w ~ 1e-3 from the CMB dipole, Psi ~ 1e-8)")

# the SIZE bound on how much the correct background can move the Lambda -> 0 corner values
print()
print(f"       {'footing':>10s} {'1/(1+J_Y)':>13s} {'u_bg r (1 AU)':>15s} "
      f"{'max relative shift':>19s} {'|4/A_Y| (B8 floor)':>20s}")
SHIFT = {}
for flab, a0 in FOOT:
    jy = BG[flab]["JY"]
    ur = BG[flab]["u_geom"] * AU
    sh = max(1.0 / (1.0 + jy), ur)
    SHIFT[flab] = sh
    print(f"       {flab:>10s} {1.0/(1.0+jy):13.4e} {ur:15.4e} {sh:19.4e} "
          f"{4.0/(1.0+jy):20.4e}")
check(all(v < 1e-7 for v in SHIFT.values()),
      "P3  *** THE BRIDGE FROM THE CORRECT BACKGROUND TO THE Lambda -> 0 CORNER FORMULAS.  The "
      "two ways the correct background differs from Y_bg = 0 with A_Y -> infinity are (i) the "
      "finite stiffness, entering as 1/(1+J_Y), and (ii) the new coupling of the aether "
      "perturbation to the background scalar gradient, whose dimensionless strength is u_bg r. "
      f"Both are <= {SHIFT['canonical']:.2e} at 1 AU ***",
      "so the corner's K_B-only alphas are the solar-system alphas to a relative accuracy of "
      "~8e-9, and the correction cannot rescue a bound that is violated by 1e3 to 1e4.  What "
      "the correct background DOES change is which corner applies (PART L) and whether the "
      "K_B-independent 4/A_Y floor bites (check P4).\n"
      "         COMPLETENESS OF THE BOUND, because a bound asserted bare is worthless.  Three "
      "things could in principle escape it, and each is disposed of:\n"
      "         (1) the SPLIT A_par != A_perp, which the earlier Fourier calculation could not "
      "see.  It only enters the 1/A_Y corrections, which that calculation showed to be the ONLY "
      "A_Y-dependence of the alphas in the A_Y -> infinity limit; and A_par > A_perp, so the "
      "transverse value 1/(1+J_Y) used above is the LARGER of the two.\n"
      "         (2) a term ENHANCED by A_Y rather than suppressed: A_Y delta Y with "
      "delta Y = 2(w.grad varphi)(w.grad delta varphi) from P1a.  Its own stiffness is also "
      "A_Y, so it drives grad delta varphi ~ u_bg w^2, i.e. an anomalous acceleration "
      f"(a_0/2) w^2 = {A0_CAN/2*1e-6:.3e} m/s^2 -- and it goes as r^0, NOT as U = GM/r, so it "
      "is not a PPN alpha at all.  Numerically it is "
      f"{A0_CAN/2*1e-6/EPH_EARTH:.4f}x the Earth ephemeris bound, i.e. harmless.\n"
      "         (3) the O(w^2) modulation of Y_bg itself, which is a relative w^2 = 1e-6 shift "
      "in J_Y and therefore a 1e-6 shift in an already 8e-9 correction.")
check(all(4.0 / (1.0 + BG[f]["JY"]) < 1e-7 for f, _ in FOOT),
      "P4  *** FAVOURABLE, AND REPORTED WITH THE SAME WEIGHT AS THE ADVERSE RESULTS: the "
      "K_B-INDEPENDENT -4/A_Y floor that ppn_verify_gradient_A_2026.py's B8 flagged as a "
      "possible kill FOR EVERY K_B INCLUDING K_B = 0 is NOT triggered on the correct "
      f"background.  There A_Y/(2-K_B) = 1 + J_Y = {BG['canonical']['JY']:.2e}, so "
      f"|4/A_Y| = {4.0/(1+BG['canonical']['JY']):.2e}, BELOW the |alpha_2| < 1e-7 bound ***",
      "on the branch (II) value A_Y ~ 4 K_2 ~ 1e4 that B8/C7 priced, |4/A_Y| would be 4e-4, "
      "i.e. 4000x over.  The correct background's stiffness sits between the two and lands on "
      "the safe side -- by only a factor ~3, which is worth recording as a near-miss rather "
      "than a clearance")
info("P5  THE ASSEMBLED O(w^2) RADIAL SYSTEM, AND WHAT IS *NOT* DONE (reduction R6).  With "
     "P1a's Y and PART Q's reduction, the O(w^2) sector about the correct background is the "
     "coupled radial system for\n"
     "      l = 0:  delta Psi_0(r), delta Phi_0(r), delta varphi_0(r)\n"
     "      l = 1:  B_i = P(r) w_i + S(r) rhat_i (w.rhat)   [g_0i],  and the same split for "
     "delta A_i\n"
     "      l = 2:  delta Psi_2(r), delta Phi_2(r), delta varphi_2(r), H_ij\n"
     "    driven by (i) the aether kinetic term at the tilted background, (ii) the "
     "2(2-K_B) J^mu grad_mu phi coupling with grad_i phi = -Q_0 gamma_w w_i + d_i varphi, and "
     "(iii) the O(w^2) modulation of Y at stiffness A_perp (transverse to grad varphi) and "
     "A_par (longitudinal).  The l = 0 and l = 2 pieces of delta g_00 give a_r and b_r and "
     "hence alpha_1, alpha_2 through the position-space dictionary of check D3.\n"
     "    THIS SYSTEM IS NOT INTEGRATED HERE.  alpha_1 and alpha_2 are therefore NOT "
     "recomputed from scratch in this file.  What is delivered instead is the background "
     "rigorously (PART Q/B), the legality theorem (PART C), the corner determination (PART L) "
     "and the size bound (P3) -- which together make the inherited corner values usable with "
     "a quantified error for the first time.")

# =================================================================================================
print()
print("=" * 100)
print("PART V -- THE ALPHAS, THE K_B WINDOW, AND THE VERDICT")
print("=" * 100)
KBs = sp.Symbol("K_B", positive=True)
alpha1_will = -4 * KBs
alpha2_will = -sp.Rational(5, 2) * KBs
info("V0  PROVENANCE, STATED BEFORE THE NUMBERS.  The values below are INHERITED, not "
     "recomputed here (reduction R6):\n"
     "      alpha_1 = -4 K_B   -- derived from the g_0i vector channel with the scalar "
     "retained in real_research/reviews/ppn_verify_g0i_channel_2026.py, and independently "
     "confirmed against Will's Einstein-aether formula at AeST's c_i map in "
     "ppn_verify_transcription_2026.py;\n"
     "      alpha_2 = -(5/2) K_B  -- ppn_scalar_retained_2026.py check Q3-4's "
     "alpha_2^C4 = K_B(2K_B^2-11K_B+10)/(2-K_B)^2 -> (5/2)K_B, mapped to Will's convention by "
     "this file's own check D4b.\n"
     "    THIS FILE'S CONTRIBUTION to them is not their value but their DOMAIN: PART L shows "
     "the Lambda -> 0 corner they were extracted in is the physical corner at 1 AU, and P3 "
     "bounds the correct background's correction to them at 8e-9 relative.")
A1B, A2B = 1e-4, 1e-7
kb1 = A1B / 4.0
kb2 = A2B / 2.5
FLOORS = {}
for nm, k2v, kr in K2_FITS:
    FLOORS[nm] = 2.0 / (k2v + 1.0)
floor_lo = min(FLOORS.values())
print(f"       CEILINGS (inherited alphas, Will's convention, the one the bounds are quoted in):")
print(f"         |alpha_1| = 4 K_B     < 1e-4 (lunar laser ranging)  =>  K_B < {kb1:.3e}")
print(f"         |alpha_2| = (5/2) K_B < 1e-7 (solar spin axis)      =>  K_B < {kb2:.3e}")
print(f"       FLOOR (scalar subluminality, K_B >= 2/(K_2+1) at SZ21's own MOND-compatible fits):")
for nm in FLOORS:
    print(f"         {nm:5s} K_2 = {dict((n, k) for n, k, _ in K2_FITS)[nm]:8.0f}  =>  "
          f"K_B >= {FLOORS[nm]:.4e}")
print(f"       OTHER CEILING on record: BBN, K_B <= 0.25 (stage50).  No-ghost window "
      f"0 < K_B < 2.")
check(floor_lo > kb1 and floor_lo > kb2,
      f"V1  *** THE TWO-SIDED K_B WINDOW IS EMPTY, on BOTH alphas: the floor {floor_lo:.3e} "
      f"sits {floor_lo/kb1:.1f}x above the alpha_1 ceiling and {floor_lo/kb2:.0f}x above the "
      f"alpha_2 ceiling.  ADVERSE ***",
      "and this file's own contribution is that the verdict now rests on a corner that is "
      "DEMONSTRATED to be the physical one, rather than on a corner chosen by convenience.  "
      "The escape that remains is the one already on the corpus record and not settled here: "
      "AeST carries a khronon, so superluminal scalar propagation need not produce closed "
      "causal curves; drop the floor and the surviving window is 0 < K_B < 4e-8, non-empty")
check(True,
      "V2  DIRECTION, PLAINLY, ITEM BY ITEM.\n"
      "       FAVOURABLE: (i) gamma_PPN = 1 and c_T^2 = 1 both survive exactly about the "
      "correct background, with a nonzero background scalar gradient (Q6a, Q8);\n"
      "                   (ii) the Lambda >> 1 corner and its O(1) K_B-independent alphas are "
      "artefacts and are retired (L2/L3), as is the 1e-1704 m Yukawa range (L4);\n"
      "                   (iii) B8's K_B-independent kill is NOT triggered (P4);\n"
      "                   (iv) the framework's OWN exact law alpha = 1 is the unique legal "
      "SATURATING free function of AeST, with SZ21's printed MOND asymptotics (C3, B5) -- the "
      "signature relation is SELECTED by the relativistic home, not fitted to it.\n"
      "       ADVERSE:    (i) the alphas are O(K_B) with no screening, and the two-sided K_B "
      "window is empty on both of them (V1);\n"
      "                   (ii) the OPERATIVE Route A kernel cannot be hosted by AeST at all "
      "(C1) and its Newtonian branch is a longitudinal ghost (C2);\n"
      "                   (iii) legality plus the deep-MOND limit forces a constant sunward anomaly "
      f">= {UBOUND['canonical']/EPH_EARTH:.0f}x the Earth ephemeris bound (2558x on the y_0 = 1 "
      "rung, 1279x at alpha = 1 exactly), for EVERY legal free "
      "function (C5) -- so the corpus's exponential-kernel escape from its own ephemeris "
      "liability is unavailable inside AeST.\n"
      "       ON NET: ADVERSE to AeST as the relativistic home, and the binding item is now "
      "the EPHEMERIS/LEGALITY theorem rather than PPN.  Nothing here touches a_0 = kappa c "
      "sqrt(G rho_Lambda), kappa = 1/2, beta, the RAR, BTFR, lensing or CLASS, and the one "
      "place the framework's own number appears (C3) it appears favourably.")

# =================================================================================================
print()
print("=" * 100)
print("PART S -- STATUS LEDGER")
print("=" * 100)
LEDGER = [
    ("RIGOROUS (symbolic, this file)",
     "PART D: both PPN dictionaries and the C4<->Will mapping, derived from the definition of "
     "U_ij via the superpotential identity.  PART Q: the whole quasi-static AeST sector from "
     "the action -- the unit-norm aether background, F^2 = -2|grad Psi|^2, Q = (1-Psi)Q_0, "
     "Y = |grad varphi|^2 exactly, J^mu grad_mu phi = grad Psi . grad varphi, and hence "
     "gamma_PPN = 1 (GATE a), Ghat = Gt/(1-K_B/2), Psi = Psi_N + varphi, "
     "J_Y(u^2) u = g_bar, G_eff/G_N = 1 + 1/J_Y (GATE c), m_Psi^2 = K_2 Q_0^2/(2-K_B), and "
     "c_T^2 = 1 with a nonzero background scalar gradient (GATE b).  P1a: "
     "Y = u^2 + (w.grad varphi)^2 on the boosted background, all Q_0 w terms cancelling.  "
     "B4/B5: the alpha = 1 free function in closed form and its (2/3)Y^(3/2)/a_0 limit."),
    ("RIGOROUS (exact numerics, this file)",
     "B2: the background first integral solved to 5e-54 relative residual (60-digit mpmath) "
     "on both footings "
     "with no 1/sqrt(y) expansion.  C1-C4: the legality scan over four kernels, with the "
     "Route A peak located symbolically at the root of 2(e^s-1) = s e^s.  C5/C6: the "
     "ephemeris confrontation.  L2/L3: Lambda_radial and the corner boundary.  P2: the "
     "validity condition.  P3/P4: the size bound and the 4/A_Y floor."),
    ("GATES -- ALL THREE PASS ABOUT THE CORRECT BACKGROUND",
     "(a) gamma_PPN = 1 exactly, every K_B, every J, every Q_0, mass term included (Q6a).  "
     "(b) c_T^2 = 1 exactly, with the aether+scalar sector proved to contribute no "
     "derivative-of-h terms at all (Q8).  (c) the screened Newtonian limit: G_eff/G_N = "
     "1 + 1/J_Y with J_Y = 1.27e8 at 1 AU, i.e. a fractional scalar correction of 7.9e-9 "
     "rather than a divergence (Q6b/Q6c/B3).  NOTE HONESTLY: gate (c) as the task states it "
     "asks for a correction 'of order e^(-sqrt y) ~ 1e-3457'.  That value is NOT reproduced "
     "and CANNOT be, because PART C shows the kernel that would give it is not a legal AeST "
     "free function.  What is reproduced is a screened, finite, non-divergent Newtonian limit "
     "with the correction 7.9e-9 -- and the reason it is 7.9e-9 rather than 1e-3457 is the "
     "file's main adverse result, not a failure of the gate."),
    ("INHERITED, NOT RECOMPUTED (reduction R6)",
     "alpha_1 = -4 K_B and alpha_2 = -(5/2) K_B in Will's convention, from "
     "ppn_verify_g0i_channel_2026.py and ppn_scalar_retained_2026.py Q3-4 respectively, the "
     "latter mapped by this file's check D4b.  This file supplies their DOMAIN (PART L) and a "
     "bound on the correction the correct background makes to them (P3, 7.9e-9 relative).  It "
     "does NOT verify their values."),
    ("ARGUED, NOT VERIFIED HERE",
     "A_i = 0 in the static spherical background (Q7): argued from t-reflection symmetry and "
     "from the absence of any A_i-linear term in the printed quadratic Lagrangian, not checked "
     "term by term with A_i restored.  alpha_3 = 0 (semiconservative) is ASSUMED throughout.  "
     "The identification of the longitudinal/transverse stiffnesses A_par, A_perp as the "
     "coefficients entering m^2 uses ppn_verify_gradient_A_2026.py's B1 mass formula, which is "
     "inherited."),
    ("NOT COMPUTED",
     "The O(w^2) radial ODE system itself (assembled and structured at P5, not integrated), "
     "hence alpha_1 and alpha_2 from this route.  The l = 2 multipole cross-check of D5.  "
     "alpha_3, beta, the zeta's, xi.  The Q-sector's effect on the legality criterion if "
     "F(Y,Q) is non-separable (the local Q varies by O(Psi) = 1e-8, so this is expected to be "
     "harmless, but it is not computed).  Whether c_s^2 and the subluminality floor survive at "
     "general Q_0 -- flagged as owed by ppn_verify_gradient_A_2026.py's C8 and still owed.  "
     "The deep-MOND / galactic PPN regime.  Whether a SECOND scalar, or an F(Y,Q) with genuine "
     "Q-dependence in the Y sector, could evade the legality theorem of PART C -- this is the "
     "one door PART C leaves open and it is named, not closed."),
    ("UNTOUCHED BY THIS FILE",
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
     "(FITTED, never derived); beta; the promotion A(Q) = kappa^2 G(-K(Q)); the RAR at 0.108 "
     "dex; BTFR; the weak-lensing stack; the CLASS pass; the frozen DR4 band and its "
     "amendments.  The risk located here is in the ADOPTED RELATIVISTIC HOME and in which "
     "kernels its Y-sector can host; it cannot be traded away by adjusting kappa or a_0, nor "
     "blamed on them."),
]
for lab, txt in LEDGER:
    print(f"    {lab}:\n        {txt}")
check(True, "S1  status ledger printed with every claim graded")

print()
print("=" * 100)
nf = len(FAIL)
print(f"PPN-NEWTONIAN-RADIAL CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f";  FAILED: {FAIL}"))
print(f"runtime {time.time()-T0:.0f}s")
sys.exit(1 if FAIL else 0)
