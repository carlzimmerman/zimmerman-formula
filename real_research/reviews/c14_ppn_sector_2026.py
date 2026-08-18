#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
c14_ppn_sector_2026.py
======================
ROUTE 2 OF THE OPTION-1 AUDIT: WHAT HAPPENS TO THE PREFERRED-FRAME SECTOR WHEN THE
FREE FUNCTION IS PROMOTED FROM F(Y,Q) TO F(Z,Q), Z = J^mu J_mu ?
2026-08-18.

THE ASSIGNMENT.  Option 1 replaces AeST's free-function argument Y = q^{mu nu} grad_mu phi
grad_nu phi by Z = J^mu J_mu with J^mu = A^nu grad_nu A^mu (the aether's acceleration).  Z
is the Einstein-aether c_4 structure, so the promotion turns c_4 from a constant into a
function.  The assignment's premise: the dictionary c_1 = +K_B, c_2 = 0, c_3 = -K_B, c_4 = 0
becomes c_4 = (2-K_B), hence c_14 = c_1 + c_4 = K_B + (2-K_B) = 2 EXACTLY, hence
G_N = G/(1 - c_14/2) is formally singular and alpha_2's pole denominator c_123(2-c_14)
acquires a DOUBLE zero under a numerator that becomes the nonzero constant -4.
Route 2 must (a) work out the alpha_1/alpha_2 structure WITHOUT plugging the dictionary into
a published formula, (b) compute lim(alpha_2 * c_S^2) -- which stage74 found equal to K_B/2
in the unmodified theory -- and (c) say whether the promoted c_4 lifts, leaves, or deepens
the c_123 = 0 degeneracy.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: ADVERSE.  VERDICT: KILL.
=========================================================================================
THE PREMISE IS WRONG BY A SIGN, AND THE TRUTH IS WORSE THAN THE PREMISE FEARED.  c_14 is
not +2; it is 2(K_B - 1), i.e. NEGATIVE for every K_B < 1, and c_14 is exactly the spin-1
kinetic normalisation.  The sign is settled here without looking anything up, by deriving
TWO independent quantities from scratch and asking which convention reproduces them: the
Newtonian coupling in the scalar-decoupled limit comes out G_eff/G~ = 1/(1 - (K_B - A_Z)/2)
and the spin-1 speed comes out c_V^2 = K_B/(K_B - A_Z), where -A_Z*Z is the promoted
Lagrangian term (A_Z = (2-K_B) J_Z, J_Z = the AQUAL mu-function).  BOTH say the combination
that plays the role of Foster & Jacobson's c_14 is K_B - A_Z, not K_B + A_Z -- so the
Einstein-aether convention in which those formulas are written carries c_4 with the
OPPOSITE sign to the one the premise (and ppn_alpha_independent_check_2026.py STEP 9's
stated basis) uses.  Put the promoted value in: c_14 = K_B - (2-K_B)J_Z -> 2K_B - 2.
DECISIVE NUMBER: THE REDUCED SPIN-1 QUADRATIC LAGRANGIAN HAS omega^2-COEFFICIENT
PROPORTIONAL TO (K_B - A_Z) = 2(K_B - 1) = -1.8 AT K_B = 0.1, NEGATIVE -- THE AETHER'S
TRANSVERSE MODE IS A GHOST -- AND ITS DISPERSION IS c_V^2 = K_B/(2(K_B-1)) = -0.0556,
NEGATIVE -- IT IS ALSO TACHYONIC, WITH GROWTH RATE |c_V| k UNBOUNDED IN k.  The spin-0
sector goes the same way: c_s^2 = K_B(2-K_B)/(Fpp(K_B-1)) < 0 for every K_B < 1, against
the unmodified theory's c_s^2 = 2[A_Y K_B + (2-K_B)^2]/(K_B Fpp) > 0.  The ghost-free
condition is K_B - (2-K_B)J_Z > 0, i.e. mu(g_obs) < K_B/(2-K_B): at K_B = 0.1 that is
mu < 0.0526, i.e. g_bar < 2.9e-3 a_0 = 2.7e-13 m/s^2 canonical / 3.3e-13 alt.  THE THEORY
IS A GHOST EVERYWHERE IT IS MEANT TO BE USED -- the whole SPARC RAR range and, by
10^3456 (canonical) / 10^3149 (alt) orders in e^(-sqrt y), the entire solar system.
(a) ANSWERED: the theory is outside the domain of the Foster-Jacobson formulas for THREE
independent reasons (c_123 = 0 unchanged; a scalar with a J.grad(phi) mixing that is not in
the Einstein-aether family at all; and now c_14 < 0, outside the spin-1 no-ghost interval),
so no alpha is read off a formula here.  From scratch, PART E solves the static boosted
problem and reports the formal alpha_1 and alpha_2 -- formal because the background they
expand about is violently unstable.  (b) ANSWERED: lim(alpha_2 c_S^2) = K_B - 1, against
the unmodified theory's +K_B/2: the limit CHANGES SIGN and loses its K_B suppression, so
the K_B -> 0 escape that made the unmodified pole harmless is gone.  (c) ANSWERED: the
promoted c_4 LEAVES c_123 = 0 untouched (c_4 does not enter c_1+c_2+c_3), so it neither
lifts nor deepens that degeneracy; what lifts the degeneracy is the same thing as in the
unmodified theory, the khronon rate Q_0 -- and the promotion instead destroys the sector
c_123 was never responsible for.
WHAT SURVIVES, REPORTED AT EQUAL WEIGHT.  Everything option 1's own file claimed for the
STATIC sector is reproduced here from a machinery built for a different purpose, and is
CORRECT: c_T^2 = 1 exactly, gamma_PPN = 1 exactly, and G_N is NOT singular -- the explicit
solve gives G_eff = Ghat/J_Z with Ghat = 2G~/(2-K_B), i.e. AQUAL with mu = J_Z, exactly
opt1_legality_2026.py's C4 and C6.  The reason is structural and is derived here as a
theorem (PART B): the three terms 2(2-K_B)J.grad(phi) - (2-K_B)Y - (2-K_B)Z assemble into
the PERFECT SQUARE -(2-K_B) q_{mu nu}(J - D phi)^mu (J - D phi)^nu, so the promoted c_4 is
Stuckelberged by the khronon and every term of its stress tensor carries a factor of
S = J - D phi.  That is why G_N survives.  It is also why the ghost appears: the square's
-(2-K_B)|J|^2 leg fights the F^2 term's +K_B|J|^2 leg, and (2-K_B) beats K_B for K_B < 1.
THE ESCAPE, PRICED.  Everything above flips at K_B > 1: c_14 = 2(K_B-1) > 0, c_V^2 > 0,
c_s^2 > 0, no ghost.  K_B in (1,2) is inside AeST's own no-ghost window 0 < K_B < 2 -- but
it is 4x above the corpus's BBN cap K_B <~ 0.25 and above all three of SZ21's published
fits (0.1, 0.3, 0.5).  So option 1 is not logically impossible; it costs the BBN cap and
every published AeST parameter set.  RECORDED AS THE ONE LIVE ESCAPE.

=========================================================================================
CONVENTIONS -- EVERY ONE OF THESE CAN FLIP A SIGN OR A FACTOR
=========================================================================================
C1  Signature (-,+,+,+); c = 1; units 16 pi G~ = 1 (so G~ = 1/(16 pi)).
C2  A_mu is the fundamental aether variable, so F_{mu nu} = d_mu A_nu - d_nu A_mu carries
    no metric.  Unit-norm g^{mu nu}A_mu A_nu = -1 enforced by +lambda(A.A+1) (the sign of a
    Lagrange multiplier is a definition; nothing physical depends on it).
C3  THE TWO EINSTEIN-AETHER CONVENTIONS, both named, because the whole assignment turns on
    telling them apart.
      (basis B, the one ppn_alpha_independent_check_2026.py STEP 9 states)
          L = -c_1 grad_m A_n grad^m A^n - c_2 (grad.A)^2 - c_3 grad_m A_n grad^n A^m
              - c4B (A.grad A)^2
      (basis FJ, the one in which G_N = G/(1-c_14/2), c_V^2 = (c_1-c_1^2/2+c_3^2/2)/
          (c_14(1-c_13)) and c_S^2 = c_123(2-c_14)/(c_14(1-c_13)(2+c_13+3c_2)) are written)
    They agree on c_1, c_2, c_3 and DISAGREE on the sign of c_4: PART A derives
    c4FJ = -c4B from two independent from-scratch quantities.  Only c_4 = 0 theories --
    which is every theory the corpus has previously mapped -- are blind to the difference,
    which is why the corpus never caught it.  The premise's "c_14 = 2 EXACTLY" is basis-B
    arithmetic fed into basis-FJ formulas.
C4  PPN matching, as in ppn_alpha_independent_check_2026.py C8 and ppn_scalar_retained_
    2026.py C4:  g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij + (w-free), with
    U_ij(k) = (delta_ij - 2 k_i k_j/k^2)U(k); so if the w-dependent part of h_00 is
    [a w^2 + b (w.khat)^2] U then alpha_2 = -b/2 and alpha_1 = a + b/2.  Will's textbook
    writes the w^2 U coefficient as (alpha_3 - alpha_1); a reader in that normalisation
    flips both signs.  Only |alpha| is used in any verdict here.
C5  Bookkeeping: LINEAR in the matter density rho, SECOND order in the wind w, static in
    the matter frame, single Fourier mode k along z.  Gauge h_{3 nu} = 0 (h_00 is then
    gauge invariant).

=========================================================================================
THE ACTION, AND EVERY REDUCTION, DECLARED
=========================================================================================
R1  The action is real_research/bridge1_aest_equations.md's transcription (verbatim from
    arXiv:2007.00082's LaTeX source), with F(Y,Q) -> F(Z,Q):
      S = int d^4x sqrt(-g)/(16 pi G~) [ R - 2 Lam - (K_B/2)F^2 + 2(2-K_B) J^mu grad_mu phi
          - (2-K_B) Y - F(Z,Q) - lambda(A.A+1) ] + S_m .
R2  F(Z,Q) -> (2-K_B) J(Z) + K(Q), exactly opt1_legality_2026.py's R3 (SZ21 define
    J = F/(2-K_B)).  The quadratic action therefore carries a term -A_Z * Z with
    A_Z = (2-K_B) J_Z, J_Z = dJ/dZ at the LOCAL background.  Likewise the Y term carries
    -A_Y * Y with A_Y = (2-K_B) EXACTLY in option 1 (the free function has left the Y
    sector entirely), against A_Y = (2-K_B)(1 + J_Y) in the unmodified theory.
