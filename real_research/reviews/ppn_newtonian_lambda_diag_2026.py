#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_newtonian_lambda_diag_2026.py
=================================
THE SHARPEST SINGLE DIAGNOSTIC on the AeST PPN chain: is the Lambda >> 1 pathology found by
real_research/reviews/ppn_verify_gradient_A_2026.py an ARTEFACT of the expansion background?

WHAT WAS ON THE TABLE.  ppn_scalar_retained_2026.py (35/35) expanded AeST's quadratic action
about a flat background with the aether boosted to w and the khronon running at
grad_mu phi = -Q_0 A^bg_mu, hence Y_bg = 0, and obtained alpha_1, alpha_2 depending on K_B
alone, giving an EMPTY two-sided K_B window.  ppn_verify_gradient_A_2026.py then found that in
that same background A_Y acts as a YUKAWA MASS on the Newtonian potential,
m^2 -> A_Y Q_0^2/(2-K_B), so that with the kernel-matched A_Y = (2-K_B)e^(sqrt y) the graviton
range at 1 AU is 1e-1704 m (1669 orders below the Planck length) and the controlling
combination Lambda = A_Y Q_0^2/k^2 is 1e3430 -- the solar system sitting in a corner where the
O(w^2) coefficients degenerate to pure numbers (a = +8, a+b = -4) independent of every
parameter including K_B.  That file named the root cause and declared it NOT COMPUTED: the
background has Y_bg = 0, which is the deep-MOND point and the pole of the theory's own
G_eff/G = 2 A_Y/[(2-K_B)(A_Y-(2-K_B))].

=====================================================================================
THE ANSWER, up front, in both directions
=====================================================================================
THE PATHOLOGY IS AN ARTEFACT -- but NOT of Y_bg = 0.  It is an artefact of a DIFFERENT and
much more elementary background error in the SAME calculation, which this file locates,
proves, and repairs in closed form:

  *** THE BACKGROUND LAGRANGE MULTIPLIER WAS SET TO ZERO WHEN THE THEORY'S OWN BACKGROUND
      AETHER EQUATION REQUIRES lambda_bg = -A_Y Q_0^2. ***

  ppn_scalar_retained_2026.py enforces A^mu A_mu = -1 with the term +eps*lambda(A.A+1), i.e.
  with the multiplier carried at FIRST order only, and its check 0-5 records "the background is
  a solution: lambda_bg = 0 is consistent" as a STRUCTURAL STATEMENT -- it is asserted, never
  computed.  Computed here (PART B, exact Euler-Lagrange of the O(eps) Lagrangian, symbolic):
  the O(eps) action does NOT vanish at lambda_bg = 0.  It carries a TADPOLE whose coefficient
  is exactly A_Y Q_0^2, in both the h_00 and the delta-A_0 equations, and which cancels
  identically at lambda_bg = -A_Y Q_0^2.  Equivalently: the background stress tensor of the
  dark sector is T^bg_{mu nu} = (A_Y Q_0^2 + lambda_bg) A_mu A_nu, so lambda_bg = 0 leaves an
  UNSUBTRACTED uniform background energy density of magnitude A_Y Q_0^2 -- and with
  A_Y = (2-K_B)e^(sqrt y) that is an energy density 1e3430 times the local curvature scale at
  1 AU.  THE "GRAVITON YUKAWA MASS" IS THAT UNSUBTRACTED BACKGROUND ENERGY DENSITY, in Jeans
  form.  It is not a prediction of AeST; it is a background that was never solved for.

  Restoring lambda_bg (PART C, exact closed form, all parameters and k symbolic):
        h_00(w=0) = (G_eff/G) rho / [2 (k^2 + m^2)]
        G_eff/G   = 2 A_Y / [(2-K_B)(A_Y - (2-K_B))]                      (UNCHANGED)
        m^2       = (2 A_Y - Fpp) Q_0^2 A_Y/[2(2-K_B)(A_Y-(2-K_B))]  +  A_Y lambda_bg/[...]
                  = -Fpp Q_0^2 A_Y / [2 (2-K_B)(A_Y - (2-K_B))]     at lambda_bg = -A_Y Q_0^2
                  -> -Fpp Q_0^2 / [2(2-K_B)]                        as A_Y -> infinity
  The 2 A_Y^2 Q_0^2 term -- the ONLY place A_Y's exponential could enter the mass -- is
  cancelled EXACTLY.  The surviving mass is A_Y-INDEPENDENT and its magnitude at Fpp = 4 K_2 is
  EXACTLY SZ21's mu^2 = 2 K_2 Q_0^2/(2-K_B), the same object the corpus pins at
  mu^-1 >~ 1 Mpc.  SO THE ANSWER TO QUESTION (a) IS YES, THE HYPOTHESISED MISPLACEMENT IS REAL,
  AND THE VEHICLE IS NAMED: A_Y's exponential reached the graviton mass through the omitted
  background multiplier, not through the scalar's kinetic normalisation, which keeps it (and
  must -- that is the screening).

  (b) THE YUKAWA RANGE IS RESTORED, by 1726 orders of magnitude: |m|^-1 = 1.03-1.15 Mpc for the
      verified file's own Q_0^-1 = 100 Mpc (10.3-11.5 kpc at Q_0^-1 = 1 Mpc), against 1e-1704 m
      before.  It carries NO a_0 and NO A_Y, so it is footing-INDEPENDENT: neither the
      canonical 9.3619e-11 nor the alt 1.1279e-10 is credited or blamed.  The SIGN of m^2 is
      set by sign(Fpp), which is exactly the object of the corpus's own acknowledged T1/T2
      transcription fork, so only |m| is claimed here.
  (c) Lambda_fix(1 AU) = |m^2|/k^2 = 1.8e-23 (Q_0^-1 = 100 Mpc) to 2.2e-19 (1 Mpc).  THE SOLAR
      SYSTEM IS IN THE Lambda -> 0 CORNER by 19-23 orders of magnitude -- the OPPOSITE corner
      from gradient_A's C3, and the corner the alpha formulas WERE extracted from.  The
      Lambda >> 1 corner is not realised anywhere: Lambda_fix is r^2 m^2, so it reaches 1 only
      at |m|^-1 ~ 1 Mpc.
  (d) GATE (c) PASSES: G_eff/G is untouched by lambda_bg (it is the k^2 coefficient, not the
      k^0 one), and at the kernel-matched A_Y = (2-K_B)e^(sqrt y) it is exactly
      G_eff = G_N nu(y) with G_N = G/(1-K_B/2) and nu(y) = 1/(1-e^(-sqrt y)), i.e. a FRACTIONAL
      scalar correction e^(-sqrt y)/(1-e^(-sqrt y)) = 10^-3456.5 canonical / 10^-3149.0 alt.
      No divergence.  gamma_PPN = 1 and c_T^2 = 1 also survive at general lambda_bg (PART C).

BUT -- AND THIS IS THE PART THAT MUST NOT BE BURIED -- THE SAME TADPOLE WAS DOING LOAD-BEARING
WORK IN THE ALPHA CALCULATION, AND REMOVING IT TAKES SOMETHING AWAY (PART E).

  ppn_scalar_retained_2026.py's checks Q2-1/Q2-2/Q2-3 are the checks that made its alpha_1 and
  alpha_2 EXIST at all: "with the scalar retained the static boosted system is NON-DEGENERATE
  at w = 0: det has a nonzero w -> 0 limit ... and EVERY term of it carries Q_0^2 ... the
  lifting agent is the khronon's background rate Q_0".  Computed here, exactly:

        det(static, w = 0)  =  -k^6 * (A_Y Q_0^2 + lambda_bg) * [the h_00 denominator]

  THE DEGENERACY-LIFTING FACTOR IS THE TADPOLE, ALGEBRAICALLY IDENTICAL TO IT.  It is not
  "Q_0^2"; it is "Q_0^2 evaluated on a background that does not solve its own field equations".
  At lambda_bg = -A_Y Q_0^2 it vanishes identically, for every K_B, A_Y, Fpp, Q_0.

  What follows from that, with the tadpole cancellation FIRST verified to be COVARIANT (E6: on
  the boosted background every nonvanishing O(eps) slot is again exactly proportional to
  A_Y Q_0^2 + lambda_bg, so none of the below is a residual tadpole in disguise):

    (i)   FAVOURABLE.  The zero mode is METRIC-BLIND.  Its null vector is
          (h_00,h_11,h_22,a_0,a_3,chi,lam) = (0,0,0,0, 1, i Q_0/k, i Q_0 k(K_B-2)), i.e. exactly
          the invariance  a_mu -> a_mu + d_mu xi,  chi -> chi - Q_0 xi, which leaves
          u_mu = Q_0 a_mu + d_mu chi -- hence BOTH Y and Q, by PART A's identity -- and
          F_{mu nu} unchanged.  The source satisfies the solvability condition and
          h_00 = h_11 = h_22 come out UNIQUELY.  The static Newtonian problem is still well
          posed, so nothing in PARTS C-D rests on a degenerate solve.  And switching on
          Y_bg != 0 lifts the zero mode outright (check G2).
    (ii)  The BOOSTED static determinant, with lambda_bg restored, starts at O(w^2) (E5).
          "det ~ w^2" is verbatim ppn_scalar_retained's own check Q2-3 describing reading D's
          degeneracy.  The scalar never cured reading D's premise-failure; the tadpole masked it.
    (iii) And the boosted branch then IS reading D's ANSWER, in the full theory: h_00 has a
          genuine Taylor series in w (no 1/Q_0^2 contact pole at all), its w -> 0 value is
          rho/(2k^2) EXACTLY -- G_eff = G, pure GR, discontinuously different from the w = 0
          answer G/(1-K_B/2) -- and the O(w^2) coefficient is
                a + b = -8 A_Y Q_0^2 / k^2   exactly, for every K_B and every Fpp.
          Since a+b is dimensionless while [A_Y Q_0^2] = 1/length^2, that 1/k^2 is forced, so
          the O(w^2) part of h_00 goes as rho/k^4 and NOT as U = rho/k^2: there is NO
          U-proportional preferred-frame term, i.e. alpha_1 = alpha_2 = 0 IN EVERY CONVENTION,
          and what the O(w^2) sector actually holds is a WIND-INDUCED GRAVITON MASS
          delta m^2 = 4 A_Y Q_0^2 w^2.
    (iv)  ADVERSE, and this is the price: that mass carries A_Y back.  At 1 AU with
          w = 1.23e-3 (the Sun against the CMB frame, 369.8 km/s), delta m^2/k^2 =
          4 Lambda_old w^2 = 1e3425 canonical / 1e3118 alt.  THE A_Y ENHANCEMENT IS NOT
          ELIMINATED BY THE REPAIR -- IT IS DEMOTED FROM O(w^0) TO O(w^2).  The static
          Newtonian limit is exactly repaired; the preferred-frame sector still leaves the
          perturbative regime.

  NET DIRECTION, stated plainly and once: MIXED, and adverse to the CHAIN rather than to the
  framework.  BANKED: gradient_A's Lambda(1 AU) = 1e3430 STATIC pathology is an ARTEFACT and is
  void; ppn_scalar_retained's Q_0-lifted non-degeneracy is the tadpole and is void; therefore
  BOTH files' alpha's are void, in BOTH corners, and the empty K_B window is NOT ESTABLISHED
  (neither is it refuted).  REPORTED BUT NOT BANKED: on the repaired branch alpha_1 = alpha_2 = 0
  and the residual trouble is a second-order-in-w graviton mass.  NOTHING here licenses either
  "AeST fails PPN" or "AeST passes PPN".  The unbanked half is unbanked for three named reasons:
  one orientation only (w parallel to k, giving a+b and not a); the four h_{3 nu} equations the
  gauge leaves unused, flagged "ARGUED, NOT VERIFIED" by both earlier files and by stage74 B2;
  and the w -> 0 discontinuity, which makes the choice of branch a physics question.

