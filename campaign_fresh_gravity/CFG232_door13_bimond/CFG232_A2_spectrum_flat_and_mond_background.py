#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A2_spectrum -- G5a (mode health) and G5c (c_T) for the local connection-difference BIMOND class, fresh code.
Labelled REPRODUCTION of the record's WF2/L70 closure (flat and static-MOND backgrounds) + NEW: the FRW background of 13b, the lapse-velocity
tuning re-derived, the u1/u0 line.  Controls C4, C5, C9; MUTATE M1, M3, M8.

Relative sector.  With H = (beta h + gamma hhat)/(beta+gamma) and delta = h - hhat the two Einstein-Hilbert terms split as (beta+gamma)EH[H] +
b EH[delta], b = beta gamma/(beta+gamma); the interaction depends on delta only.  Per 1/16piG the relative Lagrangian is
    K(delta) = b [ -1/2 delta.G[delta] ]  +  mu(b) T2(delta) ,   mu = -2 sigma_s m0 ,
with T2 the quadratic part of the tuned invariant.  The tuned degeneracy value from the static reduction (A1) is sigma_s m0 = b/8, i.e. mu = -b/4.
Fourier convention: d_mu -> i k_mu, k^mu = (omega,0,0,kappa); every bilinear is real.
"""
import os, sys, math, itertools
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A2_spectrum")
MUT = R.mutate
P = R.P
bite = []

om, ka, mu, bb, m2 = sp.symbols("omega kappa mu b m2")
u0, u1 = sp.symbols("u0 u1")
eta = sp.diag(-1, 1, 1, 1)
kup = sp.Matrix([om, 0, 0, ka])
klo = eta * kup
k2 = (kup.T * klo)[0]
idx = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
dsym = {ij: sp.Symbol(f"d{ij[0]}{ij[1]}") for ij in idx}


def dmat(sub=None):
    M = sp.zeros(4, 4)
    for (i, j), s_ in dsym.items():
        M[i, j] = s_
        M[j, i] = s_
    return M


D_ = dmat()
dvec = [dsym[ij] for ij in idx]


def up2(M):
    return eta * M * eta


def EHquad(d):
    """-1/2 d^{mn} G_mn with d_mu d_nu -> -k_mu k_nu"""
    dup = eta * d                                           # d^l_n
    trd = sum(eta[i, i] * d[i, i] for i in range(4))
    Rm = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            Rm[m, n] = sp.Rational(1, 2) * (-sum(klo[m] * kup[l] * d[l, n] for l in range(4)) - sum(klo[n] * kup[l] * d[l, m] for l in range(4))
                                             + k2 * d[m, n] + klo[m] * klo[n] * trd)
    Rs = sum(eta[i, i] * Rm[i, i] for i in range(4))
    Gm = Rm - sp.Rational(1, 2) * eta * Rs
    return sp.expand(-sp.Rational(1, 2) * sum(eta[i, i] * eta[j, j] * d[i, j] * Gm[i, j] for i in range(4) for j in range(4)))


def cconn(d):
    """c^a_{bc} = 1/2 eta^{al}(k_b d_{lc} + k_c d_{lb} - k_l d_{bc})"""
    Cc = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b_ in range(4):
            for c_ in range(4):
                Cc[a][b_][c_] = sp.Rational(1, 2) * eta[a, a] * (klo[b_] * d[a, c_] + klo[c_] * d[a, b_] - klo[a] * d[b_, c_])
    return Cc


def Tquad(d):
    Cc = cconn(d)
    R4 = range(4)
    gi = eta
    g = eta
    Pv = [sum(gi[m, n] * Cc[a][m][n] for m in R4 for n in R4) for a in R4]
    V = [sum(Cc[a][a][mu_] for a in R4) for mu_ in R4]
    T1 = sum(g[a, b_] * gi[m, r] * gi[n, s_] * Cc[a][m][n] * Cc[b_][r][s_] for a in R4 for b_ in R4 for m in R4 for n in R4 for r in R4 for s_ in R4)
    T2 = sum(g[a, b_] * Pv[a] * Pv[b_] for a in R4 for b_ in R4)
    T3 = sum(gi[m, n] * V[m] * V[n] for m in R4 for n in R4)
    T4 = sum(gi[m, n] * Cc[a][m][b_] * Cc[b_][n][a] for m in R4 for n in R4 for a in R4 for b_ in R4)
    T5 = sum(Pv[a] * V[a] for a in R4)
    return [sp.expand(T) for T in (T1, T2, T3, T4, T5)]


def tuned(Ts, uu0, uu1):
    return sp.expand(-uu0 * Ts[0] - uu1 / 2 * (Ts[1] + Ts[2]) + uu0 * Ts[3] + uu1 * Ts[4])


LEH = EHquad(D_)
TS = Tquad(D_)

R.banner("C9  calibration of the detector: gauge invariance, Stueckelberg vanishing of EH, Fierz-Pauli healthy vector")
A0_, Ax, Ay, Az, Pi = sp.symbols("A0 Ax Ay Az pi")
Avec = [A0_, Ax, Ay, Az]


def stueck(with_pi=True):
    M = sp.zeros(4, 4)
    for i in range(4):
        for j in range(4):
            M[i, j] = klo[i] * Avec[j] + klo[j] * Avec[i] + (klo[i] * klo[j] * Pi if with_pi else 0)
    return M


DS = stueck()
R.check("C9 EH quadratic form is invariant under d -> d + k A + A k + k k pi (gauge): zero on the pure-gauge directions", sp.simplify(EHquad(DS)) == 0)
# FP: L = L_EH - (m^2/4)(d_mn d^mn - d^2)
def FPmass(d):
    trd = sum(eta[i, i] * d[i, i] for i in range(4))
    return sp.expand(sum(eta[i, i] * eta[j, j] * d[i, j] * d[i, j] for i in range(4) for j in range(4)) - trd ** 2)


LA_FP = sp.factor(sp.simplify(EHquad(DS) - m2 / 4 * FPmass(DS)).subs({A0_: 0, Ay: 0, Az: 0, Pi: 0}))
P(f"  FP vector (A_x): L = {LA_FP}   (healthy iff the omega^2 coefficient is positive: -(m2/4)*... see sign)")
cw = sp.Poly(sp.expand(LA_FP), om).coeff_monomial(om ** 2)
R.check("C9 Fierz-Pauli control: the helicity-1 Stueckelberg vector has a SECOND-order operator with POSITIVE omega^2 coefficient (healthy)", sp.degree(sp.expand(LA_FP), om) == 2 and sp.simplify(cw * Ax ** 0) != 0 and sp.simplify((cw / Ax ** 2).subs(m2, 1)) > 0, f"omega^2 coeff = {sp.simplify(cw)}")
# full 10x10 det for FP: degree in omega should be 10 (5 dof)
Mfp = sp.hessian(LEH - m2 / 4 * FPmass(D_), dvec)
detfp = sp.factor(sp.simplify(Mfp.det()))
dgfp = sp.degree(sp.expand(sp.numer(sp.together(detfp))), om)
P(f"  FP det K = {detfp}   degree in omega = {dgfp} (5 dof <-> 10)")
R.check("C9 FP control: det of the 10x10 kinetic matrix has omega-degree 10 (five dof: massive graviton)", dgfp == 10, f"degree {dgfp}")

# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 1  relative-sector quadratic form K(delta) = L_EH + mu T2, tuned family (c1..c5) = (-u0,-u1/2,-u1/2,u0,u1)")
Tt = tuned(TS, u0, u1)
Kfull = sp.expand(LEH + mu * Tt)
# static check: fields d00=-2 dPhi, dij = -2 dPsi delta_ij with k along z: recover (per 1/16piG, factor 2 relative to 1/8piG)
phi_, psi_ = sp.symbols("phi psi")
static_sub = {dsym[(0, 0)]: -2 * phi_, dsym[(1, 1)]: -2 * psi_, dsym[(2, 2)]: -2 * psi_, dsym[(3, 3)]: -2 * psi_, dsym[(0, 1)]: 0, dsym[(0, 2)]: 0, dsym[(0, 3)]: 0, dsym[(1, 2)]: 0, dsym[(1, 3)]: 0, dsym[(2, 3)]: 0}
Kst = sp.expand(Kfull.subs(static_sub).subs(om, 0))
Sm = sp.hessian(Kst, (phi_, psi_)) / 2
detS = sp.factor(sp.simplify(Sm.det()))
P(f"  static (omega=0) 2x2 kinetic matrix in (dPhi, dPsi), tuned family: det = {detS}")
# expected: at u1=0: [[-4 mu*..]] ; degeneracy at mu = -1/4 * b (b=1 here) for u=(1,0)
det10 = sp.simplify(detS.subs({u0: 1, u1: 0}))
solmu = sp.solve(det10, mu)
P(f"  T4-T1 (u0=1,u1=0): static determinant vanishes at mu = {solmu}   (A1: sigma_s m0 = b/8 -> mu = -2 sigma_s m0 / b = -1/4;  or sigma_s m0 = -b/4 -> mu = +1/2)")
R.check("static degeneracy of the relative sector at mu = -1/4 and mu = +1/2 (units b=1): agrees with A1's D(x)=0 roots x = 1/8, -1/4 (mu = -2x)", sorted(solmu) == sorted([-sp.Rational(1, 4), sp.Rational(1, 2)]), f"{solmu}")

# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 2  vector (helicity-1) and scalar (helicity-0) Stueckelberg sectors on the flat background: is there a higher-derivative mode?")
sub_v = {A0_: 0, Ay: 0, Az: 0, Pi: 0}
LAx = sp.factor(sp.expand(sp.simplify(Kfull.subs({dsym[ij]: DS[ij] for ij in idx}).subs(sub_v))))
P(f"  L_A1(omega,kappa) = {LAx}")
polyA = sp.Poly(sp.expand(LAx / Ax ** 2), om)
degA = polyA.degree()
R.num("L_A1", str(LAx))
# expected -(mu/2)... times (kappa^2-omega^2)^2 (2u0+u1): record: L_A1 = -(lambda/2)(2u0+u1)(k-w)^2(k+w)^2 A1^2 with M=lambda T
ratioA = sp.simplify(LAx / (Ax ** 2 * mu * (2 * u0 + u1) * (ka ** 2 - om ** 2) ** 2))
P(f"  L_A1 / [mu (2u0+u1) (kappa^2-omega^2)^2 A_x^2] = {ratioA}")
R.check("C4/G5a: the helicity-1 Stueckelberg vector has a FOURTH-order operator (omega-degree 4) proportional to (2u0+u1)(kappa^2-omega^2)^2, i.e. to the static MOND coefficient a = -2(2u0+u1) (record's WF2/L70 structure, fresh code)",
        degA == 4 and ratioA.free_symbols.isdisjoint({om, ka, u0, u1, mu}), f"omega-degree {degA}, ratio {ratioA}")
# relation to a: a = -4u0 - 2u1 = -2(2u0+u1): L_A1 = (mu/4) * a * (kappa^2-omega^2)^2 * ratio-fixed
ghost_indep_of_sign = True
P("  a fourth-order operator (kappa^2-omega^2)^2 is a dipole ghost (Ostrogradsky) for either sign of its coefficient: no sign choice of mu removes it while a != 0")
# scalar sector: pure pi row/column
sub_s = {Ax: 0, Ay: 0}
Ls = sp.expand(Kfull.subs({dsym[ij]: DS[ij] for ij in idx}).subs(sub_s))
Hs = sp.hessian(Ls, (A0_, Az, Pi)) / 2
P(f"  helicity-0 Stueckelberg 3x3 form (A0, Az, pi) row for pi: {[sp.factor(sp.simplify(e)) for e in Hs[2, :]]}")
pi_row_zero = all(sp.simplify(e.subs({u0: 1, u1: 0})) == 0 for e in Hs[2, :])
R.check("C4: on the tuned subspace the pure-pi row and column of the helicity-0 Stueckelberg form vanish identically (record: 'removes the leading pure-helicity-0 term')", pi_row_zero, "T4-T1")
detHs = sp.factor(sp.simplify(Hs.det()))
P(f"  det of the 3x3 helicity-0 form = {detHs}")

# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 3  TT branch dispersion (c_T) and the whole u1/u0 line")
sub_t = {dsym[ij]: 0 for ij in idx}
tens = {dsym[(1, 2)]: sp.Symbol("hx")}
LT = sp.expand(Kfull.subs({dsym[ij]: (sp.Symbol('hx') if ij == (1, 2) else 0) for ij in idx}))
LT = sp.factor(sp.simplify(LT))
P(f"  L_TT(cross polarisation) = {LT}")
solw = sp.solve(sp.numer(sp.together(LT / sp.Symbol('hx') ** 2)), om)
P(f"  omega solutions: {solw}")
cT = {}
for (a_, b_) in [(1, 0), (0, 1), (1, 1), (1, -1), (2, -1), (1, 3)]:
    LTv = sp.simplify(LT.subs({u0: a_, u1: b_, mu: -sp.Rational(1, 4)}) / sp.Symbol("hx") ** 2)
    sols = sp.solve(sp.numer(sp.together(LTv)), om)
    cT[(a_, b_)] = [sp.simplify(s_ ** 2 / ka ** 2) for s_ in sols]
    P(f"    (u0,u1)=({a_},{b_}), mu=-1/4 (b=1): L_TT = {sp.factor(LTv)} ; omega^2/kappa^2 = {cT[(a_, b_)]}")
LTgen = sp.simplify(LT / sp.Symbol("hx") ** 2)
P(f"  L_TT(relative) = {LTgen}  -> for any mu with 1 + 4 mu u0 != 0 the dispersion is omega^2 = kappa^2 (c_T = 1); at the H1 degeneracy mu = -1/(4 u0) (u1 = 0) the relative TT kinetic term VANISHES")
R.check("C4/G5c: for a non-degenerate mu the relative TT dispersion is omega^2 = kappa^2 exactly (c_T = 1), as the record states (record: c_T^2 = 1 at T4-T1)",
        sp.simplify(LTgen / ((ka ** 2 - om ** 2) * (1 + 4 * mu * u0))).free_symbols.isdisjoint({om, ka, mu, u0, u1}))
c14 = cT[(1, 0)]
R.num("cT_line", {str(k): [str(v) for v in vv] for k, vv in cT.items()})

# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 4  lapse-velocity tuning on a generic FRW background (own derivation) and the two-lapse Hessian (M8 target)")
tt = sp.Symbol("t")
N_, Nh, a_, ah = [sp.Function(n)(tt) for n in ["N", "Nh", "a", "ah"]]
XX = [tt] + list(sp.symbols("x y z"))


def chris_t(g):
    gi = g.inv()
    Gm = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                Gm[l][m][n] = sum(gi[l, s_] * (sp.diff(g[s_, m], XX[n]) + sp.diff(g[s_, n], XX[m]) - sp.diff(g[m, n], XX[s_])) for s_ in range(4)) / 2
    return Gm


gF = sp.diag(-N_ ** 2, a_ ** 2, a_ ** 2, a_ ** 2)
ghF = sp.diag(-Nh ** 2, ah ** 2, ah ** 2, ah ** 2)
C1, C2 = chris_t(gF), chris_t(ghF)
CF = [[[sp.simplify(C1[l][m][n] - C2[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]


def Tinv_full(Cc, g, gi):
    R4 = range(4)
    Pv = [sum(gi[m, n] * Cc[a][m][n] for m in R4 for n in R4) for a in R4]
    V = [sum(Cc[a][a][mu_] for a in R4) for mu_ in R4]
    T1 = sum(g[a, b_] * gi[m, r] * gi[n, s_] * Cc[a][m][n] * Cc[b_][r][s_] for a in R4 for b_ in R4 for m in R4 for n in R4 for r in R4 for s_ in R4)
    T2 = sum(g[a, b_] * Pv[a] * Pv[b_] for a in R4 for b_ in R4)
    T3 = sum(gi[m, n] * V[m] * V[n] for m in R4 for n in R4)
    T4 = sum(gi[m, n] * Cc[a][m][b_] * Cc[b_][n][a] for m in R4 for n in R4 for a in R4 for b_ in R4)
    T5 = sum(Pv[a] * V[a] for a in R4)
    return [sp.simplify(T) for T in (T1, T2, T3, T4, T5)]


TF = Tinv_full(CF, gF, gF.inv())
dN, dNh = sp.symbols("dN dNh")
Ndot, Nhdot = sp.diff(N_, tt), sp.diff(Nh, tt)
cs5 = sp.symbols("c1:6")
comb = sp.expand(sum(c * T for c, T in zip(cs5, TF)))
comb = comb.subs({Ndot: dN, Nhdot: dNh})
pol = sp.Poly(comb, dN, dNh)
conds = []
Ns, Nhs, as_, ahs, das, dahs = sp.symbols("Ns Nhs as ahs das dahs", positive=True)
bg = {N_: Ns, Nh: Nhs, a_: as_, ah: ahs, sp.diff(a_, tt): das, sp.diff(ah, tt): dahs}
for (i, j), co in pol.terms():
    if i + j > 0:
        num = sp.expand(sp.numer(sp.together(co.subs(bg))))
        pp = sp.Poly(num, Ns, Nhs, as_, ahs, das, dahs)
        conds += [c_ for c_ in pp.coeffs()]
solc = sp.solve(conds, cs5, dict=True)
P(f"  lapse-velocity-free conditions on (c1..c5) for generic FRW: {solc}")
sol0 = solc[0] if solc else {}
free = [c for c in cs5 if c not in sol0]
P(f"  free parameters: {free}")
# compare with the record's family: substitute and check the conditions hold
rec = {cs5[0]: -u0, cs5[1]: -u1 / 2, cs5[2]: -u1 / 2, cs5[3]: u0, cs5[4]: u1}
hold = all(sp.simplify(c_.subs(rec)) == 0 for c_ in conds)
dim_sol = len(free)
R.check("C4: the record's tuned family (-u0,-u1/2,-u1/2,u0,u1) removes every lapse-velocity term on a generic FRW background, and the solution space of the lapse-velocity-free conditions is 2-dimensional (own derivation)",
        hold and dim_sol == 2, f"holds={hold}, dim={dim_sol}, sol={sol0}")
# off-line: T1 alone
offc = {cs5[0]: 1, cs5[1]: 0, cs5[2]: 0, cs5[3]: 0, cs5[4]: 0}
poff = sp.Poly(sp.expand(sum(offc[c] * T for c, T in zip(cs5, TF))).subs({Ndot: dN, Nhdot: dNh}), dN, dNh)
lapse_terms_off = [sp.simplify(co.subs(bg)) for (i, j), co in poff.terms() if i + j > 0]
P(f"  M8 target: an off-line point (T1 alone) has lapse-velocity terms: {lapse_terms_off}")
R.num("lapse_terms_off_line", [str(t_) for t_ in lapse_terms_off])

# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 5  nonlinear static-MOND background: exact pulled-back metric g' = phi*g for xi^x = eps A(t,z), g-hat = eta (own code)")
t_, z_, e_ = sp.symbols("t z epsilon")
pp_, qq_ = sp.symbols("p q")
Af = sp.Function("A")(t_, z_)
XY = [t_, sp.Symbol("x"), sp.Symbol("y"), z_]
gxx = 1 - 2 * qq_ * z_
gtt = -(1 + 2 * pp_ * z_)
# g'_{mu nu} = d_mu X^a d_nu X^b g_ab(X), X = (t, x + eps A(t,z), y, z); g depends on z only -> g_ab(X)=g_ab(z)
gp = sp.zeros(4, 4)
gp[0, 0] = gtt + e_ ** 2 * sp.diff(Af, t_) ** 2 * gxx
gp[0, 3] = gp[3, 0] = e_ ** 2 * sp.diff(Af, t_) * sp.diff(Af, z_) * gxx
gp[3, 3] = gxx + e_ ** 2 * sp.diff(Af, z_) ** 2 * gxx
gp[1, 1] = gxx
gp[2, 2] = gxx
gp[0, 1] = gp[1, 0] = e_ * sp.diff(Af, t_) * gxx
gp[3, 1] = gp[1, 3] = e_ * sp.diff(Af, z_) * gxx
g0 = sp.diag(gtt, gxx, gxx, gxx)
g0i = sp.diag(1 / gtt, 1 / gxx, 1 / gxx, 1 / gxx)
h1m = sp.zeros(4, 4); h2m = sp.zeros(4, 4)
h1m[0, 1] = h1m[1, 0] = sp.diff(Af, t_) * gxx
h1m[3, 1] = h1m[1, 3] = sp.diff(Af, z_) * gxx
h2m[0, 0] = sp.diff(Af, t_) ** 2 * gxx
h2m[0, 3] = h2m[3, 0] = sp.diff(Af, t_) * sp.diff(Af, z_) * gxx
h2m[3, 3] = sp.diff(Af, z_) ** 2 * gxx
gp = g0 + e_ * h1m + e_ ** 2 * h2m
gpi = g0i - e_ * g0i * h1m * g0i + e_ ** 2 * (-g0i * h2m * g0i + g0i * h1m * g0i * h1m * g0i)


def trunc(ex, n=2):
    ex = sp.expand(ex)
    return sum(ex.coeff(e_, k) * e_ ** k for k in range(n + 1))


Gp = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            Gp[l][m][n] = trunc(sum(gpi[l, s_] * (sp.diff(gp[s_, m], XY[n]) + sp.diff(gp[s_, n], XY[m]) - sp.diff(gp[m, n], XY[s_])) for s_ in range(4)) / 2)
R4 = range(4)
nz = [(a, m, n) for a in R4 for m in R4 for n in R4 if Gp[a][m][n] != 0]
T1b = 0
for (a, m, n) in nz:
    for (b_, r, s_) in nz:
        if gp[a, b_] == 0:
            continue
        T1b += gp[a, b_] * gpi[m, r] * gpi[n, s_] * Gp[a][m][n] * Gp[b_][r][s_]
T1b = trunc(T1b)
T4b = 0
for (a, m, b_) in nz:
    for (b2, n, a2) in nz:
        if b2 == b_ and a2 == a:
            T4b += gpi[m, n] * Gp[a][m][b_] * Gp[b_][n][a]
T4b = trunc(T4b)
Tb41 = T4b - T1b
Tser = trunc(Tb41)
Att, Atz, Azz, At, Az = sp.symbols("Att Atz Azz At Az")
jet2 = {sp.Derivative(Af, (t_, 2)): Att, sp.Derivative(Af, t_, z_): Atz, sp.Derivative(Af, (z_, 2)): Azz}
jet1 = {sp.Derivative(Af, t_): At, sp.Derivative(Af, z_): Az}


def atpoint(ex):
    ex = ex.subs(jet2).subs(jet1)
    return ex.subs(z_, 0)


T0 = sp.simplify(atpoint(Tser.coeff(e_, 0)))
T1c = sp.simplify(atpoint(Tser.coeff(e_, 1)))
T2j = sp.expand(sp.simplify(atpoint(Tser.coeff(e_, 2))))
P(f"  background T(T4-T1) at z=0 (exact in p,q): {sp.factor(T0)}")
R.check("C4: background value T4-T1 = -4(p^2 + 2q^2) and vanishing first-order variation of T (record: T-bar = -4(p^2+2q^2), delta T = 0)", sp.simplify(T0 + 4 * (pp_ ** 2 + 2 * qq_ ** 2)) == 0 and sp.simplify(T1c) == 0, f"delta T_1 = {T1c}")
hi_form = sp.expand(T2j.subs({At: 0, Az: 0}))
P(f"  second-jet quadratic form of T_2 (exact in p,q): {sp.factor(hi_form)}")
sym4 = sp.factor(sp.expand(hi_form.subs({Att: -om ** 2, Atz: -om * ka, Azz: -ka ** 2})))
P(f"  four-derivative symbol of the vector operator on the static-MOND background: {sym4}")
R.check("Part 5: on the static-MOND background the vector operator's principal part is (kappa^2-omega^2)^2 times a coefficient independent of the background gradients p,q (the interaction contributes L2 = -sigma_s M'(Qbar) T_2): still fourth order at every M' != 0",
        sp.simplify(sym4 / ((ka ** 2 - om ** 2) ** 2)).free_symbols.isdisjoint({om, ka, pp_, qq_}) and sp.simplify(sym4) != 0, f"symbol = {sym4}")
first = sp.expand(T2j.subs({Att: 0, Atz: 0, Azz: 0}))
P(f"  first-jet part of T_2 (background dependent): {sp.factor(first)}")
R.num("vector_background", dict(sym4=str(sym4), first=str(first), second_jets=str(hi_form)))
# ---------------------------------------------------------------------------------------------------------------
R.banner("Part 6  full 10x10 determinant: degree in omega and dof count for the tuned relative sector (mu = -1/4, u=(1,0))")
K10 = sp.hessian(Kfull.subs({u0: 1, u1: 0, mu: sp.Symbol("mu")}), dvec)
P(f"  full 10x10 form for generic mu, T4-T1: det = {sp.factor(sp.simplify(K10.det()))}   (identically zero: a residual gauge-like null direction, the pure-pi direction d = k k pi, on which K vanishes: pi row = 0 above)")
kill = dvec.index(dsym[(3, 3)])                                    # gauge-fix d_zz = 0 (pi shifts d_zz by kappa^2 pi)
keep = [i for i in range(10) if i != kill]
K9 = K10.extract(keep, keep)
det9 = sp.factor(sp.simplify(K9.det()))
P(f"  9x9 form after fixing d_zz=0: det = {det9}")
den9 = sp.numer(sp.together(det9))
dg9 = sp.degree(sp.expand(den9), om) if det9 != 0 else -1
P(f"  omega-degree of the 9x9 determinant (generic mu) = {dg9}  -> dof = {dg9/2 if dg9>=0 else 'n/a'} counting an Ostrogradsky vector as 2")
K9t = K9.subs(sp.Symbol("mu"), -sp.Rational(1, 4))
det9t = sp.factor(sp.simplify(K9t.det()))
P(f"  9x9 at the tuned mu = -1/4: det = {det9t}")
dg9t = sp.degree(sp.expand(sp.numer(sp.together(det9t))), om) if det9t != 0 else -1
R.num("det9", dict(generic=str(det9), tuned=str(det9t), deg_generic=int(dg9), deg_tuned=int(dg9t)))
# pure EH + FP comparison degree already checked in C9
# ---------------------------------------------------------------------------------------------------------------
R.banner("DC-018 control C5: helicity-0 Galileon spherical flux")
n_, r_ = sp.symbols("n r", positive=True)
R.check("C5 DC-018: r^(3-n)(pi')^n ~ GM => pi' ~ r^(1-3/n); pi' ~ r^-1 requires n = 3/2 (not an integer Galileon order)", sp.solve(sp.Eq(1 - 3 / n_, -1), n_) == [sp.Rational(3, 2)])

# ---------------------------------------------------------------------------------------------------------------
R.banner("G5a / G5c verdicts")
vector_ghost = degA == 4
R.verdict("G5a (13a/13b, flat and static-MOND: REPRODUCTION)", "FAIL" if vector_ghost else "PASS",
          "the helicity-1 Stueckelberg vector has a fourth-order operator whose coefficient is the MOND coefficient; a != 0 <=> higher-derivative vector (dipole ghost for either sign)")
tt_zero = sp.simplify(sp.numer(sp.together(LT / sp.Symbol('hx') ** 2)).subs({u0: 1, u1: 0, mu: -sp.Rational(1, 4)})) == 0
R.verdict("G5c (T4-T1, branch A)", "UNDEFINED for the relative TT modes (their kinetic term vanishes exactly at the tuned value: strong coupling); the sum graviton has c_T = 1" if tt_zero else "PASS",
          "L_TT(relative) = -(hx^2/2)(kappa^2-omega^2)(1+4 mu u0): zero at mu = -1/(4u0), which is the H1 degeneracy needed for MOND; the record's c_T^2 = 1 was at a non-degenerate lambda")
R.verdict("G5a (13c single scalar)", "see A7", "")

# ============================================================================================ MUTATE
if MUT:
    R.banner(f"MUTATE {MUT}")
    if MUT == "M1":                                   # interaction off
        LA0 = sp.simplify(Kfull.subs({dsym[ij]: DS[ij] for ij in idx}).subs(sub_v).subs(mu, 0))
        P(f"  mu=0: L_A1 = {LA0} (pure EH: identically 0 on the Stueckelberg vector); ghost claim fails: {LA0 == 0}")
        bite.append(LA0 == 0)
    elif MUT == "M3":                                 # gamma -> infinity: b -> beta
        # b enters only the relative EH weight; the ghost coefficient is mu*T2 (independent of b); re-run the vector at b = 1e-6-shifted weights
        LAg = sp.simplify(LAx.subs(mu, -sp.Rational(1, 4) * sp.Rational(1, 1)))
        Ldeg = sp.degree(sp.expand(sp.numer(sp.together(LAg / Ax ** 2))), om)
        P(f"  gamma -> inf changes b = beta gamma/(beta+gamma) -> beta only; the Stueckelberg vector L_A1 has omega-degree {Ldeg} regardless of b (EH drops out on pure gauge directions): the counting does NOT change")
        bite.append(Ldeg != 4)                        # frozen expectation 'counting must change' -> expected NOT to bite
    elif MUT == "M8":                                 # detune off the tuned line: lapse-velocity terms appear
        nz = any(sp.simplify(t_) != 0 for t_ in lapse_terms_off)
        P(f"  off-line c = (1,0,0,0,0): lapse-velocity coefficients {lapse_terms_off} -> non-zero: {nz}")
        # flat-space pi row
        Toff = TS[0]
        Ls_off = sp.expand((LEH + mu * Toff).subs({dsym[ij]: DS[ij] for ij in idx}).subs({Ax: 0, Ay: 0}))
        Hs_off = sp.hessian(Ls_off, (A0_, Az, Pi)) / 2
        pirow = [sp.simplify(e) for e in Hs_off[2, :]]
        P(f"  off-line pi row of the helicity-0 form: {pirow} (nonzero => a pure-scalar higher-derivative term appears, the BD-type signature)")
        bite.append(nz and any(e != 0 for e in pirow))
R.finish(bite if MUT else None)