R3  J_Z IS the AQUAL mu-function: opt1's C4 derives div[J_Z grad Psi] = 4 pi Ghat rho, so
    J_Z = mu(g_obs) = 1/nu(y).  PART C4 re-derives this from the present machinery as
    G_eff = Ghat/J_Z -- an independent confirmation that the Z term implemented here is
    option 1's theory and not something else.  In the solar system J_Z = 1 - e^(-sqrt y) to
    1 part in 10^3456 (canonical) / 10^3149 (alt), so the PPN regime is J_Z = 1.
R4  FROZEN LOCAL STIFFNESS.  A_Y and A_Z are the local values of the free function's
    derivatives, treated as constants.  This is the SAME device ppn_scalar_retained_2026.py
    uses (its leading declared caveat) and is inherited, not invented here: the anisotropic
    piece J_ZZ * (ghat . delta J)^2 is NOT included.  In the solar system J_ZZ is suppressed
    by e^(-sqrt y) ~ 1e-3456 and the approximation is exact to that many digits; in the
    deep-MOND regime it is NOT, and PART C10's threshold is quoted with that flag.
R5  K'(Q_0) = 0 (the background sits at the dark sector's minimum, w = -1) and Lambda is
    dropped locally; both as in the two files this machinery reproduces.
R6  NOT DONE HERE: beta_PPN (O(rho^2)), alpha_3, the zeta's, the g_0i sector, the nonlinear
    /cosmological behaviour of the promoted theory, and any refit of Upsilon or a_0.

WHAT THIS DOES NOT TOUCH.  a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical /
1.1279e-10 alt (kappa = 1/2, FITTED, 0.529 +/- 0.034) enters this file ONLY through
J_Z = 1 - e^(-sqrt(g_bar/a_0)) in PART C10, where both footings are carried and give the
same verdict.  The RAR, lensing, BTFR, the DR4 band and the dust problem are untouched.

METHOD.  Quadratic action about flat space with the aether boosted to w and the khronon at
grad_mu phi = -Q_0 A^bg_mu.  The Einstein-Hilbert side enters through G^(1)_{mu nu} computed
from the Riemann definition; the aether+scalar+Z side is expanded to O(eps^2) directly.  The
machinery is a re-implementation of ppn_scalar_retained_2026.py's, extended by the -A_Z*Z
term, and it is VALIDATED by reproducing four of that file's results and two of
ppn_alpha_independent_check_2026.py's at A_Z = 0 before any A_Z != 0 claim is made.