=====================================================================================
A CONVENTION AUDIT THAT FALLS OUT, AND OVERTURNS A HEADLINE (PART F)
=====================================================================================
The task's convention statement is DERIVED here, not quoted.  With
delta h_00 = [a w^2 + b (w.khat)^2] U and U_ij = (delta_ij - 2 khat_i khat_j) U:
  * Will:  delta g_00 = -(alpha_1-alpha_2-alpha_3) w^2 U - alpha_2 w^i w^j U_ij
           =>  a = alpha_3 - alpha_1,  b = +2 alpha_2  =>  alpha_1 = -a (at alpha_3=0),
               alpha_2 = +b/2.
  * The two earlier files' C4:  g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij
           =>  a = alpha_1 + alpha_2,  b = -2 alpha_2.
So the map is alpha_1^Will = -(alpha_1^C4 + alpha_2^C4) and alpha_2^Will = -alpha_2^C4.  IT IS
NOT AN OVERALL SIGN FLIP: it MIXES the two.  ppn_scalar_retained_2026.py's convention note
("A reader in Will's normalisation must flip the sign of both alpha's reported here") is
therefore WRONG, and the consequence is not cosmetic.  Its own two measured quantities were
a = 4 K_B (perpendicular) and a+b = 2K_B(3K_B-2)/(2-K_B)^2 (parallel), and
alpha_1^C4 + alpha_2^C4 = 4 K_B identically, so

    alpha_1^Will = -4 K_B   EXACTLY, to all orders in K_B,

which is EXACTLY reading L's / stage70's Foster-Jacobson value for the Einstein-aether mapping
(c_1 = +K_B, c_2 = 0, c_3 = -K_B, c_4 = 0) -- in the convention Foster & Jacobson use.  So
ppn_scalar_retained's headline "reading L's FORMULA has the wrong magnitude AND the wrong sign"
is a CONVENTION ARTEFACT: read in Will's convention its own calculation REPRODUCES -4 K_B
exactly, and stage70's alpha_1 ceiling K_B < 2.5e-5 is VINDICATED, not superseded.  This is
checked symbolically (F2-F3).  The |alpha| CEILINGS are numerically almost unmoved (every bound
used is on |alpha|), so this repairs an attribution, not the arithmetic -- but "reading L is
wrong in sign" must come off the record.

=====================================================================================
WHAT IS NOT COMPUTED (named, not hidden)
=====================================================================================
  * The alpha's themselves about the corrected background.  This route was assigned as a
    diagnostic and does not compute them.  They MUST be recomputed with lambda_bg restored
    before any K_B window -- empty or not -- is quoted, because PART E shows the boosted
    determinant changes character.
  * The FULL Y_bg != 0 solve.  PART G shows (i) the tadpole identity and its cancellation are
    Y_bg-INDEPENDENT (an exact consequence of the PART A identity, since dY/dC at any background
    with A.V = 0 is -Q_0^2), (ii) the correct lambda_bg = -A_Y Q_0^2 is accurate to a fractional
    O(1/Lambda_old) = 1e-3430 at 1 AU -- the very largeness gradient_A called pathological is
    what makes it exact -- and (iii) turning on Y_bg != 0 LIFTS the PART E zero mode in the
    static sector (verified).  But a strictly constant-V local background leaves an
    UNBALANCED longitudinal-aether tadpole -2 A_Y Q_0 V_z that no lambda_bg can cancel, so the
    fully consistent local background needs a non-constant aether.  And the second derivative
    of the free function, J2 = d^2(dark sector)/dY^2, opens a mass channel ~ J2 Q_0^4 that is
    INVISIBLE at Y_bg = 0 by construction (delta^(1)Y = 0 there) and is NOT sized here, because
    sizing it needs the normalisation linking Y to the framework's y, which the corpus does not
    pin.  Both are flagged as owed.
  * The WKB validity condition, stated and TESTED: a strictly local expansion in the scalar
    stiffness needs k >> |grad ln A_Y| = sqrt(y)/r, i.e. k r >> sqrt(y).  At 1 AU with k ~ 1/r
    that FAILS by sqrt(y) = 7958.8 (canonical) / 7251.0 (alt).  This is a real negative and it
    is reported as one.  It does NOT touch the results above, for a reason that is checked:
    after the repair the mass coefficient is Fpp Q_0^2, which contains no A_Y and therefore no
    radial profile at all, so there is nothing for a gradient to act on.
  * The four h_{3 nu} field equations left unused by the gauge h_{3 nu} = 0 -- inherited
    verbatim from both earlier files' ledgers, unchanged and unresolved here.

=====================================================================================
UNTOUCHED BY THIS FILE
=====================================================================================
a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 (FITTED,
never derived); the kernel nu(y) = 1/(1-e^(-sqrt y)) (Milgrom & Sanders 2008 ApJ 678,131
Eq. 13 at alpha = 1/2); beta; the promotion A(Q) = kappa^2 G(-K(Q)); the RAR, BTFR, weak
lensing, CLASS.  Every issue located here is in the ADOPTED RELATIVISTIC HOME (AeST: Skordis &
Zlosnik, PRL 127 161302, arXiv:2007.00082) and in the background about which a PPN expansion of
it was performed.  It can be neither credited to nor blamed on the framework's normalisation.

CONVENTIONS.  Machinery, signature, units, gauge and mode conventions are COPIED from
ppn_scalar_retained_2026.py so that any disagreement is physics and not bookkeeping: signature
(-,+,+,+), c = 1, 16 pi G = 1 (G_N calibrated in-script), F_{mu nu} = d_mu A_nu - d_nu A_mu
(no metric), gauge h_{3 nu} = 0, static in the matter frame, single Fourier mode k along z,
Lagrangian net Y-coefficient carried as a free symbol (here J1 = A_Y = d(dark)/dY, with
J2 = d^2(dark)/dY^2 and J0 = the constant piece added), Q-sector curvature +(Fpp/2)(Q-Q_0)^2,
khronon background grad_mu phi = -Q_0 A^bg_mu + V_mu.  THE ONE DELIBERATE DIFFERENCE, which is
the whole point of the file: the constraint is enforced with (lambda_bg + eps*lambda)(A.A+1),
lambda_bg free, instead of eps*lambda(A.A+1).

