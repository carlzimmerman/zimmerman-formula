#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sector4_cosmology_dark_energy_a0_2026.py
========================================
SECTOR 4 -- COSMOLOGY, DARK ENERGY, AND WHERE a0 COMES FROM.
The field equations of THE_GENERALIZED_COMPLETION action reduced on flat FRW, DERIVED by variation
(minisuperspace with lapse, aether A_0(t) and multiplier lambda(t) kept as independent variables),
with controls that can fail.  Nothing below is transcribed from the record; where the record is
reproduced (stage 17 / 19 / 5) it is re-derived and compared.

THE ACTION (qwen_claude_field_theory/closure_2026/THE_GENERALIZED_COMPLETION.md; signature -+++, c=1):
  S = int d^4x sqrt(-g) { (R - 2 Lambda)/(16 pi G)  - (K_B/2) F_{mn}F^{mn} + c2 (div A)^2 + c4 a_m a^m
        + lambda (A_m A^m + 1) + 2(2-K_B) a^m d_m phi - (2-K_B) Y
        + (a0^2(Q)/8 pi G) Gcal( sqrt(Y)/a0(Q) ) + sigma K(Q) + Acal B(Y/a0^2(Q)) (Q-Q0)^2 } + S_m
  a^m = A^n nabla_n A^m ,  Q = A^m d_m phi ,  Y = (g^{mn} + A^m A^n) d_m phi d_n phi ,
  Gcal(y) = y^2 + 2(1+y) e^{-y} - 2 ,  K(Q) = -M^4 sqrt(1 - mu^2 (Q-Q0)^2 / M^4)  (beta = 1 DBI),
  a0^2(Q) = -kappa^2 c^2 G K(Q)  (the promotion),  B(u) = u/(1+u)^2 .

sigma = the coefficient of K(Q) in the Lagrangian density.  THE_GENERALIZED_COMPLETION.md line 14
writes "-2 K(Q)"; THE_COMPLETION.md (v9) sec. 1.2 prose has p = K, rho = -K = M^4, i.e. sigma = +1.
sigma is kept SYMBOLIC and the derivation decides which sign is consistent with -K(Q0) = rho_Lambda > 0
and with a real promoted a0 (Part B).  Likewise c2, c4 are kept symbolic as the literal coefficients
written in the generalized action (outside the 1/16 pi G prefactor); the dictionary to the
Einstein-aether normalisation is given where it matters (Part B, G_cos).

WHAT IS INPUT vs DERIVED (stated up front, repeated at the end):
  INPUT:   kappa = 1/2 (FITTED: 0.465 +/- 0.076 BTFR, 0.551 +/- 0.043 distance-free);  the promotion
           a0^2(Q) = -kappa^2 c^2 G K(Q) (a definitional choice, NOT derived);  M^4 = rho_Lambda with
           Lambda_bare = 0 (an identification);  beta = 1 (boundary-pinned, stage 20, not derived);
           the charge n0 (an initial condition).
  DERIVED: everything labelled (E1)-(E12) below, by variation / reduction in this script.
  NOT DERIVED: a0(z) ~ H(z).  The action yields a DIFFERENT law (E11); see Part E.

