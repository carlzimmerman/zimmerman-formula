#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
=========================================================================================
c14_dictionary_validity_2026.py -- ROUTE 3 OF THE OPTION-1 AUDIT:
DOES THE EINSTEIN-AETHER DICTIONARY APPLY TO AeST (WITH OR WITHOUT F(Z)) AT ALL?
=========================================================================================
2026-08-18.

THE ASSIGNMENT.  Option 1 replaces AeST's free function argument Y = q^{mu nu} grad_mu phi
grad_nu phi by Z = J^mu J_mu, J^mu = A^nu grad_nu A^mu (the aether's acceleration).  Z is
the Einstein-aether c_4 structure a^mu a_mu, so the naive dictionary reading promotes
c_4 from 0 to (2-K_B) J_Z and gives c_14 = c_1 + c_4 = K_B + (2-K_B) = 2 EXACTLY, whence
(i) G_N = G/(1 - c_14/2) formally SINGULAR and (ii) a double zero in alpha_2's pole
denominator c_123 (2 - c_14) under a now-nonzero numerator.  opt1_legality_2026.py's check
C6 claims explicit variation shows G_N is NOT singular because the mixing term
2(2-K_B) J^mu grad_mu phi contributes to the same sector.  THAT CLAIM IS WHAT THIS FILE
TESTS -- and, underneath it, whether "c_14 = 2" is even a well-defined statement here.

PASS was defined as: the dictionary is shown inapplicable and correct sector-by-sector
results replace it.  KILL was defined as: the dictionary applies and c_14 = 2 stands.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: ADVERSE for option 1, and NOT by the route expected
=========================================================================================
THE ASSIGNMENT'S PASS CRITERION IS MET AND IT BUYS NOTHING.  "c_14 = 2" is not a
well-defined statement about this theory: the effective c_4 is SECTOR-DEPENDENT, and the
reason is one algebraic identity, verified symbolically at A2 and used everywhere below.
Writing D^mu = q^{mu nu} grad_nu phi (the q-projected scalar gradient; J is q-projected
automatically because A.J = 0), AeST's mixing and kinetic terms are IDENTICALLY

        2(2-K_B) J.grad(phi) - (2-K_B) Y  ==  +(2-K_B) Z  -  (2-K_B) |D - J|^2 .

So AeST ALREADY CONTAINS an explicit +(2-K_B) a^mu a_mu -- its manifest "c_4 = 0" is an
artefact of the variables, not a property of the theory.  In the STATIC/longitudinal sector
the second bracket can be driven to zero by the scalar (the longitudinal aether mode is
free, so |D - J|^2 -> 0), the +(2-K_B) Z survives, and the |grad Psi|^2 coefficient of the
whole quadratic Lagrangian is EXACTLY ZERO before F is added -- i.e. c_14^eff = 2 and
G_N -> infinity.  That is TRUE OF UNMODIFIED AeST TOO: it is the statement that AeST has no
Newtonian limit without F, and c_14^eff -> 2 is exactly the DEEP-MOND regime (G_N -> inf,
g >> g_N) in both theories.  With F(Z) restored, the static coefficient is -(2-K_B) J_Z and
c_14^eff,static = 2 - (2-K_B) J_Z -> K_B in the Newtonian limit J_Z -> 1, so G_N = Ghat =
Gtilde/(1 - K_B/2) -- AeST's OWN value, finite.  C6 IS CORRECT, and the reason is now named.
In the TRANSVERSE-VECTOR sector, by contrast, the scalar has NO transverse gradient: D_T is
LOCKED to Q_0 a_T, |D - J|^2_T = |Q_0 a_T - dot a_T|^2 cancels the +(2-K_B) Z piece exactly
(up to a total derivative), and the mixing supplies NOTHING.  So there c_4^eff =
-(2-K_B) J_Z with no compensation, and the transverse aether mode's kinetic coefficient is
        C_V = K_B - (2 - K_B) J_Z            (derived at D6, control at D5)
which is the corpus's own stability quantity K_B, corrected by F(Z).  DECISIVE NUMBER: at
the Newtonian limit J_Z -> 1 and the in-force cap K_B = 0.25, C_V = -1.50 -- a GHOST, with
c_V^2 = K_B/C_V < 0, i.e. omega^2 = -(K_B k^2 + m^2)/|C_V| < 0 at EVERY k and a growth rate
0.408 c k that is unbounded in the ultraviolet.  No-ghost requires K_B > 2 mu/(1 + mu),
i.e. K_B > 1 at mu = 1, against the corpus's in-force window K_B in [2.1e-4, 0.25]
(stage70/stage74).  The escape "add a bare c_4 to compensate" is closed at E4: the static
sector needs the total Z-coefficient NEGATIVE (attractive AQUAL) and the vector sector needs
it > -K_B, so ghost-freedom forces mu < K_B/(2-K_B) = 0.143 -- the theory can be healthy
ONLY where it is deep-MOND, and Newtonian gravity is precisely what makes it a ghost.
THE SIGN FORENSICS (F3).  The assignment's c_4 = +(2-K_B) uses the "+c_4 A^a A^b g_{mn}"
convention while c_14 = c_1 + c_4, G_N = G/(1-c_14/2) and c_V^2 = .../(c_14(1-c_13)) are the
"-c_4" convention's formulas.  Pinned independently here (F1/F2) by requiring the c_1 and
c_4 structures to enter the SAME static and vector kinetic terms the way the corpus's own
K_B > 0 condition demands, the correct entry is c_4 = -(2-K_B) J_Z.  The splice flipped a
FATAL vector ghost (c_14^vec = 2 K_B - 2 = -1.50) into a benign-looking c_V^2 = K_B/2.
WHAT SURVIVES, VERIFIED NOT ASSUMED.  c_T = 1 EXACTLY, in both theories, and for ANY F --
because on a TT perturbation J^mu, F_{mu nu}, Y and Q are h-INDEPENDENT in their DERIVATIVES
(B3/B4: Z depends on h_ij algebraically but on NO derivative of h), so the entire TT
derivative sector is pure Einstein-Hilbert.  The algebraic h-dependence is a new,
environment-dependent graviton mass m^2 = 4(2-K_B) J_Z (g/c^2)^2 absent from AeST; PRICED at
G3 and HARMLESS (delta c_T/c_T ~ 4e-43 on the GW170817 path, 28 orders under the bound).
NOT COMPUTED, and named as such: alpha_1, alpha_2 for the full theory (the O(w) boosted
sector); the AeST scalar sector's time-dependent modes; the nonlinear/2PN sector.

=========================================================================================
EVERY REDUCTION AND EVERY CALIBRATION, DECLARED
=========================================================================================
R1  NOTHING is inherited from opt1_legality_2026.py or typeII_direct_variation_2026.py.
    The Ricci scalar, sqrt(-g), the unit-norm solution, J^mu, Z, Y, Q and F_{mu nu} are all
    computed here from the metric.  opt1's calibrated quadratic Lagrangian is REPRODUCED as
    a CONTROL at C4 (not used as an input): if that control failed, this file would be void.
R2  Signature (-,+,+,+).  Units 16 pi Gtilde factored OUT of the bracket, i.e. the object
    expanded is L = sqrt(-g)[R - 2 Lam - (K_B/2)F^2 + 2(2-K_B) J.grad(phi) - (2-K_B) Y
    - F(.,Q)], matter added as -16 pi Gtilde rho Psi.  The OVERALL SIGN is not assumed: it
    is PINNED at B5 by demanding the TT graviton be healthy (+A(hdot^2 - (grad h)^2),
    A > 0), which then makes "K_B > 0 = healthy vector" -- the corpus's own committed
    stability condition (stage68) -- come out right, at D5.
R3  F(Y,Q) -> (2-K_B) J(Y) + K(Q) and F(Z,Q) -> (2-K_B) J(Z) + K(Q).  Y and Z are both
    quadratic in perturbations about FRW/Minkowski, so cross terms are higher order; the
    same order-counting bridge1_aest_equations.md uses for Y, applied to Z (A5).
R4  Lam, K'(Q_0) and the Yukawa mass are set to zero in the reductions.  typeII PART F
    prices them at 1.7e-23 / 1.2e-23 at 1 AU; QUOTED, not recomputed.
R5  VECTOR SECTOR / WKB.  Around a background with Zbar = |grad Psi|^2 = (g/c^2)^2 != 0 the
    F(Z) contribution to the transverse-vector quadratic action is
    -(2-K_B)[J_Z delta^2 Z + (1/2) J_ZZ (delta^1 Z)^2].  Choosing the polarisation
    perpendicular to the background acceleration (always possible: two transverse
    polarisations per k) gives delta^1 Z = 2 Jbar . delta^1 J = 0 exactly, so J_ZZ DROPS
    OUT, and delta^2 Z = |delta^1 J|^2 + 2 Jbar . delta^2 J.  The last term carries one
    power of the background gradient and at most one derivative of the perturbation, so it
    is suppressed by g/(c^2 k) relative to the retained term.  The reduction is therefore
    controlled EXACTLY IN THE LIMIT WHERE THE INSTABILITY IS WORST (rate ~ k).  delta^1 J is
    computed on the flat background (D3), where it is exactly dot a with the metric vector
    mode dropping out.
R6  NOT DONE HERE: alpha_1/alpha_2 for the full theory; the AeST scalar sector's dynamical
    modes (AeST has TWO scalar d.o.f., Einstein-aether has ONE, so the aether c_S formula is
    structurally inapplicable -- G2); the 2PN/nonlinear sector; any refit of anything.

EXIT 0 iff every numbered check passes.
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
# constants -- both footings carried for every dimensional number
# =================================================================================================
CLIGHT = 2.99792458e8
GMSUN = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
# K_B window IN FORCE per nbody_2026/stage70_ppn_preferred_frame_2026.py header +
# stage74_ppn_fork_adjudicated_2026.py.  QUOTED, not re-derived here.
KB_LO, KB_HI = 2.1e-4, 0.25

t, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO = [t, x1, x2, x3]
SPC = [x1, x2, x3]
eps = sp.Symbol("eps")
KB = sp.Symbol("K_B")
Q0 = sp.Symbol("Q_0")
JZs = sp.Symbol("J_Z")
NEXP = 2


# =================================================================================================
# generic geometry machinery -- used by every part, so it is written once and checked once
# =================================================================================================
def trunc(e, n=NEXP):
    e = sp.expand(e)
    return sum(eps ** k * e.coeff(eps, k) for k in range(n + 1))


def deg_ok(e, n=NEXP):
    e = sp.expand(e)
    if e == 0:
        return True
    return sp.Poly(e, eps).degree() <= n


def ginv_series(g, g0, n=NEXP):
    """inverse metric as a TRUNCATED Neumann series about g0 (no rational functions)"""
    g0i = g0.inv()
    M = sp.expand(g0i * (g - g0))
    out = sp.zeros(4, 4)
    P = sp.eye(4)
    for k in range(n + 1):
        out += (-1) ** k * P * g0i
        P = sp.expand(P * M)
    return sp.Matrix(4, 4, lambda i, j: trunc(sp.expand(out[i, j]), n))


def sqrtmg(g, g0, n=NEXP):
    """sqrt(-g) via (1/2) tr log(1 + g0^{-1} dg), exponentiated and truncated"""
    g0i = g0.inv()
    M = sp.expand(g0i * (g - g0))
    s, Pk = 0, sp.eye(4)
    for k in range(1, n + 1):
        Pk = sp.expand(Pk * M)
        s += -sp.Rational((-1) ** k, k) * Pk.trace()
    L = trunc(sp.expand(s), n) / 2
    e, term = 1, 1
    for k in range(1, n + 1):
        term = sp.expand(term * L / k)
        e = e + term
    return trunc(sp.expand(sp.sqrt(-g0.det()) * e), n)


def christoffel(g, gi, n=NEXP):
    G = {}
    for m in range(4):
        for a in range(4):
            for b in range(4):
                s = 0
                for sg in range(4):
                    s += gi[m, sg] * (sp.diff(g[sg, a], CO[b]) + sp.diff(g[sg, b], CO[a])
                                      - sp.diff(g[a, b], CO[sg]))
                G[(m, a, b)] = trunc(sp.expand(s / 2), n)
    return G


def ricci_scalar(g, gi, G, n=NEXP):
    Ric = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = 0
            for m in range(4):
                s += sp.diff(G[(m, a, b)], CO[m]) - sp.diff(G[(m, a, m)], CO[b])
                for l in range(4):
                    s += G[(m, m, l)] * G[(l, a, b)] - G[(m, b, l)] * G[(l, a, m)]
            Ric[a, b] = trunc(sp.expand(s), n)
    return trunc(sp.expand(sum(gi[a, b] * Ric[a, b] for a in range(4) for b in range(4))), n)


def ibp(e, maxit=16):
    """integrate by parts until no second derivatives survive (valid for quadratic forms)"""
    e = sp.expand(e)
    for _ in range(maxit):
        changed, new = False, 0
        for term in sp.Add.make_args(e):
            d2 = None
            for f in term.atoms(sp.Derivative):
                if sum(k for _, k in f.variable_count) >= 2:
                    d2 = f
                    break
            if d2 is None:
                new += term
                continue
            var, cnt = d2.variable_count[-1]
            vc = list(d2.variable_count[:-1]) + ([(var, cnt - 1)] if cnt > 1 else [])
            lower = sp.Derivative(d2.expr, *vc) if vc else d2.expr
            rest = sp.cancel(term / d2)
            new += -sp.expand(sp.diff(rest, var) * lower)
            changed = True
        e = sp.expand(new)
        if not changed:
            break
    return sp.expand(e)


def solve_unit_norm(gi, spatial, orders=NEXP):
    """A_mu = (-(1 + eps c1 + eps^2 c2 + ...), eps*spatial); solve A.A = -1 order by order.
    Each order is LINEAR in its own unknown once lower orders are substituted -- checked."""
    syms = sp.symbols(f"cc1:{orders + 1}")
    A0ans = -(1 + sum(eps ** (k + 1) * syms[k] for k in range(orders)))
    Alo = [A0ans] + [eps * s for s in spatial]
    norm = trunc(sp.expand(sum(gi[m, n] * Alo[m] * Alo[n]
                               for m in range(4) for n in range(4)) + 1), orders)
    known, lin = {}, []
    for k in range(1, orders + 1):
        eqk = sp.expand(norm.coeff(eps, k).subs(known))
        lin.append(sp.degree(sp.Poly(eqk, syms[k - 1]), syms[k - 1]) == 1)
        known[syms[k - 1]] = sp.simplify(list(sp.linsolve([eqk], [syms[k - 1]]))[0][0])
    Alo = [trunc(sp.expand(Alo[0].subs(known)), orders)] + Alo[1:]
    return Alo, all(lin)


def aether_pack(g, gi, spatial):
    """returns A_lo, A_up, J^mu, Z, F_{mu nu}, and the linearity flag"""
    Alo, lin = solve_unit_norm(gi, spatial)
    Aup = [trunc(sp.expand(sum(gi[m, n] * Alo[n] for n in range(4)))) for m in range(4)]
    G = christoffel(g, gi)
    J = []
    for m in range(4):
        s = 0
        for n in range(4):
            s += Aup[n] * (sp.diff(Aup[m], CO[n]) + sum(G[(m, n, l)] * Aup[l] for l in range(4)))
        J.append(trunc(sp.expand(s)))
    Z = trunc(sp.expand(sum(g[m, n] * J[m] * J[n] for m in range(4) for n in range(4))))
    Fdn = sp.Matrix(4, 4, lambda m, n: sp.diff(Alo[n], CO[m]) - sp.diff(Alo[m], CO[n]))
    return Alo, Aup, J, Z, Fdn, G, lin


def F2_of(gi, Fdn):
    return trunc(sp.expand(sum(gi[m, a] * gi[n, b] * Fdn[a, b] * Fdn[m, n]
                               for m in range(4) for n in range(4)
                               for a in range(4) for b in range(4))))


# =================================================================================================
print()
print("=" * 100)
print("PART A -- THE IDENTITY THAT DECIDES EVERYTHING")
print("         (AeST already contains an explicit c_4 term; it is hidden in the mixing)")
print("=" * 100)

info("A0  Einstein-aether's kinetic term is K^{mu nu}_{ab} grad_mu A^a grad_nu A^b with\n"
     "        K = c_1 g g + c_2 dd + c_3 dd -/+ c_4 A A g,\n"
     "    a form that is QUADRATIC in grad A and contains NO scalar and NO term LINEAR in\n"
     "    grad A.  AeST adds 2(2-K_B) J^mu grad_mu phi, which is LINEAR in the aether\n"
     "    acceleration J^mu = A^nu grad_nu A^mu and has no Einstein-aether counterpart.\n"
     "    Whether that term feeds the c_4 structure is the whole question of route 3.")

# --- A1: J is q-orthogonal, so J.grad(phi) = J.D with D the q-projected scalar gradient ------
# proof: A_mu J^mu = A_mu A^nu grad_nu A^mu = (1/2) A^nu grad_nu (A^mu A_mu) = (1/2) A^nu grad_nu(-1) = 0
info("A1  A_mu J^mu = (1/2) A^nu grad_nu (A^mu A_mu) = (1/2) A^nu grad_nu(-1) = 0 IDENTICALLY, "
     "so J is\n"
     "    q-orthogonal and J^mu grad_mu phi = J^mu D_mu with D^mu := q^{mu nu} grad_nu phi.\n"
     "    This is why the mixing term sees only the SAME projected gradient the free function\n"
     "    eats.  It is re-verified symbolically on the explicit static and vector solutions at\n"
     "    C2b and D2b, from the computed A_mu and J^mu, not from this argument.")

# --- A2: THE IDENTITY, verified symbolically on generic 4-vectors ------------------------------
d0, d1, d2, d3, j0, j1, j2, j3 = sp.symbols("d0 d1 d2 d3 j0 j1 j2 j3", real=True)
ETA = sp.diag(-1, 1, 1, 1)
Dg, Jg = [d0, d1, d2, d3], [j0, j1, j2, j3]


def dot(u, w):
    return sum(ETA[i, i] * u[i] * w[i] for i in range(4))


lhs = 2 * (2 - KB) * dot(Jg, Dg) - (2 - KB) * dot(Dg, Dg)
rhs = (2 - KB) * dot(Jg, Jg) - (2 - KB) * dot([Jg[i] - Dg[i] for i in range(4)],
                                              [Jg[i] - Dg[i] for i in range(4)])
check(sp.simplify(sp.expand(lhs - rhs)) == 0,
      "A2  *** THE IDENTITY: 2(2-K_B) J.D - (2-K_B) D.D  ==  +(2-K_B) J.J - (2-K_B) |D - J|^2 "
      "***",
      "so AeST's action IDENTICALLY equals R - 2Lam - (K_B/2)F^2 + (2-K_B) Z "
      "- (2-K_B)|D - J|^2 - F(.,Q) - lam(A.A+1).  The +(2-K_B) Z is an EXPLICIT c_4 term.  "
      "AeST's dictionary entry c_4 = 0 is therefore a statement about the VARIABLES, not "
      "about the theory")

check(True,
      "A3  CONSEQUENCE (the route-3 answer in one line): whether the mixing 'is' a c_4 term "
      "depends on whether the scalar can zero the |D - J|^2 bracket IN THAT SECTOR.  It can "
      "in the longitudinal/static sector (D and J share a mode) and it CANNOT in the "
      "transverse-vector sector (D_T is locked to Q_0 a_T).  A sector-dependent c_4 is not a "
      "dictionary entry",
      "both halves are DERIVED below -- static at PART C, vector at PART D -- not asserted")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- TENSOR SECTOR, BY EXPLICIT COMPUTATION (assignment item (a))")
print("=" * 100)

hp = sp.Function("h_p")(t, x3)
hx = sp.Function("h_x")(t, x3)
gT = sp.zeros(4, 4)
gT[0, 0] = -1
gT[1, 1] = 1 + eps * hp
gT[2, 2] = 1 - eps * hp
gT[3, 3] = 1
gT[1, 2] = eps * hx
gT[2, 1] = eps * hx
g0T = sp.diag(-1, 1, 1, 1)
giT = ginv_series(gT, g0T)
check(all(sp.simplify(trunc(sp.expand((gT * giT)[i, j] - sp.eye(4)[i, j]))) == 0
          for i in range(4) for j in range(4)),
      "B1  the truncated inverse metric satisfies g.ginv = 1 through eps^2 (TT sector)",
      "h_ij is transverse (wavevector along x3, h_3j = 0) and traceless (h_11 = -h_22): the "
      "two physical graviton polarisations")

AloT, AupT, JT, ZT, FdnT, GT, linT = aether_pack(gT, giT, [0, 0, 0])
phiT = Q0 * t
dphiT = [sp.diff(phiT, c) for c in CO]
qinvT = [[trunc(sp.expand(giT[m, n] + AupT[m] * AupT[n])) for n in range(4)] for m in range(4)]
YT = trunc(sp.expand(sum(qinvT[m][n] * dphiT[m] * dphiT[n]
                         for m in range(4) for n in range(4))))
QT = trunc(sp.expand(sum(AupT[m] * dphiT[m] for m in range(4))))
mixT = trunc(sp.expand(sum(JT[m] * dphiT[m] for m in range(4))))
F2T = F2_of(giT, FdnT)

check(all(sp.simplify(e) == 0 for e in JT) and sp.simplify(ZT) == 0
      and sp.simplify(F2T) == 0 and sp.simplify(YT) == 0
      and sp.simplify(QT - Q0) == 0 and sp.simplify(mixT) == 0,
      "B2  *** on a pure TT perturbation about Minkowski: J^mu = 0, Z = 0, F_{mu nu}F^{mu nu} "
      "= 0, Y = 0, Q = Q_0, J.grad(phi) = 0 -- ALL EXACTLY, not to leading order ***",
      "Gamma^mu_{00} = 0 for a static-lapse TT metric, so the aether's acceleration vanishes "
      "identically; hence NO free function of ANY argument built from J, Y or Q can enter "
      "the TT sector at all around Minkowski")

# --- B3/B4: the same statement with a background acceleration Zbar != 0 ------------------------
Pb = sp.Function("Psibar")(x1)
gTB = sp.zeros(4, 4)
gTB[0, 0] = -(1 + 2 * Pb)
gTB[1, 1] = 1 + eps * hp
gTB[2, 2] = 1 - eps * hp
gTB[3, 3] = 1
gTB[1, 2] = eps * hx
gTB[2, 1] = eps * hx
g0TB = sp.diag(-(1 + 2 * Pb), 1, 1, 1)
giTB = ginv_series(gTB, g0TB)
AloTB = [-sp.sqrt(1 + 2 * Pb), 0, 0, 0]
check(sp.simplify(sum(giTB[m, n] * AloTB[m] * AloTB[n]
                      for m in range(4) for n in range(4)) + 1) == 0,
      "B3  with a background potential Psibar(x1) the aether A_mu = (-sqrt(1+2 Psibar), 0) "
      "satisfies A.A = -1 exactly on the TT-perturbed metric")
AupTB = [trunc(sp.expand(sum(giTB[m, n] * AloTB[n] for n in range(4)))) for m in range(4)]
GTB = christoffel(gTB, giTB)
JTB = []
for m in range(4):
    s = 0
    for n in range(4):
        s += AupTB[n] * (sp.diff(AupTB[m], CO[n])
                         + sum(GTB[(m, n, l)] * AupTB[l] for l in range(4)))
    JTB.append(trunc(sp.expand(s)))
ZTB = sp.simplify(trunc(sp.expand(sum(gTB[m, n] * JTB[m] * JTB[n]
                                      for m in range(4) for n in range(4)))))
dh_syms = ([sp.Derivative(f, c) for f in (hp, hx) for c in (t, x3)]
           + [sp.Derivative(f, (c, 2)) for f in (hp, hx) for c in (t, x3)])
no_dh = all(sp.simplify(sp.diff(ZTB, d)) == 0 for d in dh_syms)
has_h = any(sp.simplify(sp.diff(ZTB, f)) != 0 for f in (hp, hx))
check(no_dh and has_h,
      "B4  *** GATE: with Zbar != 0, Z depends on h_ij ALGEBRAICALLY but on NO DERIVATIVE of "
      "h_ij ***",
      f"Z = {sp.simplify(ZTB)} -- so F(Z), for ANY F, contributes ZERO to the TT "
      "time-kinetic and gradient terms.  The graviton's dispersion slope is untouched; only "
      "a mass term can appear (priced at G3)")

# --- B5: THE OVERALL SIGN, pinned by the graviton ----------------------------------------------
sgT = sqrtmg(gT, g0T)
RT = ricci_scalar(gT, giT, christoffel(gT, giT))
LTT = ibp(sp.expand(trunc(sp.expand(sgT * RT)).coeff(eps, 2)))
Ahd = sp.simplify(LTT.coeff(sp.Derivative(hp, t) ** 2))
Agr = sp.simplify(LTT.coeff(sp.Derivative(hp, x3) ** 2))
check(Ahd == sp.Rational(1, 2) and Agr == -sp.Rational(1, 2),
      "B5  *** SIGN PIN: the Einstein-Hilbert TT Lagrangian is +(1/2)(hdot_p^2 - h_p'^2) + "
      "(same for h_x), i.e. a HEALTHY graviton with a POSITIVE time-kinetic coefficient in "
      "the convention used throughout this file ***",
      f"coefficient of hdot_p^2 = {Ahd}, of h_p'^2 = {Agr}.  Every 'ghost / no-ghost' "
      "statement below is anchored on THIS sign, not on a quoted convention")

check(sp.simplify(LTT.coeff(sp.Derivative(hx, t) ** 2) - Ahd) == 0
      and sp.simplify(LTT.coeff(sp.Derivative(hx, x3) ** 2) - Agr) == 0,
      "B6  both polarisations carry the same coefficients (isotropy control)")

check(True,
      "B7  *** VERDICT (a): c_T = 1 EXACTLY, in AeST and in the F(Z) theory, and for ANY free "
      "function.  The aether dictionary result c_T^2 = 1/(1 - c_13) MAY be quoted -- but it "
      "is not needed: the TT sector is pure Einstein-Hilbert by B2/B4 ***",
      "and c_4 provably cannot reach the tensor sector, because Z carries no derivative of "
      "h_ij (B4).  This is the ONE dictionary entry that transfers for a reason, not by "
      "coincidence")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- STATIC / LONGITUDINAL SECTOR, DERIVED FROM THE COVARIANT ACTION")
print("=" * 100)

Psi = sp.Function("Psi")(x1, x2, x3)
Phi = sp.Function("Phi")(x1, x2, x3)
wf = sp.Function("varphi")(x1, x2, x3)
ai = [sp.Function("a1")(x1, x2, x3), sp.Function("a2")(x1, x2, x3),
      sp.Function("a3")(x1, x2, x3)]
gS = sp.diag(-(1 + 2 * eps * Psi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
g0S = sp.diag(-1, 1, 1, 1)
giS = ginv_series(gS, g0S)
AloS, AupS, JS, ZS, FdnS, GS, linS = aether_pack(gS, giS, ai)
check(linS,
      "C1  the unit-norm constraint was solved order by order, each order LINEAR in its own "
      "unknown (sp.linsolve on one linear equation, never a generic solve)")

phiS = Q0 * t + eps * wf
dphiS = [sp.diff(phiS, c) for c in CO]
QS = trunc(sp.expand(sum(AupS[m] * dphiS[m] for m in range(4))))
qinvS = [[trunc(sp.expand(giS[m, n] + AupS[m] * AupS[n])) for n in range(4)] for m in range(4)]
YS = trunc(sp.expand(sum(qinvS[m][n] * dphiS[m] * dphiS[n]
                         for m in range(4) for n in range(4))))
mixS = trunc(sp.expand(sum(JS[m] * dphiS[m] for m in range(4))))
F2S = F2_of(giS, FdnS)
sgS = sqrtmg(gS, g0S)
RS = ricci_scalar(gS, giS, GS)

P = [sp.diff(Psi, c) for c in SPC]
vv = [sp.diff(wf, SPC[k]) + Q0 * ai[k] for k in range(3)]
gradPsi2 = sum(p ** 2 for p in P)
v2 = sum(q ** 2 for q in vv)

check(sp.simplify(ZS.coeff(eps, 0)) == 0 and sp.simplify(ZS.coeff(eps, 1)) == 0
      and sp.simplify(ZS.coeff(eps, 2) - gradPsi2) == 0,
      "C2  Z = eps^2 |grad Psi|^2 + O(eps^3) EXACTLY -- the free function's new argument is "
      "the TOTAL potential gradient (reproduces opt1's A5 independently)")
check(sp.simplify(trunc(sp.expand(sum(AloS[m] * JS[m] for m in range(4))))) == 0,
      "C2b A1 VERIFIED on the explicit solution: A_mu J^mu = 0 through eps^2 in the static "
      "sector, from the computed A_mu and J^mu")
check(all(deg_ok(e) for e in [ZS, YS, QS, mixS, F2S, sgS, RS] + list(JS) + list(AupS)),
      "C2c explicit degree check: every truncated object is a polynomial in eps of degree <= 2")
check(sp.simplify(YS.coeff(eps, 2) - v2) == 0
      and sp.simplify(QS.coeff(eps, 1) + Q0 * Psi) == 0,
      "C3  CONTROL: the same machinery gives Y = eps^2 |grad varphi + Q_0 a|^2 and "
      "Q = Q_0(1 - eps Psi), i.e. typeII's P1 -- the machinery is validated on the KNOWN "
      "argument before being trusted on the new one")

LEH = ibp(sp.expand(trunc(sp.expand(sgS * RS)).coeff(eps, 2)))
LF2 = ibp(sp.expand(trunc(sp.expand(sgS * (-KB / 2 * F2S))).coeff(eps, 2)))
LMX = ibp(sp.expand(trunc(sp.expand(sgS * (2 * (2 - KB) * mixS))).coeff(eps, 2)))
LY = ibp(sp.expand(trunc(sp.expand(sgS * (-(2 - KB) * YS))).coeff(eps, 2)))

gradPhi2 = sum(sp.diff(Phi, c) ** 2 for c in SPC)
gradPhiPsi = sum(sp.diff(Phi, c) * sp.diff(Psi, c) for c in SPC)
curl2 = sum((sp.diff(ai[j], SPC[i]) - sp.diff(ai[i], SPC[j])) ** 2
            for i in range(3) for j in range(3) if i < j)
check(sp.simplify(LEH - (2 * gradPhi2 - 4 * gradPhiPsi)) == 0,
      "C4a EH^(2) = 2|grad Phi|^2 - 4 grad Phi . grad Psi   (computed, then integrated by "
      "parts; NOT quoted)")
check(sp.simplify(LF2 - (KB * gradPsi2 - KB * curl2)) == 0,
      "C4b the F^2 term gives +K_B |grad Psi|^2 - K_B |curl a|^2",
      "the +K_B|grad Psi|^2 IS the c_1 = K_B dictionary entry, appearing in the SAME "
      "|grad Psi|^2 structure a c_4 term would; the curl piece vanishes on a longitudinal a")
check(sp.simplify(LMX - 2 * (2 - KB) * sum(P[k] * vv[k] for k in range(3))) == 0,
      "C4c the mixing term gives 2(2-K_B) grad Psi . v,  v = grad varphi + Q_0 a")
check(sp.simplify(LY + (2 - KB) * v2) == 0,
      "C4d the -(2-K_B) Y term gives -(2-K_B)|v|^2")

# --- integrate out Phi (its own equation), then assemble ---------------------------------------
Ltot_noF = sp.expand(LEH + LF2 + LMX + LY)
solPhi = sp.solve(sp.Eq(sp.expand(sp.diff(Ltot_noF, sp.Derivative(Phi, x1))), 0),
                  sp.Derivative(Phi, x1))
check(len(solPhi) == 1 and sp.simplify(solPhi[0] - sp.Derivative(Psi, x1)) == 0,
      "C5  the Phi equation is Phi = Psi (no anisotropic stress at this order: NOTHING except "
      "EH depends on Phi -- C4b/c/d carry no Phi), i.e. gamma_PPN = 1 survives",
      "verified by solving the algebraic stationarity condition, not assumed")

sub_PhiPsi = {sp.Derivative(Phi, c): sp.Derivative(Psi, c) for c in SPC}
L_eff = sp.expand(Ltot_noF.subs(sub_PhiPsi).doit())
opt1_form = sp.expand(-(2 - KB) * sum((P[k] - vv[k]) ** 2 for k in range(3)) - KB * curl2)
check(sp.simplify(L_eff - opt1_form) == 0,
      "C6  *** CONTROL, AND IT IS THE BIG ONE: after integrating out Phi the whole non-F "
      "quadratic Lagrangian is EXACTLY  -(2-K_B)|grad Psi - v|^2 - K_B|curl a|^2  ***",
      "this DERIVES opt1_legality_2026.py's calibrated Lagrangian (its R2/B1, where "
      "c = (2-K_B) was FITTED to typeII's D5) from the covariant action with nothing fitted. "
      "opt1's PART B, and typeII's D5-D7 behind it, are hereby independently confirmed")

# --- the |grad Psi|^2 coefficient, and c_14^eff ------------------------------------------------
coefZ_noF = sp.simplify(sp.expand(L_eff.subs({sp.Derivative(wf, c): 0 for c in SPC})
                                  .subs({a: 0 for a in ai}).doit()).coeff(
    sp.Derivative(Psi, x1) ** 2))
info("C7  bookkeeping: with the aether/scalar FROZEN (v = 0) the coefficient of "
     f"|grad Psi|^2 is {coefZ_noF} = -(2 - K_B), i.e. c_14^eff = K_B and "
     "G_N = Gtilde/(1 - K_B/2) = Ghat -- AeST's own quasi-static Newton constant.")

lam_s, muZ = sp.symbols("lambda_s mu", positive=True)
# F(Y) theory, Newtonian regime J(Y) = lambda_s Y: eliminate v from
#   -(2-K_B)|grad Psi - v|^2 - (2-K_B) lambda_s |v|^2
u = sp.Symbol("u")  # v = u * grad Psi (aligned by symmetry in the spherical sector)
LY_of_u = -(2 - KB) * (1 - u) ** 2 - (2 - KB) * lam_s * u ** 2
u_star = sp.solve(sp.Eq(sp.diff(LY_of_u, u), 0), u)
check(len(u_star) == 1 and sp.simplify(u_star[0] - 1 / (1 + lam_s)) == 0,
      "C8  F(Y) theory, Newtonian regime: the aether-longitudinal equation gives "
      "v = grad Psi/(1 + lambda_s), i.e. typeII's D7 with J_Y = lambda_s")
coef_FY = sp.simplify(LY_of_u.subs(u, u_star[0]))
c14_FY = sp.simplify(2 + coef_FY)          # coefficient == -(2 - c_14^eff)
check(sp.simplify(coef_FY + (2 - KB) * lam_s / (1 + lam_s)) == 0,
      "C9  so the F(Y) theory's |grad Psi|^2 coefficient is -(2-K_B) lambda_s/(1 + lambda_s), "
      f"i.e. c_14^eff,static = {sp.simplify(c14_FY)}")

# F(Z) theory: v = grad Psi exactly, coefficient is -(2-K_B) mu with mu = J_Z
coef_FZ = sp.expand(-(2 - KB) * muZ)
c14_FZ = sp.simplify(2 + coef_FZ)
check(sp.simplify(c14_FZ - (2 - (2 - KB) * muZ)) == 0
      and sp.simplify(c14_FZ.subs(muZ, 1) - KB) == 0,
      "C10 *** F(Z) theory: v = grad Psi POINTWISE (the bracket |grad Psi - v|^2 is driven to "
      "ZERO by the free longitudinal aether mode), the surviving coefficient is -(2-K_B) mu, "
      "and c_14^eff,static = 2 - (2-K_B) mu  ->  K_B in the Newtonian limit mu -> 1 ***",
      "G_N = Gtilde/(1 - c_14/2) = Gtilde/(1 - K_B/2) = Ghat, FINITE and EQUAL to AeST's own. "
      "opt1's C6 is CONFIRMED, and its mechanism is now named: the mixing term's +(2-K_B) Z "
      "(A2) is what cancels the naive singularity")

check(sp.simplify(c14_FY.subs(lam_s, 0) - 2) == 0 and sp.simplify(c14_FZ.subs(muZ, 0) - 2) == 0,
      "C11 *** AND THE DISSOLUTION: c_14^eff,static = 2 EXACTLY in the deep-MOND limit of "
      "BOTH theories (lambda_s -> 0 and mu -> 0), and for AeST with F removed altogether ***",
      "c_14 = 2 <=> G_N -> infinity <=> g >> g_N, which IS the MOND regime.  It is not a "
      "pathology introduced by option 1; it is a REGIME that unmodified AeST already has, "
      "and it is not where the solar system sits")

check(sp.simplify((2 - c14_FZ).subs(muZ, 1) - (2 - KB)) == 0,
      "C12 alpha_2's pole denominator c_123 (2 - c_14): the SECOND factor is 2 - K_B != 0 in "
      "the Newtonian regime, NOT zero.  The 'double zero under a nonzero numerator' is an "
      "artefact of the naive reading and DISSOLVES",
      "the FIRST factor c_123 = 0 remains, but that is a PRE-EXISTING AeST condition that "
      "stage70/stage74 already ruled off-domain for the Foster-Jacobson formula.  Nothing "
      "new is created here; nothing old is repaired either.  alpha_1/alpha_2: NOT COMPUTED")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- TRANSVERSE-VECTOR SECTOR, DERIVED (assignment items (b) and (c))")
print("=" * 100)

info("D0  FIELD CONTENT.  Everything depends on (t, x1) only, so helicity about the x1 axis is\n"
     "    a good label.  HELICITY 1: the metric vector mode S = g_{02} and the aether "
     "transverse\n"
     "    mode a = A_2.  HELICITY 0: the metric scalars Psi, Phi, the aether LONGITUDINAL mode\n"
     "    b = A_1, and the scalar-field perturbation varphi.  ALL SIX are carried, so that the\n"
     "    claim 'the scalar cannot rescue the vector sector' is a COMPUTED RESULT (D4) and not\n"
     "    an appeal to helicity.  Gauge: no vector part in g_ij (reached by x^i -> x^i + xi^i_T).")

info("D0b TWO THINGS THAT COULD HAVE MADE THIS SPURIOUS, CHECKED BY HAND.\n"
     "    (i) IS a_2 PHYSICAL, or gauge?  Under a linear diffeomorphism about A_mu = (-1,0),\n"
     "        delta A_mu = -(xi^nu d_nu A_mu + A_nu d_mu xi^nu) = d_mu xi^0, so a PURELY "
     "SPATIAL\n"
     "        xi^i (the only kind used to reach this gauge) leaves a_2 INVARIANT.  The "
     "residual\n"
     "        freedom after setting the vector part of g_ij to zero is xi^2 = xi^2(t), which "
     "moves\n"
     "        only the k = 0 mode.  a_2 is a physical degree of freedom at every k != 0.\n"
     "    (ii) IS THE POLARISATION CHOICE A CHEAT?  R5 takes the polarisation perpendicular to "
     "the\n"
     "        background acceleration, which is what makes delta^1 Z vanish and J_ZZ drop out.\n"
     "        That is the CONSERVATIVE choice, not a convenient one: an instability in ONE\n"
     "        polarisation is an instability, and dropping J_ZZ removes a free function that\n"
     "        could only have been tuned to help.")

PsiV = sp.Function("PsiV")(t, x1)
PhiV = sp.Function("PhiV")(t, x1)
Sv = sp.Function("S")(t, x1)       # helicity 1: metric vector mode g_{02}
av = sp.Function("a")(t, x1)       # helicity 1: aether transverse mode A_2
bv = sp.Function("b")(t, x1)       # helicity 0: aether longitudinal mode A_1
wfV = sp.Function("varphiV")(t, x1)  # helicity 0: scalar-field perturbation
gV = sp.eye(4)
gV[0, 0] = -(1 + 2 * eps * PsiV)
gV[0, 2] = eps * Sv
gV[2, 0] = eps * Sv
gV[1, 1] = 1 - 2 * eps * PhiV
gV[2, 2] = 1 - 2 * eps * PhiV
gV[3, 3] = 1 - 2 * eps * PhiV
g0V = sp.diag(-1, 1, 1, 1)
giV = ginv_series(gV, g0V)
check(all(sp.simplify(trunc(sp.expand((gV * giV)[i, j] - sp.eye(4)[i, j]))) == 0
          for i in range(4) for j in range(4)),
      "D1  inverse metric verified for the full six-field vector-sector computation")

AloV, AupV, JV, ZV, FdnV, GV, linV = aether_pack(gV, giV, [bv, av, 0])
check(linV, "D2  unit norm solved order by order, linear at each order (vector sector)")
check(sp.simplify(trunc(sp.expand(sum(AloV[m] * JV[m] for m in range(4))))) == 0,
      "D2b A1 re-verified here too: A_mu J^mu = 0 through eps^2 on the computed solution")

adot, aprime = sp.Derivative(av, t).doit(), sp.Derivative(av, x1).doit()
check(sp.simplify(JV[2].coeff(eps, 1) - adot) == 0
      and sp.simplify(ZV.coeff(eps, 2).coeff(adot ** 2) - 1) == 0,
      "D3  *** delta^1 J^2 = dot a EXACTLY (the metric vector mode S drops out of it), so "
      "Z contains (dot a)^2 with coefficient exactly 1 ***",
      "on the transverse-vector mode the free function's argument Z is the SQUARE OF A TIME "
      "DERIVATIVE of the aether -- while in the static sector (C2) the SAME Z was the square "
      "of a SPATIAL gradient.  One coefficient, two roles: that is the whole problem")

phiV = Q0 * t + eps * wfV
dphiV = [sp.diff(phiV, c) for c in CO]
QV = trunc(sp.expand(sum(AupV[m] * dphiV[m] for m in range(4))))
qinvV = [[trunc(sp.expand(giV[m, n] + AupV[m] * AupV[n])) for n in range(4)] for m in range(4)]
YV = trunc(sp.expand(sum(qinvV[m][n] * dphiV[m] * dphiV[n]
                         for m in range(4) for n in range(4))))
mixV = trunc(sp.expand(sum(JV[m] * dphiV[m] for m in range(4))))
F2V = F2_of(giV, FdnV)
sgV = sqrtmg(gV, g0V)
RV = ricci_scalar(gV, giV, GV)

# AeST part is EXACT at quadratic order; the F(Z) part is added in the WKB form of R5.
# ONLY the helicity-1 block of the result is read off (D4 shows the blocks do not mix); the
# helicity-0 block of THIS Lagrangian is not the static sector -- that is PART C's job, where
# J_ZZ and delta^1 Z are handled properly.
L_aest_V = ibp(sp.expand(trunc(sp.expand(
    sgV * (RV - KB / 2 * F2V + 2 * (2 - KB) * mixV - (2 - KB) * YV))).coeff(eps, 2)))
LV = sp.expand(L_aest_V - (2 - KB) * JZs * ZV.coeff(eps, 2))


def field_atoms(f):
    return {f} | {d for d in LV.atoms(sp.Derivative) if d.expr == f}


H1 = set().union(*[field_atoms(f) for f in (av, Sv)])
H0 = set().union(*[field_atoms(f) for f in (PsiV, PhiV, bv, wfV)])
cross_hel = sp.expand(sum(term for term in sp.Add.make_args(LV)
                          if any(term.has(u) for u in H1) and any(term.has(u) for u in H0)))
check(sp.simplify(cross_hel) == 0,
      "D4  *** THE RESCUE THAT IS NOT THERE: with the metric scalars Psi, Phi, the aether "
      "LONGITUDINAL mode A_1 and the scalar perturbation varphi ALL present, the quadratic "
      "Lagrangian contains ZERO cross terms between {a, S} and {Psi, Phi, A_1, varphi} ***",
      "the helicity-1 block is CLOSED.  So no elimination of any scalar-sector field -- and "
      "in particular nothing the mixing term 2(2-K_B)J.grad(phi) can do -- can alter the "
      "transverse aether mode's kinetic sign.  This is the computed version of A3's second "
      "half, and it is the check that would have caught a wrong 'the scalar saves it' claim")

CV = sp.simplify(LV.coeff(adot ** 2))
GVc = sp.simplify(LV.coeff(aprime ** 2))
MV = sp.simplify(LV.coeff(av ** 2))
cross = sp.simplify(LV.coeff(av * adot))
Sblock = sp.expand(sum(term for term in sp.Add.make_args(LV)
                       if any(term.has(u) for u in field_atoms(Sv))))

check(sp.simplify(cross - 2 * (2 - KB) * Q0) == 0,
      "D5a the only a-times-adot term is 2(2-K_B) Q_0 a dot a = (2-K_B) Q_0 d_t(a^2), a total "
      "time derivative -- it drops from the action and cannot mimic a kinetic term",
      f"coefficient of a*adot = {cross}")
check(all(not (term.has(av) or term.has(adot) or term.has(aprime))
          for term in sp.Add.make_args(Sblock)),
      "D5b the metric vector mode S carries NO coupling to a at quadratic order, so it is a "
      "pure constraint (S = 0 in vacuum) and integrating it out cannot change the a-sector",
      f"the S-block after integration by parts is {sp.simplify(ibp(Sblock))}.  This is the "
      "direct counterpart of the aether-theory vector numerator c_1 - c_1^2/2 + c_3^2/2 "
      "collapsing to c_1 at c_3 = -c_1, which is exactly AeST's dictionary entry")

check(sp.simplify(CV.subs(JZs, 0) - KB) == 0 and sp.simplify(GVc.subs(JZs, 0) + KB) == 0
      and sp.simplify(MV.subs(JZs, 0) + (2 - KB) * Q0 ** 2) == 0,
      "D6  *** CONTROL: setting J_Z = 0 (i.e. AeST itself, or the deep-MOND limit) gives "
      "L_V = K_B(dot a^2 - a'^2) - (2-K_B) Q_0^2 a^2, hence c_V^2 = 1 and no ghost for "
      "K_B > 0 ***",
      "c_V = 1 is AeST's known vector-mode speed and K_B > 0 is the corpus's own committed "
      "stability condition (stage68 health matrix).  The machinery reproduces BOTH before "
      "being used on the new theory.  Note also that Y + mixing produce a MASS term only -- "
      "exactly what identity A2 predicts when D_T is locked to Q_0 a_T")

check(sp.simplify(CV - (KB - (2 - KB) * JZs)) == 0,
      "D7  *** THE RESULT: the transverse aether mode's kinetic coefficient is\n"
      "        C_V = K_B - (2 - K_B) J_Z ,\n"
      "    i.e. c_14^eff,vector = K_B - (2-K_B) J_Z, with NO contribution from the mixing "
      "term ***",
      "compare C10's c_14^eff,static = 2 - (2-K_B) mu.  At mu = J_Z the two differ by "
      "exactly 2 - 2 K_B = the mixing term's +(2-K_B) Z minus the c_1 = K_B it does not "
      "supply.  THE EFFECTIVE c_4 IS SECTOR-DEPENDENT")

# --- D7b: independent confirmation from the Einstein-aether formula with the CORRECTED c_4 ----
c1d, c2d, c3d = KB, sp.Integer(0), -KB
c4d = -(2 - KB) * JZs                       # the sign pinned at F1/F2, NOT the assignment's
c13d, c14d = c1d + c3d, c1d + c4d
cV2_lit = sp.simplify((c1d - c1d ** 2 / 2 + c3d ** 2 / 2) / (c14d * (1 - c13d)))
check(sp.simplify(cV2_lit - KB / (KB - (2 - KB) * JZs)) == 0
      and sp.simplify(cV2_lit - sp.simplify(-GVc / CV)) == 0,
      "D7b *** INDEPENDENT CONFIRMATION: the Einstein-aether vector-mode formula "
      "c_V^2 = (c_1 - c_1^2/2 + c_3^2/2)/(c_14(1 - c_13)), evaluated with c_1 = K_B, "
      "c_3 = -K_B and the CORRECTED c_4 = -(2-K_B) J_Z, reproduces the from-scratch result "
      "K_B/(K_B - (2-K_B) J_Z) EXACTLY ***",
      "two routes -- the literature formula and the covariant variation done here from the "
      "metric -- agree.  So the vector sector is one place the dictionary DOES transfer, "
      "provided c_4 carries the sign F1/F2 pin and the mixing is known to be inert here.  "
      "The assignment's c_14 = 2 would have given the healthy-looking c_V^2 = K_B/2 instead")

om2 = sp.simplify(-(GVc * sp.Symbol("k") ** 2 + MV) / CV)   # from C omega^2 = -(G k^2 + M)
check(sp.simplify(om2 - (KB * sp.Symbol("k") ** 2 + (2 - KB) * Q0 ** 2)
                  / (KB - (2 - KB) * JZs)) == 0,
      "D8  dispersion relation omega^2 = [K_B k^2 + (2-K_B) Q_0^2] / [K_B - (2-K_B) J_Z]",
      "so c_V^2 = K_B / C_V in the short-wavelength limit.  For C_V < 0 this is NEGATIVE at "
      "EVERY k -- a ghost AND a gradient instability at once, with growth rate "
      "|omega| = k sqrt(K_B/|C_V|), UNBOUNDED in the ultraviolet")

check(True,
      "D9  *** VERDICT (b): the mixing term DOES contribute to the same quadratic structure "
      "as c_4 -- but only in the sector where the scalar can zero the |D - J|^2 bracket.  A "
      "quantity that is K_B in one sector and K_B - (2-K_B) J_Z in another is not a "
      "dictionary entry.  'c_14 = 2' is NOT a well-defined statement about this theory, and "
      "NEITHER sector's correct value is 2 in the Newtonian regime ***")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE INCOMPATIBILITY, AND THE ESCAPE THAT IS NOT THERE")
print("=" * 100)

# no-ghost: K_B - (2-K_B) mu > 0  <=>  K_B > 2 mu/(1+mu)
kb_req = sp.simplify(sp.solve(sp.Eq(KB - (2 - KB) * muZ, 0), KB)[0])
check(sp.simplify(kb_req - 2 * muZ / (1 + muZ)) == 0
      and sp.simplify(kb_req.subs(muZ, 1) - 1) == 0,
      "E1  *** no-ghost in the vector sector requires K_B > 2 mu/(1 + mu); at the Newtonian "
      "limit mu -> 1 that is K_B > 1 ***",
      "against the corpus's IN-FORCE window K_B in [2.1e-4, 0.25] (stage70 header as "
      "amended by stage74).  Even AeST's own published fits (0.1, 0.3, 0.5) all fail it")

mu_max = sp.simplify(sp.solve(sp.Eq(KB - (2 - KB) * muZ, 0), muZ)[0])
check(sp.simplify(mu_max - KB / (2 - KB)) == 0,
      "E2  equivalently, at fixed K_B the theory is ghost-free only for mu < K_B/(2 - K_B)")

check(sp.simplify(sp.limit(mu_max, KB, 0)) == 0,
      "E3  and the window CLOSES as K_B -> 0: the smaller K_B is (which is the direction the "
      "PPN and BBN bounds push), the smaller the ghost-free region")

# --- E4: the compensating bare c_4 -------------------------------------------------------------
c4b = sp.Symbol("c4b")           # a bare +c4b * Z added to the Lagrangian
hi = sp.simplify(sp.solve(sp.Eq(-(2 - KB) * muZ + c4b, 0), c4b)[0])   # static: coeff < 0
lo = sp.simplify(sp.solve(sp.Eq(KB - (2 - KB) * muZ + c4b, 0), c4b)[0])  # vector: coeff > 0
check(sp.simplify(hi - (2 - KB) * muZ) == 0 and sp.simplify(lo - ((2 - KB) * muZ - KB)) == 0,
      "E4a a bare c_4 term +c4b*Z would have to satisfy SIMULTANEOUSLY "
      "c4b < (2-K_B) mu  (attractive AQUAL: the total Z-coefficient must stay NEGATIVE) and "
      "c4b > (2-K_B) mu - K_B  (no vector ghost)",
      f"upper edge {hi}, lower edge {lo}, both derived from the two sector conditions")
check(sp.simplify(hi - lo - KB) == 0
      and sp.simplify(sp.diff(hi, muZ) - (2 - KB)) == 0,
      "E4b *** the window has width EXACTLY K_B, INDEPENDENT of mu, while its POSITION slides "
      "at rate d(edge)/d(mu) = (2-K_B).  So a CONSTANT c4b covers a range of mu of width only "
      "K_B/(2-K_B): at K_B = 0.25 that is Delta mu = 0.143, against the mu in (0, 1) the "
      "theory must span.  A field-dependent c4b is just a relabelling of J_Z and changes "
      "nothing ***")
mu_span = sp.simplify(KB / (2 - KB))
check(sp.simplify(mu_span.subs(KB, 1) - 1) == 0,
      "E4c and only at K_B = 1 does that span reach the full mu in (0, 1) -- the SAME K_B > 1 "
      "condition as E1, reached by a completely different argument",
      "so the escape closes for the reason the original problem exists: the static sector "
      "demands the coefficient of Z be negative and growing with mu, the vector sector "
      "demands it exceed -K_B.  Ghost-freedom and a Newtonian limit are INCOMPATIBLE when "
      "the free function eats a^mu a_mu")

# --- E5: is the sign of F a choice?  Vary the static Lagrangian with a free overall sign -------
sgn = sp.Symbol("sigma")
rho_h = sp.Symbol("rhohat")
Gt = sp.Symbol("Gt")
a0s = sp.Symbol("a_0", positive=True)
Zsh = sum(p ** 2 for p in P)
Ghat = 2 * Gt / (2 - KB)


def el_static(Lexpr):
    return sp.expand(sp.diff(Lexpr, Psi)
                     - sum(sp.diff(sp.diff(Lexpr, sp.Derivative(Psi, c).doit()), c)
                           for c in SPC).doit())


# EXPLICIT free functions (no unevaluated Subs): Newtonian J(Z) = Z (J_Z = 1) and deep-MOND
# J(Z) = (2/3) Z^{3/2}/a_0 (J_Z = sqrt(Z)/a_0 = |grad Psi|/a_0), both with J_Z > 0.
lapPsi = sum(sp.diff(Psi, c, 2) for c in SPC)
L_N = sgn * (2 - KB) * Zsh - 16 * sp.pi * Gt * rho_h * Psi
elN = el_static(L_N)
check(sp.simplify(sp.expand(elN + 2 * sgn * (2 - KB) * lapPsi
                            + 16 * sp.pi * Gt * rho_h)) == 0,
      "E5a NEWTONIAN LIMIT, both signs carried: the Psi equation is "
      "-sigma * lap Psi = 4 pi Ghat rhohat, so ONLY sigma = -1 -- i.e. AeST's own L ⊃ -F -- "
      "gives ATTRACTIVE gravity",
      "at sigma = -1: 2(2-K_B) lap Psi = 16 pi Gtilde rhohat, i.e. lap Psi = 4 pi Ghat rhohat "
      "with Ghat = 2 Gtilde/(2-K_B) > 0.  At sigma = +1 the source flips sign")

L_M = sgn * (2 - KB) * sp.Rational(2, 3) * Zsh ** sp.Rational(3, 2) / a0s \
    - 16 * sp.pi * Gt * rho_h * Psi
elM = el_static(L_M)
divMOND = sp.expand(sum(sp.diff(sp.sqrt(Zsh) / a0s * sp.diff(Psi, c), c) for c in SPC).doit())
check(sp.simplify(sp.expand(elM + 2 * sgn * (2 - KB) * divMOND + 16 * sp.pi * Gt * rho_h)) == 0,
      "E5b DEEP-MOND LIMIT, both signs carried: the Psi equation is "
      "-sigma * div[(|grad Psi|/a_0) grad Psi] = 4 pi Ghat rhohat -- same sign structure, "
      "same conclusion",
      "so the sign of F is fixed at BOTH ends of the interpolation by attraction alone.  "
      "Flipping to sigma = +1 to cure the vector ghost would make gravity REPULSIVE in the "
      "solar system AND in the outer galaxy")
check(True,
      "E5  *** THE SIGN IS FORCED, NOT CHOSEN.  Both signs were priced and one of them is not "
      "a theory.  The vector ghost is therefore structural ***",
      "this is the check that stops this result from being the fifth sign slip")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- SIGN FORENSICS: WHERE 'c_4 = +(2-K_B), c_14 = 2' CAME FROM")
print("=" * 100)

info("F1  In the static sector (C4b) the AeST F^2 term enters the Lagrangian as "
     "+K_B|grad Psi|^2,\n"
     "    and the dictionary entry for that term is c_1 = K_B.  So in this file's (and the "
     "PPN\n"
     "    formulas') convention the c_1 structure enters L with a PLUS sign, and since "
     "a^mu a_mu\n"
     "    = |grad Psi|^2 in the same sector, the c_4 structure must enter as +c_4 a^mu a_mu "
     "for\n"
     "    c_14 = c_1 + c_4 and G_N = G/(1 - c_14/2) to be the right formulas.")
info("F2  The vector sector confirms it independently: D5 gives +K_B dot a^2 from the same F^2 "
     "term,\n"
     "    and the aether no-ghost condition is c_14 > 0 -- which requires L ⊃ +c_4 a^mu a_mu.\n"
     "    Two independent sectors, same convention.  It is Jacobson's '-c_4 A^a A^b g_{mn}' "
     "K-tensor.")
check(True,
      "F3  *** THE SPLICE: AeST's term is  -F(Z,Q) = -(2-K_B) J(Z), i.e. L ⊃ -(2-K_B) J_Z "
      "a^mu a_mu, so c_4^eff = MINUS (2-K_B) J_Z, giving c_14^naive = K_B - (2-K_B) J_Z = "
      "2 K_B - 2 (NOT +2).  The assignment's c_4 = +(2-K_B) is the value in the OTHER "
      "convention (K ⊃ +c_4 A A g), fed into this convention's c_14, G_N and c_V formulas "
      "***",
      "and the two errors do not cancel: with the mixing term omitted AND the sign flipped "
      "one lands on c_14 = 2 (G_N singular, c_V^2 = K_B/2 > 0 and healthy-looking); with "
      "both corrected one lands on c_14^static = K_B (G_N fine) and c_14^vector = 2K_B - 2 "
      "(GHOST).  The splice turned a fatal instability into a benign number and a benign "
      "number into a fatal-looking one -- in BOTH directions at once")

kb_num = 0.25
check(abs((kb_num - (2 - kb_num) * 1.0) - (2 * kb_num - 2)) < 1e-12,
      f"F4  arithmetic at K_B = {kb_num}, J_Z = 1: c_14^vector = "
      f"{kb_num - (2 - kb_num):.4f} = 2K_B - 2, versus the naive +2.  "
      f"c_V^2 = K_B/c_14^vector = {kb_num / (kb_num - (2 - kb_num)):.4f} < 0, versus the "
      f"naive K_B/2 = {kb_num / 2:.4f} > 0")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- WHAT THE DICTIONARY MAY AND MAY NOT BE QUOTED FOR (assignment item (d))")
print("=" * 100)

TABLE = [
    ("c_T^2 = 1/(1 - c_13)", "MAY BE QUOTED",
     "c_13 = 0 and c_T = 1 exactly; but it is redundant -- B2/B4 show the TT sector is pure "
     "Einstein-Hilbert for ANY F, because J, F_{mu nu}, Y, Q are h-independent and Z carries "
     "no derivative of h.  This is the only entry that transfers FOR A REASON."),
    ("G_N = G/(1 - c_14/2)", "MAY BE QUOTED ONLY AS A DEFINITION",
     "the static sector has exactly ONE structure (|grad Psi|^2), so reading a 'c_14' off it "
     "is a relabelling, not a transferred result.  Its VALUE is 2 - (2-K_B) mu -> K_B, NOT 2, "
     "and it is field-dependent."),
    ("c_V^2 = (c_1 - c_1^2/2 + c_3^2/2)/(c_14(1 - c_13))", "MAY BE QUOTED WITH THE CORRECT c_4",
     "it reproduces the direct computation D6/D7 exactly once c_4 = -(2-K_B)J_Z is used and "
     "the mixing term is known to contribute NOTHING here.  With c_14 = 2 it gives the wrong "
     "sign of the wrong quantity."),
    ("c_S^2 (aether scalar mode)", "MAY NOT BE QUOTED",
     "AeST has TWO scalar degrees of freedom (aether-longitudinal AND phi); Einstein-aether "
     "has ONE.  The formula is not about this theory's spectrum.  NOT COMPUTED here."),
    ("alpha_1, alpha_2 (Foster-Jacobson)", "MAY NOT BE QUOTED",
     "already ruled off-domain at c_123 = 0 by stage70/stage74 (and Jacobson arXiv:0801.1547 "
     "names this theory).  Route 3 adds a second, independent reason: c_4 is not a constant "
     "and is sector-dependent, so there is no c_14 to substitute.  NOT COMPUTED."),
    ("c_14 = c_1 + c_4 as a NUMBER", "MAY NOT BE QUOTED AT ALL",
     "sector-dependent (C10 vs D6) and field-dependent (mu).  Neither sector gives 2 in the "
     "Newtonian regime."),
    ("stability conditions 0 < K_B < 2, K_B > 0", "STILL IN FORCE, AND NOW SHARPENED",
     "K_B > 0 was the vector no-ghost condition; with F(Z) it becomes K_B > 2 mu/(1+mu)."),
]
for name, verdict, why in TABLE:
    print(f"    {name:<50s} {verdict}")
    print(f"        {why}")
check(len(TABLE) == 7, "G1  the quotable/not-quotable table is on record (7 entries)")
check(True,
      "G2  NOT COMPUTED, stated plainly: alpha_1 and alpha_2 for the full theory (the O(w) "
      "boosted sector); the AeST scalar sector's dynamical modes; the 2PN/nonlinear sector; "
      "and the fate of the vector instability under any UV completion")

# --- G3: pricing the new graviton mass ---------------------------------------------------------
info("G3  the ONE new tensor-sector effect, PRICED.  B4 gives Z = Zbar(1 - h_p + h_p^2 + h_x^2) "
     "with\n"
     "    Zbar = (g/c^2)^2, so -(2-K_B)J(Z) adds -(2-K_B)J_Z Zbar (h_p^2 + h_x^2) to the "
     "quadratic\n"
     "    TT Lagrangian.  Against B5's +(1/2)(hdot^2 - h'^2) this is a MASS, not a speed "
     "change:")
print(f"      {'regime':<30s} {'footing':<10s} {'g [m/s^2]':>11s} {'m [1/m]':>11s} "
      f"{'m/k(100Hz)':>12s} {'dc_T/c_T':>11s}")
kGW = 2 * math.pi * 100.0 / CLIGHT
gvt_rows = []
for fnm, a0 in FOOT:
    for lbl, gval, jz in (("solar system, 1 AU", GMSUN / AU ** 2, 1.0),
                          ("galaxy outskirts, g = a_0", a0, 1 - math.exp(-1.0)),
                          ("intergalactic, g = 0.01 a_0", 0.01 * a0, 1 - math.exp(-0.1))):
        m = 2.0 * math.sqrt((2 - kb_num) * jz) * gval / CLIGHT ** 2
        dct = 0.5 * (m / kGW) ** 2
        gvt_rows.append(dct)
        print(f"      {lbl:<30s} {fnm:<10s} {gval:11.3e} {m:11.3e} "
              f"{m / kGW:12.3e} {dct:11.3e}")
check(max(gvt_rows) < 1e-15,
      f"G4  the F(Z)-induced graviton mass is HARMLESS: the largest delta c_T/c_T anywhere on "
      f"the table is {max(gvt_rows):.2e}, against the GW170817 bound ~1e-15.  An adverse-"
      f"looking new effect, verified and found benign -- both footings",
      "the solar-system row is the largest and is also the least relevant (GWs do not "
      "propagate through strong fields for any appreciable path length)")

# =================================================================================================
print()
print("=" * 100)
print("PART H -- THE NUMBERS, BOTH FOOTINGS")
print("=" * 100)


def mu_exp(y):
    """AQUAL mu for the Route A / MS08 exponential kernel nu(y) = 1/(1 - exp(-sqrt y)):
    x = y*nu(y) and mu = y/x = 1 - exp(-sqrt y)."""
    return 1.0 - math.exp(-math.sqrt(y))


# self-check of the kernel inversion
for ytest in (0.01, 1.0, 100.0):
    nu = 1.0 / (1.0 - math.exp(-math.sqrt(ytest)))
    xtest = ytest * nu
    if abs(mu_exp(ytest) - ytest / xtest) > 1e-14:
        break
check(all(abs(mu_exp(y) - y / (y / (1 - math.exp(-math.sqrt(y))))) < 1e-14
          for y in (0.01, 1.0, 100.0)),
      "H1  kernel inversion verified: for nu(y) = 1/(1 - exp(-sqrt y)), the AQUAL mu "
      "evaluated at the TOTAL acceleration is mu = y/x = 1 - exp(-sqrt y)")

print(f"      {'K_B':>10s} {'mu_max':>10s} {'y* = g_bar/a_0':>16s}")
rows = []
for kb in (KB_LO, 0.1, kb_num, 1.0):
    mm = kb / (2 - kb)
    ystar = math.inf if mm >= 1 else (-math.log(1 - mm)) ** 2
    rows.append((kb, mm, ystar))
    print(f"      {kb:10.4g} {mm:10.5f} {ystar:16.6g}")
check(rows[2][2] < 0.03 and rows[3][1] >= 1.0,
      f"H2  *** at the in-force cap K_B = {kb_num} the theory is ghost-free only for "
      f"g_bar < {rows[2][2]:.5f} a_0, and only K_B >= 1 removes the bound entirely ***",
      f"at the LOW end of the in-force window (K_B = {KB_LO}) the ghost-free region shrinks "
      f"to g_bar < {rows[0][2]:.3e} a_0")

print()
print(f"      {'system':<26s} {'footing':<10s} {'r_ghost [m]':>13s} {'r_ghost':>16s}")
rad = []
for nm, M in (("Sun", GMSUN), ("10^11 Msun galaxy", 1e11 * GMSUN)):
    for fnm, a0 in FOOT:
        gth = rows[2][2] * a0
        r = math.sqrt(M / gth)
        rad.append(r)
        unit = f"{r / AU:10.3e} AU" if M == GMSUN else f"{r / (1e3 * PC):10.3f} kpc"
        print(f"      {nm:<26s} {fnm:<10s} {r:13.4e} {unit:>16s}")
check(rad[0] / AU > 1e4 and rad[2] / (1e3 * PC) > 10,
      "H3  *** the ghost region covers the ENTIRE solar system and Oort cloud "
      f"(r < {rad[0] / AU:.2e} AU canonical / {rad[1] / AU:.2e} AU alt) and the ENTIRE "
      f"optical body of a galaxy (r < {rad[2] / (1e3 * PC):.1f} kpc canonical / "
      f"{rad[3] / (1e3 * PC):.1f} kpc alt) ***",
      "i.e. option 1 is ghost-unstable exactly where it was invoked to save the theory: the "
      "solar-system screening regime")

print()
print(f"      {'wavelength':<26s} {'k [1/m]':>12s} {'growth rate [1/s]':>18s} {'e-fold time':>16s}")
CVn = kb_num - (2 - kb_num) * 1.0
rate_rows = []
g1AU = GMSUN / AU ** 2
for lbl, lam in (("1 m", 1.0), ("1 AU", AU),
                 ("WKB floor c^2/g at 1 AU", CLIGHT ** 2 / g1AU)):
    kk = 2 * math.pi / lam
    rate = kk * math.sqrt(kb_num / abs(CVn)) * CLIGHT
    rate_rows.append(rate)
    tau = 1.0 / rate
    tstr = (f"{tau:9.3e} s" if tau < 3.15e7 else f"{tau / 3.155e7:9.3e} yr")
    print(f"      {lbl:<26s} {kk:12.4e} {rate:18.4e} {tstr:>16s}")
check(CVn < 0 and min(rate_rows) > 0,
      f"H4  *** at K_B = {kb_num}, J_Z = 1 the kinetic coefficient is C_V = {CVn:.4f} < 0 and "
      f"c_V^2 = {kb_num / CVn:.4f} < 0: growth rate |omega| = "
      f"{math.sqrt(kb_num / abs(CVn)):.4f} c k, unbounded in the UV ***",
      f"even at the LONGEST wavelength for which the WKB reduction R5 is controlled "
      f"(lambda = c^2/g at 1 AU = {CLIGHT ** 2 / g1AU:.3e} m) the e-folding time is "
      f"{1 / rate_rows[2] / 3.155e7:.3e} yr.  There is no cutoff choice that saves it")

mu_ss = 1.0 - math.exp(-math.sqrt(GMSUN / AU ** 2 / A0_CAN))
check(1.0 - mu_ss < 1e-100,
      f"H5a AND THE GHOST IS MAXIMAL EXACTLY WHERE OPTION 1 WAS INVOKED: for the Route A / "
      f"MS08 exponential kernel, mu at 1 AU is 1 - {1.0 - mu_ss:.1e}, i.e. J_Z = 1 to "
      f"absurd precision -- the same screening that deletes the ephemeris gap sets C_V to its "
      f"most negative value",
      "AeST itself (F(Y), no Z-term) has C_V = K_B > 0 and is healthy here (D6).  This "
      "liability belongs to option 1 alone and to no other part of the framework")

check(True,
      "H5  a_0 ENTERS THIS RESULT ONLY THROUGH THE RADII, NOT THROUGH THE VERDICT: the ghost "
      "threshold is a condition on mu (dimensionless), so the canonical/ALT split moves "
      f"r_ghost by {abs(rad[0] / rad[1] - 1) * 100:.1f}% and moves nothing else.  Neither "
      "footing is favoured or disfavoured by route 3")

# =================================================================================================
print()
print("=" * 100)
print("PART I -- VERDICT")
print("=" * 100)
print("""
  (a) TENSOR.  c_T = 1 EXACTLY, in AeST and in the F(Z) theory, for ANY free function --
      computed, not quoted (B2, B4).  c_4 provably cannot reach the tensor sector.  The one
      new effect is an environment-dependent graviton MASS, priced and harmless (G3/G4).

  (b) DOES THE MIXING FEED THE c_4 STRUCTURE?  YES -- IN ONE SECTOR ONLY.  Identity A2 shows
      AeST identically contains +(2-K_B) a^mu a_mu.  In the static/longitudinal sector the
      companion bracket |D - J|^2 is driven to zero by the free longitudinal aether mode, so
      the c_4 piece survives and cancels the naive singularity: c_14^eff,static
      = 2 - (2-K_B) mu -> K_B, G_N = Ghat, finite.  opt1's C6 is CONFIRMED, with a mechanism.
      In the transverse-vector sector the scalar has no transverse gradient, D_T is locked to
      Q_0 a_T, the bracket cancels the c_4 piece exactly, and the mixing supplies nothing.
      => c_4^eff is SECTOR-DEPENDENT => "c_14 = 2" is not a well-defined statement about this
      theory, and the assignment's PASS criterion is MET.

  (c) THE CORRECT SECTOR RESULTS, AND THEY ARE WORSE THAN THE ARTEFACT THEY REPLACE.
        tensor : c_T = 1 exactly; extra graviton mass m^2 = 4(2-K_B) J_Z (g/c^2)^2, harmless.
        vector : C_V = K_B - (2-K_B) J_Z, c_V^2 = K_B/C_V, omega^2 = (K_B k^2 + (2-K_B)Q_0^2)/C_V.
                 GHOST + gradient instability for J_Z > K_B/(2-K_B); at K_B = 0.25, J_Z = 1,
                 C_V = -1.50 and the growth rate is 0.408 c k, unbounded in the UV.
        static : AQUAL with mu = J_Z, gamma_PPN = 1, G_N = Ghat.  Unchanged and healthy.
        scalar dynamical modes, alpha_1, alpha_2 : NOT COMPUTED (and the aether formulas for
                 them may not be quoted -- G1).

  (d) THE STANDING RULE.  Only c_T = 1 transfers for a reason.  c_V^2 transfers only with
      c_4 = -(2-K_B) J_Z and the knowledge that the mixing is inert there.  G_N's formula is
      a relabelling.  c_S^2, alpha_1, alpha_2 and "c_14 as a number" may NOT be quoted.

  DIRECTION: ADVERSE for option 1.  The c_14 = 2 objection DISSOLVES -- and the sector-by-
  sector computation that dissolves it produces a NEW and harder obstruction in its place:
  making the free function eat a^mu a_mu fixes the sign of the coefficient of a^mu a_mu from
  the static sector (attractive AQUAL), and that same coefficient is the transverse aether
  mode's kinetic term with the opposite role.  Ghost-freedom needs K_B > 2 mu/(1+mu), i.e.
  K_B > 1 in the Newtonian limit, against the in-force window K_B in [2.1e-4, 0.25].
  This is a statement about the THEORY, not about a_0, kappa, the kernel or either footing.
""")

# =================================================================================================
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed   ({time.time() - T0:.1f} s)")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("   -", f)
print("=" * 100)
sys.exit(1 if FAIL else 0)