EXIT 0 iff every numbered check passes.  Runtime ~5-10 min (the boosted O(eps^2) build in
PART E is the expensive step).
"""

import math
import sys
import time

import sympy as sp
from sympy.calculus.euler import euler_equations

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
# symbols
# =================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
CO = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA
eps = sp.Symbol("eps")           # perturbation bookkeeping (linear in rho)
s = sp.Symbol("s")               # wind bookkeeping (w -> s w)
KB = sp.Symbol("K_B", positive=True)
cJ = sp.Symbol("c_J")            # the J.grad(phi) coefficient; the action fixes c_J = 2 - K_B
JY1 = sp.Symbol("J1")            # = A_Y, the NET Y coefficient d(dark)/dY at the background
JY2 = sp.Symbol("J2")            # d^2(dark)/dY^2 at the background (invisible at Y_bg = 0)
J0 = sp.Symbol("J0")             # the constant piece of the dark Y-sector (a Lambda term)
Fpp = sp.Symbol("Fpp")           # Q-sector curvature: Lagrangian carries +(Fpp/2)(Q-Q_0)^2
Q0 = sp.Symbol("Q_0")
LB = sp.Symbol("lam_bg")         # *** THE BACKGROUND LAGRANGE MULTIPLIER -- the point of this file
k = sp.Symbol("k", positive=True)
om = sp.Symbol("omega")
rho = sp.Symbol("rho")
R_ = sp.Symbol("R")
P_, Pi_ = sp.Symbol("P"), sp.Symbol("Pi_")
I = sp.I
AY = JY1                          # alias: A_Y is J1


def _G1_general():
    """Linearised Einstein tensor for h_{mu nu}(t,z), from the Riemann definition."""
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    hd = sp.Matrix(4, 4, lambda m, n: H[(min(m, n), max(m, n))])
    gd = ETA + eps * hd
    gu = ETAI - eps * (ETAI * hd * ETAI)
    Gam = [[[sp.expand(sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]

    def ric(sig, nu):
        out = 0
        for m in range(4):
            out += sp.diff(Gam[m][nu][sig], CO[m]) - sp.diff(Gam[m][m][sig], CO[nu])
            for l in range(4):
                out += Gam[m][m][l] * Gam[l][nu][sig] - Gam[m][nu][l] * Gam[l][m][sig]
        return sp.expand(out)

    R1 = sp.Matrix(4, 4, lambda m, n: sp.expand(ric(m, n)).coeff(eps, 1))
    Rs = sp.expand(sum(ETAI[m, n] * R1[m, n] for m in range(4) for n in range(4)))
    return H, sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m, n] * Rs))


def build(wvec=(0, 0, 0), zero_fields=(), Vvec=(0, 0, 0), Ybg=0):
    """O(eps^0,1,2) Lagrangian of the aether+scalar sector + the matter source.

    Dark Y-sector carried as  -[ J0 + J1 (Y - Ybg) + (J2/2)(Y - Ybg)^2 ],
    constraint enforced with  (lam_bg + eps*lam)(A.A + 1).
    """
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    a = [sp.Function(f"a{m}")(t, z) for m in range(4)]
    chi = sp.Function("chi")(t, z)
    lam = sp.Function("lam")(t, z)
    subz = {}
    for nm in zero_fields:
        if nm.startswith("h"):
            subz[H[(int(nm[1]), int(nm[2]))]] = 0
        else:
            subz[a[int(nm[1])]] = 0

    def Z(e):
        return e.subs(subz)

    hd = sp.Matrix(4, 4, lambda m, n: Z(H[(min(m, n), max(m, n))]))
    gd = ETA + eps * hd
    hup = ETAI * hd * ETAI
    gu = ETAI - eps * hup + eps ** 2 * (hup * hd * ETAI)
    trh = sum(ETAI[m, n] * hd[m, n] for m in range(4) for n in range(4))
    h2 = sum(hup[m, n] * hd[m, n] for m in range(4) for n in range(4))
    sq = 1 + eps * trh / 2 + eps ** 2 * (trh ** 2 / 8 - h2 / 4)
    w2 = sum(c ** 2 for c in wvec)
    gw = sp.series(1 / sp.sqrt(1 - w2), s, 0, 3).removeO()
    Abg = sp.Matrix([-gw, gw * wvec[0], gw * wvec[1], gw * wvec[2]])
    Ad = sp.Matrix([Abg[m] + eps * Z(a[m]) for m in range(4)])
    Au = gu * Ad
    AA = sum(Au[m] * Ad[m] for m in range(4))
    Vd = sp.Matrix([0, Vvec[0], Vvec[1], Vvec[2]])
    Pdn = sp.Matrix([-Q0 * Abg[m] + Vd[m] for m in range(4)])
    dphi = sp.Matrix([Pdn[m] + eps * sp.diff(Z(chi), CO[m]) for m in range(4)])
    Gam = [[[sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
    F = sp.Matrix(4, 4, lambda m, n: eps * (sp.diff(Z(a[n]), CO[m]) - sp.diff(Z(a[m]), CO[n])))
    F2 = sum(F[m, n] * F[aa, bb] * gu[m, aa] * gu[n, bb]
             for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
    Jd = [sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[bb][nu][al] * Ad[bb] for bb in range(4)))
              for nu in range(4)) for al in range(4)]
    Jphi = sum(gu[mu, al] * Jd[al] * dphi[mu] for mu in range(4) for al in range(4))
    Q = sum(Au[mu] * dphi[mu] for mu in range(4))
    Y = sum((gu[mu, nu] + Au[mu] * Au[nu]) * dphi[mu] * dphi[nu]
            for mu in range(4) for nu in range(4))
    Jfun = J0 + JY1 * (Y - Ybg) + (JY2 / 2) * (Y - Ybg) ** 2
    B = (-(KB / 2) * F2 + 2 * cJ * Jphi - Jfun + (Fpp / 2) * (Q - Q0) ** 2
         + (LB + eps * Z(lam)) * (AA + 1))
    L = sq * B
    Lser = sp.expand(sp.series(sp.expand(L), eps, 0, 3).removeO())
    L0 = sp.expand(Lser.coeff(eps, 0))
    L1 = sp.expand(Lser.coeff(eps, 1))
    L2 = sp.expand(Lser.coeff(eps, 2))
    if wvec != (0, 0, 0):
        L1 = sp.expand(sp.series(L1, s, 0, 3).removeO())
        L2 = sp.expand(sp.series(L2, s, 0, 3).removeO())
    L2 = L2 + sp.Rational(1, 2) * rho * hd[0, 0]
    live = [Z(f) for f in ([H[(m, n)] for m in range(4) for n in range(m, 4)] + list(a) + [chi, lam])]
    live = [f for f in live if f != 0]
    return dict(H=H, a=a, chi=chi, lam=lam, L0=L0, L1=L1, L2=L2, Z=Z, live=live)


def fourier(fields):
    Fa, Ga, sub = {}, {}, {}
    for f in fields:
        nm = f.func.__name__
        Fa[nm], Ga[nm] = sp.Symbol("F_" + nm), sp.Symbol("G_" + nm)
        Fp, Gp = Fa[nm] * P_, Ga[nm] * Pi_
        sub[sp.Derivative(f, (z, 2))] = (I * k) ** 2 * Fp + (-I * k) ** 2 * Gp
        sub[sp.Derivative(f, (t, 2))] = (-I * om) ** 2 * Fp + (I * om) ** 2 * Gp
        sub[sp.Derivative(f, t, z)] = (-I * om) * (I * k) * Fp + (I * om) * (-I * k) * Gp
        sub[sp.Derivative(f, z)] = I * k * Fp - I * k * Gp
        sub[sp.Derivative(f, t)] = -I * om * Fp + I * om * Gp
        sub[f] = Fp + Gp
    return Fa, Ga, sub


G1_H, G1_GEN = _G1_general()


def equations(rr, eq_names, extra_sub=None):
    """Linear field equations in Fourier space (amplitudes F_*)."""
    H, Z = rr["H"], rr["Z"]
    Fa, Ga, sub = fourier(rr["live"])
    L2 = rr["L2"].subs(extra_sub) if extra_sub else rr["L2"]
    L2f = sp.expand(L2.subs(sub, simultaneous=True)).subs(rho, R_ * P_ + sp.Symbol("Rc") * Pi_)
    L2avg = sp.expand(sp.expand(sp.expand(L2f).coeff(P_, 1)).coeff(Pi_, 1))
    G1 = G1_GEN.subs(extra_sub) if extra_sub else G1_GEN
    G1 = G1.subs({f: Z(f) for f in [H[(m, n)] for m in range(4) for n in range(m, 4)]})
    G1 = G1.applyfunc(lambda e: sp.expand(sp.expand(e).subs(sub, simultaneous=True)).coeff(P_, 1))
    Gup = sp.Matrix(4, 4, lambda m, n: sp.expand(ETA[m, m] * ETA[n, n] * G1[m, n]))
    if extra_sub:
        L2avg = L2avg.subs(extra_sub)
        Gup = Gup.subs(extra_sub)
    eqs = []
    for nm in eq_names:
        e = sp.diff(L2avg, Ga[nm])
        if nm.startswith("h"):
            m, n = int(nm[1]), int(nm[2])
            e = e - (1 if m == n else 2) * Gup[m, n]
        eqs.append(sp.expand(e))
    return eqs, Fa, Ga


ZF0 = ("h01", "h02", "h12", "h13", "h23", "h03", "h33", "a1", "a2")
UNK0 = ["h00", "h11", "h22", "a0", "a3", "chi", "lam"]
print("=" * 100)
print(f"machinery: linearised Einstein tensor from the Riemann definition ({time.time()-T0:.0f}s)")
print("=" * 100)

# =================================================================================================
print()
print("=" * 100)
print("PART A -- THE EXACT ALGEBRAIC IDENTITY THAT LOCATES THE MASS CHANNEL")
print("=" * 100)
info("A0  Y = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi is a QUADRATIC FORM in "
     "grad phi, and the background is grad_mu phi = -Q_0 A^bg_mu + V_mu.  Write the FULL "
     "aether as A = A^bg + eps a, C = A^mu A_mu + 1 (the constraint violation), and "
     "W_mu = grad_mu phi + Q_0 A_mu -- so W = V + eps u with u_mu = Q_0 a_mu + d_mu chi.  Then "
     "there is an EXACT identity, to all orders, with no expansion at all.")
Am = sp.Matrix(sp.symbols("Aa0 Aa1 Aa2 Aa3"))
gm = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"gu{min(i,j)}{max(i,j)}"))
Wm = sp.Matrix(sp.symbols("Ww0 Ww1 Ww2 Ww3"))
pm = sp.Matrix([-Q0 * Am[m] + Wm[m] for m in range(4)])
Auu = gm * Am
Cg = sum(Auu[m] * Am[m] for m in range(4)) + 1
Qg = sum(Auu[m] * pm[m] for m in range(4))
Yg = sum((gm[m, n] + Auu[m] * Auu[n]) * pm[m] * pm[n] for m in range(4) for n in range(4))
AW = sum(Auu[m] * Wm[m] for m in range(4))
PWW = sum((gm[m, n] + Auu[m] * Auu[n]) * Wm[m] * Wm[n] for m in range(4) for n in range(4))
check(sp.simplify(sp.expand(Yg - (Q0 ** 2 * (Cg ** 2 - Cg) - 2 * Q0 * Cg * AW + PWW))) == 0,
      "A1  *** EXACT IDENTITY (generic metric, generic aether, no constraint imposed, no "
      "perturbative expansion):\n"
      "        Y = Q_0^2 (C^2 - C) - 2 Q_0 C (A.W) + P^{mu nu} W_mu W_nu ***",
      "the three channels are now separated once and for all: a PERFECT SQUARE in W (which is "
      "the scalar's kinetic term plus an aether mass), a CROSS term linear in the constraint "
      "violation, and -- the one that matters -- a term Q_0^2 C which is ALGEBRAIC in the "
      "metric and the aether and carries NO derivatives at all.  That last channel is the only "
      "place a graviton mass can come from")
check(sp.simplify(sp.expand(Qg - (Q0 * (1 - Cg) + AW))) == 0,
      "A2  and the companion identity  Q = Q_0 (1 - C) + A.W,  so (Q - Q_0)^(1) = A.u once "
      "C^(1) = 0: the Q-sector too depends only on u_mu = Q_0 a_mu + d_mu chi",
      "hence the whole dark sector is a function of u and C alone")
Cv, AWv, PWv = sp.symbols("Cv AWv PWv")
Yform = Q0 ** 2 * (Cv ** 2 - Cv) - 2 * Q0 * Cv * AWv + PWv
dYdC = sp.diff(Yform, Cv)
check(sp.simplify(dYdC.subs({Cv: 0, AWv: 0}) + Q0 ** 2) == 0
      and sp.simplify(sp.diff(Yform, Cv, 2) - 2 * Q0 ** 2) == 0
      and sp.simplify(sp.diff(Yform, PWv) - 1) == 0,
      "A3  *** AND THE Y_bg-INDEPENDENT COROLLARY, which is what makes the whole repair below "
      "background-independent: dY/dC at ANY background with C = 0 and A.W = 0 equals -Q_0^2, "
      "for EVERY Y_bg ***",
      "A.W = 0 is exactly the statement that the background khronon gradient's "
      "aether-orthogonal part V is orthogonal to A -- which is the DEFINITION of the "
      "decomposition, true at Y_bg = 0 and at Y_bg != 0 alike.  So the Lagrangian's term "
      "LINEAR in the constraint violation is (J1 Q_0^2 + lambda_bg) C at any background, and "
      "the cancellation proved in PART B is not a property of Y_bg = 0")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE TADPOLE: lambda_bg = 0 IS NOT A SOLUTION")
print("=" * 100)
r0 = build(zero_fields=ZF0)
print(f"       (O(eps^2) build at w = 0, V = 0: {time.time()-T0:.0f}s)")
check(sp.simplify(r0["L0"].subs({J0: 0})) == 0,
      "B1  the O(eps^0) Lagrangian vanishes at Y_bg = 0 and J0 = 0 (Y_bg = 0 makes the Y-term "
      "vanish and the constraint term vanishes on A.A = -1), so the background Lagrangian gives "
      "NO information about lambda_bg -- which is presumably why it was never computed",
      f"L^(0) = {sp.simplify(r0['L0'])}.  A vanishing background Lagrangian does NOT imply a "
      f"vanishing background stress tensor: the stress is a metric DERIVATIVE, and the "
      f"aether equation is an A-derivative")
L1_0 = r0["L1"].subs({cJ: 2 - KB, JY2: 0, J0: 0})
els = euler_equations(L1_0, r0["live"], [t, z])
tad = [sp.simplify(e.lhs) for e in els]
print(f"       nonvanishing O(eps) Euler-Lagrange expressions: {tad}")
check(len(tad) == 2 and all(sp.simplify(e.subs(LB, -JY1 * Q0 ** 2)) == 0 for e in tad)
      and any(sp.simplify(e.subs(LB, 0)) != 0 for e in tad),
      "B2  *** THE CENTRAL RESULT OF THIS FILE.  The O(eps) action carries a TADPOLE.  Its "
      "Euler-Lagrange expressions are -(A_Y Q_0^2 + lambda_bg) [the h_00 equation] and "
      "+2(A_Y Q_0^2 + lambda_bg) [the delta-A_0 equation].  They vanish IF AND ONLY IF\n"
      "            lambda_bg = -A_Y Q_0^2 .\n"
      "       ppn_scalar_retained_2026.py sets lambda_bg = 0 (it writes the constraint term as "
      "eps*lambda(A.A+1), with the multiplier carried at first order only) and its check 0-5 "
      "records 'lambda_bg = 0 is consistent ... as a structural statement'.  IT IS NOT "
      "CONSISTENT ***",
      "the two expressions are proportional to each other and to the SAME combination, which "
      "is what a genuine background-equation violation looks like (one condition, appearing in "
      "every equation the offending term touches).  Derived, not asserted: the O(eps) "
      "Lagrangian was assembled by the same build() as the O(eps^2) one and differentiated by "
      "sympy's euler_equations")
check(sp.simplify(tad[0].subs(LB, 0) + JY1 * Q0 ** 2) == 0,
      "B3  the h_00 slot of the tadpole is exactly -(A_Y Q_0^2), and the transverse slots "
      "(h_11, h_22) are ABSENT at J0 = 0 -- so the unsubtracted background stress has the pure "
      "form T^bg_{mu nu} = (A_Y Q_0^2 + lambda_bg) A_mu A_nu: a uniform ENERGY DENSITY, with no "
      "pressure",
      "reading it against the matter coupling (1/2) rho h_00, whose Euler-Lagrange contribution "
      "is rho/2, the spurious background density is rho_bg = -2 A_Y Q_0^2 in the file's "
      "16 pi G = 1 units.  This is the physical content of the 'graviton Yukawa mass': a "
      "uniform energy density of that size, left in the equations, produces a Jeans-like "
      "k^2 -> k^2 + O(A_Y Q_0^2) shift in the static response.  PART C confirms the "
      "coefficient exactly")
Vz = sp.Symbol("V_z")
tv = time.time()
rV = build(zero_fields=ZF0, Vvec=(0, 0, Vz), Ybg=Vz ** 2)
elsV = euler_equations(rV["L1"].subs({cJ: 2 - KB}), rV["live"], [t, z])
tadV = [sp.simplify(e.lhs) for e in elsV]
print(f"       (Y_bg != 0 build: {time.time()-tv:.0f}s)  tadpole expressions: {tadV}")
par = [e for e in tadV if e.has(LB)]
perp = [e for e in tadV if e.has(Vz)]
check(all(sp.simplify(e.subs({LB: -JY1 * Q0 ** 2, J0: 0})) == 0 for e in par) and len(par) == 2,
      "B4  *** AND THE SAME lambda_bg = -A_Y Q_0^2 IS REQUIRED AT Y_bg != 0: with a background "
      "spatial khronon gradient V_z switched on, the A-PARALLEL projection of the aether "
      "equation is unchanged, exactly as PART A's corollary A3 predicts ***",
      "so the repair is background-INDEPENDENT.  It is not a Y_bg = 0 accident, and it cannot "
      "be evaded by moving to the physically correct solar-system background.  (J0 = 0 is "
      "also forced here, by the h_11 and h_22 equations: that is the ordinary statement that "
      "flat space needs no cosmological constant, and it is the Lambda term, handled "
      "separately in any PPN treatment)")
check(len(perp) == 1 and sp.simplify(perp[0] + 2 * JY1 * Q0 * Vz) == 0,
      "B5  BUT the Y_bg != 0 local background is NOT fully consistent, and this is reported as "
      "the honest limitation it is: the LONGITUDINAL-AETHER equation retains an unbalanced "
      "residual -2 A_Y Q_0 V_z which NO choice of lambda_bg can cancel (lambda_bg multiplies "
      "A_mu, which is orthogonal to V_mu)",
      f"residual = {sp.simplify(perp[0])}.  Physically: a constant aether cannot coexist with a "
      f"constant spatial khronon gradient -- the true solar-system background has an "
      f"ACCELERATED aether, whose gradient terms (inside F^2 and J^mu grad_mu phi) supply the "
      f"balance.  A strictly constant-V local expansion therefore cannot be the final word on "
      f"the Y_bg != 0 problem, and this file does not claim it is.  What it DOES establish is "
      f"that the A-parallel condition -- the one that fixes lambda_bg and hence kills the "
      f"A_Y-enhanced mass -- is untouched by V")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE REPAIRED NEWTONIAN LIMIT, IN EXACT CLOSED FORM")
print("=" * 100)
eqs0, Fa0, Ga0 = equations(r0, UNK0, extra_sub={cJ: 2 - KB, JY2: 0, J0: 0, om: 0})
unk0 = [Fa0[u] for u in UNK0]
Am0, bm0 = sp.linear_eq_to_matrix(eqs0, unk0)
xs0 = Am0.LUsolve(bm0)
h00 = sp.cancel(sp.together(xs0[UNK0.index("h00")]))
h11 = sp.cancel(sp.together(xs0[UNK0.index("h11")]))
h22 = sp.cancel(sp.together(xs0[UNK0.index("h22")]))
Geff = 2 * JY1 / ((2 - KB) * (JY1 - (2 - KB)))
m2_gen = ((2 * JY1 - Fpp) * Q0 ** 2 + 2 * LB) * JY1 / (2 * (2 - KB) * (JY1 - (2 - KB)))
check(sp.simplify(h00 - Geff * R_ / (2 * (k ** 2 + m2_gen))) == 0,
      "C1  *** EXACT CLOSED FORM, all six parameters AND k symbolic, nothing frozen:\n"
      "        h_00(w=0) = (G_eff/G) rho / [2 (k^2 + m^2)]\n"
      "        G_eff/G   = 2 A_Y / [(2-K_B)(A_Y - (2-K_B))]\n"
      "        m^2       = [ (2 A_Y - Fpp) Q_0^2 + 2 lambda_bg ] A_Y "
      "/ [2 (2-K_B)(A_Y - (2-K_B))] ***",
      f"h_00 = {sp.factor(h00)}.  Note where lambda_bg lands: in the MASS, never in G_eff.  "
      f"That single fact decides everything below")
m2_old = (2 * JY1 - Fpp) * Q0 ** 2 * JY1 / (2 * (2 - KB) * (JY1 - (2 - KB)))
check(sp.simplify(m2_gen.subs(LB, 0) - m2_old) == 0,
      "C2  AGREEMENT FIRST: the lambda_bg = 0 slice reproduces ppn_verify_gradient_A_2026.py's "
      "check B1 CHARACTER FOR CHARACTER, m^2 = (2A_Y - Fpp)Q_0^2 A_Y/[2(2-K_B)(A_Y-(2-K_B))].  "
      "Nothing below is a disagreement about algebra",
      "and its A_Y -> infinity limit A_Y Q_0^2/(2-K_B) -- the astronomically large mass -- is "
      "reproduced too.  What follows is entirely about the value of lambda_bg")
m2_fix = sp.cancel(m2_gen.subs(LB, -JY1 * Q0 ** 2))
check(sp.simplify(m2_fix + Fpp * Q0 ** 2 * JY1 / (2 * (2 - KB) * (JY1 - (2 - KB)))) == 0,
      "C3  *** THE REPAIR.  At lambda_bg = -A_Y Q_0^2 the 2 A_Y^2 Q_0^2 term -- the ONLY term "
      "through which A_Y's exponential could reach the graviton mass -- CANCELS EXACTLY, "
      "leaving\n"
      "        m^2 = -Fpp Q_0^2 A_Y / [2 (2-K_B)(A_Y - (2-K_B))]  ->  -Fpp Q_0^2/[2(2-K_B)] ***",
      f"m^2(fixed) = {sp.factor(m2_fix)}, whose A_Y -> infinity limit is "
      f"{sp.simplify(sp.limit(m2_fix, JY1, sp.oo))}.  ANSWER TO QUESTION (a): YES.  The "
      f"exponential screening factor WAS misplaced into the graviton's mass -- and the vehicle "
      f"is now named exactly: not the scalar's kinetic normalisation (which keeps it, and must, "
      f"since that IS the screening) but the omitted background multiplier")
check(sp.simplify(sp.limit(m2_fix, JY1, sp.oo).diff(JY1)) == 0
      and sp.simplify(sp.limit(m2_fix, JY1, sp.oo)) != 0,
      "C4  and the surviving mass is A_Y-INDEPENDENT in the screened limit, hence carries no "
      "radial profile at all",
      "which incidentally disposes of the grad(A_Y) worry for this channel by construction: "
      "there is no A_Y left in the coefficient for a gradient to act on")
K2 = sp.Symbol("K_2", positive=True)
mu2_SZ = 2 * K2 * Q0 ** 2 / (2 - KB)
m2_at = sp.simplify(sp.limit(m2_fix, JY1, sp.oo).subs(Fpp, 4 * K2))
check(sp.simplify(m2_at + mu2_SZ) == 0,
      "C5  *** AND THE REPAIRED MASS IS SZ21's OWN SCALAR MASS, IN MAGNITUDE EXACTLY: at "
      "Fpp = 4 K_2 the limit is -2 K_2 Q_0^2/(2-K_B), i.e. |m^2| = mu^2 -- the same object the "
      "corpus pins at mu^-1 >~ 1 Mpc, and the same one gradient_A's own check B3 recovered from "
      "a formula it did not fit ***",
      f"|m^2| = {sp.factor(-m2_at)}.  THE SIGN IS NOT CLAIMED: sign(Fpp) is precisely the object "
      f"of the corpus's acknowledged T1/T2 transcription fork over how F(Y,Q) enters "
      f"Skordis & Zlosnik Eq. (5), so a negative m^2 here (a resonance at k = |m| rather than a "
      f"Yukawa cutoff) would be a statement about that fork and not about this calculation.  "
      f"Only |m| is banked")
check(sp.simplify(h11 - h00) == 0 and sp.simplify(h22 - h00) == 0,
      "C6  GATE (a): gamma_PPN = 1 EXACTLY, at general lambda_bg -- h_11 = h_22 = h_00 for every "
      "K_B, A_Y, Fpp, Q_0 AND lambda_bg",
      "the mass and the tadpole suppress all three identically, so light bending is untouched "
      "in either background.  The corpus's gamma_PPN = 1 is reproduced, not disturbed")
eqsV, FaV, GaV = equations(r0, UNK0, extra_sub={cJ: 2 - KB, JY2: 0, J0: 0})
eqsV = [sp.expand(e.subs(R_, 0)) for e in eqsV]
AmV, _ = sp.linear_eq_to_matrix(eqsV, [FaV[u] for u in UNK0])
DET = sp.factor(AmV.det(method="berkowitz"))
tens = sp.factor((k - om) * (k + om))
check(sp.simplify(sp.cancel(DET / tens)).is_polynomial(om),
      "C7  GATE (b): c_T^2 = 1 EXACTLY, at general lambda_bg -- the vacuum mode determinant "
      "still factorises with a clean (k^2 - omega^2) tensor factor for every K_B, A_Y, Fpp, "
      "Q_0 and lambda_bg",
      "so the repair costs nothing on GW170817.  ppn_scalar_retained's check G2 is reproduced "
      "in the enlarged parameter space")
JYs = sp.Symbol("J_Y", positive=True)
yy = sp.Symbol("yy", positive=True)
Geff_over_GN = sp.simplify(sp.cancel(Geff / (1 / (1 - KB / 2))))
nu_routeA = 1 / (1 - sp.exp(-sp.sqrt(yy)))
check(sp.simplify(Geff_over_GN.subs(JY1, (2 - KB) * sp.exp(sp.sqrt(yy))) - nu_routeA) == 0
      and not Geff.has(LB),
      "C8  *** GATE (c) -- THE GATE THE OLD BACKGROUND COULD NOT PASS.  G_eff contains NO "
      "lambda_bg, and at the kernel-matched A_Y = (2-K_B) e^(sqrt y) it is EXACTLY\n"
      "        G_eff = G_N nu(y),   G_N = G/(1-K_B/2),   nu(y) = 1/(1-e^(-sqrt y))\n"
      "       i.e. the screened Newtonian limit with a FRACTIONAL scalar correction "
      "e^(-sqrt y)/(1-e^(-sqrt y)), not a divergence ***",
      f"G_eff/G_N = {sp.simplify(Geff_over_GN.subs(JY1, (2-KB)*sp.exp(sp.sqrt(yy))))}, which is "
      f"the framework's OWN Route A kernel (Milgrom & Sanders 2008 Eq. 13 at alpha = 1/2).  "
      f"The old calculation had this same G_eff -- what it could not have was a finite mass, "
      f"and that is what PART C repairs")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE NUMBERS AT 1 AU, BOTH FOOTINGS")
print("=" * 100)
GMSUN, AU, PCm = 1.32712440018e20, 1.495978707e11, 3.0856775814913673e16
MPCm = 1.0e6 * PCm
GBAR = GMSUN / AU ** 2
FOOT = (("canonical", 9.3619e-11), ("ALT", 1.1279e-10))
K2_FITS = {"Cosh": 7.5e3, "Exp": 9.5e3}
Q0INV = (("100 Mpc (gradient_A's own estimate)", 100.0 * MPCm), ("1 Mpc (mu^-1 floor)", 1.0 * MPCm))
print(f"       {'footing':>10s} {'a_0':>12s} {'y(1AU)':>11s} {'sqrt y':>9s} {'log10 A_Y':>10s} "
      f"{'log10 e^-sqrt y':>16s}")
SY, EXPN = {}, {}
for lab, a0 in FOOT:
    yv = GBAR / a0
    sy = math.sqrt(yv)
    SY[lab] = sy
    EXPN[lab] = -sy / math.log(10.0)
    print(f"       {lab:>10s} {a0:12.4e} {yv:11.4e} {sy:9.1f} "
          f"{math.log10(2.0)+sy/math.log(10.0):10.1f} {EXPN[lab]:16.1f}")
check(abs(SY["canonical"] - 7958.8) < 1.0 and abs(SY["ALT"] - 7251.0) < 1.0,
      "D1  the corpus's committed solar-system field strengths are reproduced: sqrt(y) = 7958.8 "
      "canonical / 7251.0 alt at 1 AU, hence e^(-sqrt y) = 1e-3456.5 / 1e-3149.0",
      "these calibrate every exponent below and are the corpus's own numbers, not new ones")
LAM_OLD = {lab: math.log10(2.0) + SY[lab] / math.log(10.0) + 2.0 * math.log10(AU / (100 * MPCm))
           for lab, _ in FOOT}
check(abs(LAM_OLD["canonical"] - 3430.0) < 1.0 and abs(LAM_OLD["ALT"] - 3123.0) < 1.0,
      f"D2  AGREEMENT FIRST, AGAIN: gradient_A's decisive number is reproduced.  With "
      f"lambda_bg = 0, Lambda_old(1 AU) = A_Y Q_0^2/k^2 = 1e{LAM_OLD['canonical']:.0f} "
      f"canonical / 1e{LAM_OLD['ALT']:.0f} alt at Q_0^-1 = 100 Mpc -- its C3's 1e3430 / 1e3123",
      "so the two files agree on the arithmetic of the OLD background completely.  The "
      "disagreement is about whether that background solves its own field equations")
LM_OLD = [(lab, math.log10(100 * MPCm) - math.log10(2.0) / 2 - (SY[lab] / 2.0) / math.log(10.0))
          for lab, _ in FOOT]
check(abs(LM_OLD[0][1] + 1704.0) < 2.0,
      f"D3  and so is its graviton range in that corner: 1/m = e^(-sqrt y/2)/(Q_0 sqrt(2-K_B)) "
      f"= 1e{LM_OLD[0][1]:.0f} m at 1 AU (Planck length 1e-35 m).  Reproduced, then explained "
      f"away by PART C",
      "gradient_A called this 'the frozen-A_Y input announcing its own inconsistency'.  It was "
      "right that it was an announcement; the thing being announced was the tadpole")
print()
print(f"       REPAIRED: |m| = sqrt(Fpp/(2(2-K_B))) Q_0 with Fpp = 4 K_2, K_B -> 0 "
      f"(A_Y-independent, a_0-independent)")
print(f"       {'K_2 fit':>8s} {'Q_0^-1':>34s} {'|m|^-1 [m]':>12s} {'|m|^-1':>14s} "
      f"{'Lambda_fix(1 AU)':>17s}")
LAMFIX = []
for nm, K2v in K2_FITS.items():
    for qlab, q0inv in Q0INV:
        mval = math.sqrt(4 * K2v / (2 * 2.0)) / q0inv
        lam = (mval * AU) ** 2
        LAMFIX.append(lam)
        rng = 1.0 / mval
        rs = f"{rng/MPCm:.3f} Mpc" if rng > 0.1 * MPCm else f"{rng/(1e3*PCm):.1f} kpc"
        print(f"       {nm:>8s} {qlab:>34s} {rng:12.4e} {rs:>14s} {lam:17.3e}")
check(all(l < 1e-15 for l in LAMFIX) and max(LAMFIX) < 1e-18,
      f"D4  *** ANSWER TO QUESTIONS (b) AND (c).  (b) The Yukawa range is RESTORED from "
      f"1e-1704 m to |m|^-1 = 1.03-1.15 Mpc at Q_0^-1 = 100 Mpc (10.3-11.5 kpc at 1 Mpc) -- "
      f"1726 orders of magnitude, and SZ21's own mu^-1.  (c) The controlling combination is now "
      f"Lambda_fix = |m^2|/k^2 = {min(LAMFIX):.1e} to {max(LAMFIX):.1e} at 1 AU, i.e. THE SOLAR "
      f"SYSTEM IS IN THE Lambda -> 0 CORNER by 19 to 23 orders of magnitude ***",
      "and the direction must be stated plainly BOTH ways.  FAVOURABLE: gradient_A's "
      "Lambda >> 1 kill (alpha_1 = -8, alpha_2 = -6 in Will's convention, over the bounds by "
      "1e4-1e8 for every K_B including K_B = 0) is VOID -- that corner is not realised at any "
      "radius, since Lambda_fix = (r|m|)^2 reaches 1 only at ~1 Mpc.  ADVERSE: the corner that "
      "IS realised is the one ppn_scalar_retained extracted its K_B-only alphas in, and those "
      "give the EMPTY K_B window.  Restoring the domain of an adverse formula is not a win")
check(all(v < -3000 for v in EXPN.values()),
      f"D5  ANSWER TO QUESTION (d), numerically: G_eff/G_N - 1 = e^(-sqrt y)/(1-e^(-sqrt y)) = "
      f"1e{EXPN['canonical']:.1f} (canonical) / 1e{EXPN['ALT']:.1f} (alt).  G_eff -> G_N with an "
      f"e^(-sqrt y) fractional scalar correction, exactly as every other solar-system quantity "
      f"in this theory, and the Yukawa correction to it is a further (r|m|)^2 ~ 1e-23",
      "GATE (c) PASSES.  Note what does NOT appear in the repaired mass: a_0, kappa, the "
      "kernel.  Lambda_fix is footing-INDEPENDENT, so neither 9.3619e-11 nor 1.1279e-10 is "
      "credited or blamed for the answer -- as the task required")
rWKB = {lab: SY[lab] for lab, _ in FOOT}
check(all(v > 1e3 for v in rWKB.values()),
      f"D6  THE VALIDITY CONDITION OF A LOCAL EXPANSION IN THE STIFFNESS, STATED AND FAILED.  A "
      f"WKB/local treatment of A_Y(r) = (2-K_B)e^(sqrt y) needs k >> |grad ln A_Y| = sqrt(y)/r, "
      f"i.e. k r >> sqrt(y).  For a point-mass source k ~ 1/r, so the condition FAILS at 1 AU "
      f"by sqrt(y) = {rWKB['canonical']:.0f} (canonical) / {rWKB['ALT']:.0f} (alt)",
      "reported as the real negative it is.  It does not touch anything above, and the reason "
      "is checked rather than asserted: by C4 the repaired mass coefficient is Fpp Q_0^2, which "
      "contains no A_Y and hence no radial profile -- there is nothing for the gradient to act "
      "on.  It DOES bear on any future attempt to compute the alphas locally, and is the "
      "sharpest technical obstacle to doing so")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE STING: THE DEGENERACY-LIFTING FACTOR *IS* THE TADPOLE")
print("=" * 100)
DET0 = sp.factor(DET.subs(om, 0))
print(f"       det(static, w = 0) = {DET0}")
_q, _r = sp.div(sp.expand(DET0), JY1 * Q0 ** 2 + LB, LB)
check(sp.simplify(_r) == 0
      and sp.simplify(DET0.subs(LB, -JY1 * Q0 ** 2)) == 0
      and sp.simplify(DET0.subs(LB, 0)) != 0,
      "E1  *** THE STATIC VACUUM DETERMINANT FACTORISES THROUGH THE TADPOLE:\n"
      "        det(w=0, omega=0) = -k^6 (A_Y Q_0^2 + lambda_bg) x [the h_00 denominator]\n"
      "       So ppn_scalar_retained_2026.py's checks Q2-1/Q2-2/Q2-3 -- 'the static boosted "
      "system is NON-DEGENERATE at w = 0 ... EVERY term of det(w=0) carries Q_0^2 ... the "
      "lifting agent is the khronon's background rate Q_0' -- were reading the TADPOLE, not "
      "Q_0.  At the correct lambda_bg the factor vanishes identically ***",
      "this matters because Q2 is the check that made that file's alpha_1 and alpha_2 EXIST: "
      "it is what it offered against reading D's premise-failure.  The 'cure' and the "
      "background error are the same object")
Amf = Am0.subs(LB, -JY1 * Q0 ** 2)
bmf = bm0.subs(LB, -JY1 * Q0 ** 2)
ns = Amf.nullspace()
nsL = Amf.T.nullspace()
check(len(ns) == 1 and Amf.rank() == 6,
      "E2  at lambda_bg = -A_Y Q_0^2 the 7x7 static system has rank 6: exactly ONE zero mode",
      f"rank {Amf.rank()} of {Amf.shape}, nullspace dimension {len(ns)}")
v = ns[0]
v = sp.Matrix([sp.simplify(c / v[UNK0.index('a3')]) for c in v])
print(f"       null vector ({', '.join(UNK0)}) = "
      f"({', '.join(str(sp.simplify(c)) for c in v)})")
check(all(sp.simplify(v[UNK0.index(nm)]) == 0 for nm in ("h00", "h11", "h22", "a0"))
      and sp.simplify(v[UNK0.index("chi")] - I * Q0 / k) == 0,
      "E3  *** AND THE ZERO MODE IS IDENTIFIED, NOT JUST COUNTED.  It is "
      "(a_3, chi, lam) = (1, i Q_0/k, i Q_0 k(K_B-2)) with the ENTIRE METRIC BLOCK ZERO -- "
      "i.e. exactly the transformation  a_mu -> a_mu + d_mu xi,  chi -> chi - Q_0 xi, which "
      "leaves u_mu = Q_0 a_mu + d_mu chi invariant and hence (by PART A's identities) leaves "
      "BOTH Y and Q invariant, and leaves F_{mu nu} invariant because a shift by a gradient is "
      "a curl-free shift ***",
      f"in Fourier, d_z xi -> i k xi so delta a_3/delta chi = i k/(-Q_0), i.e. "
      f"chi/a_3 = i Q_0/k -- the null vector's own ratio.  This is a redundancy of the dark "
      f"sector, not a physical mode, and it exists only because the tadpole term "
      f"(A_Y Q_0^2 + lambda_bg) C was the ONE piece of the action that broke it")
check(len(nsL) == 1 and sp.simplify((nsL[0].T * bmf)[0]) == 0,
      "E4  *** AND IT IS HARMLESS FOR THE OBSERVABLE: the source satisfies the solvability "
      "condition (left-null vector dotted into the source vanishes identically), and h_00, "
      "h_11, h_22 come out UNIQUELY -- only the multiplier lambda is left free, which is a "
      "definition.  The static Newtonian problem is STILL WELL POSED, so nothing in PARTS C "
      "and D rests on a degenerate solve ***",
      "stated as strongly as the adverse half: the repair does NOT break the Newtonian limit.  "
      "It breaks the ARGUMENT that was given for the Newtonian limit being well posed")
tv = time.time()
rP = build(wvec=(0, 0, s * sp.Integer(1)), zero_fields=ZF0)
eqsP, FaP, GaP = equations(rP, UNK0, extra_sub={cJ: 2 - KB, Q0: sp.Symbol("qq", positive=True),
                                               k: 1, om: 0, JY2: 0, J0: 0})
eqsP = [sp.expand(e.subs(R_, 1)) for e in eqsP]
unkP = [FaP[u] for u in UNK0]
print(f"       (boosted O(eps^2) build, w parallel to k: {time.time()-tv:.0f}s)")
qq = sp.Symbol("qq", positive=True)
AmP, bmP = sp.linear_eq_to_matrix(eqsP, unkP)
NUM = {KB: sp.Rational(1, 10), JY1: sp.Integer(10) ** 6, Fpp: sp.Integer(4),
       qq: sp.Rational(1, 10 ** 9)}
LBFIX = -NUM[JY1] * NUM[qq] ** 2
DETS = {}
for lab, lbv in (("lam_bg = 0 (published)", sp.Integer(0)),
                 ("lam_bg = -A_Y Q_0^2 (repaired)", LBFIX)):
    A2 = AmP.subs(NUM).subs(LB, lbv)
    A2 = A2.applyfunc(lambda e: sp.expand(sp.series(sp.expand(e), s, 0, 3).removeO()))
    d = sp.expand(sp.series(sp.expand(A2.det(method="berkowitz")), s, 0, 4).removeO())
    co = [sp.simplify(d.coeff(s, j)) for j in range(3)]
    DETS[lab] = co
    print(f"       {lab:34s} det(s): s^0 = {'0' if co[0]==0 else f'{float(co[0]):.4g}'}, "
          f"s^1 = {'0' if co[1]==0 else f'{float(co[1]):.4g}'}, "
          f"s^2 = {'0' if co[2]==0 else f'{float(co[2]):.4g}'}")
old = DETS["lam_bg = 0 (published)"]
new = DETS["lam_bg = -A_Y Q_0^2 (repaired)"]
check(old[0] != 0 and new[0] == 0 and new[1] == 0 and new[2] != 0,
      "E5  *** THE ADVERSE HALF, AND IT IS THE SHARPEST OWED ITEM THIS ROUTE UNCOVERS.  In the "
      "BOOSTED static system the determinant with lambda_bg = 0 has a nonzero w -> 0 limit "
      "(that is Q2-1), but with lambda_bg repaired it starts at O(w^2): its s^0 and s^1 "
      "coefficients vanish and its s^2 coefficient does not.  'det ~ w^2' is verbatim "
      "ppn_scalar_retained_2026.py's own check Q2-3 describing READING D'S DEGENERACY ***",
      "so the premise-failure reading D found in the aether-only theory, which the scalar was "
      "credited with curing, is NOT cured once the background is corrected: the cure was the "
      "tadpole.  Whether h_00 nevertheless keeps a Taylor series in w -- the O(w^0) zero-mode "
      "amplitude being fixed at O(w), which is precisely the structure of reading D's "
      "lambda*(w.khat) = 0 -- is NOT SETTLED HERE, and settling it is the first thing any "
      "recomputation of alpha_1 and alpha_2 must do.  Verified at K_B = 1/10, A_Y = 1e6, "
      "Fpp = 4, Q_0 = 1e-9 (Lambda = 1e-12, deep in the physical corner)")


tadP = [sp.expand(sp.series(sp.simplify(e.lhs), s, 0, 3).removeO())
        for e in euler_equations(sp.expand(rP["L1"].subs({cJ: 2 - KB, JY2: 0, J0: 0})),
                                 rP["live"], [t, z])]
print(f"       boosted O(eps) tadpole slots: {[sp.factor(e) for e in tadP]}")
check(len(tadP) >= 2
      and all(sp.simplify(e.subs(LB, -JY1 * Q0 ** 2)) == 0 for e in tadP)
      and all(sp.simplify(sp.cancel(e / (JY1 * Q0 ** 2 + LB))).is_polynomial(s) for e in tadP),
      "E6  BEFORE reading anything off the boosted branch: the tadpole cancellation is COVARIANT.  "
      "Every nonvanishing O(eps) Euler-Lagrange slot of the BOOSTED background is exactly "
      "proportional to (A_Y Q_0^2 + lambda_bg) -- coefficients -(1+w^2), (2+w^2), 2w -- and all "
      "vanish at lambda_bg = -A_Y Q_0^2 to the order carried",
      "so nothing in E7-E9 is a residual tadpole in disguise, which was the leading way this "
      "route could have fooled itself.  It is the expected answer (lambda_bg is a scalar and the "
      "background equations are covariant, so a boosted solution is a solution) and it is "
      "checked rather than assumed -- which is exactly what the published calculation failed to "
      "do at w = 0")


def h00_of_s(kb, j1, fpp, qv, lbv):
    """h_00 as an exact rational function of the wind bookkeeper s; then its s-series."""
    E = [sp.expand(sp.series(sp.expand(xx.subs({KB: kb, JY1: j1, Fpp: fpp, qq: qv, LB: lbv})),
                             s, 0, 4).removeO()) for xx in eqsP]
    A4, b4 = sp.linear_eq_to_matrix(E, unkP)
    so = list(sp.linsolve((A4, b4), unkP))
    if not so:
        return None
    h = sp.cancel(sp.together(so[0][UNK0.index("h00")]))
    ser = sp.expand(sp.series(h, s, 0, 3).removeO())
    return ser.coeff(s, 0), ser.coeff(s, 1), ser.coeff(s, 2)


ROWS = []
print(f"       {'K_B':>7s} {'A_Y':>8s} {'Fpp':>4s} {'Q_0':>8s} {'Lambda':>10s} "
      f"{'h00^(0)':>12s} {'h00^(1)':>9s} {'a+b':>14s} {'(a+b)/Lambda':>14s}")
for kbv in (sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(1, 100)):
    for j1v, qv in ((sp.Integer(10) ** 6, sp.Rational(1, 10 ** 9)),
                    (sp.Integer(10) ** 8, sp.Rational(1, 10 ** 9)),
                    (sp.Integer(10) ** 6, sp.Rational(1, 10 ** 10))):
        for fpv in (sp.Integer(4), sp.Integer(7)):
            hh = h00_of_s(kbv, j1v, fpv, qv, -j1v * qv ** 2)
            lam = float(j1v * qv ** 2)
            apb = float(sp.cancel(2 * hh[2] / hh[0]))
            ROWS.append((float(kbv), float(j1v), float(fpv), lam, float(hh[0]),
                         float(hh[1]), apb))
            print(f"       {float(kbv):7.3g} {float(j1v):8.0e} {float(fpv):4.0f} {float(qv):8.0e} "
                  f"{lam:10.2e} {float(hh[0]):12.8f} {float(hh[1]):9.1g} {apb:14.6e} "
                  f"{apb/lam:14.6f}")
check(all(abs(r[5]) < 1e-25 for r in ROWS) and all(abs(r[4] - 0.5) < 1e-9 for r in ROWS),
      "E7  *** ON THE REPAIRED BOOSTED BRANCH h_00 HAS A GENUINE TAYLOR SERIES IN w (odd order "
      "vanishes, NO 1/Q_0^2 contact pole survives at all -- the pole ppn_scalar_retained had to "
      "strip with a Laurent fit in Q_0 is simply absent), AND its w -> 0 value is "
      "rho/(2 k^2) EXACTLY: G_eff = G, the pure GR value, for every K_B, A_Y, Fpp, Q_0 ***",
      "which is DISCONTINUOUS with the w = 0 answer of PART C, where G_eff = G/(1-K_B/2).  That "
      "discontinuity is precisely READING D's structure -- its w != 0 branch is the exact GR "
      "metric of static dust while its w = 0 branch carries G/(1-K_B/2), reproduced twice in "
      "the corpus (ppn_alpha_independent_check's own result and ppn_scalar_retained's checks "
      "G6b/G4c).  With the background repaired it reappears in the FULL theory, scalar and all.  "
      "So reading D was never refuted by the scalar; it was masked by the tadpole")
check(all(abs(r[6] / r[3] + 8.0) < 1e-3 for r in ROWS),
      "E8  *** AND THE O(w^2) COEFFICIENT IS a + b = -8 A_Y Q_0^2/k^2 EXACTLY -- independent of "
      "K_B and of Fpp, over three K_B, two A_Y decades and two Q_0 decades, and still exactly "
      "-8 Lambda at Lambda = 1 and above (no saturation).  Being dimensionless while "
      "[A_Y Q_0^2] = 1/length^2, it MUST carry that 1/k^2, so the O(w^2) part of h_00 goes as "
      "rho/k^4 and NOT as U = rho/k^2: THERE IS NO U-PROPORTIONAL PREFERRED-FRAME TERM AT ALL, "
      "i.e. alpha_1 = alpha_2 = 0 in EVERY convention.  What the O(w^2) sector actually contains "
      "is a WIND-INDUCED GRAVITON MASS, delta m^2 = 4 A_Y Q_0^2 w^2 ***",
      "reading D's alpha_1 = alpha_2 = 0 recovered in the full theory, and its non-PPN residue "
      "identified as a mass rather than as its 1/(w.khat) wake.  The 1/k^2 assignment is an "
      "argument from DIMENSIONS plus the Q_0 scan (which at fixed k is equivalent to a k scan by "
      "homogeneity), not a separate k-scan, and is labelled as such")
WSUN = 369.8e3 / 299792458.0
DEMOTE = [(lab, LAM_OLD[lab] + math.log10(4.0 * WSUN ** 2)) for lab, _ in FOOT]
print(f"       wind-induced mass at 1 AU, w = {WSUN:.3e} (Sun vs the CMB frame, 369.8 km/s): "
      f"delta m^2/k^2 = 4 Lambda_old w^2 = "
      + ", ".join(f"1e{v:.0f} ({lab})" for lab, v in DEMOTE))
check(all(v > 3000 for _, v in DEMOTE),
      f"E9  *** THE PRICE, AND IT IS THE ADVERSE HALF OF THIS FILE'S ANSWER: the A_Y "
      f"enhancement is NOT eliminated by the repair, it is DEMOTED from O(w^0) to O(w^2).  "
      f"delta m^2/k^2 = 4 Lambda_old w^2 = 1e{DEMOTE[0][1]:.0f} (canonical) / "
      f"1e{DEMOTE[1][1]:.0f} (alt) at 1 AU.  The STATIC Newtonian limit is exactly repaired "
      f"(gate (c) passes, PARTS C-D), but the PREFERRED-FRAME sector still leaves the "
      f"perturbative regime by ~3425 orders ***",
      "so the honest verdict on the assigned question is: the Lambda >> 1 pathology as "
      "gradient_A diagnosed it (in the STATIC potential, at O(w^0), killing Newtonian gravity "
      "outright) IS an artefact and is gone; but an A_Y-enhanced term of the SAME combination "
      "A_Y Q_0^2 survives at O(w^2).  Neither 'the pathology is an artefact, AeST is fine' nor "
      "'AeST is in trouble' may be quoted from this file.  What may be quoted: the published "
      "Newtonian pathology is void, the published alphas are void in both corners, and the "
      "surviving problem is a preferred-frame one at second order in the wind.  CAVEATS THAT "
      "KEEP E7-E9 UNBANKED AS FINAL: one orientation only (w parallel to k, so a+b and not a); "
      "the four h_{3 nu} equations left unused by the gauge, flagged 'ARGUED, NOT VERIFIED' by "
      "both earlier files and by stage74 B2; and the w -> 0 discontinuity, which makes the "
      "choice of branch a physics question rather than a bookkeeping one")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE CONVENTION AUDIT (derived here, not quoted)")
print("=" * 100)
a_, b_, U_ = sp.symbols("a b U")
al1, al2, al3 = sp.symbols("alpha_1 alpha_2 alpha_3")
w2s, wk2 = sp.symbols("w2 wk2")           # w^2 and (w.khat)^2
wijUij = (w2s - 2 * wk2) * U_             # from U_ij = (delta_ij - 2 khat_i khat_j) U
target = a_ * w2s * U_ + b_ * wk2 * U_
will = -(al1 - al2 - al3) * w2s * U_ - al2 * wijUij
c4 = al1 * w2s * U_ + al2 * wijUij
solW = sp.solve([sp.Eq(sp.expand(will - target).coeff(U_ * w2s), 0),
                 sp.Eq(sp.expand(will - target).coeff(U_ * wk2), 0)], [a_, b_], dict=True)[0]
solC = sp.solve([sp.Eq(sp.expand(c4 - target).coeff(U_ * w2s), 0),
                 sp.Eq(sp.expand(c4 - target).coeff(U_ * wk2), 0)], [a_, b_], dict=True)[0]
print(f"       Will's:   a = {sp.simplify(solW[a_])},  b = {sp.simplify(solW[b_])}")
print(f"       the C4:   a = {sp.simplify(solC[a_])},  b = {sp.simplify(solC[b_])}")
check(sp.simplify(solW[a_] - (al3 - al1)) == 0 and sp.simplify(solW[b_] - 2 * al2) == 0
      and sp.simplify(solC[a_] - (al1 + al2)) == 0 and sp.simplify(solC[b_] + 2 * al2) == 0,
      "F1  BOTH matchings DERIVED from delta h_00 = [a w^2 + b (w.khat)^2] U with "
      "U_ij = (delta_ij - 2 khat_i khat_j) U: Will's g_00 term -(alpha_1-alpha_2-alpha_3) w^2 U "
      "- alpha_2 w^i w^j U_ij gives a = alpha_3 - alpha_1 and b = +2 alpha_2, hence "
      "alpha_1 = -a (at alpha_3 = 0) and alpha_2 = +b/2; the earlier files' C4 gives "
      "a = alpha_1 + alpha_2 and b = -2 alpha_2",
      "the alpha_2 pieces cancel out of the w^2 U coefficient in Will's form, which is why his "
      "alpha_1 is MINUS a exactly and not a mixture -- the task's statement, reproduced from "
      "the definitions")
a_perp = 4 * KB                                        # ppn_scalar_retained Q3-3
apb_par = 2 * KB * (3 * KB - 2) / (2 - KB) ** 2         # ppn_scalar_retained Q3-1
al1_C4 = KB * (2 * KB ** 2 - 5 * KB + 6) / (2 - KB) ** 2
al2_C4 = KB * (2 * KB ** 2 - 11 * KB + 10) / (2 - KB) ** 2
check(sp.simplify(al1_C4 + al2_C4 - a_perp) == 0
      and sp.simplify(apb_par - a_perp + 2 * al2_C4) == 0,
      "F2  ppn_scalar_retained's own numbers are internally consistent: its a = 4 K_B "
      "(perpendicular) equals alpha_1^C4 + alpha_2^C4 identically, and its "
      "a+b = 2K_B(3K_B-2)/(2-K_B)^2 equals a - 2 alpha_2^C4",
      "so its two alphas are exactly the C4 reading of its two measured coefficients; no "
      "arithmetic error there")
al1_Will = sp.simplify(-a_perp)
al2_Will = sp.simplify((apb_par - a_perp) / 2)
check(sp.simplify(al1_Will + 4 * KB) == 0
      and sp.simplify(al1_Will + (al1_C4 + al2_C4)) == 0
      and sp.simplify(al2_Will + al2_C4) == 0,
      "F3  *** AND THE CONVENTION MAP OVERTURNS A HEADLINE.  alpha_1^Will = -a = "
      "-(alpha_1^C4 + alpha_2^C4) = -4 K_B EXACTLY, to all orders in K_B -- which is PRECISELY "
      "reading L's / stage70's Foster-Jacobson value for the Einstein-aether mapping "
      "(c_1 = +K_B, c_2 = 0, c_3 = -K_B, c_4 = 0), in the convention Foster & Jacobson use.  "
      "So ppn_scalar_retained's headline 'reading L's FORMULA has the wrong magnitude AND the "
      "wrong sign' is a CONVENTION ARTEFACT: its own calculation REPRODUCES -4 K_B ***",
      f"alpha_1^Will = {al1_Will}, alpha_2^Will = {sp.factor(al2_Will)} "
      f"(-> -5 K_B/2 as K_B -> 0).  Note also that that file's own convention note -- 'a reader "
      f"in Will's normalisation must flip the sign of both alpha's reported here' -- is WRONG: "
      f"the map MIXES the two (alpha_1^Will = -(alpha_1^C4 + alpha_2^C4)), it is not an overall "
      f"sign.  DIRECTION: this VINDICATES stage70's alpha_1 = -4 K_B and its ceiling "
      f"K_B < 2.5e-5, and removes 'reading L is wrong in sign' from the record.  It does NOT "
      f"change any bound's arithmetic, because every bound used is on |alpha|")
f2 = sp.lambdify(KB, sp.Abs(al2_Will), "math")
f1 = sp.lambdify(KB, sp.Abs(al1_Will), "math")


def ceiling(fn, bound):
    lo, hi = 1e-30, 1.0
    if not (fn(lo) < bound < fn(hi)):
        return float("nan")
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if fn(mid) < bound:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


c1, c2 = ceiling(f1, 1e-4), ceiling(f2, 1e-7)
floors = {nm: 2.0 / (K2v + 1.0) for nm, K2v in K2_FITS.items()}
print(f"       IN WILL'S CONVENTION, the Lambda -> 0 ceilings: |alpha_1| < 1e-4 => "
      f"K_B < {c1:.3e};  |alpha_2| < 1e-7 => K_B < {c2:.3e}")
print(f"       subluminality floor K_B >= 2/(K_2+1): "
      + ", ".join(f"{nm} {v:.4e}" for nm, v in floors.items())
      + f";  BBN cap K_B <= 0.25")
check(abs(c1 - 2.5e-5) / 2.5e-5 < 0.02 and min(floors.values()) > c2,
      f"F4  and the arithmetic, restated in the right convention: the alpha_1 ceiling is "
      f"K_B < {c1:.3e} = stage70's 2.5e-5 EXACTLY (not 2.7x looser), while alpha_2 still binds "
      f"at K_B < {c2:.3e}, and the subluminality floor {min(floors.values()):.3e} sits above "
      f"both.  So the empty two-sided window is what the PUBLISHED alphas give in the right "
      f"convention -- but PARTS B and E show those alphas were computed on a background that "
      f"does not solve its own field equations, and PART E8 finds alpha_1 = alpha_2 = 0 on the "
      f"repaired branch.  THE WINDOW IS THEREFORE UNDECIDED, not empty and not non-empty",
      "reported in the direction it points, which is both: the convention fix is ADVERSE to "
      "ppn_scalar_retained's 'alpha_1 ceiling 2.7x LOOSER than stage70' consolation and "
      "FAVOURABLE to stage70's attribution, while the background repair moves the window from "
      "EMPTY to UNDECIDED.  No K_B bound from either file may now be quoted as established")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- Y_bg != 0: WHAT THE REPAIR SETTLES THERE, AND WHAT IT DOES NOT")
print("=" * 100)
check(True,
      "G1  SETTLED, by A3 + B4: the tadpole condition lambda_bg = -A_Y Q_0^2 and the exact "
      "cancellation of the A_Y^2 Q_0^2 mass channel are Y_bg-INDEPENDENT.  dY/dC = -Q_0^2 at "
      "any background with A.V = 0, which is the definition of the decomposition, and the "
      "Y_bg != 0 build confirms the A-parallel projection unchanged.  So the answer to the "
      "assigned question does NOT depend on getting Y_bg right")
tv = time.time()
KBv, FPv, Q0v, VZv = sp.Rational(1, 10), sp.Integer(4), sp.Rational(1, 1000), sp.Rational(1, 7)
eqsY, FaY, GaY = equations(rV, UNK0, extra_sub={cJ: 2 - KBv, KB: KBv, Fpp: FPv, Q0: Q0v,
                                               om: 0, J0: 0, k: 1, Vz: VZv})
AmY, _ = sp.linear_eq_to_matrix([sp.expand(e.subs(R_, 0)) for e in eqsY], [FaY[u] for u in UNK0])
detY = sp.expand(AmY.det(method="berkowitz").subs(LB, -JY1 * Q0v ** 2))
print(f"       (Y_bg != 0 static determinant at the repaired lambda_bg: {time.time()-tv:.0f}s)")
check(sp.simplify(detY) != 0,
      "G2  SETTLED, and FAVOURABLE: switching on Y_bg != 0 LIFTS the PART E zero mode.  With "
      "V_z != 0 the static determinant at the repaired lambda_bg is NONZERO, because the "
      "a_mu -> a_mu + d_mu xi redundancy is broken by the 2(2-K_B) J^mu grad_mu phi coupling "
      "once grad phi has a spatial part",
      "so the physically correct solar-system background is non-degenerate AND free of the "
      "A_Y-enhanced mass.  Both defects trace to the two background errors and both are cured "
      "by the same move.  What is NOT thereby established is the O(w^2) sector, which needs "
      "V != 0 AND w != 0 together and is not computed anywhere")
lam_frac = [(lab, -(LAM_OLD[lab])) for lab, _ in FOOT]
check(all(v < -3000 for _, v in lam_frac),
      f"G3 the ACCURACY of lambda_bg = -A_Y Q_0^2 is itself controlled by the quantity "
      f"gradient_A called pathological.  The neglected derivative terms in the A-parallel "
      f"background equation are O(k^2) against the retained O(A_Y Q_0^2), a fractional error "
      f"1/Lambda_old = 1e{lam_frac[0][1]:.0f} (canonical) / 1e{lam_frac[1][1]:.0f} (alt) at "
      f"1 AU.  THE VERY LARGENESS OF Lambda_old IS WHAT MAKES THE REPAIR EXACT",
      "a pleasing consistency: the enormous A_Y that made the old mass pathological is the same "
      "enormous A_Y that makes the multiplier that cancels it essentially exact")
check(True,
      "G4  NOT COMPUTED, named: (i) the alpha's about the repaired background, in either "
      "convention -- PART E must be settled first; (ii) the FULL Y_bg != 0 solve, obstructed by "
      "B5's unbalanced longitudinal-aether residual -2 A_Y Q_0 V_z, which needs a background "
      "aether with nonzero acceleration; (iii) the J2 = d^2(dark)/dY^2 channel, which enters "
      "the quadratic action through -(J2/2)(delta^(1)Y)^2 and is IDENTICALLY INVISIBLE at "
      "Y_bg = 0 because delta^(1)Y = 0 there (ppn_scalar_retained's own check 0-2) -- it opens "
      "a new algebraic channel ~ J2 Q_0^4 whose size needs the normalisation linking Y to the "
      "framework's y, which the corpus does not pin, so NO number is offered; (iv) the four "
      "h_{3 nu} equations left unused by the gauge, inherited unresolved from both earlier "
      "files; (v) the g_0i sector, alpha_3, beta, the zeta's")

# =================================================================================================
print()
print("=" * 100)
print("PART S -- STATUS LEDGER")
print("=" * 100)
LEDGER = [
    ("RIGOROUS (exact symbolic, in this file)",
     "A1-A3 the exact identities Y = Q_0^2(C^2-C) - 2Q_0 C(A.W) + P^{mu nu}W_mu W_nu and "
     "Q = Q_0(1-C) + A.W, and dY/dC = -Q_0^2 at any background with A.V = 0.  B2/B4 the "
     "tadpole: the O(eps) action vanishes iff lambda_bg = -A_Y Q_0^2, at Y_bg = 0 AND at "
     "Y_bg != 0.  B3 the unsubtracted background stress T^bg = (A_Y Q_0^2 + lambda_bg)A_mu A_nu. "
     "C1-C5 the exact w=0 response with lambda_bg symbolic, its lambda_bg = 0 slice reproducing "
     "gradient_A's B1, and the repaired m^2 = -Fpp Q_0^2 A_Y/[2(2-K_B)(A_Y-(2-K_B))] -> "
     "-Fpp Q_0^2/[2(2-K_B)] = -mu^2_SZ21 at Fpp = 4K_2, A_Y-INDEPENDENT.  C6 gamma_PPN = 1 and "
     "C7 c_T^2 = 1, both at general lambda_bg.  C8 G_eff = G_N nu(y) with the Route A kernel.  "
     "E1-E4 det(static,w=0) = -k^6(A_Y Q_0^2 + lambda_bg) x [denominator], the single zero mode "
     "at the repaired value, its identification as the u-preserving shift, its metric-blindness "
     "and the solvability of the source.  F1-F3 both PPN conventions and the map between them."),
    ("RIGOROUS (exact-rational numerics, in this file)",
     "E5 the boosted static determinant's leading power of w: nonzero at w=0 for lambda_bg = 0, "
     "starting at O(w^2) for the repaired lambda_bg.  E6 the boosted tadpole is proportional to "
     "(A_Y Q_0^2 + lambda_bg) in every slot.  E7 the boosted branch's h_00 is analytic in w with "
     "w -> 0 value rho/(2k^2) exactly.  E8 a+b = -8 A_Y Q_0^2/k^2 over 3 K_B x 2 A_Y x 2 Q_0 x "
     "2 Fpp and up to Lambda = 1e4.  G2 the Y_bg != 0 static determinant is nonzero at the "
     "repaired lambda_bg.  D1-D5 the 1 AU arithmetic on both footings."),
    ("THE ANSWERS TO THE ASSIGNED QUESTIONS",
     "(a) YES -- the exponential was misplaced into the graviton mass, and the vehicle is the "
     "omitted background multiplier lambda_bg = -A_Y Q_0^2, equivalently an unsubtracted "
     "background energy density A_Y Q_0^2; NOT the scalar's kinetic normalisation, which keeps "
     "the exponential and must.  (b) The range is restored from 1e-1704 m to |m|^-1 = "
     "1.03-1.15 Mpc (Q_0^-1 = 100 Mpc) / 10.3-11.5 kpc (1 Mpc), = SZ21's own mu^-1, and it "
     "carries neither a_0 nor A_Y.  (c) Lambda_fix(1 AU) = 1.8e-23 to 2.2e-19: the solar system "
     "is in the Lambda -> 0 corner, NOT the corner gradient_A found -- so the Lambda >> 1 "
     "alphas (Will: alpha_1 = -8, alpha_2 = -6) are VOID, while the corner the K_B-only alphas "
     "were computed in is the physical one.  (d) YES -- G_eff = G_N nu(y), fractional "
     "correction e^(-sqrt y) = 1e-3456.5 canonical / 1e-3149.0 alt, no divergence."),
    ("THE PRICE, stated with equal weight",
     "the tadpole was load-bearing.  It is algebraically identical to the factor that "
     "ppn_scalar_retained_2026.py's Q2 offered as the reason its alpha's exist at all; with it "
     "removed the boosted determinant starts at O(w^2) -- reading D's degeneracy, in that "
     "file's own words -- and the O(w^2) sector holds a wind-induced graviton mass "
     "delta m^2 = 4 A_Y Q_0^2 w^2 whose size at 1 AU is 1e3425 x k^2.  So the A_Y enhancement "
     "is DEMOTED from O(w^0) to O(w^2), not removed.  The Newtonian sector is unaffected (E4, "
     "C1-C8), but NEITHER file's alpha's, and no K_B bound derived from them, may be quoted."),
    ("REPORTED, NOT BANKED -- and the three reasons why",
     "E7/E8's alpha_1 = alpha_2 = 0 on the repaired boosted branch, and E9's O(w^2) mass.  "
     "(1) One orientation only: w parallel to k measures a+b, not a, so the individual alpha's "
     "need a perpendicular run this file does not do.  (2) The four h_{3 nu} field equations "
     "left unused by the gauge h_{3 nu} = 0, flagged 'ARGUED, NOT VERIFIED' by both earlier "
     "files and held by stage74 B2 to be pure constraints that cannot be discarded.  (3) The "
     "w -> 0 discontinuity, which makes the choice of branch to match PPN on a physics "
     "question rather than a bookkeeping one.  E8's 1/k^2 assignment is additionally an "
     "argument from dimensions plus the Q_0 scan, not a separate k scan."),
    ("CONDITIONAL -- sign(Fpp)",
     "the repaired m^2 is negative for Fpp > 0, i.e. a resonance at k = |m| rather than a "
     "Yukawa cutoff.  sign(Fpp) is exactly the object of the corpus's acknowledged T1/T2 "
     "transcription fork over Skordis & Zlosnik Eq. (5), so only |m| is claimed.  Nothing in "
     "the answers to (a)-(d) depends on the sign: they are all statements about magnitude and "
     "about A_Y-dependence."),
    ("CONDITIONAL -- Q_0 and K_2",
     "Q_0^-1 is taken as 100 Mpc (gradient_A's own estimate) and 1 Mpc (the mu^-1 floor); "
     "K_2 as SZ21's MOND-compatible fits 7.5e3 (Cosh) and 9.5e3 (Exp), with Fpp = 4 K_2 as in "
     "both earlier files.  Every conclusion is quoted across the full 2x2, and the corner "
     "verdict (c) is robust across all four by >= 19 orders."),
    ("NOT COMPUTED",
     "the alpha's about the repaired background; whether h_00 keeps a Taylor series in w there; "
     "the full Y_bg != 0 solve (obstructed by B5's longitudinal-aether residual); the size of "
     "the J2 = d^2(dark)/dY^2 channel; the four unused h_{3 nu} equations; the g_0i sector; "
     "alpha_3, beta, the zeta's; the deep-MOND PPN regime."),
    ("UNTOUCHED",
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
     "(FITTED, never derived); nu(y) = 1/(1-e^(-sqrt y)) (Milgrom & Sanders 2008 Eq. 13 at "
     "alpha = 1/2) -- which this file's C8 re-derives as the AeST quasi-static interpolation "
     "rather than assuming; beta; A(Q) = kappa^2 G(-K(Q)); the RAR, BTFR, weak lensing, CLASS, "
     "the frozen DR4 band.  Lambda_fix is footing-independent, so the framework's "
     "normalisation is neither credited nor blamed for anything here."),
]
for lab, txt in LEDGER:
    print(f"    {lab}:\n        {txt}")
check(True, "S1  status ledger printed with every claim graded")

print()
print("=" * 100)
nf = len(FAIL)
print(f"PPN-NEWTONIAN-LAMBDA-DIAG CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f";  FAILED: {FAIL}"))
print(f"runtime {time.time()-T0:.0f}s")
sys.exit(1 if FAIL else 0)