Exit 0 <=> every check passed.  Checks are constructed so that a wrong sign, a wrong factor, or a
dropped lambda-contribution fails them (mutation controls in B5, B6).
"""
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
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


def banner(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


print(__doc__)

# =================================================================================================
banner("PART A -- geometry and the invariants on flat FRW (lapse N(t) kept; A_mu = (A_0(t),0,0,0))")
# =================================================================================================
t = sp.Symbol('t', real=True)
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
X = [t, x1, x2, x3]
N = sp.Function('N', positive=True)(t)
a = sp.Function('a', positive=True)(t)
phi = sp.Function('phi', real=True)(t)
A0f = sp.Function('A0', real=True)(t)
lamf = sp.Function('lam', real=True)(t)

G, Lam, KB, c2, c4, sigma = sp.symbols('G Lambda K_B c_2 c_4 sigma', real=True)
pi = sp.pi


def christoffel(g, ginv):
    n = 4
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                Gam[l][m][nu] = sp.simplify(sum(
                    ginv[l, s] * (sp.diff(g[s, m], X[nu]) + sp.diff(g[s, nu], X[m]) - sp.diff(g[m, nu], X[s]))
                    for s in range(n)) / 2)
    return Gam


def ricci_scalar(g, ginv, Gam):
    n = 4
    R = 0
    for m in range(n):
        for nu in range(n):
            Rmn = sum(sp.diff(Gam[l][m][nu], X[l]) - sp.diff(Gam[l][m][l], X[nu])
                      + sum(Gam[l][l][s] * Gam[s][m][nu] - Gam[l][nu][s] * Gam[s][m][l] for s in range(n))
                      for l in range(n))
            R += ginv[m, nu] * Rmn
    return sp.simplify(R)


def frw_invariants(A_lower, A_upper, g, ginv, Gam):
    """All scalar invariants of the action on the homogeneous ansatz, as functions of t."""
    dphi = [sp.diff(phi, xx) for xx in X]
    Q = sum(A_upper[m] * dphi[m] for m in range(4))
    Y = sum((ginv[m, n] + A_upper[m] * A_upper[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
    F = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            F[m, n] = sp.diff(A_lower[n], X[m]) - sp.diff(A_lower[m], X[n])
    F2 = sum(ginv[m, r] * ginv[n, s] * F[m, n] * F[r, s] for m in range(4) for n in range(4)
             for r in range(4) for s in range(4))
    sqrtg = N * a ** 3
    divA = sum(sp.diff(A_upper[m], X[m]) + sum(Gam[m][m][s] * A_upper[s] for s in range(4)) for m in range(4))
    divA_alt = sum(sp.diff(sqrtg * A_upper[m], X[m]) for m in range(4)) / sqrtg
    acc = [sum(A_upper[n] * (sp.diff(A_upper[m], X[n]) + sum(Gam[m][n][s] * A_upper[s] for s in range(4)))
               for n in range(4)) for m in range(4)]
    acc2 = sum(g[m, n] * acc[m] * acc[n] for m in range(4) for n in range(4))
    Jdphi = sum(acc[m] * dphi[m] for m in range(4))
    AA = sum(ginv[m, n] * A_lower[m] * A_lower[n] for m in range(4) for n in range(4))
    return dict(Q=sp.simplify(Q), Y=sp.simplify(Y), F2=sp.simplify(F2), divA=sp.simplify(divA),
                divA_alt=sp.simplify(divA_alt), acc=[sp.simplify(z) for z in acc], acc2=sp.simplify(acc2),
                Jdphi=sp.simplify(Jdphi), AA=sp.simplify(AA), sqrtg=sqrtg)


g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2)
ginv = g.inv()
Gam = christoffel(g, ginv)
R = ricci_scalar(g, ginv, Gam)
R_expected = 6 * (sp.diff(a, t, 2) / (a * N ** 2) + sp.diff(a, t) ** 2 / (a ** 2 * N ** 2)
                  - sp.diff(a, t) * sp.diff(N, t) / (a * N ** 3))
check(sp.simplify(R - R_expected) == 0,
      "A1  Ricci scalar of ds^2 = -N^2 dt^2 + a^2 dx^2 computed from the Christoffels: "
      "R = 6[ a''/(a N^2) + a'^2/(a^2 N^2) - a' N'/(a N^3) ]")
Hs = sp.Symbol('H', positive=True)
check(sp.simplify(R.subs(N, 1).subs(a, sp.exp(Hs * t)).doit() - 12 * Hs ** 2) == 0,
      "A1' de Sitter control: N = 1, a = e^{Ht} gives R = 12 H^2")

# covariant A_mu fundamental (SZ2021 convention)
A_lower = [A0f, 0, 0, 0]
A_upper = [sum(ginv[m, n] * A_lower[n] for n in range(4)) for m in range(4)]
inv = frw_invariants(A_lower, A_upper, g, ginv, Gam)

check(sp.simplify(inv['Y'] - sp.diff(phi, t) ** 2 * (A0f ** 2 - N ** 2) / N ** 4) == 0
      and sp.simplify(inv['Y'].subs(A0f, -N)) == 0,
      "A2  Y = (g^{mn} + A^m A^n) d_m phi d_n phi = phi'^2 (A_0^2 - N^2)/N^4  ==>  Y = 0 EXACTLY on the "
      "unit-norm surface A_0 = -N.  The spatial projector g^{mn}+A^mA^n annihilates the purely "
      "temporal gradient of phi(t): the MOND argument vanishes identically on FRW.")
check(sp.simplify(inv['Q'] - (-A0f * sp.diff(phi, t) / N ** 2)) == 0
      and sp.simplify(inv['Q'].subs(A0f, -N) - sp.diff(phi, t) / N) == 0,
      "A3  Q = A^m d_m phi = -A_0 phi'/N^2  ==>  Q = phi'/N on the constraint surface (Q = phi-dot in "
      "the N = 1 gauge)")
check(inv['F2'] == 0 and sp.simplify(inv['AA'] - (-A0f ** 2 / N ** 2)) == 0,
      "A4  F_{mn} = 0 IDENTICALLY for A_mu = (A_0(t),0,0,0) (the K_B Maxwell term cannot contribute to "
      "any background variation);  A_m A^m = -A_0^2/N^2 so the multiplier enforces A_0 = -N (future-"
      "directed A^0 = +1/N)")
check(sp.simplify(inv['divA'] - inv['divA_alt']) == 0
      and sp.simplify(inv['divA'].subs(A0f, -N).doit() - 3 * sp.diff(a, t) / (a * N)) == 0,
      "A5  div A (Christoffel route == sqrt(-g) route) = 3 a'/(a N) = 3H on the constraint surface: the "
      "c2 term is ALIVE on the background")
acc_on = [sp.simplify(z.subs(A0f, -N).doit()) for z in inv['acc']]
check(all(z == 0 for z in acc_on) and sp.simplify(inv['acc2'].subs(A0f, -N).doit()) == 0
      and sp.simplify(inv['Jdphi'].subs(A0f, -N).doit()) == 0,
      "A6  a^m = A^n nabla_n A^m = 0 on the constraint surface (the comoving aether is geodesic): the "
      "c4 term and the scalar drag 2(2-K_B) a.dphi VANISH on the background -- but their VARIATIONS "
      "need not (Part B tracks them)")

# the MOND kernel and the bump at Y -> 0, with a0(Q) GENERIC (the promotion is a generic function here)
Ysym, Qsym = sp.symbols('Y Q', positive=True)
a0f = sp.Function('a0', positive=True)(Qsym)
yv = sp.sqrt(Ysym) / a0f
Gcal = yv ** 2 + 2 * (1 + yv) * sp.exp(-yv) - 2
L_MOND = a0f ** 2 / (8 * pi * G) * Gcal
mu_of_y = sp.simplify(sp.diff(Gcal, Ysym) * 2 * yv * a0f ** 2 / (2 * yv) )  # placeholder, not used
dLdY = sp.simplify(sp.diff(L_MOND, Ysym))
dLdQ = sp.simplify(sp.diff(L_MOND, Qsym))
ys = sp.Symbol('y', positive=True)
Gy = ys ** 2 + 2 * (1 + ys) * sp.exp(-ys) - 2
ser = sp.series(Gy, ys, 0, 5).removeO()
check(sp.simplify(ser - sp.Rational(2, 3) * ys ** 3 + sp.Rational(1, 4) * ys ** 4) == 0
      and sp.simplify(sp.diff(Gy, ys) / (2 * ys) - (1 - sp.exp(-ys))) == 0,
      "A7  Gcal(y) = (2/3) y^3 - (1/4) y^4 + ...  (Gcal(0) = Gcal'(0) = 0), and Gcal'(y)/(2y) = 1 - e^{-y} "
      "= mu(y) exactly (the exponential constitutive law, spec req 12)")
check(sp.limit(dLdY, Ysym, 0, '+') == 0 and sp.limit(dLdQ, Ysym, 0, '+') == 0
      and sp.limit(L_MOND, Ysym, 0, '+') == 0,
      "A8  dL_MOND/dY -> mu(0)/(8 pi G) = 0,  dL_MOND/dQ|_{Y->0} = a0 a0'(Q) [2Gcal - y Gcal']/(8 pi G) -> 0, "
      "L_MOND -> 0:  with a0(Q) GENERIC, every first variation of the promoted MOND term vanishes at Y = 0. "
      "The MOND sector is ABSENT from the background field equations (all of them), not just from the "
      "background Lagrangian.",
      "this is stage 17's A5 (F(0)=0) done with the actual kernel and the promotion switched on")
Bu = sp.Symbol('u', positive=True)
Bfun = Bu / (1 + Bu) ** 2
check(Bfun.subs(Bu, 0) == 0 and sp.diff(Bfun, Bu).subs(Bu, 0) == 1,
      "A9  bump: B(0) = 0 but B'(0) = 1  ==>  the bump contributes a Y-LINEAR piece Acal (Q-Q0)^2 / a0^2(Q) "
      "at Y = 0.  Such pieces DO enter the A_0 variation; Part B shows they drop out after lambda is "
      "eliminated (the same mechanism that removes the -(2-K_B) Y term)")

# =================================================================================================
banner("PART B -- minisuperspace variation: the Friedmann equations, DERIVED (generic K, P; sigma, c2, c4 symbolic)")
# =================================================================================================
# Symbols for the jet of each variable (chains long enough for two total derivatives of second-order terms)
N_, Nd, Ndd, Nddd, Ndddd = sp.symbols('N_ N_d N_dd N_ddd N_dddd', real=True)
a_, ad, add, addd, adddd = sp.symbols('a_ a_d a_dd a_ddd a_dddd', positive=True)
pd, pdd, pddd, pdddd = sp.symbols('Qd Qdd Qddd Qdddd', real=True)      # phi-dot and its derivatives
A0_, A0d, A0dd, A0ddd, A0dddd = sp.symbols('A0_ A0_d A0_dd A0_ddd A0_dddd', real=True)
lam_, lamd, lamdd = sp.symbols('lam_ lam_d lam_dd', real=True)
CH = [[N_, Nd, Ndd, Nddd, Ndddd], [a_, ad, add, addd, adddd], [pd, pdd, pddd, pdddd],
      [A0_, A0d, A0dd, A0ddd, A0dddd], [lam_, lamd, lamdd]]


def to_syms(e):
    """functions of t -> jet symbols (highest derivatives first)."""
    e = e.doit()
    reps = []
    for f, ch in ((N, CH[0]), (a, CH[1]), (A0f, CH[3]), (lamf, CH[4])):
        for k in range(len(ch) - 1, 0, -1):
            reps.append((sp.Derivative(f, (t, k)), ch[k]))
        reps.append((f, ch[0]))
    for k in range(len(CH[2]), 0, -1):
        reps.append((sp.Derivative(phi, (t, k)), CH[2][k - 1]))
    for old, new in reps:
        e = e.subs(old, new)
    assert not e.has(phi), "phi appears undifferentiated -- shift symmetry broken?"
    return e


def Dt(e):
    for ch in CH:
        assert not e.has(ch[-1]), "jet chain too short"
    return sum(sp.diff(e, ch[i]) * ch[i + 1] for ch in CH for i in range(len(ch) - 1))


def EL(L, ch):
    """Euler-Lagrange expression for the variable whose jet chain is ch (up to 2nd derivatives in L)."""
    q, qd, qdd = ch[0], ch[1], ch[2]
    return sp.diff(L, q) - Dt(sp.diff(L, qd)) + Dt(Dt(sp.diff(L, qdd)))


ONSHELL = {N_: 1, Nd: 0, Ndd: 0, Nddd: 0, A0_: -1, A0d: 0, A0dd: 0, A0ddd: 0}


def onshell(e):
    return sp.simplify(e.subs(ONSHELL).doit())


Kf, Pf, R2f = sp.Function('K'), sp.Function('P'), sp.Function('R2')
w_m, rho0 = sp.symbols('w rho_0', real=True)

Qs = to_syms(inv['Q'])
Ys = to_syms(inv['Y'])
Rs = to_syms(R)
divAs = to_syms(inv['divA'])
acc2s = to_syms(inv['acc2'])
Jdphis = to_syms(inv['Jdphi'])
AAs = to_syms(inv['AA'])
sqrtg_s = N_ * a_ ** 3
rho_m = rho0 * a_ ** (-3 * (1 + w_m))

pieces = {
    'EH':   sqrtg_s * (Rs - 2 * Lam) / (16 * pi * G),
    'c2':   sqrtg_s * c2 * divAs ** 2,
    'c4':   sqrtg_s * c4 * acc2s,
    'lam':  sqrtg_s * lam_ * (AAs + 1),
    'J':    sqrtg_s * 2 * (2 - KB) * Jdphis,
    'K':    sqrtg_s * sigma * Kf(Qs),                 # sigma K(Q): the DBI sector (generic K here)
    'P':    sqrtg_s * Ys * Pf(Qs),                     # every Y-linear piece: -(2-K_B)Y, the bump, ...
    'R2':   sqrtg_s * Ys ** 2 * R2f(Qs),               # Y^2 and higher: must drop out entirely
    'm':    -sqrtg_s * rho_m,                          # perfect fluid, p = w rho
}
# (the MOND term is omitted here because A8 proved all its first variations vanish at Y=0)

EN, Ea, Ephi, EA, Elam = {}, {}, {}, {}, {}
for k, L in pieces.items():
    EN[k] = onshell(EL(L, CH[0]))
    Ea[k] = onshell(EL(L, CH[1]))
    Ephi[k] = onshell(-Dt(sp.diff(L, pd)))            # phi absent: E_phi = -d/dt (dL/dphi-dot)
    EA[k] = onshell(EL(L, CH[3]))
    Elam[k] = sp.simplify(EL(L, CH[4]))

H = ad / a_
Hdot = add / a_ - ad ** 2 / a_ ** 2

# constraint
check(sp.simplify(Elam['lam'] - N_ * a_ ** 3 * (1 - A0_ ** 2 / N_ ** 2)) == 0,
      "B0  the lambda equation is the unit-norm constraint A_0^2 = N^2; all other pieces are lambda-free")

# per-sector energy densities rho_X = -E_N[L_X]/a^3 and pressures p_X = E_a[L_X]/(3 a^2)  (N = 1)
rho, p = {}, {}
for k in pieces:
    rho[k] = sp.simplify(-EN[k] / a_ ** 3)
    p[k] = sp.simplify(Ea[k] / (3 * a_ ** 2))

check(sp.simplify(rho['EH'] + (3 * H ** 2 - Lam) / (8 * pi * G)) == 0
      and sp.simplify(p['EH'] - (2 * Hdot + 3 * H ** 2 - Lam) / (8 * pi * G)) == 0,
      "B1  Einstein-Hilbert sector: -E_N/a^3 = -(3H^2 - Lambda)/(8 pi G),  E_a/(3a^2) = (2H' + 3H^2 - "
      "Lambda)/(8 pi G): the identification rho_X = -E_N[L_X]/a^3, p_X = E_a[L_X]/(3a^2) reproduces the "
      "two Friedmann operators (E_N: 3H^2 = Lambda + 8 pi G rho;  E_a: 2H'+3H^2 = Lambda - 8 pi G p)")
check(sp.simplify(rho['m'] - rho_m) == 0 and sp.simplify(p['m'] - w_m * rho_m) == 0,
      "B2  perfect-fluid control: rho_m = rho_0 a^{-3(1+w)}, p_m = w rho_m from the same operators")

# raw per-sector pieces BEFORE lambda elimination (printed so the cancellation is visible)
info("B3  raw sector contributions (N = 1, A_0 = -1, before eliminating lambda):")
for k in ('K', 'P', 'R2', 'J', 'c2', 'c4', 'lam'):
    print(f"        {k:>3s}:  rho = {rho[k]}\n              p   = {p[k]}\n              E_A = {sp.simplify(EA[k])}")

check(all(sp.simplify(z) == 0 for z in (rho['R2'], p['R2'], EA['R2'], Ephi['R2'])),
      "B4a Y^2 (and higher) pieces of any Phi(Y,Q) contribute NOTHING to any background variation "
      "(their first variations carry a factor Y = 0): only Phi(0,Q) and Phi_Y(0,Q) can matter")
check(all(sp.simplify(z) == 0 for z in (rho['c4'], p['c4'], EA['c4'], Ephi['c4'])),
      "B4b c4 a_m a^m contributes NOTHING to the background (quadratic in a^m = 0): c4 is INVISIBLE to FRW")
check(sp.simplify(Ephi['P']) == 0 and sp.simplify(Ephi['J']) == 0 and sp.simplify(Ephi['c2']) == 0,
      "B4c the phi equation receives contributions ONLY from sigma K(Q): E_phi = -d/dt[a^3 sigma K'(Q)]")

# eliminate lambda from the total A_0 equation
EA_tot = sp.simplify(sum(EA.values()))
lam_sol = sp.solve(sp.Eq(EA_tot, 0), lam_)
check(len(lam_sol) == 1, "B5  the A_0 equation is linear in lambda and fixes it uniquely")
lam_sol = sp.simplify(lam_sol[0])
print("        lambda =", lam_sol)

rho_tot = sp.simplify(sum(rho.values()).subs(lam_, lam_sol))
p_tot = sp.simplify(sum(p.values()).subs(lam_, lam_sol))
Kq = sp.Derivative(Kf(pd), pd)
rho_Q_claim = sigma * (pd * Kq - Kf(pd))
p_Q_claim = sigma * Kf(pd)
E1_res = sp.simplify(rho_tot - (-(3 * H ** 2 - Lam) / (8 * pi * G) + rho_m + rho_Q_claim + 9 * c2 * H ** 2))
E2_res = sp.simplify(p_tot - ((2 * Hdot + 3 * H ** 2 - Lam) / (8 * pi * G) + w_m * rho_m + p_Q_claim
                              - 9 * c2 * H ** 2 - 6 * c2 * Hdot))
print("        sum rho (after lambda) =", rho_tot)
print("        sum p   (after lambda) =", p_tot)
check(E1_res == 0,
      "B6  *** (E1) FIRST FRIEDMANN EQUATION, DERIVED:  3H^2 (1 - 24 pi G c2) = Lambda + 8 pi G [ rho_m + "
      "sigma (Q K_Q - K) ] ***   -- the Y-linear coefficient P(Q) (i.e. -(2-K_B) and the bump), the scalar "
      "drag J.dphi and the c2 H' pieces all cancel against lambda; c4 never appears")
check(E2_res == 0,
      "B7  *** (E2) SECOND FRIEDMANN EQUATION, DERIVED:  (2H' + 3H^2)(1 - 24 pi G c2) = Lambda - 8 pi G [ "
      "w rho_m + sigma K ] ***   -- same c2 renormalisation, so G_cos = G/(1 - 24 pi G c2) in BOTH")
check(sp.simplify(sum(Ephi.values()) + sigma * Dt(a_ ** 3 * Kq)) == 0,
      "B8  *** (E3) THE phi EQUATION = SHIFT-CHARGE CONSERVATION:  d/dt [ a^3 sigma K_Q ] = 0,  "
      "n = dL/d(phi-dot) = sigma K_Q ~ a^{-3} ***")
n_def = sp.simplify(sum(sp.diff(L, pd) for L in pieces.values()).subs(ONSHELL).doit() / a_ ** 3)
check(sp.simplify(n_def - sigma * Kq) == 0,
      "B8' the Noether charge density of the shift symmetry phi -> phi + const is n = sigma K_Q "
      "(computed from dL/d(phi-dot) of the FULL Lagrangian on shell)")

# what dropped out: show explicitly that P(Q) is gone
check(not rho_tot.has(Pf) and not p_tot.has(Pf) and not rho_tot.has(R2f) and not rho_tot.has(KB),
      "B9  the final equations contain neither P(Q) [so neither -(2-K_B) Y nor the bump] nor K_B nor "
      "R2(Q): on FRW the whole aether-scalar coupling structure is INERT; only sigma K(Q) and c2 survive")

# --- sign / normalisation of the K term
rhoQ = rho_Q_claim
pQ = p_Q_claim
info("B10 (E4) the dark-sector fluid, for ANY K(Q):   rho_Q = sigma (Q K_Q - K),   p_Q = sigma K.")
M4, mu, Q0 = sp.symbols('M4 mu Q_0', positive=True)
Kdbi = -M4 * sp.sqrt(1 - mu ** 2 * (pd - Q0) ** 2 / M4)
rho_dbi = sp.simplify(rhoQ.subs(Kf(pd), Kdbi).doit())
p_dbi = sp.simplify(pQ.subs(Kf(pd), Kdbi).doit())
rho_min = sp.simplify(rho_dbi.subs(pd, Q0))
p_min = sp.simplify(p_dbi.subs(pd, Q0))
check(rho_min == sigma * M4 and p_min == -sigma * M4,
      "B11 at the DBI minimum Q = Q0 (K_Q = 0):  rho_Q = sigma M^4,  p_Q = -sigma M^4  ==>  w = -1 EXACTLY "
      "for every sigma, but the SIGN of the vacuum energy is sign(sigma)")
check(rho_min.subs(sigma, 1) > 0 and rho_min.subs(sigma, -2) < 0,
      "B12 *** NORMALISATION SETTLED BY THE DERIVATION: -K(Q0) = rho_Lambda > 0 requires sigma = +1 "
      "(v9 sec. 1.2 prose: p = K, rho = Q K_Q - K, rho_vac = -K(Q0) = M^4).  The literal '-2 K(Q)' of "
      "THE_GENERALIZED_COMPLETION.md line 14 (sigma = -2, with K(Q0) = -M^4) gives rho_vac = -2 M^4 < 0 "
      "(anti-de Sitter, w = -1 still) and contradicts the same file's '-K(Q0) = rho_Lambda' and the "
      "reality of a0^2 = -kappa^2 c^2 G K.  Transcription slip; sigma = +1 adopted below. ***")

# --- controls
V0 = sp.Symbol('V_0', positive=True)
rho_can = sp.simplify(rhoQ.subs(sigma, 1).subs(Kf(pd), pd ** 2 / 2 - V0).doit())
p_can = sp.simplify(pQ.subs(sigma, 1).subs(Kf(pd), pd ** 2 / 2 - V0).doit())
check(sp.simplify(rho_can - (pd ** 2 / 2 + V0)) == 0 and sp.simplify(p_can - (pd ** 2 / 2 - V0)) == 0,
      "B13 canonical-scalar control: K = Q^2/2 - V0 (i.e. L = -(1/2)(d phi)^2 - V0) gives rho = phi'^2/2 + V0, "
      "p = phi'^2/2 - V0 -- the textbook signs, from the SAME operators")
rho_gh = sp.simplify(rhoQ.subs(sigma, 1).subs(Kf(pd), -pd ** 2 / 2).doit())
check(sp.simplify(rho_gh + pd ** 2 / 2) == 0,
      "B14 ghost control: K = -Q^2/2 gives rho = -phi'^2/2 < 0 -- the pipeline tracks the sign (a sign-blind "
      "pipeline would pass B13 and fail here)")

# mutation control: DROP the lambda contribution deliberately -> the Friedmann equation must come out wrong
rho_nolam = sp.simplify(sum(rho[k] for k in pieces if k != 'lam'))
check(sp.simplify(rho_nolam - rho_tot) != 0
      and sp.simplify(rho_nolam - (-(3 * H ** 2 - Lam) / (8 * pi * G) + rho_m + rho_Q_claim + 9 * c2 * H ** 2)) != 0,
      "B15 mutation control: omitting the lambda A_mu A_nu stress (i.e. substituting A_0 = -N BEFORE varying) "
      "gives a DIFFERENT and WRONG rho (it still contains P(Q), the drag, and 2 sigma Q K_Q - sigma K): "
      "the multiplier's stress is load-bearing")

# --- route independence: A^0 (contravariant) as the fundamental variable
uf = sp.Function('u', positive=True)(t)
A_upper2 = [uf, 0, 0, 0]
A_lower2 = [sum(g[m, n] * A_upper2[n] for n in range(4)) for m in range(4)]
inv2 = frw_invariants(A_lower2, A_upper2, g, ginv, Gam)
u_, ud, udd, uddd, udddd = sp.symbols('u_ u_d u_dd u_ddd u_dddd', positive=True)
CH_u = [u_, ud, udd, uddd, udddd]


def to_syms2(e):
    e = e.doit()
    for k in range(4, 0, -1):
        e = e.subs(sp.Derivative(uf, (t, k)), CH_u[k])
    e = e.subs(uf, u_)
    return to_syms(e)


CH_saved = list(CH)
CH[3] = CH_u                      # swap the aether chain
pieces2 = {
    'EH': sqrtg_s * (Rs - 2 * Lam) / (16 * pi * G),
    'c2': sqrtg_s * c2 * to_syms2(inv2['divA']) ** 2,
    'c4': sqrtg_s * c4 * to_syms2(inv2['acc2']),
    'lam': sqrtg_s * lam_ * (to_syms2(inv2['AA']) + 1),
    'J': sqrtg_s * 2 * (2 - KB) * to_syms2(inv2['Jdphi']),
    'K': sqrtg_s * sigma * Kf(to_syms2(inv2['Q'])),
    'P': sqrtg_s * to_syms2(inv2['Y']) * Pf(to_syms2(inv2['Q'])),
    'm': -sqrtg_s * rho_m,
}
ONSHELL2 = {N_: 1, Nd: 0, Ndd: 0, Nddd: 0, u_: 1, ud: 0, udd: 0, uddd: 0}
EN2 = {k: sp.simplify(EL(L, CH[0]).subs(ONSHELL2).doit()) for k, L in pieces2.items()}
Ea2 = {k: sp.simplify(EL(L, CH[1]).subs(ONSHELL2).doit()) for k, L in pieces2.items()}
EA2 = {k: sp.simplify(EL(L, CH_u).subs(ONSHELL2).doit()) for k, L in pieces2.items()}
CH[3] = CH_saved[3]
lam2 = sp.solve(sp.Eq(sp.simplify(sum(EA2.values())), 0), lam_)[0]
rho_tot2 = sp.simplify(sum(-EN2[k] / a_ ** 3 for k in pieces2).subs(lam_, lam2))
p_tot2 = sp.simplify(sum(Ea2[k] / (3 * a_ ** 2) for k in pieces2).subs(lam_, lam2))
check(sp.simplify(rho_tot2 - rho_tot) == 0 and sp.simplify(p_tot2 - p_tot) == 0
      and sp.simplify(lam2 - lam_sol) != 0,
      "B16 route independence: with the CONTRAVARIANT A^0 as the fundamental variable, lambda comes out "
      "DIFFERENT but (E1), (E2) come out IDENTICAL -- the physical equations do not depend on which "
      "aether variable is varied (as they must)")

# --- continuity and Bianchi
cont = sp.simplify(Dt(rhoQ) + 3 * H * (rhoQ + pQ))
charge_eq = sp.simplify(Dt(a_ ** 3 * Kq) / a_ ** 3)          # = K_QQ Qd' + 3H K_Q
check(sp.simplify(cont - sigma * pd * charge_eq) == 0,
      "B17 (E5) continuity IS charge conservation:  rho_Q' + 3H(rho_Q + p_Q) = sigma Q d/dt[a^3 K_Q]/a^3 "
      "-- identically zero on (E3), for ANY K(Q)")
# Bianchi: d/dt(E1) using (E3) and matter conservation must reproduce (E2)-(E1)
E1 = 3 * H ** 2 * (1 - 24 * pi * G * c2) - Lam - 8 * pi * G * (rho_m + rhoQ)
E2 = (2 * Hdot + 3 * H ** 2) * (1 - 24 * pi * G * c2) - Lam + 8 * pi * G * (w_m * rho_m + pQ)
dE1 = Dt(E1)
# on the phi equation: Qdd = -3 H K_Q / K_QQ
Kqq = sp.Derivative(Kf(pd), (pd, 2))
dE1_on = sp.simplify(dE1.subs(pdd, -3 * H * Kq / Kqq))
bianchi = sp.simplify(dE1_on - 3 * H * (E2 - E1))
check(bianchi == 0,
      "B18 (E6) BIANCHI IDENTITY on FRW:  d/dt(E1) = 3H (E2 - E1)  given (E3) and fluid conservation -- "
      "the second Friedmann equation is not independent of the first; the reduced system is consistent")

# --- c2: the cosmological Newton constant
c2EA = sp.Symbol('c_2^EA', real=True)
Gcos = G / (1 - 24 * pi * G * c2)
check(sp.simplify(Gcos.subs(c2, -c2EA / (16 * pi * G)) - G / (1 + sp.Rational(3, 2) * c2EA)) == 0,
      "B19 (E7) G_cos = G/(1 - 24 pi G c2).  Dictionary: the Einstein-aether normalisation "
      "L = -(c2^EA/16 pi G)(div A)^2 is c2 = -c2^EA/(16 pi G), giving G_cos = G/(1 + 3 c2^EA/2): the "
      "Carroll-Lim (2004) result at c13 = 0, reproduced.  (If the generalized action intends c2 INSIDE "
      "the 1/16 pi G bracket, read c2^EA = -c2.)  c2 = 0 recovers plain GR.",
      "c2 is the ONE new coupling that touches the background; BBN bounds |G_cos/G_N - 1| at the "
      "~5-10% level, where G_N itself is renormalised by the scalar sector (wf3: G_N = (1+J_Y)/J_Y G~) "
      "-- a cross-sector consistency condition NOT computed here")

# =================================================================================================
banner("PART C -- the beta = 1 DBI sector: de Sitter minimum, dust excitation, invariants (sigma = 1)")
# =================================================================================================
u = sp.Symbol('u', real=True)                       # u = Q - Q0
nu = sp.Symbol('nu', positive=True)                 # nu = n/(mu M^2), the dimensionless charge
K_u = -M4 * sp.sqrt(1 - mu ** 2 * u ** 2 / M4)
n_u = sp.diff(K_u, u)                               # n = K_Q  (sigma = 1)
rho_u = sp.simplify((Q0 + u) * n_u - K_u)
p_u = K_u
check(sp.simplify(n_u - mu ** 2 * u / sp.sqrt(1 - mu ** 2 * u ** 2 / M4)) == 0,
      "C1  n = K_Q = mu^2 u / sqrt(1 - mu^2 u^2/M^4)  (exact, from the DBI)")
# exact inversion: s = mu u / M^2 = nu / sqrt(1+nu^2)
u_of_nu = (sp.sqrt(M4) / mu) * nu / sp.sqrt(1 + nu ** 2)
check(sp.simplify(n_u.subs(u, u_of_nu) / (mu * sp.sqrt(M4)) - nu) == 0,
      "C2  exact inversion of the charge relation: u = (M^2/mu) nu/sqrt(1+nu^2) with nu = n/(mu M^2); "
      "n ~ a^{-3} (E3)  ==>  nu(z) = nu_0 (1+z)^3 EXACTLY")
rho_nu = sp.simplify(rho_u.subs(u, u_of_nu))
p_nu = sp.simplify(p_u.subs(u, u_of_nu))
rho_nd = sp.simplify(rho_nu - Q0 * mu * sp.sqrt(M4) * nu)      # non-dust remainder = rho - Q0 n
check(sp.simplify(p_nu + M4 / sp.sqrt(1 + nu ** 2)) == 0
      and sp.simplify(rho_nd - M4 * sp.sqrt(1 + nu ** 2)) == 0,
      "C3  *** (E8) CLOSED FORM:  p = -M^4/sqrt(1+nu^2),   rho = Q0 n + M^4 sqrt(1+nu^2)  ***  "
      "(stage 19's rho_nd = M^4 sqrt(1+nu^2), p_nd = -M^4/sqrt(1+nu^2), re-derived)")
check(sp.simplify(rho_nd * p_nu + M4 ** 2) == 0,
      "C4  rho_nd . p = -M^8 : an EXACT invariant along the whole background (stage 19), re-derived")
check(sp.simplify(rho_nu.subs(nu, 0) - M4) == 0 and sp.simplify(p_nu.subs(nu, 0) + M4) == 0,
      "C5  (E9) DE SITTER MINIMUM nu = 0 (Q = Q0, K_Q = 0):  rho = M^4, p = -M^4, w = -1 EXACTLY;  "
      "Lambda_eff = Lambda_bare + 8 pi G M^4 (c=1; SI: Lambda_bare + 8 pi G M^4/c^2 with M^4 a mass density)")

# the excitation above the minimum, for GENERIC ghost-free K: series in the charge
n_s, K2, K3 = sp.symbols('n K2 K3', positive=True)
u_ser = sp.Symbol('u_s')
K_gen = -M4 + K2 * u_ser ** 2 / 2 + K3 * u_ser ** 3 / 6
n_gen = sp.diff(K_gen, u_ser)
# invert n(u) as a series
u_of_n = sp.Symbol('u_n')
sol_u = sp.series(sp.solve(sp.Eq(n_gen, n_s), u_ser)[0], n_s, 0, 3).removeO()
rho_gen = sp.series(((Q0 + u_ser) * n_gen - K_gen).subs(u_ser, sol_u), n_s, 0, 3).removeO()
p_gen = sp.series(K_gen.subs(u_ser, sol_u), n_s, 0, 3).removeO()
rho_exc = sp.simplify(rho_gen - M4)
p_exc = sp.simplify(p_gen + M4)
check(sp.simplify(rho_exc - (Q0 * n_s + n_s ** 2 / (2 * K2))) == 0
      and sp.simplify(sp.expand(p_exc) - n_s ** 2 / (2 * K2)) == 0,
      "C6  *** (E10) THE EXCITATION IS DUST, for ANY K with K_QQ(Q0) = K2 > 0:  rho_exc = Q0 n + "
      "n^2/(2 K2) + O(n^3),  p_exc = n^2/(2 K2) + O(n^3)  ==>  rho_exc LINEAR in the conserved charge, "
      "w_exc = p_exc/rho_exc -> n/(2 K2 Q0) -> 0. ***  (stage 5's rho = Q0 n, p = n^2/(2 mu^2) at K2 = mu^2)")
w_exc = sp.simplify(p_exc / rho_exc)
check(sp.limit(w_exc, n_s, 0) == 0 and sp.simplify(sp.limit(rho_exc / n_s, n_s, 0) - Q0) == 0,
      "C7  w_exc -> 0 and rho_exc/n -> Q0 as n -> 0: the dust mass IS the shift charge times Q0 (the "
      "stage-5 theorem), independent of K3 and of everything but Q0")
# adiabatic sound speed from the background alone
ca2 = sp.simplify(sp.diff(K_u, u) / ((Q0 + u) * sp.diff(K_u, u, 2)))
ca2_nu = sp.simplify(ca2.subs(u, u_of_nu))
check(sp.simplify(ca2_nu - u_of_nu / ((Q0 + u_of_nu) * (1 + nu ** 2))) == 0
      and sp.limit(ca2_nu, nu, 0) == 0 and sp.limit(ca2_nu, nu, sp.oo) == 0,
      "C8  adiabatic sound speed c_a^2 = p'/rho' = K_Q/(Q K_QQ) = u/[(Q0+u)(1+nu^2)]: -> 0 at the minimum "
      "AND -> 0 at the DBI wall (nu -> inf).  Background-only statement; the perturbative c_s^2 belongs "
      "to the SVT sector (stage 22), not re-derived here")
# full DBI w of the excitation and the w -> 0 at both ends
w_exc_dbi = sp.simplify((p_nu + M4) / (rho_nu - M4))
check(sp.limit(w_exc_dbi, nu, 0) == 0 and sp.limit(w_exc_dbi, nu, sp.oo) == 0,
      "C9  full DBI: w_exc(nu) -> 0 both as nu -> 0 (dust) and nu -> inf (the wall: p_exc -> M^4 while "
      "rho_exc ~ nu); the excitation is never a stiff fluid")

info("C10 (E10') Omega_dm bookkeeping: Omega_dm = Q0 n0/rho_crit is set by the INITIAL CHARGE n0 (free); "
     "with nu_0 = n0/(mu M^2) and M^4 = Omega_Lambda rho_crit this is the relation "
     "Q0 mu / M^2 = Omega_dm/(Omega_Lambda nu_0).  Stage 17's window nu_0 in [2.1e-5, 1.8e-4] with the SAME "
     "field carrying the full Omega_dm = 0.265 therefore needs Q0 mu/M^2 in [2.1e3, 1.8e4].  The v9 record "
     "instead books Omega_dm on a separate chi field and keeps the khronon at trace Omega <= 4.4e-7 "
     "(stage-3 black-hole ceiling); which bookkeeping holds is a FORK outside this sector.  (E1)-(E10) are "
     "identical in form either way.")

# numeric sanity along an actual background (parameters at the fork's single-field reading)
OmL, Omdm, Omb = mp.mpf('0.685'), mp.mpf('0.265'), mp.mpf('0.05')
Q0mu_over_M2 = mp.mpf('5000')
nu0 = Omdm / (OmL * Q0mu_over_M2)


def bg(z):
    nuz = nu0 * (1 + mp.mpf(z)) ** 3
    rho_d = OmL * (Q0mu_over_M2 * nuz + mp.sqrt(1 + nuz ** 2))      # in units of rho_crit,0 (M^4 = OmL)
    p_d = -OmL / mp.sqrt(1 + nuz ** 2)
    return nuz, rho_d, p_d


nu_0, rho_d0, p_d0 = bg(0)
check(abs(p_d0 / rho_d0 + OmL / (OmL + Omdm)) < mp.mpf('1e-6'),
      f"C11 numeric: today w_dark = {mp.nstr(p_d0 / rho_d0, 6)} = -Omega_Lambda/(Omega_Lambda+Omega_dm) "
      f"(the LCDM dark fluid), nu_0 = {mp.nstr(nu0, 4)}")
nu_r, rho_r, p_r = bg(1090)
check(abs((rho_r - OmL * Q0mu_over_M2 * nu_r) * p_r + OmL ** 2) < mp.mpf('1e-20')
      and abs(rho_r / (Omdm * 1091 ** 3) - 1) < mp.mpf('1e-3'),
      f"C12 numeric at z = 1090: rho_nd p = -M^8 holds to machine precision; rho_dark = "
      f"{mp.nstr(rho_r / (Omdm * 1091 ** 3), 8)} x Omega_dm (1+z)^3 (dust to 0.1%); the a^-6 transient "
      f"today is M^4 nu_0^2/2 = {mp.nstr(OmL * nu0 ** 2 / 2, 3)} rho_crit (stage 19 bound 3.2e-8: OK)")

# =================================================================================================
banner("PART D -- WHERE a0 COMES FROM: the promotion (INPUT) and the number (SI units restored)")
# =================================================================================================
kap, c_, G_, Lam_, H0, OmL_ = sp.symbols('kappa c G Lambda H_0 Omega_Lambda', positive=True)
rho_L_of_Lam = Lam_ * c_ ** 2 / (8 * pi * G_)                    # mass density of the vacuum
a0_prom = kap * c_ * sp.sqrt(G_ * rho_L_of_Lam)                 # the promotion at the minimum: a0^2 = kappa^2 c^2 G (-K(Q0)) = kappa^2 c^2 G rho_L
check(sp.simplify(a0_prom - kap * c_ ** 2 * sp.sqrt(Lam_ / (8 * pi))) == 0,
      "D1  (E11) a0 = kappa c sqrt(G rho_Lambda) with rho_Lambda = Lambda c^2/(8 pi G)  ==>  "
      "a0 = kappa c^2 sqrt(Lambda/(8 pi)):  G CANCELS identically; the single 8 pi of the vacuum density "
      "survives")
check(sp.simplify(a0_prom.subs(kap, sp.Rational(1, 2)) - c_ ** 2 * sp.sqrt(Lam_ / (32 * pi))) == 0,
      "D2  at kappa = 1/2:  a0 = c^2 sqrt(Lambda/(32 pi))  -- the committed closed form, reproduced "
      "(32 pi = 4 x 8 pi, the 4 being 1/kappa^2)")
HL = c_ * sp.sqrt(Lam_ / 3)                                     # H_Lambda = c sqrt(Lambda/3)
Zv = 2 * sp.sqrt(8 * pi / 3)
check(sp.simplify(c_ * HL / Zv - c_ ** 2 * sp.sqrt(Lam_ / (32 * pi))) == 0,
      "D3  a0 = c H_Lambda / Z with Z = 2 sqrt(8 pi/3) (v9 sec. 1.1) is the SAME number: kappa = 1/2 <=> Z "
      "identically; neither is derived from the other")
# numbers, both footings (memory rule 4)
cS = mp.mpf('299792458')
GS = mp.mpf('6.67430e-11')
MPC = mp.mpf('3.0856775814913673e22')


def a0_canonical(H0_kms, OmLam, kappa=mp.mpf('0.5')):
    H0s = mp.mpf(H0_kms) * 1000 / MPC
    rhoL = OmLam * 3 * H0s ** 2 / (8 * mp.pi * GS)
    return kappa * cS * mp.sqrt(GS * rhoL), rhoL, 3 * H0s ** 2 * OmLam / cS ** 2


a0_A, rhoL_A, Lam_A = a0_canonical('67.4', mp.mpf('0.685'))
a0_B = cS ** 2 * mp.sqrt(mp.mpf('1.1056e-52') / (32 * mp.pi))
a0_alt = mp.mpf('0.5') * cS * (mp.mpf('67.4') * 1000 / MPC) * mp.sqrt(3 / (8 * mp.pi))
check(abs(a0_A / mp.mpf('9.3619e-11') - 1) < mp.mpf('2e-3'),
      f"D4  NUMBER (canonical footing rho_DE/cH_Lambda, H0 = 67.4, Omega_Lambda = 0.685): "
      f"rho_Lambda = {mp.nstr(rhoL_A, 4)} kg/m^3, Lambda = {mp.nstr(Lam_A, 5)} m^-2, "
      f"a0 = {mp.nstr(a0_A, 5)} m/s^2  (committed 9.3619e-11; {mp.nstr(100 * (a0_A / mp.mpf('9.3619e-11') - 1), 2)}% = rounding)")
check(abs(cS ** 2 * mp.sqrt(Lam_A / (32 * mp.pi)) / a0_A - 1) < mp.mpf('1e-12'),
      "D4' the two routes (kappa c sqrt(G rho_Lambda) vs c^2 sqrt(Lambda/32 pi)) agree numerically to 1e-12")
info(f"D5  footing spread (rule: run both ways):  Planck-2018 Lambda = 1.1056e-52 m^-2 (H0 = 67.66, "
     f"Omega_Lambda = 0.6889) gives a0 = {mp.nstr(a0_B, 4)};  ALT footing rho_total/cH0 "
     f"(a0 = (1/2) c H0 sqrt(3/8 pi)) gives {mp.nstr(a0_alt, 4)}.  Canonical 9.36-9.43e-11 vs alt 1.13e-10.")
info("D6  *** kappa = 1/2 IS FITTED, NOT DERIVED.  Measured: 0.465 +/- 0.076 (BTFR) / 0.551 +/- 0.043 "
     "(distance-free); 1/2 lies within 1.2 sigma of both.  Nothing in this action fixes kappa: it enters "
     "the promotion as a free constant.  ***")
info("D7  *** THE PROMOTION a0^2(Q) = -kappa^2 c^2 G K(Q) IS A DEFINITIONAL CHOICE (stage 17), NOT A "
     "CONSEQUENCE OF THE ACTION.  What (E1)-(E9) DO establish is that the object it reads, -K(Q0) = M^4, is "
     "the dark sector's vacuum energy density AND its pressure magnitude (p = -M^4), so the identification "
     "a0^2 = kappa^2 c^2 G rho_Lambda is exact AT THE MINIMUM -- given two further inputs: ***")
info("D7a Lambda_bare = 0.  Otherwise Lambda_eff = Lambda_bare + 8 pi G M^4 (C5) and a0 reads only K's share: "
     "a0 = kappa c sqrt(G M^4) != kappa c sqrt(G rho_Lambda,obs).  (Stage 20's 'constants live in "
     "Lambda_bare' fixes beta; the coefficient additionally needs that Lambda_bare to be zero.)")
info("D7b which G.  The observable form a0 = kappa c^2 sqrt(Lambda_obs/8 pi) is G-free (D1).  The promotion "
     "contains an explicit G: with (E7) Lambda_obs = 8 pi G_cos M^4/c^2 (at Lambda_bare = 0), a0^2 = kappa^2 "
     "c^2 G_X M^4 = kappa^2 c^4 (G_X/G_cos) Lambda_obs/(8 pi).  The fitted kappa_obs = 1/2 refers to the "
     "G-free form, so the action-level constant is kappa_action = kappa_obs sqrt(G_cos/G_X): G_X = G_cos "
     "gives 1/2; G_X = bare G with c2 != 0 gives 1/(2 sqrt(1 - 24 pi G c2)); G_X = G_N with G_N = 2 G~ (wf3, "
     "J_Y = 1) gives 1/(2 sqrt 2) x sqrt(G_cos/G~).  An O(1) convention that must be fixed before 'kappa = 1/2' "
     "is compared to the action.  SUGGESTIVE (G_N is sector 2/3's).")

# =================================================================================================
banner("PART E -- a0(z): what the action gives (constant, then declining) vs the framework's a0 ~ H(z)")
# =================================================================================================
check(sp.simplify(sp.diff(K_u, u).subs(u, 0)) == 0 and sp.simplify((-K_u).subs(u, 0) - M4) == 0,
      "E1  at the EXACT minimum (n = 0) the promoted a0^2 = -kappa^2 c^2 G K(Q0) = kappa^2 c^2 G M^4 is a "
      "CONSTANT: no evolution without an excitation")
# theorem: for the pressure promotion and ANY ghost-free K, a0 is non-increasing in |n|
Kgen = sp.Function('K')
Qv = sp.Symbol('Q', real=True)
dnegK_dn = sp.simplify(sp.diff(-Kgen(Qv), Qv) / sp.diff(sp.diff(Kgen(Qv), Qv), Qv))   # d(-K)/dn = -K_Q/K_QQ = -n/K_QQ
check(sp.simplify(dnegK_dn + sp.diff(Kgen(Qv), Qv) / sp.diff(Kgen(Qv), Qv, 2)) == 0,
      "E2  (E12) THEOREM: along the background, d(-K)/dn = -K_Q/K_QQ = -n/K_QQ.  For a ghost-free K "
      "(K_QQ > 0) this is <= 0 for n >= 0 (and d(-K)/d|n| <= 0 for either sign), so under the PRESSURE "
      "promotion a0(z) is NON-INCREASING into the past (n ~ a^{-3} grows) for EVERY ghost-free K(Q). "
      "A rising a0(z) is impossible in this class -- not a property of the DBI choice.")
# the density promotion rises
drho_dn = sp.simplify(sp.diff(Qv * sp.diff(Kgen(Qv), Qv) - Kgen(Qv), Qv) / sp.diff(Kgen(Qv), Qv, 2))
check(sp.simplify(drho_dn - Qv) == 0,
      "E2' by contrast d(rho_Q)/dn = Q > 0: the DENSITY promotion a0^2 ~ rho_Q RISES into the past for "
      "every K.  The sign of da0/dz is fixed by WHICH scalar is promoted, not by K(Q).  Stage 17 chose the "
      "pressure (declining) on the CMB-off requirement and rejected the density (rising).")
# the beta = 1 closed form
negK_nu = sp.simplify((-K_u).subs(u, u_of_nu))
nu0s = sp.Symbol('nu_0', positive=True)
law = sp.simplify(negK_nu / negK_nu.subs(nu, nu0s))
check(sp.simplify(law - sp.sqrt(1 + nu0s ** 2) / sp.sqrt(1 + nu ** 2)) == 0,
      "E3  (E13) THE ACTION'S OWN LAW (beta = 1):  a0^2(z)/a0^2(0) = sqrt(1+nu_0^2)/sqrt(1+nu_0^2 (1+z)^6)  "
      "(stage 17 B2, re-derived from the DBI via (E3), (E8))")


def a0_ratio(z, nu0v):
    nuz = nu0v * (1 + mp.mpf(z)) ** 3
    return mp.sqrt(mp.sqrt(1 + nu0v ** 2) / mp.sqrt(1 + nuz ** 2))


nu_floor, nu_ceil = mp.mpf('2.1e-5'), mp.mpf('1.8e-4')
Omr = mp.mpf('9.2e-5')
Omm = mp.mpf('0.315')


def E_of_z(z):
    z = mp.mpf(z)
    return mp.sqrt(Omr * (1 + z) ** 4 + Omm * (1 + z) ** 3 + OmL)


def dens_prom(z):
    z = mp.mpf(z)
    return mp.sqrt((OmL + Omdm * (1 + z) ** 3) / (OmL + Omdm))


print("\n     a0(z)/a0(0):   action (pressure promotion, beta=1 DBI)   |  density promotion   |  H(z)/H0   |  w=-1 rho_DE")
print("        z        nu_0 = 2.1e-5      nu_0 = 1.8e-4               |  sqrt(rho_Q/rho_Q0)   |  (alt)     |  (canonical)")
rows = {}
for z in ('0.5', '1', '2', '5', '17', '35', '1090'):
    r1, r2 = a0_ratio(z, nu_floor), a0_ratio(z, nu_ceil)
    rows[z] = (r1, r2)
    print(f"   {z:>6s}       {mp.nstr(r1, 6):>10s}        {mp.nstr(r2, 6):>10s}                  |   "
          f"{mp.nstr(dens_prom(z), 5):>8s}          |  {mp.nstr(E_of_z(z), 5):>8s}  |   1")
check(all(abs(rows[z][1] - 1) < mp.mpf('0.01') for z in ('0.5', '1', '2', '5')),
      "E4  in-window the action's a0 is CONSTANT to < 1% for z <= 5 (every MOND test), stage 17 E2 reproduced")
check(rows['1090'][0] < mp.mpf('0.0065') and rows['1090'][1] > mp.mpf('0.0019'),
      f"E5  and OFF at recombination: a0(1090)/a0(0) = {mp.nstr(rows['1090'][1], 3)}-{mp.nstr(rows['1090'][0], 3)} "
      f"across the window (stage 17: 0.002-0.006), transition z_t = nu_0^{{-1/3}} - 1 in "
      f"[{mp.nstr(nu_ceil ** (-mp.mpf(1) / 3) - 1, 3)}, {mp.nstr(nu_floor ** (-mp.mpf(1) / 3) - 1, 3)}]")
check(E_of_z('1') > mp.mpf('1.7') and rows['1'][1] > mp.mpf('0.999'),
      f"E6  *** a0(z) ~ H(z) IS NOT A THEOREM OF THIS ACTION.  At z = 1 the framework's H(z) footing predicts "
      f"a0/a0(0) = {mp.nstr(E_of_z('1'), 4)} (rising); the action gives {mp.nstr(rows['1'][1], 6)} (constant); "
      f"the canonical w = -1 sqrt(rho_DE) footing gives exactly 1.  The three are distinguishable at the "
      f"factor-1.8 level by z = 1, and by 10^7 at recombination.  The 'a0 ~ H(z)' prediction is the "
      f"framework's, made outside this action; the action's promotion can only give the declining/constant "
      f"branch (E2).  THE INVERSE-K(Q) PROBLEM -- find a dark sector whose a0 tracks H(z) while its "
      f"excitation stays dust and its minimum stays w = -1 -- is OPEN, and E2 shows it has NO solution "
      f"inside 'single ghost-free K(Q) + pressure promotion'. ***")
info("E7  the density promotion (E2') tracks H(z) to ~4% (it is sqrt(rho_Lambda + rho_dm) vs sqrt(rho_total) "
     "-- the column above); stage 17 rejected it because MOND would be ON at recombination.  Whether that "
     "is fatal is a NONLINEAR-perturbation question (stage 22: the MOND term starts at THIRD order in FRW "
     "perturbations, so the linear CMB does not see a0(z) at all) -- NOT COMPUTED here, and it is exactly "
     "where the rising-vs-declining fork is decided.")

# =================================================================================================
banner("PART F -- the physical picture, with its one kinematic check")
# =================================================================================================
# Minkowski, comoving aether, phi = phibar(t) + chi(x): Y is exactly the spatial gradient squared of chi
tt, xx, yy, zz = sp.symbols('tt xx yy zz', real=True)
chi = sp.Function('chi')(xx, yy, zz)
phib = sp.Function('phib')(tt)
Phi_tot = phib + chi
XX = [tt, xx, yy, zz]
eta_inv = sp.diag(-1, 1, 1, 1)
Aup = [1, 0, 0, 0]
Y_mink = sum((eta_inv[m, n] + Aup[m] * Aup[n]) * sp.diff(Phi_tot, XX[m]) * sp.diff(Phi_tot, XX[n])
             for m in range(4) for n in range(4))
grad2 = sum(sp.diff(chi, s) ** 2 for s in (xx, yy, zz))
check(sp.simplify(Y_mink - grad2) == 0,
      "F1  with the aether comoving and phi = phibar(t) + chi(x):  Y = |grad chi|^2 EXACTLY -- Y is "
      "nonzero ONLY where phi has SPATIAL gradients in the aether frame, i.e. only where baryons (via the "
      "Poisson-like chi equation, sector 2) make them.  On FRW Y = 0 (A2) and the MOND kernel is switched "
      "off (A8).  Cf. stage 22: delta Y^(2) = |d(chi + Qbar alpha)|^2/a^2.")
info("F2  THE PICTURE (labelled SUGGESTIVE as prose, SOLID in its three checked parts A2/A8/F1 + C5/C6):  "
     "the dark sector is a shift-symmetric condensate sitting at the DBI minimum with w = -1 (its vacuum "
     "energy M^4 = rho_Lambda) and carrying a conserved charge whose excitation is dust (the CMB dark "
     "matter).  MOND is what that condensate does when baryonic gradients STRETCH it spatially (Y != 0): "
     "the response kernel Gcal(sqrt(Y)/a0) is normalised by the condensate's own scale, a0^2 = kappa^2 c^2 "
     "G (-K), i.e. a0 = kappa c sqrt(G rho_Lambda).  The normalisation is a choice (the promotion) whose "
     "coefficient kappa is fitted; the two faces (w = -1 and dust) and the switch-off on FRW are derived.")

# =================================================================================================
banner("SUMMARY -- equations, with status")
# =================================================================================================
print(r"""
  (E1)  3H^2 (1 - 24 pi G c2) = Lambda + 8 pi G [ rho_m + sigma (Q K_Q - K) ]                    SOLID (B6)
  (E2)  (2 dH/dt + 3H^2)(1 - 24 pi G c2) = Lambda - 8 pi G [ p_m + sigma K ]                     SOLID (B7)
  (E3)  d/dt [ a^3 sigma K_Q ] = 0 ,   n = sigma K_Q ~ a^{-3}   (shift charge)                    SOLID (B8)
  (E4)  rho_Q = sigma (Q K_Q - K) ,  p_Q = sigma K ;  sigma = +1 forced by -K(Q0) = rho_Lambda > 0   SOLID (B10-B12)
  (E5)  rho_Q' + 3H (rho_Q + p_Q) = sigma Q a^{-3} d/dt[a^3 K_Q] = 0 on (E3)                    SOLID (B17)
  (E6)  d/dt (E1) = 3H [(E2) - (E1)]  on (E3) + fluid conservation  (Bianchi)                  SOLID (B18)
  (E7)  G_cos = G/(1 - 24 pi G c2) = G/(1 + 3 c2^EA/2);  c4, K_B, (2-K_B) terms, bump: inert    SOLID (B19, B4, B9)
  (E8)  beta=1 DBI:  p = -M^4/sqrt(1+nu^2),  rho = Q0 n + M^4 sqrt(1+nu^2),  rho_nd p = -M^8    SOLID (C3, C4)
  (E9)  minimum Q = Q0:  rho = M^4, p = -M^4, w = -1 EXACTLY;  Lambda_eff = Lambda + 8 pi G M^4  SOLID (C5)
  (E10) excitation: rho_exc = Q0 n + n^2/(2 K_QQ) ,  p_exc = n^2/(2 K_QQ) ,  w_exc -> 0  (DUST)  SOLID (C6, C7)
  (E11) a0 = kappa c sqrt(G rho_Lambda) = kappa c^2 sqrt(Lambda/8 pi) -> c^2 sqrt(Lambda/32 pi)
        = 9.36e-11 m/s^2 (H0 = 67.4, Omega_Lambda = 0.685; 9.43e-11 at Planck Lambda; alt 1.13e-10)
        ARITHMETIC SOLID;  the promotion = INPUT (definitional);  kappa = 1/2 = INPUT (fitted);
        Lambda_bare = 0 and 'which G' = INPUT conventions (D7a, D7b)                          INPUT
  (E12) d(-K)/dn = -n/K_QQ <= 0 :  pressure-promoted a0 never rises into the past             SOLID (E2)
  (E13) a0^2(z)/a0^2(0) = sqrt(1+nu_0^2)/sqrt(1+nu_0^2(1+z)^6):  const to <1% (z<=5), off at
        recombination (0.002-0.006)                                                            SOLID (E3-E5)
  a0(z) ~ H(z):  NOT DERIVED from this action; rising branch = density promotion (E2'),
        rejected by stage 17 on a nonlinear-CMB argument that is NOT-COMPUTED here            NOT-COMPUTED
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