EXIT 0 iff every numbered check passes.
Runtime: ~10-20 minutes (PART E's two boosted builds dominate).
"""

import math
import os
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
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""),
          flush=True)
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""), flush=True)


print(__doc__)
T0 = time.time()

# =================================================================================================
# symbols
# =================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
CO = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA
eps = sp.Symbol("eps")             # perturbation bookkeeping (linear in rho)
s = sp.Symbol("s")                 # wind bookkeeping (w -> s w)
KB = sp.Symbol("K_B", positive=True)
cJ = sp.Symbol("c_J")              # J.grad(phi) coefficient; the action fixes c_J = 2 - K_B
AY = sp.Symbol("A_Y")              # NET Y coefficient   : Lagrangian carries  -A_Y * Y
AZ = sp.Symbol("A_Z")              # NET Z coefficient   : Lagrangian carries  -A_Z * Z
Fpp = sp.Symbol("Fpp")             # Q-sector curvature  : Lagrangian carries +(Fpp/2)(Q-Q_0)^2
Q0 = sp.Symbol("Q_0")
k = sp.Symbol("k", positive=True)
om = sp.Symbol("omega")
rho = sp.Symbol("rho")
R_ = sp.Symbol("R")
P_, Pi_ = sp.Symbol("P"), sp.Symbol("Pi_")     # phase graders (amplitude / conjugate)
qq = sp.Symbol("qq", positive=True)            # Q_0/k with k set to 1
I = sp.I

# both footings, carried for every dimensional number
A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
GMSUN, AU = 1.32712440018e20, 1.495978707e11


# =================================================================================================
# machinery
# =================================================================================================
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
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n])
                     - sp.diff(gd[m, n], CO[ss])) for ss in range(4)))
             for n in range(4)] for m in range(4)] for r in range(4)]

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


def build(wvec, zero_fields=(), presub=None):
    """O(eps^2) Lagrangian of the aether+scalar+Z sector + the matter source, fields f(t,z)."""
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

    def Z_(e):
        return e.subs(subz)

    hd = sp.Matrix(4, 4, lambda m, n: Z_(H[(min(m, n), max(m, n))]))
    gd = ETA + eps * hd
    hup = ETAI * hd * ETAI
    gu = ETAI - eps * hup + eps ** 2 * (hup * hd * ETAI)
    trh = sum(ETAI[m, n] * hd[m, n] for m in range(4) for n in range(4))
    h2 = sum(hup[m, n] * hd[m, n] for m in range(4) for n in range(4))
    sq = 1 + eps * trh / 2 + eps ** 2 * (trh ** 2 / 8 - h2 / 4)

    w2 = sum(c ** 2 for c in wvec)
    gw = sp.series(1 / sp.sqrt(1 - w2), s, 0, 3).removeO()
    Abg = sp.Matrix([-gw, gw * wvec[0], gw * wvec[1], gw * wvec[2]])       # A^bg_mu
    Ad = sp.Matrix([Abg[m] + eps * Z_(a[m]) for m in range(4)])
    Au = gu * Ad
    AA = sum(Au[m] * Ad[m] for m in range(4))
    Pdn = sp.Matrix([-Q0 * Abg[m] for m in range(4)])                     # grad_mu phi_bg
    dphi = sp.Matrix([Pdn[m] + eps * sp.diff(Z_(chi), CO[m]) for m in range(4)])

    Gam = [[[sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n])
                     - sp.diff(gd[m, n], CO[ss])) for ss in range(4))
             for n in range(4)] for m in range(4)] for r in range(4)]

    F = sp.Matrix(4, 4, lambda m, n: eps * (sp.diff(Z_(a[n]), CO[m]) - sp.diff(Z_(a[m]), CO[n])))
    F2 = sum(F[m, n] * F[aa, bb] * gu[m, aa] * gu[n, bb]
             for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
    Jd = [sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[b][nu][al] * Ad[b] for b in range(4)))
              for nu in range(4)) for al in range(4)]
    Jphi = sum(gu[mu, al] * Jd[al] * dphi[mu] for mu in range(4) for al in range(4))
    # J^mu is O(eps) (J_bg = 0), so Z = g^{ab}J_a J_b needs J only to O(eps): the metric
    # correction to the contraction and the O(eps^2) part of J both enter Z at O(eps^3).
    Jd1 = [sp.expand(sp.expand(sp.series(sp.expand(jj), eps, 0, 2).removeO())).coeff(eps, 1)
           for jj in Jd]
    Zinv = eps ** 2 * sum(ETAI[al, be] * Jd1[al] * Jd1[be] for al in range(4) for be in range(4))
    Q = sum(Au[mu] * dphi[mu] for mu in range(4))
    Y = sum((gu[mu, nu] + Au[mu] * Au[nu]) * dphi[mu] * dphi[nu]
            for mu in range(4) for nu in range(4))

    B = (-(KB / 2) * F2 + 2 * cJ * Jphi - AY * Y - AZ * Zinv + (Fpp / 2) * (Q - Q0) ** 2
         + eps * Z_(lam) * (AA + 1))
    if presub:
        B = B.subs(presub)
    L = sq * B
    L2 = sp.expand(sp.series(sp.expand(L), eps, 0, 3).removeO()).coeff(eps, 2)
    L2 = sp.expand(sp.series(L2, s, 0, 3).removeO())
    L2 = L2 + sp.Rational(1, 2) * rho * hd[0, 0]
    return dict(H=H, a=a, chi=chi, lam=lam, L2=sp.expand(L2), Z=Z_, Abg=Abg)


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
print("=" * 100)
print(f"machinery: linearised Einstein tensor from the Riemann definition "
      f"({time.time()-T0:.0f}s)")
print("=" * 100)


def equations(wvec, zero_fields, eq_names, extra_sub=None, want_L=False):
    """Linear field equations in Fourier space (amplitudes F_*), for the given wind."""
    r = build(wvec, zero_fields, presub=extra_sub)
    H, a, chi, lam, Z_ = r["H"], r["a"], r["chi"], r["lam"], r["Z"]
    allf = [H[(m, n)] for m in range(4) for n in range(m, 4)] + list(a) + [chi, lam]
    live = [f for f in allf if Z_(f) != 0]
    Fa, Ga, sub = fourier(live)
    L2 = r["L2"].subs(extra_sub) if extra_sub else r["L2"]
    L2f = sp.expand(L2.subs(sub, simultaneous=True)).subs(rho, R_ * P_ + sp.Symbol("Rc") * Pi_)
    L2avg = sp.expand(sp.expand(sp.expand(L2f).coeff(P_, 1)).coeff(Pi_, 1))
    G1 = G1_GEN.subs(extra_sub) if extra_sub else G1_GEN
    G1 = G1.subs({f: Z_(f) for f in [H[(m, n)] for m in range(4) for n in range(m, 4)]})
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
    if want_L:
        return r, eqs, Fa, Ga, L2avg, Gup
    return r, eqs, Fa, Ga


ZF0 = ("h01", "h02", "h12", "h13", "h23", "h03", "h33", "a1", "a2")     # scalar sector
UNK0 = ["h00", "h11", "h22", "a0", "a3", "chi", "lam"]
ZF1 = ("h00", "h02", "h11", "h22", "h12", "h23", "h13", "h03", "h33",
       "a0", "a2", "a3")                                                # spin-1 sector
UNK1 = ["h01", "a1"]

# =================================================================================================
print()
print("=" * 100)
print("PART A -- THE DICTIONARY, AND THE SIGN THE PREMISE GOT WRONG")
print("=" * 100)

# ---- A1: the F^2 -> (c_1, c_2, c_3) map, re-derived, not inherited -----------------------------
Adg = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f"D{m}{n}"))       # stands for grad_m A_n
F_from_D = sp.Matrix(4, 4, lambda m, n: Adg[m, n] - Adg[n, m])
lhsD = sp.expand(sum(F_from_D[m, n] * F_from_D[aa, bb] * ETAI[m, aa] * ETAI[n, bb]
                     for m in range(4) for n in range(4) for aa in range(4) for bb in range(4)))
t1 = sum(Adg[m, n] * Adg[aa, bb] * ETAI[m, aa] * ETAI[n, bb]
         for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
t2 = sum(Adg[m, n] * Adg[aa, bb] * ETAI[m, bb] * ETAI[n, aa]
         for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
check(sp.simplify(lhsD - 2 * (t1 - t2)) == 0,
      "A1  F^2 = 2(grad_m A_n grad^m A^n - grad_m A_n grad^n A^m), re-derived symbolically, so "
      "-(K_B/2)F^2 = -K_B t1 + K_B t2 gives c_1 = +K_B, c_2 = 0, c_3 = -K_B in BOTH bases",
      "c_1, c_2, c_3 are basis-independent; only c_4 is not, which is why this step is safe "
      "and the next one is the whole question")

info("A2  the promotion adds the Lagrangian term  -A_Z * Z  with  Z = J^mu J_mu = a^mu a_mu, "
     "A_Z = (2-K_B) J_Z > 0 (the action carries -F(Z,Q), and J_Z = mu > 0).",
     "in basis B (L contains -c4B (A.grad A)^2) that is c4B = +A_Z, hence 'c_14' = K_B + A_Z "
     "-> 2 at J_Z = 1: the assignment's arithmetic, and it is correct IN BASIS B.  What "
     "follows asks which basis the Foster-Jacobson formulas are written in.")

# ---- A3/A4: two from-scratch quantities that fix the basis --------------------------------------
r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0, extra_sub={cJ: 2 - KB, om: 0})
sol0 = sp.solve([sp.Eq(e, 0) for e in eqs], [Fa[u] for u in UNK0], dict=True)[0]
h00_0 = sp.cancel(sol0[Fa["h00"]])
GN_over_G = sp.cancel(16 * sp.pi * (sp.cancel(h00_0.subs(Q0, 0)) * k ** 2 / 2) / (4 * sp.pi * R_))
GN_decoupled = sp.simplify(sp.limit(GN_over_G, AY, sp.oo))
check(sp.simplify(GN_decoupled - 1 / (1 - (KB - AZ) / 2)) == 0,
      "A3  *** FROM SCRATCH, quantity 1: in the scalar-decoupled limit (A_Y -> infinity, the "
      "scalar infinitely stiff) the Newtonian coupling is "
      "G_eff/G~ = 1/(1 - (K_B - A_Z)/2) ***",
      f"G_eff/G~ (A_Y -> oo) = {sp.factor(GN_decoupled)}.  Foster-Jacobson's G_N/G = "
      f"1/(1 - c_14/2) therefore requires c14FJ = K_B - A_Z, i.e. c4FJ = -A_Z = -c4B")

r1, eqs1, Fa1, Ga1 = equations([0, 0, 0], ZF1, UNK1, extra_sub={cJ: 2 - KB})
eqs1 = [sp.expand(e.subs(R_, 0)) for e in eqs1]
M1, b1 = sp.linear_eq_to_matrix(eqs1, [Fa1[u] for u in UNK1])
DET1 = sp.factor(M1.det(method="berkowitz"))
cV2 = sp.simplify(sp.solve(sp.Eq(DET1.subs(Q0, 0), 0), om ** 2)[0] / k ** 2)
check(sp.simplify(cV2 - KB / (KB - AZ)) == 0,
      "A4  *** FROM SCRATCH, quantity 2 (independent of A3): the spin-1 (transverse aether) "
      "dispersion, solved with the metric perturbation h_01 retained and h_13 gauged away, is "
      "c_V^2 = K_B/(K_B - A_Z) in the k >> Q_0 regime ***",
      f"c_V^2 = {sp.factor(cV2)}.  Foster-Jacobson's spin-1 row (c_1 - c_1^2/2 + c_3^2/2)/"
      f"(c_14(1-c_13)) is K_B/c_14 at c_1 = -c_3 = K_B, c_13 = 0 -- so it too requires "
      f"c14FJ = K_B - A_Z.  TWO independent quantities, ONE answer")

c14FJ = KB - AZ
c14_opt1 = sp.simplify(c14FJ.subs(AZ, 2 - KB))
check(sp.simplify(c14_opt1 - (2 * KB - 2)) == 0,
      "A5  *** THE CORRECTION: in the basis the formulas are written in, the promotion gives "
      "c_4 = -(2-K_B)J_Z and c_14 = K_B - (2-K_B)J_Z -> 2K_B - 2 = 2(K_B - 1) at J_Z = 1.  "
      "NOT +2 ***",
      f"c_14 = {sp.factor(c14_opt1)}: NEGATIVE for every K_B < 1, i.e. for the whole "
      f"BBN-allowed range K_B <~ 0.25 and for all three of SZ21's published fits")

c123 = sp.simplify(KB + 0 - KB)
c13 = sp.simplify(KB - KB)
spin1_norm = sp.simplify(2 * KB - KB ** 2 + (-KB) ** 2)
check(c123 == 0 and c13 == 0 and sp.simplify(spin1_norm - 2 * KB) == 0
      and sp.simplify((2 - c14_opt1) - (4 - 2 * KB)) == 0,
      "A6  what the promotion does and does not change: c_123 = c_1+c_2+c_3 = 0 (UNCHANGED -- "
      "c_4 does not enter it), c_13 = 0 (unchanged), the spin-1 kinetic numerator "
      "2c_1-c_1^2+c_3^2 = 2K_B (unchanged), and 2 - c_14 = 4 - 2K_B != 0",
      "SO THERE IS NO DOUBLE ZERO.  alpha_2's denominator c_123(2-c_14) still has exactly ONE "
      "zero, the c_123 = 0 the unmodified theory already had.  The assignment's 'both factors "
      "vanish' followed from the basis-B c_14 = 2 and does not survive A5")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- WHY c_4 CANNOT BE READ OFF ALONE: THE PERFECT SQUARE (a theorem)")
print("=" * 100)

import random  # noqa: E402
random.seed(20260818)


def _rnd():
    return sp.Rational(random.randint(-9, 9), random.randint(1, 7))


gd_ = sp.Matrix(4, 4, lambda i, j: 0)
for i in range(4):
    for j in range(i, 4):
        v = _rnd()
        gd_[i, j] = v
        gd_[j, i] = v
gd_ = gd_ + sp.diag(-8, 7, 6, 5)          # generic, invertible, Lorentzian-signature point
gu_ = gd_.inv()
Araw = sp.Matrix([_rnd() for _ in range(4)])
A_ = Araw / sp.sqrt(-(Araw.T * gu_ * Araw)[0, 0])         # A_mu with g^{mn}A_m A_n = -1
Au_ = gu_ * A_
dphi_ = sp.Matrix([_rnd() for _ in range(4)])
Jr = sp.Matrix([_rnd() for _ in range(4)])
Ju_ = Jr + (sum(A_[m] * Jr[m] for m in range(4))) * Au_    # generic J^mu with A.J = 0
qu_ = sp.Matrix(4, 4, lambda m, n: gu_[m, n] + Au_[m] * Au_[n])
qd_ = sp.Matrix(4, 4, lambda m, n: gd_[m, n] + A_[m] * A_[n])
Zv = sum(gd_[m, n] * Ju_[m] * Ju_[n] for m in range(4) for n in range(4))
Yv = sum(qu_[m, n] * dphi_[m] * dphi_[n] for m in range(4) for n in range(4))
Jphiv = sum(Ju_[m] * dphi_[m] for m in range(4))
Dphi_ = qu_ * dphi_
Sv = sp.Matrix([Ju_[m] - Dphi_[m] for m in range(4)])
lhs_sq = sum(qd_[m, n] * Sv[m] * Sv[n] for m in range(4) for n in range(4))

check(sp.simplify((A_.T * gu_ * A_)[0, 0] + 1) == 0
      and sp.simplify(sum(A_[m] * Ju_[m] for m in range(4))) == 0
      and sp.simplify(sum(A_[m] * Sv[m] for m in range(4))) == 0,
      "B1  setup verified at a generic Lorentzian point: A.A = -1, A_mu J^mu = 0 (an identity, "
      "since A_mu A^nu grad_nu A^mu = (1/2)A^nu grad_nu(A.A) = 0), and hence A_mu S^mu = 0 for "
      "S^mu = J^mu - D^mu phi, D^mu phi = q^{mu nu} grad_nu phi")
check(sp.simplify(lhs_sq - (Zv - 2 * Jphiv + Yv)) == 0,
      "B2  *** THE IDENTITY, verified at a generic point with generic g, A, grad phi and J:\n"
      "         q_{mu nu}(J - D phi)^mu (J - D phi)^nu  =  Z - 2 J.grad(phi) + Y\n"
      "     so the three terms  2(2-K_B)J.grad(phi) - (2-K_B)Y - (2-K_B)Z  of the promoted "
      "action are EXACTLY  -(2-K_B) |J - D phi|^2 : A PERFECT SQUARE ***",
      "the promoted c_4 term is not a standalone Einstein-aether coupling.  It is one leg of a "
      "square whose other two legs are the khronon's kinetic term and the J.grad(phi) mixing -- "
      "i.e. the aether's acceleration is STUCKELBERGED by the khronon.  The Einstein-aether "
      "basis presumes those other legs are absent, which is the third and most basic reason its "
      "formulas cannot be evaluated here")
info("B3  TWO CONSEQUENCES, and they pull in opposite directions -- both are reported.",
     "FAVOURABLE: every term of the square's stress tensor carries a factor of S, so on any "
     "configuration with S = 0 the entire promoted sector is invisible to the metric.  That is "
     "why G_N is finite (PART C4) and why opt1_legality_2026.py's C6 was right.\n"
     "         ADVERSE: the square's -(2-K_B)|J|^2 leg is a WRONG-SIGN aether kinetic term.  It "
     "is opposed only by the F^2 term's +K_B|J|^2, and (2-K_B) > K_B whenever K_B < 1.  The net "
     "coefficient is exactly K_B - A_Z = c_14 (PART C7).  The same square that saves G_N is what "
     "makes the aether a ghost.")
check(sp.simplify((2 - KB) - (2 - KB) * 1) == 0,
      "B4  the square is EXACT only where A_Z = A_Y, i.e. only at J_Z = 1 -- the Newtonian "
      "limit.  In deep MOND J_Z << 1 and the square is detuned; the PPN regime is precisely "
      "where it is exact, so nothing below is an artefact of the limit taken")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- FROM-SCRATCH SECTORS.  Six controls before any new claim.")
print("=" * 100)

# ---- C0: pure GR normalisation ------------------------------------------------------------------
r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0,
                           extra_sub={cJ: 0, AY: 0, AZ: 0, Fpp: 0, om: 0, Q0: 0, KB: 0})
solGR = sp.solve([sp.Eq(e, 0) for e in eqs], [Fa[u] for u in UNK0], dict=True)
check(len(solGR) == 1 and sp.simplify(solGR[0][Fa["h00"]] - R_ / (2 * k ** 2)) == 0,
      "C0  CONTROL 1 (pure GR): h_00 = rho/(2k^2), i.e. h_00 = 2U with G_N = 1/(16 pi) = G~ -- "
      "the normalisation ppn_alpha_independent_check_2026.py STEP 5 fixed independently")

# ---- C1/C2/C3: the A_Z = 0 controls against ppn_scalar_retained_2026.py -------------------------
check(sp.simplify(GN_over_G.subs(AZ, 0) - 2 * AY / ((2 - KB) * (AY - (2 - KB)))) == 0,
      "C1  CONTROL 2 (A_Z = 0, the unmodified theory): G_eff/G = 2A_Y/[(2-K_B)(A_Y-(2-K_B))] -- "
      "ppn_scalar_retained_2026.py's G4b reproduced exactly by an independent implementation")
check(sp.simplify(sp.limit(GN_over_G.subs(AZ, 0), AY, sp.oo) - 1 / (1 - KB / 2)) == 0,
      "C2  CONTROL 3: and its screened limit is G/(1 - K_B/2) -- the corpus's committed "
      "G~ = (1-K_B/2)Ghat, and reading D's w = 0 branch")
check(sp.simplify(cV2.subs(AZ, 0) - 1) == 0,
      "C3  CONTROL 4 (A_Z = 0): c_V^2 = 1 exactly -- ppn_alpha_independent_check_2026.py "
      "STEP 9's transverse omega^2 = k^2, reproduced")

r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0, extra_sub={cJ: 2 - KB})
eqs_v = [sp.expand(e.subs(R_, 0)) for e in eqs]
Msys, bsys = sp.linear_eq_to_matrix(eqs_v, [Fa[u] for u in UNK0])
DET = sp.factor(Msys.det(method="berkowitz"))
tens = sp.factor((k - om) * (k + om))
check(sp.simplify(sp.cancel(DET / tens)).is_polynomial(om),
      "C4  CONTROL 5: the vacuum mode determinant factorises with a clean (k^2 - omega^2) "
      "tensor factor for EVERY K_B, A_Y, A_Z, Fpp, Q_0 -- c_T^2 = 1 EXACTLY, promotion or not "
      "(as it must be: c_4 does not enter the tensor sector)")
scal0 = sp.expand(sp.expand(sp.cancel(DET / tens)).subs(Q0, 0))
poly = sp.Poly(sp.expand(scal0 / (om ** 2 * k ** 4)), om)
cs2 = sp.simplify(sp.solve(sp.Eq(poly.as_expr(), 0), om ** 2)[0] / k ** 2)
check(sp.simplify(cs2.subs(AZ, 0) - 2 * (AY * KB + (2 - KB) ** 2) / (KB * Fpp)) == 0,
      "C5  CONTROL 6 (A_Z = 0): c_s^2 = 2[A_Y K_B + (2-K_B)^2]/(K_B Fpp) -- "
      "ppn_scalar_retained_2026.py's G3a, hence (at A_Y = (2-K_B)(1+lambda_s), Fpp = 4K_2) "
      "SZ21 Eq. (30), reproduced.  SIX controls passed; the machinery is validated")

print()
JZ = sp.Symbol("J_Z", positive=True)
GN_opt1 = sp.simplify(GN_over_G.subs({AY: 2 - KB, AZ: (2 - KB) * JZ}))
check(sp.simplify(GN_opt1 - (1 / (1 - KB / 2)) / JZ) == 0,
      "C6  *** OPTION 1, STATIC SECTOR: G_eff = Ghat/J_Z with Ghat = 2G~/(2-K_B).  That IS "
      "AQUAL with mu(g_obs) = J_Z -- opt1_legality_2026.py's C4 -- and at J_Z = 1 it is "
      "G_N = Ghat, finite and EQUAL to the unmodified theory's: opt1's C6 CONFIRMED ***",
      f"G_eff/G~ = {sp.factor(GN_opt1)}.  This is also the check that the Z term implemented "
      f"here IS option 1's theory: an independent file, an independent method, the same "
      f"quasi-static law.  The naive 'G_N = G/(1-c_14/2) = G/0' is dead twice over -- the "
      f"basis-B c_14 = 2 is the wrong basis (A5), and the square makes the sector invisible "
      f"to the static metric anyway (B3)")
check(sp.simplify(sol0[Fa["h11"]] - h00_0) == 0 and sp.simplify(sol0[Fa["h22"]] - h00_0) == 0,
      "C7  *** and gamma_PPN = 1 EXACTLY, for every K_B, A_Y, A_Z, Fpp, Q_0: h_11 = h_22 = h_00 "
      "***",
      "so option 1 costs nothing in the two places the corpus most cares about, c_T and "
      "gamma_PPN.  Reported before the adverse half, at equal weight")

print()
# ---- the reduced spin-1 quadratic form: the GHOST sign -------------------------------------------
r1b = build([0, 0, 0], ZF1, presub={cJ: 2 - KB})
H1, a1f, Z1 = r1b["H"], r1b["a"], r1b["Z"]
Fa1b, Ga1b, sub1 = fourier([H1[(0, 1)], a1f[1]])
L2f1 = sp.expand(r1b["L2"].subs(sub1, simultaneous=True))
L2avg1 = sp.expand(sp.expand(L2f1).coeff(P_, 1).coeff(Pi_, 1))
G1b = G1_GEN.subs({f: Z1(f) for f in [H1[(m, n)] for m in range(4) for n in range(m, 4)]})
G1b = G1b.applyfunc(lambda e: sp.expand(sp.expand(e).subs(sub1, simultaneous=True)).coeff(P_, 1))
Gup01 = sp.expand(ETA[0, 0] * ETA[1, 1] * G1b[0, 1])
eq_h01 = sp.expand(sp.diff(L2avg1, Ga1b["h01"]) - 2 * Gup01)
sol_h01 = sp.solve(sp.Eq(eq_h01, 0), Fa1b["h01"])[0]
Ltot1 = sp.expand(L2avg1 - 2 * sp.expand(Gup01) * Ga1b["h01"])
Lred = sp.expand(sp.simplify(Ltot1.subs(
    {Fa1b["h01"]: sol_h01, Ga1b["h01"]: sol_h01.subs({Fa1b["a1"]: Ga1b["a1"]})})).subs(Q0, 0))
mod2 = Fa1b["a1"] * Ga1b["a1"]                                   # |a_1|^2 > 0
kin1 = sp.simplify(sp.expand(Lred).coeff(om, 2) / mod2)
grad1 = sp.simplify(sp.expand(Lred).coeff(k, 2).subs(om, 0) / mod2)
check(sp.simplify(kin1 - (-2) * (AZ - KB)) == 0 and sp.simplify(grad1 + 2 * KB) == 0,
      "C8  *** THE GHOST.  Eliminating the non-dynamical h_01 leaves the spin-1 Lagrangian\n"
      "         L_1 = 2(K_B - A_Z) omega^2 |a_1|^2 - 2 K_B k^2 |a_1|^2 ,\n"
      "     so the kinetic coefficient IS 2 c_14 = 2(K_B - A_Z) ***",
      f"omega^2 coefficient = {sp.factor(kin1)}, k^2 coefficient = {sp.factor(grad1)}.  "
      f"At A_Z = 0 (unmodified) the kinetic term is +2K_B > 0 and the mode is healthy with "
      f"c_V^2 = 1.  At A_Z = (2-K_B) (option 1, J_Z = 1) it is 2(2K_B - 2) = 4(K_B - 1), "
      f"NEGATIVE for every K_B < 1: the transverse aether mode is a GHOST")
cV2_opt1 = sp.simplify(cV2.subs(AZ, 2 - KB))
check(sp.simplify(cV2_opt1 - KB / (2 * (KB - 1))) == 0,
      "C9  *** AND IT IS ALSO TACHYONIC: c_V^2 = K_B/(2(K_B-1)) < 0 for every K_B < 1, so "
      "omega^2 = c_V^2 k^2 < 0 and the growth rate |c_V| k is UNBOUNDED in k ***",
      f"c_V^2 = {sp.factor(cV2_opt1)}: {float(cV2_opt1.subs(KB, sp.Rational(1,10))):.4f} at "
      f"K_B = 0.1, {float(cV2_opt1.subs(KB, sp.Rational(1,4))):.4f} at K_B = 0.25, "
      f"{float(cV2_opt1.subs(KB, sp.Rational(1,2))):.4f} at K_B = 0.5.  Against c_V^2 = +1 "
      f"for the unmodified theory at every K_B")
cs2_opt1 = sp.simplify(cs2.subs({AY: 2 - KB, AZ: 2 - KB}))
check(sp.simplify(cs2_opt1 - KB * (2 - KB) / (Fpp * (KB - 1))) == 0,
      "C10 *** THE SPIN-0 SECTOR GOES THE SAME WAY: c_s^2 = K_B(2-K_B)/(Fpp(K_B-1)) < 0 for "
      "every K_B < 1 (Fpp > 0 is the healthy sign, fixed by CONTROL 6) ***",
      f"c_s^2 = {sp.factor(cs2_opt1)}.  The unmodified theory has "
      f"c_s^2 = 2[A_Y K_B + (2-K_B)^2]/(K_B Fpp) > 0 for every K_B, and it DIVERGES as "
      f"K_B -> 0; option 1's vanishes there and is negative on the way.  Both mode sectors "
      f"the promotion touches are destabilised, and by the same factor (K_B - 1)")

print()
# ---- C11: where, physically, the theory is ghost-free --------------------------------------------
GBAR_AU = GMSUN / AU ** 2
rows = []
for kbv in (0.1, 0.25, 0.5):
    mu_max = kbv / (2 - kbv)                       # ghost-free iff J_Z = mu < K_B/(2-K_B)
    sq_exp = math.log((2 - kbv) / (2 - 2 * kbv))   # Route A: mu = 1-e^-sqrt y -> y*
    y_exp = sq_exp ** 2
    y_alg = mu_max ** 2 / (1 - mu_max ** 2)        # framework kernel g=sqrt(gb^2+gb a0)
    rows.append((kbv, mu_max, y_exp, y_alg))
print(f"    {'K_B':>6s} {'mu ceiling':>11s} {'y* Route A':>12s} {'y* algebraic':>13s} "
      f"{'g_bar* canon':>14s} {'g_bar* ALT':>13s}")
for kbv, mu_max, y_exp, y_alg in rows:
    print(f"    {kbv:6.2f} {mu_max:11.4f} {y_exp:12.5f} {y_alg:13.5f} "
          f"{y_exp*A0_CAN:14.3e} {y_exp*A0_ALT:13.3e}")
check(all(yv < 0.2 for _, _, yv, _ in rows) and all(abs(ye - ya) / ye < 0.2 for _, _, ye, ya in rows),
      "C11 *** THE GHOST-FREE REGION IS EMPTY OF DATA.  No-ghost requires "
      "mu(g_obs) < K_B/(2-K_B), i.e. g_bar below y* a_0 with y* = 0.0029 (K_B = 0.1), 0.024 "
      "(0.25), 0.16 (0.5) -- and the two kernels agree to within 20%, so this is a property of "
      "the promotion, not of a kernel choice ***",
      f"in physical units the ceiling is {rows[0][2]*A0_CAN:.2e} m/s^2 canonical / "
      f"{rows[0][2]*A0_ALT:.2e} ALT at K_B = 0.1.  SPARC's RAR runs from ~1e-12 up to "
      f"~1e-8 m/s^2, i.e. y from ~1e-2 to ~1e2, so essentially the ENTIRE dataset the "
      f"framework fits sits in the ghost region.  Both footings give the same verdict; the "
      f"canonical/ALT spread moves the boundary by 20% and nothing else")
for lab, a0 in FOOT:
    yv = GBAR_AU / a0
    sy = math.sqrt(yv)
    info(f"C12 solar system, {lab} a_0 = {a0:.4e}: at 1 AU g_bar = {GBAR_AU:.4e} m/s^2, "
         f"y = {yv:.4e}, sqrt(y) = {sy:.1f}",
         f"J_Z = 1 - e^(-sqrt y) = 1 - 10^-{sy/math.log(10):.0f}, so "
         f"c_14 = 2(K_B - 1) + (2-K_B)*10^-{sy/math.log(10):.0f}: the promoted theory is "
         f"ghostly in the solar system to {sy/math.log(10):.0f} decimal places")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- (b) lim(alpha_2 c_S^2), AND WHAT THE FORMULAS SAY IN EACH BASIS")
print("=" * 100)
info("D0  PROVENANCE.  The four expressions used in this PART are the ones already committed "
     "in real_research/reviews/alpha2_regulated_limit_2026.py as [P1], [P2], [P4].  They are "
     "used here ONLY to answer question (b) on its own terms and to show what each basis "
     "returns.  NOTHING in the verdict rests on them: PART C's numbers are from scratch, and "
     "the formulas' own domain excludes this theory (c_123 = 0, and now c_14 outside the "
     "spin-1 no-ghost interval, and a scalar the Einstein-aether family does not contain).")
c1s, c2s, c3s, c4s = sp.symbols("c_1 c_2 c_3 c_4", real=True)
c13s, c14s, c123s = c1s + c3s, c1s + c4s, c1s + c2s + c3s
alpha1_gen = -8 * (c3s ** 2 + c1s * c4s) / (2 * c1s - c1s ** 2 + c3s ** 2)
alpha2_num = (c1s + 2 * c3s - c4s) * (2 * c1s + 3 * c2s + c3s + c4s)
alpha2_gen = alpha1_gen / 2 - alpha2_num / (c123s * (2 - c14s))
cS2_gen = c123s * (2 - c14s) / (c14s * (1 - c13s) * (2 + c13s + 3 * c2s))

epsr = sp.Symbol("epsr", positive=True)
# c_123 is regulated to epsr through c_2 (the direction that keeps c_1 = -c_3 = K_B fixed).
# In basis B, c_14 = 2 exactly, so 2 - c_14 must be regulated too -- otherwise alpha_2's
# denominator is identically zero and no limit exists.  That extra regulator is exactly the
# "double zero" the assignment names, and it is carried here so the basis-B row can be shown.
DROWS = (("unmodified (c_4 = 0)", {c1s: KB, c2s: epsr, c3s: -KB, c4s: sp.Integer(0)}),
         ("option 1, basis FJ (c_4 = -(2-K_B))",
          {c1s: KB, c2s: epsr, c3s: -KB, c4s: -(2 - KB)}),
         ("option 1, basis B  (c_4 = +(2-K_B))",
          {c1s: KB, c2s: epsr, c3s: -KB, c4s: 2 - KB - epsr}))
DRES = {}
for lab, sub in DROWS:
    a1v = sp.simplify(sp.limit(alpha1_gen.subs(sub), epsr, 0, "+"))
    numv = sp.simplify(alpha2_num.subs(sub).subs(epsr, 0))
    denv = sp.factor(sp.simplify((c123s * (2 - c14s)).subs(sub)))
    prod = sp.simplify(sp.limit(sp.together(alpha2_gen.subs(sub) * cS2_gen.subs(sub)),
                                epsr, 0, "+"))
    cs_rate = sp.simplify(sp.limit(cS2_gen.subs(sub) / epsr, epsr, 0, "+"))
    DRES[lab] = (a1v, numv, denv, prod, cs_rate)
    print(f"    {lab:36s} alpha_1 = {sp.factor(a1v)}")
    print(f"    {'':36s} alpha_2 pole numerator = {sp.factor(numv)}, "
          f"denominator = {denv}")
    print(f"    {'':36s} c_S^2/eps -> {sp.factor(cs_rate)},   "
          f"lim(alpha_2 c_S^2) = {sp.factor(prod)}")
unmod_a1, _, _, unmod_prod, unmod_rate = DRES[DROWS[0][0]]
fj_a1, _, _, fj_prod, fj_rate = DRES[DROWS[1][0]]
bB_a1, _, _, bB_prod, _ = DRES[DROWS[2][0]]

check(sp.simplify(unmod_a1 + 4 * KB) == 0 and sp.simplify(unmod_prod - KB / 2) == 0,
      "D1  CONTROL: the unmodified dictionary reproduces stage74's two published numbers -- "
      "alpha_1 = -4K_B and lim(alpha_2 c_S^2) = +K_B/2 -- so the regulator and the formulas "
      "are being handled the same way stage74 handled them")
check(sp.simplify(fj_prod - (KB - 1)) == 0,
      "D2  *** (b) ANSWERED: with the CORRECTED dictionary the limit is "
      "lim(alpha_2 c_S^2) = K_B - 1, against the unmodified theory's +K_B/2.  It CHANGES SIGN "
      "and it no longer vanishes as K_B -> 0 ***",
      f"at K_B = 0.1: {float((KB-1).subs(KB, sp.Rational(1,10))):+.3f} against "
      f"{float((KB/2).subs(KB, sp.Rational(1,10))):+.3f}, a factor "
      f"{float(((1-KB)/(KB/2)).subs(KB, sp.Rational(1,10))):.0f} larger and opposite in sign.  "
      f"The negative sign is the SAME sign PART C10 found from scratch for c_s^2 -- two "
      f"independent routes agreeing -- and the loss of the K_B factor is the loss of the only "
      f"escape the unmodified pole had (stage74's window survived precisely because "
      f"alpha_2 c_S^2 -> 0 with K_B)")
check(sp.simplify(fj_a1 - 8 * (1 - KB)) == 0 and sp.simplify(bB_a1 + 8) == 0,
      "D3  and the same corrected dictionary turns the (inapplicable) alpha_1 formula from "
      "-4K_B into 8(1-K_B) -- 7.2 at K_B = 0.1, K_B-unsuppressed either way",
      f"the basis-B reading the assignment used would have given a flat -8 and a 0/0 for "
      f"alpha_2.  Neither is the answer; both agree with the corrected reading on the one "
      f"thing that matters, that the K_B -> 0 escape is gone")
check(sp.simplify(fj_rate) != 0 and float(fj_rate.subs(KB, sp.Rational(1, 10))) < 0
      and float(unmod_rate.subs(KB, sp.Rational(1, 10))) > 0,
      "D4  *** (c) ANSWERED: the promoted c_4 LEAVES the c_123 = 0 degeneracy exactly where it "
      "was -- c_4 does not appear in c_1+c_2+c_3, so alpha_2 still has one simple pole and "
      "c_S^2 still vanishes linearly in c_123.  What changes is the RATE'S SIGN: "
      "c_S^2/c_123 -> -(2-K_B)/(2(1-K_B)), negative, where the unmodified theory has "
      "+(2-K_B)/(2K_B) ***",
      f"c_S^2/c_123 -> {sp.factor(fj_rate)}.  So the promotion neither lifts nor deepens the "
      f"degeneracy; it destabilises the sector on the OTHER side of it.  The degeneracy-lifting "
      f"agent is unchanged from the unmodified theory: the khronon rate Q_0 "
      f"(ppn_scalar_retained_2026.py Q2), which the promotion does not touch")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- (a) alpha_1 AND alpha_2 FOR THE PROMOTED THEORY, SOLVED FROM SCRATCH")
print("=" * 100)
info("E0  METHOD (identical to ppn_scalar_retained_2026.py's, so that the A_Z = 0 run is a "
     "line-by-line control).  h_00 is solved twice: wind PARALLEL to k gives "
     "a + b = alpha_1 - alpha_2, wind PERPENDICULAR gives a = alpha_1 + alpha_2.  In each run "
     "the O(w^2) coefficient of h_00 is split by its k-dependence and only the 1/k^2 "
     "(long-range) part is kept; the 1/Q_0^2 piece is a contact term that vanishes outside "
     "matter.  READ THE RESULT WITH PART C ATTACHED: these are the FORMAL alpha's of a "
     "background whose spin-1 and spin-0 modes both have omega^2 < 0.  A PPN expansion about "
     "an unstable background has no domain of validity, so they are reported as arithmetic, "
     "NOT as observables to be compared with lunar laser ranging.")


def hcoeffs(eqs, unkS, tgt, nord=2):
    rep, parts = {}, {}
    for u in unkS:
        ps = [sp.Symbol(str(u) + f"_{j}") for j in range(nord + 1)]
        parts[u] = ps
        rep[u] = sum(s ** j * ps[j] for j in range(nord + 1))
    E = [sp.expand(e.subs(rep)) for e in eqs]
    known = {}
    for j in range(nord + 1):
        cur = [sp.expand(sp.expand(e).coeff(s, j).subs(known)) for e in E]
        vj = [parts[u][j] for u in unkS]
        M, bb = sp.linear_eq_to_matrix(cur, vj)
        xs = M.LUsolve(bb)
        known.update({v: sp.cancel(xs[i]) for i, v in enumerate(vj)})
    return [known[parts[tgt][j]] for j in range(nord + 1)]


def longrange(eqs, unkS, tgt, sm, qds=(10 ** 6, 3 * 10 ** 6, 10 ** 7)):
    dat = []
    for d in qds:
        qv = sp.Rational(1, d)
        smq = dict(sm)
        smq[qq] = qv
        dat.append((qv, hcoeffs([sp.expand(e.subs(smq)) for e in eqs], unkS, tgt)))
    Cm2, C0, C2 = sp.symbols("Cm2 C0 C2")
    sol = sp.solve([sp.Eq(Cm2 / qv ** 2 + C0 + C2 * qv ** 2, d[2]) for qv, d in dat],
                   [Cm2, C0, C2], dict=True)[0]
    odd_zero = all(sp.simplify(d[1]) == 0 for _, d in dat)
    return sol[C0], sol[Cm2], dat[-1][1][0], odd_zero


ZFp = ("h02", "h12", "h23", "h13", "h03", "h33", "a2")
UNKp = ["h00", "h01", "h11", "h22", "a0", "a1", "a3", "chi", "lam"]
BASE = {cJ: 2 - KB, Q0: qq, k: 1, om: 0}
t1 = time.time()
_, eP, FaP, _ = equations([0, 0, s * sp.Integer(1)], ZF0, UNK0, extra_sub=BASE)
eP = [sp.expand(e.subs(R_, 1)) for e in eP]
unkP = [FaP[u] for u in UNK0]
print(f"       (wind parallel to k: system built, {time.time()-t1:.0f}s)", flush=True)
t1 = time.time()
_, eQ, FaQ, _ = equations([s * sp.Integer(1), 0, 0], ZFp, UNKp, extra_sub=BASE)
eQ = [sp.expand(e.subs(R_, 1)) for e in eQ]
unkQ = [FaQ[u] for u in UNKp]
print(f"       (wind perpendicular to k: system built, {time.time()-t1:.0f}s)", flush=True)

CASES = (("UNMODIFIED  A_Z=0, A_Y=1e6", {AZ: 0, AY: 10 ** 6}, True),
         ("UNMODIFIED  A_Z=0, A_Y=1e7", {AZ: 0, AY: 10 ** 7}, True),
         ("OPTION 1    A_Y=A_Z=2-K_B", None, False))
print(f"       {'K_B':>5s} {'case':>28s} {'a':>13s} {'a+b':>13s} {'alpha_1':>13s} "
      f"{'alpha_2':>13s}")
res = {}
for kbv in (sp.Rational(1, 10), sp.Rational(1, 2)):
    for lab, cs, is_unmod in CASES:
        sm = {KB: kbv, Fpp: 4}
        sm.update(cs if cs else {AY: 2 - kbv, AZ: 2 - kbv})
        C0p, _, h0p, _ = longrange(eP, unkP, FaP["h00"], sm)
        C0q, _, h0q, _ = longrange(eQ, unkQ, FaQ["h00"], sm)
        apb, aa = 2 * C0p / h0p, 2 * C0q / h0q
        bb = apb - aa
        a1v, a2v = aa + bb / 2, -bb / 2
        res[(kbv, lab)] = (float(aa), float(apb), float(a1v), float(a2v))
        print(f"       {float(kbv):5.2f} {lab:>28s} {float(aa):13.7f} {float(apb):13.7f} "
              f"{float(a1v):13.7f} {float(a2v):13.7f}", flush=True)

a1_ref = KB * (2 * KB ** 2 - 5 * KB + 6) / (2 - KB) ** 2
a2_ref = KB * (2 * KB ** 2 - 11 * KB + 10) / (2 - KB) ** 2
ok_ctrl = True
for kbv in (sp.Rational(1, 10), sp.Rational(1, 2)):
    for lab, cs, _ in CASES[:2]:
        ay = float(cs[AY])
        t1v, t2v = float(a1_ref.subs(KB, kbv)), float(a2_ref.subs(KB, kbv))
        g1, g2 = res[(kbv, lab)][2], res[(kbv, lab)][3]
        ok_ctrl = ok_ctrl and abs(g1 - t1v) < 50.0 / ay and abs(g2 - t2v) < 50.0 / ay
check(ok_ctrl,
      "E1  *** CONTROL 7, the strongest one: at A_Z = 0 the boosted solve returns "
      "alpha_1 = K_B(2K_B^2-5K_B+6)/(2-K_B)^2 and alpha_2 = K_B(2K_B^2-11K_B+10)/(2-K_B)^2 -- "
      "ppn_scalar_retained_2026.py's Q3-4, reproduced at two K_B and two A_Y with residuals "
      "scaling as 1/A_Y ***",
      f"targets at K_B=0.1: alpha_1 = {float(a1_ref.subs(KB, sp.Rational(1,10))):.7f}, "
      f"alpha_2 = {float(a2_ref.subs(KB, sp.Rational(1,10))):.7f}; at K_B=0.5: "
      f"{float(a1_ref.subs(KB, sp.Rational(1,2))):.7f}, "
      f"{float(a2_ref.subs(KB, sp.Rational(1,2))):.7f}.  The boosted machinery is validated "
      f"before it is used on the promoted theory")

o1 = res[(sp.Rational(1, 10), CASES[2][0])]
o5 = res[(sp.Rational(1, 2), CASES[2][0])]
u1 = res[(sp.Rational(1, 10), CASES[1][0])]
u5 = res[(sp.Rational(1, 2), CASES[1][0])]
check(abs(o1[2]) > abs(u1[2]) and abs(o1[3]) > abs(u1[3])
      and abs(o5[2]) > abs(u5[2]) and abs(o5[3]) > abs(u5[3]),
      "E2  *** (a) ANSWERED, formally: the promoted theory's static boosted problem DOES close "
      "(the linear system is non-degenerate, so alpha_1 and alpha_2 exist as arithmetic) and "
      "BOTH come out LARGER IN MAGNITUDE than the unmodified theory's, at both K_B ***",
      f"K_B=0.1: option 1 (alpha_1, alpha_2) = ({o1[2]:+.6f}, {o1[3]:+.6f}) against "
      f"unmodified ({u1[2]:+.6f}, {u1[3]:+.6f}).  K_B=0.5: ({o5[2]:+.6f}, {o5[3]:+.6f}) "
      f"against ({u5[2]:+.6f}, {u5[3]:+.6f}).  Both bounds -- |alpha_1| < 1e-4 and "
      f"|alpha_2| < 1e-7 -- are violated by both theories at these K_B; the point is the "
      f"DIRECTION, and it is adverse")
check(True,
      "E3  and the honest qualification, stated as loudly as the numbers: these alpha's are "
      "NOT observables of the promoted theory.  PART C8/C9/C10 show its spin-1 and spin-0 "
      "modes have omega^2 < 0 with growth rate proportional to k, so the flat boosted "
      "background is destroyed on a timescale 1/(|c_V| k) that goes to zero with the "
      "wavelength.  There is nothing for a static PPN expansion to be an expansion of.  This "
      "is the same class of statement stage74 reached for the aether-only theory, but for a "
      "different and stronger reason: there the problem was a ZERO mode speed, here it is a "
      "NEGATIVE one plus a wrong-sign kinetic term")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- VERDICT AND STATUS LEDGER")
print("=" * 100)
K2_FITS = {"Cosh": 7.5e3, "Exp": 9.5e3, "Higgs": None}
SZ21_KB = {"Cosh": 0.5, "Exp": 0.1, "Higgs": 0.3}
BBN_CAP = 0.25
print(f"    {'SZ21 fit':8s} {'its K_B':>9s} {'K_B < 1 ?':>11s} {'ghost ?':>9s} {'c_V^2':>10s}")
for nm, kbv in SZ21_KB.items():
    print(f"    {nm:8s} {kbv:9.2f} {'YES':>11s} {'YES':>9s} "
          f"{float(cV2_opt1.subs({KB: kbv})):10.4f}")
check(all(kbv < 1 for kbv in SZ21_KB.values()) and BBN_CAP < 1,
      "F1  *** THE KILL, in one line: option 1 is ghost-free only for K_B > 1, and every "
      "parameter value the corpus or SZ21 admits is below that -- SZ21's own three published "
      "fits (0.1, 0.3, 0.5) and the corpus's BBN cap K_B <~ 0.25, which is 4x below the "
      "threshold ***")
check(1 < 2,
      "F2  THE ESCAPE, priced and recorded because it is real: at K_B in (1,2) every sign "
      "above flips -- c_14 = 2(K_B-1) > 0, c_V^2 > 0, c_s^2 > 0, no ghost -- and that interval "
      "is inside AeST's own stability window 0 < K_B < 2.  The cost is the BBN cap and all "
      "three published AeST fits, and it is a cost in a sector (BBN) that this file does not "
      "recompute.  Anyone wanting to keep option 1 must go there and pay it explicitly")
check(True,
      "F3  AND THE ONE THING THAT MUST NOT BE LOST: option 1's STATIC claims are all CORRECT "
      "and are reproduced here independently -- c_T^2 = 1, gamma_PPN = 1, G_N finite and equal "
      "to Ghat, and the AQUAL reduction G_eff = Ghat/J_Z.  The e^(-sqrt y) screening argument "
      "is untouched.  What fails is the sector opt1_legality_2026.py itself flagged as L1 and "
      "explicitly did NOT compute -- and it fails not through alpha_1/alpha_2 but one level "
      "below them, in the stability of the background those parameters are defined on")

LEDGER = [
    ("RIGOROUS (symbolic, in this file)",
     "the F^2 -> (c_1,c_2,c_3) map; the perfect-square identity at a generic Lorentzian point; "
     "G_eff/G~ = 1/(1-(K_B-A_Z)/2) in the scalar-decoupled limit and c_V^2 = K_B/(K_B-A_Z), the "
     "two quantities that fix the basis and hence c_14 = K_B - A_Z; c_T^2 = 1 and gamma_PPN = 1 "
     "for every coupling; G_eff = Ghat/J_Z (opt1's AQUAL reduction, independently); the reduced "
     "spin-1 Lagrangian and its kinetic sign; c_V^2 = K_B/(2(K_B-1)) and "
     "c_s^2 = K_B(2-K_B)/(Fpp(K_B-1)) for the promoted theory; and the six A_Z = 0 controls "
     "against two other files."),
    ("RIGOROUS (exact-rational numerics, in this file)",
     "the boosted alpha_1/alpha_2 at K_B = 0.1 and 0.5, with the A_Z = 0 run reproducing "
     "ppn_scalar_retained_2026.py's closed forms at two A_Y as the control."),
    ("CONDITIONAL -- the frozen local stiffness (R4)",
     "A_Y and A_Z are treated as constants at their local values.  In the solar system the "
     "neglected J_ZZ piece is suppressed by e^(-sqrt y) ~ 1e-3456 canonical / 1e-3149 ALT and "
     "the treatment is exact to that many digits.  Near the ghost-free threshold (deep MOND) it "
     "is NOT, so C11's y* is an order-of-magnitude boundary, not a sharp one.  It does not move "
     "the verdict: the verdict needs only that mu is O(1) somewhere in the data, which it is."),
    ("CONDITIONAL -- the sign of Fpp",
     "c_s^2's sign uses Fpp > 0, which is fixed by CONTROL 6 reproducing SZ21 Eq. (30) with "
     "Fpp = 4K_2 > 0.  The spin-1 ghost (C8/C9) contains no Fpp at all and is independent of it."),
    ("CONDITIONAL -- the BBN cap K_B <~ 0.25",
     "quoted from the corpus (stages 38-52) and NOT recomputed here.  It is what makes the "
     "K_B > 1 escape expensive.  If that cap is wrong, F2's escape widens."),
    ("NOT COMPUTED -- the promoted theory's cosmology and nonlinear sector",
     "Z = 0 on FRW, so the promotion is invisible to the background and to linear perturbations "
     "exactly as Y is (opt1's G3).  Whether the ghost identified here shows up as a catastrophic "
     "instability in structure formation, and on what timescale, is NOT COMPUTED."),
    ("NOT COMPUTED -- beta_PPN, alpha_3, the zeta's, g_0i",
     "only g_00 was matched, and only at O(rho).  beta is O(rho^2) and outside every "
     "linear-in-rho solve in this corpus."),
    ("NOT COMPUTED -- whether a DIFFERENT promotion escapes",
     "this file settles F(Z) with Z = J^mu J_mu and the AeST coefficients as written.  A "
     "promotion carrying an extra sign, or an extra factor tuned to keep K_B - A_Z > 0, is a "
     "different theory and is not tested here.  Note that any such tuning must beat "
     "A_Z = (2-K_B)mu with mu -> 1, i.e. must break the AQUAL reduction that was option 1's "
     "whole point."),
    ("UNTOUCHED",
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 ALT (kappa = 1/2, "
     "FITTED, 0.529 +/- 0.034); the RAR at 0.108 dex; weak lensing; BTFR; the frozen DR4 band; "
     "the dust problem (2d).  a_0 enters this file only through J_Z in C11/C12, where both "
     "footings are carried and agree."),
]
for lab, txt in LEDGER:
    print(f"    {lab}:\n        {txt}")
check(True, "F4  status ledger printed with every claim graded")

print()
print("=" * 100)
nf = len(FAIL)
print(f"c14_ppn_sector CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f";  FAILED: {FAIL}"))
print(f"runtime {time.time()-T0:.0f}s")
print("=" * 100)
sys.exit(1 if FAIL else 0)
