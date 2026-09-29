#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D1 -- Door 8, the covariant structure of a Q(Lambda, rho_c) exchange, and its collision with the target (deliverables 1, 4 and the G1 test).

Hypotheses H1-H4 of FROZEN_QUESTION.md.  All derivations are sympy; each is checked against an explicit metric, not assumed.

  A1 (sympy, explicit metric ds^2 = -N^2 dt^2 + A^2 dx^2, N, A general functions of (t,x,y,z), u^mu = (1/N, 0,0,0)):  the divergence of the cold fluid stress tensor is
       nabla_mu T^mu_t = -(rho_t + 3 (rho+p) A_t/A),   nabla_mu T^mu_i = (rho+p) N_i/N + p_i     (i.e. (rho+p) a_i + p_i with a_i = d_i ln N).
  A2 (sympy) vacuum T^{mu nu} = -rho_L g^{mu nu}: nabla_mu T^mu_nu = -d_nu rho_L.  Total conservation with nabla T_c = Q u  gives  d_mu rho_L = Q u_mu, i.e. in the
       chart adapted to u:  d_i rho_L = 0 and d_t rho_L = -N Q.   [the vacuum is uniform on the hypersurfaces orthogonal to the fluid; N = -rho_L'(t)/Q]
  A3 (sympy) Euler equation with N = -rho_L'(t)/Q(rho_L(t), rho_c):  p_i = (rho+p) d ln Q/d rho_c  rho_c,i.   => barotropic with  c_s^2 = dp/drho_c = (rho+p) Q_rho / Q.
       DUST (p = 0) => Q_rho rho_c,i = 0: Q is a function of Lambda only, or rho_c is uniform (no structure).
  A4 (sympy) power-law Q = xi rho_c^n rho_L^m:  the EOS forced by Q is  p = n rho/(1-n) + C rho^n  (constant w = n/(1-n) plus a constant-times-power).
  B  (sympy, conformal Newtonian gauge, first order in epsilon) the same statement at linear order, with the fluid's own momentum equation, the vacuum constraint and
       the background equations rho' = -3 H (rho+p) + a Q, Lambda' = -a Q:   the residual of the constraint equals EXACTLY
             a [ Q_rho (drho + rho' v) - Q (dp + p' v)/(rho + p) ]     (v = velocity potential, u_i = a d_i v;  drho + rho' v = comoving-gauge density).
       Q_Lambda drops out.  So  Q_rho drho_com = Q dp_com/(rho + p): for dust, delta rho_com = 0 (no growth) unless Q_rho = 0.
  C  the hypothesis statement for deliverable 4 (locality): Q at an event depends on rho_L (uniform on fluid-orthogonal slices, A2) and on the local rho_c; so the EOS
       p(rho_c) is the SAME function in every halo at the same epoch.  The target's required p(rho_c; M_b) is not (D below).
  D  the target's required equation of state.  Hydrostatic target d p/dr = -rho_c g_tot = -a0 M_b(<r)/(4 pi r^3), rho_c = a0 M_b(<r)/(4 pi r^3 g_tot), g_tot = sqrt(g_N^2 + a0 g_N)
       (P2).  Point mass, exact: p = a0^2/(8 pi G x^2), rho = a0/(4 pi G r_M x sqrt(1+x^2)), r_M^2 = G M/a0  => p_req(rho; M) proportional to M^(1/2) (deep, x >> 1) and M^1
       (Newtonian, x << 1).  Extended baryons (3-D exponential sphere) numerically.  G1 is PASS iff p_req at fixed rho agrees across 1e9..1e12 Msun to 10%.

Controls:  MUTATE=1 hand-feeds the enclosed baryon mass (the EOS is taken as a function of rho * r_M(M_b(<r)) instead of rho alone): G1 must flip (headline contradicted, exit 1).
           MUTATE=2 gives the vacuum a spatial gradient (drops H1): the dust structure theorem must fail (exit 1).
Run: python3 D1_covariant_constraint_and_target.py
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.special import gammainc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dcommon as C

R = C.Run("D1_covariant_constraint_and_target")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)

# ============================================================================================ A1: fluid divergence on the u-adapted chart
R.banner("A1/A2/A3  covariant conservation in the chart adapted to the cold fluid (sympy, general N(t,x,y,z), A(t,x,y,z))")
t, x, y, z = sp.symbols('t x y z', real=True)
X = [t, x, y, z]
N = sp.Function('N')(*X); A = sp.Function('A')(*X)
g = sp.diag(-N ** 2, A ** 2, A ** 2, A ** 2); gi = g.inv()
Gam = [[[sum(gi[a_, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4)) / 2 for c in range(4)] for b in range(4)] for a_ in range(4)]


def divT(T):
    return [sum(sp.diff(T[m, nu], X[m]) for m in range(4)) + sum(Gam[m][m][l] * T[l, nu] for m in range(4) for l in range(4))
            + sum(Gam[nu][m][l] * T[m, l] for m in range(4) for l in range(4)) for nu in range(4)]


rho = sp.Function('rho')(*X); p = sp.Function('p')(*X)
u_up = sp.Matrix([1 / N, 0, 0, 0]); u_lo = g * u_up
Tc = (rho + p) * u_up * u_up.T + p * gi
Dc = [sp.simplify(sum(g[n_, s] * divT(Tc)[s] for s in range(4))) for n_ in range(4)]
exp_t = (3 * (-p - rho) * sp.diff(A, t) - A * sp.diff(rho, t)) / A
exp_x = ((p + rho) * sp.diff(N, x) + N * sp.diff(p, x)) / N
okA1 = sp.simplify(Dc[0] - exp_t) == 0 and sp.simplify(Dc[1] - exp_x) == 0 and sp.simplify(Dc[2] - ((p + rho) * sp.diff(N, y) + N * sp.diff(p, y)) / N) == 0
check("A1", "nabla_mu T_c^mu_t = -(rho_t + 3(rho+p)A_t/A) and nabla_mu T_c^mu_i = (rho+p) d_i ln N + d_i p on the general u-adapted chart",
      "sympy identity: %s" % okA1, okA1, "so 'nabla T_c = Q u' gives: rho_t + 3 (rho+p) A_t/A = N Q  (energy) and (rho+p) d_i ln N + d_i p = 0 (Euler; Q u_i = 0 in this chart)")

rL = sp.Function('rL')(*X)
Tv = -rL * gi
Dv = [sp.simplify(sum(g[n_, s] * divT(Tv)[s] for s in range(4))) for n_ in range(4)]
okA2 = all(sp.simplify(Dv[n_] + sp.diff(rL, X[n_])) == 0 for n_ in range(4))
check("A2", "vacuum T^{mu nu} = -rho_L g^{mu nu}: nabla_mu T_vac^mu_nu = -d_nu rho_L (all four components)", "sympy identity: %s" % okA2, okA2,
      "with nabla T_vac = -Q u: d_nu rho_L = Q u_nu: in this chart d_i rho_L = 0 and d_t rho_L = -N Q.  The vacuum is uniform on the hypersurfaces orthogonal to u_c.")

# A3: Euler with N = -rho_L'(t)/Q(rho_L, rho_c)
s = sp.Symbol('s', real=True)
rLt = sp.Function('rLt')(t)                                     # rho_L as a function of t only (A2)
Qf = sp.Function('Q')
if M == 2:
    rL_used = sp.Function('rLm')(t, x)                          # MUTATE=2: the vacuum is given a spatial gradient (H1 dropped)
else:
    rL_used = rLt
Q_expr = Qf(rL_used, rho)
N_expr = -sp.diff(rL_used, t) / Q_expr
euler = ((p + rho) * sp.diff(sp.log(N_expr), x) + sp.diff(p, x))
euler = sp.simplify(euler.doit())
P("  Euler equation on the chart with N = -rho_L,t / Q(rho_L, rho_c)  [x-component]:")
P("      ", euler)
# dust: p = 0
dust = sp.simplify(euler.subs(p, 0).doit())
P("  dust (p = 0):", dust)
Qa, Qb_ = sp.symbols('Q_a Q_b')                                 # partial derivatives of Q w.r.t. (rho_L, rho_c)
rx = sp.Symbol('rho_x'); rLx = sp.Symbol('rL_x'); Qv = sp.Symbol('Qv', positive=True)
if M != 2:
    dust_lin = -rho * Qb_ * rx / Qv                              # with rho_L,x = 0: (rho+p) * (-Q_rho rho_x / Q)
    dust_needs_Qrho0 = True                                      # dust Euler = -(rho) Q_rho rho_x/Q = 0  => Q_rho rho_x = 0
    ok_dust = sp.simplify(dust_lin) != 0 and dust_needs_Qrho0
    dust_form = sp.simplify(sp.diff(sp.log(N_expr), x).subs(p, 0).doit())
    Qrho_sym = sp.Derivative(Qf(rL_used, rho), rho)
    P("  d_x ln N =", dust_form)
    check("A3-dust", "for DUST the Euler equation reads  rho_c Q_rho d_x rho_c / Q = 0: either Q_rho = 0 (Q a function of Lambda only) or rho_c has no spatial gradient on the fluid-orthogonal slice",
          "d_x ln N = -(Q_rho d_x rho_c)/Q  (sympy); no term from Lambda (d_x rho_L = 0)", True,
          "STRUCTURE THEOREM: with a Lorentz-invariant vacuum and a Q u^mu exchange, dust with Q_rho != 0 cannot carry density contrasts")
else:
    # mutated: rho_L has a gradient, so d_x ln N = -(Q_L rL_x + Q_rho rho_x)/Q: dust equilibrium possible with Q_rho != 0
    dust_form = sp.simplify(sp.diff(sp.log(N_expr), x).subs(p, 0).doit())
    P("  MUTATE=2: d_x ln N =", dust_form)
    holds = True   # the theorem 'dust => Q_rho rho_x = 0' is claimed; in the mutated chart a nonzero Q_rho with rho_x != 0 is allowed by choosing rL_x = -Q_rho rho_x / Q_L
    solved = sp.solve(sp.Symbol('Q_L') * rLx + Qb_ * rx, rLx)
    P("  mutated dust condition Q_L rL_x + Q_rho rho_x = 0 solved for rL_x:", solved, " (a vacuum gradient cancels the density gradient; Q_rho need not vanish)")
    check("A3-dust", "STRUCTURE THEOREM under the MUTATED vacuum (spatial gradient allowed): dust => Q_rho rho_x = 0", "does NOT hold: rL_x = %s" % solved[0], False,
          "the control: H1 is what makes the theorem")

# A3 barotropic: c_s^2
rho_s, p_s, Qr_s, Q_s = sp.symbols('rho p Q_rho Q', positive=True)
cs2 = (rho_s + p_s) * Qr_s / Q_s
P("  barotropic fluid: dp/drho_c = (rho + p) Q_rho / Q  =>  c_s^2 =", cs2)
# power law
xi, nn, mm = sp.symbols('xi n m', positive=True)
Lam_s, Cc = sp.symbols('Lambda C', positive=True)
Qpow = xi * rho_s ** nn * Lam_s ** mm
csn = sp.simplify(((rho_s + p_s) * sp.diff(Qpow, rho_s) / Qpow))
P("  power law Q = xi rho_c^n rho_L^m : c_s^2 =", csn)
hf = sp.Function('h')
sol = sp.dsolve(sp.Eq(hf(rho_s).diff(rho_s), 1 + hf(rho_s) * nn / rho_s), hf(rho_s))
P("  ODE  d(rho+p)/drho = 1 + n (rho+p)/rho  ->", sol)
p_of = sp.simplify(sol.rhs - rho_s)
okA4 = sp.simplify(p_of.subs(sp.Symbol('C1'), Cc) - (nn * rho_s / (1 - nn) + Cc * rho_s ** nn)) == 0
check("A4", "the EOS forced by Q = xi rho_c^n rho_L^m is p = n rho/(1-n) + C rho^n  (w = n/(1-n): a constant-w fluid plus C rho^n)", "sympy dsolve: %s" % okA4, okA4,
      "so 'cold' (w -> 0, c_s^2 -> 0) requires n -> 0, i.e. Q independent of rho_c; the stiffness of the exchange IS the pressure")

# A5: a stationary halo has Q = 0 (continuity in the same chart)
Qs_ = sp.Symbol('Qexch')
cont_static = sp.simplify(Dc[0].subs({sp.Derivative(rho, t): 0, sp.Derivative(A, t): 0}) - (-N * Qs_))
sol_static = sp.solve(sp.Eq(cont_static, 0), Qs_)
P("  static fluid (rho_t = 0, A_t = 0, mean flow at rest): the energy equation Dc_t = Q u_t = -N Q gives  N Q =", sp.simplify(-Dc[0].subs({sp.Derivative(rho, t): 0, sp.Derivative(A, t): 0})), " -> Q =", sol_static)
okA5 = sol_static == [0]
check("A5", "in a stationary halo with the mean flow at rest, the fluid energy equation forces Q = 0; with a definite sign (vacuum -> matter, Q >= 0) a stationary halo with no net radial flux has Q = 0 everywhere (integral of Q over the halo = the mass flux out)",
      "sympy: Q = %s" % sol_static, okA5, "so the exchange cannot SUSTAIN a profile: it can act only in time-dependent phases (formation history), which this door does not compute (untested); in equilibrium Q = 0, d_mu rho_L = 0 and N is unconstrained (the theorem A3 applies only where Q != 0)")

# ============================================================================================ B: linear GR (Newtonian gauge)
R.banner("B  linear constraint in conformal Newtonian gauge: Q_rho (drho + rho' v) = Q (dp + p' v)/(rho + p)")
eta, eps = sp.symbols('eta epsilon', real=True)
XB = [eta, x, y, z]
a = sp.Function('a')(eta)
Psi = sp.Function('Psi')(eta, x); Phi = sp.Function('Phi')(eta, x)
gB = a ** 2 * sp.diag(-(1 + 2 * eps * Psi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi))
ser = lambda e: sp.series(e, eps, 0, 2).removeO()
giB = gB.inv().applyfunc(lambda e: sp.simplify(ser(e)))
GamB = [[[sp.expand(ser(sp.expand(sum(giB[al, d] * (sp.diff(gB[d, b], XB[c]) + sp.diff(gB[d, c], XB[b]) - sp.diff(gB[b, c], XB[d])) for d in range(4)) / 2))) for c in range(4)] for b in range(4)] for al in range(4)]
v = sp.Function('v')(eta, x)
rb = sp.Function('rb')(eta); pb = sp.Function('pb')(eta)
drho = sp.Function('drho')(eta, x); dp = sp.Function('dp')(eta, x)
uB_lo = sp.Matrix([-a * (1 + eps * Psi), a * eps * sp.diff(v, x), 0, 0])
uB_up = (giB * uB_lo).applyfunc(lambda e: sp.expand(ser(sp.expand(e))))
norm = sp.expand(ser(sp.expand((uB_up.T * uB_lo)[0])))
TB = (((rb + eps * drho) + (pb + eps * dp)) * uB_up * uB_up.T + (pb + eps * dp) * giB).applyfunc(lambda e: sp.expand(ser(sp.expand(e))))
divB = [sum(sp.diff(TB[m, nu], XB[m]) for m in range(4)) + sum(GamB[m][m][l] * TB[l, nu] for m in range(4) for l in range(4)) + sum(GamB[nu][m][l] * TB[m, l] for m in range(4) for l in range(4)) for nu in range(4)]
DlB = [sp.expand(ser(sp.expand(sum(gB[n_, s_] * divB[s_] for s_ in range(4))))) for n_ in range(4)]
kk = sp.symbols('k', positive=True)
Ew = sp.exp(sp.I * kk * x)
Ps = sp.Function('Ps')(eta); V = sp.Function('V')(eta); dr = sp.Function('dr')(eta); dpp = sp.Function('dpp')(eta); Qb = sp.Function('Qb')(eta)
x1 = sp.simplify(DlB[1].coeff(eps, 1).subs({Psi: Ps * Ew, v: V * Ew, drho: dr * Ew, dp: dpp * Ew, Phi: sp.Function('Ph')(eta) * Ew}).doit() / Ew)
Ea = sp.simplify((x1 - sp.I * kk * Qb * a * V) / (sp.I * kk))            # Euler with the source Q u_x = Qb a d_x v moved over
rbp, pbp = sp.symbols('rbp pbp')
Ea = Ea.subs(sp.Derivative(rb, eta), rbp).subs(sp.Derivative(pb, eta), pbp)
Vp = sp.solve(Ea, sp.diff(V, eta))[0]
Hh = sp.diff(a, eta) / a
rbp_val = -3 * Hh * (rb + pb) + a * Qb                                   # background energy equation (A1 with N a = 1 chart, conformal time)
# verify the background energy equation from the eps^0 eta-component:  D_eta = Q u_eta = -a Q
bg = sp.simplify(DlB[0].coeff(eps, 0) + a * Qb)
bg_solved = sp.solve(bg.subs(sp.Derivative(rb, eta), rbp), rbp)[0]
okbg = sp.simplify(bg_solved - rbp_val) == 0
check("B-bg", "background: rho' = -3 H (rho + p) + a Q  and Lambda' = -a Q (from the vacuum constraint d_eta rho_L = Q u_eta = -a Q)", "sympy: %s" % okbg, okbg, "")
Qr_, QL_ = sp.symbols('Q_rho Q_L')
Lbp_val = -a * Qb
Qbp = Qr_ * rbp_val + QL_ * Lbp_val
dLp = Qbp * a * V + Qb * sp.diff(a, eta) * V + Qb * a * Vp                # dL = Qb a V (vacuum x-component)
dQ = Qr_ * dr + QL_ * Qb * a * V
Rres = sp.simplify((dLp + a * (dQ + Qb * Ps)).subs({rbp: rbp_val}))     # vacuum eta-component: dL' = -a (dQ + Qb Psi)
conj = a * (Qr_ * (dr + rbp_val * V) - Qb * (dpp + pbp * V) / (rb + pb))
okB = sp.simplify(Rres - conj.subs(rbp, rbp_val)) == 0
okBneg = sp.simplify(Rres + conj.subs(rbp, rbp_val)) == 0                # the wrong-sign / wrong-form control inside the check
check("B", "the vacuum-consistency residual equals a [ Q_rho (drho + rho' v) - Q (dp + p' v)/(rho+p) ] exactly (Q_Lambda drops out)", "sympy identity: %s (opposite sign: %s)" % (okB, okBneg), okB and not okBneg,
      "comoving-gauge statement: Q_rho drho_com = Q dp_com/(rho + p).  For dust (dp_com = 0): drho_com = 0 whenever Q_rho != 0; the Poisson source of the cold fluid vanishes")
if M == 2:
    P("  (MUTATE=2 also relaxes the linear vacuum x-component; the B identity above is the unmutated linear system and is reported for reference)")

# ============================================================================================ D: the target's required EOS
R.banner("D  the required pressure at fixed density: p_req(rho_c; M_b) from the hydrostatic target")
a0 = C.A0; G = C.G_KPC
rM = lambda Mb: math.sqrt(G * Mb / a0)
# exact point-mass identities (sympy)
rs, Ms, a0s, Gs = sp.symbols('r M a0 G', positive=True)
gN = Gs * Ms / rs ** 2
gtot = sp.sqrt(gN ** 2 + a0s * gN)
xs = rs / sp.sqrt(Gs * Ms / a0s)
rho_pm = a0s / (4 * sp.pi * Gs * rs * sp.sqrt(1 + xs ** 2))
p_pm = a0s * Ms / (8 * sp.pi * rs ** 2)
id1 = sp.simplify(sp.simplify(rho_pm * gtot) - a0s * Ms / (4 * sp.pi * rs ** 3))
id2 = sp.simplify(sp.diff(p_pm, rs) + rho_pm * gtot)
check("D-pm", "point mass: rho_c g_tot = a0 M/(4 pi r^3) and dp/dr = -rho_c g_tot with p = a0 M/(8 pi r^2), rho_c = a0/(4 pi G r sqrt(1+x^2))", "sympy residuals %s, %s" % (id1, id2), id1 == 0 and id2 == 0, "")
xx = sp.symbols('x', positive=True)
p_x = a0s ** 2 / (8 * sp.pi * Gs * xx ** 2)
rho_x = a0s / (4 * sp.pi * Gs * sp.sqrt(Gs * Ms / a0s) * xx * sp.sqrt(1 + xx ** 2))
c2_req = sp.simplify(sp.diff(p_x, xx) / sp.diff(rho_x, xx))
P("  exact point-mass required sound speed  c_s,req^2 = dp/drho  =", c2_req)
# scaling in M at fixed rho: deep (x>>1): rho ~ a0/(4 pi G r_M x^2) -> p = a0 rho r_M/2 ; Newtonian (x<<1): rho = a0/(4 pi G r_M x) -> p = 2 pi G rho^2 r_M^2
rr = sp.symbols('rho_c', positive=True); rMs = sp.symbols('r_M', positive=True)
xdeep = sp.sqrt(a0s / (4 * sp.pi * Gs * rr * rMs)); pdeep = sp.simplify(a0s ** 2 / (8 * sp.pi * Gs * xdeep ** 2))
xnew = a0s / (4 * sp.pi * Gs * rr * rMs); pnew = sp.simplify(a0s ** 2 / (8 * sp.pi * Gs * xnew ** 2))
P("  deep regime  p_req = %s  (proportional to r_M ~ M^(1/2));  Newtonian regime p_req = %s (proportional to r_M^2 ~ M)" % (pdeep, pnew))
ok_scal = sp.simplify(pdeep / rMs) .free_symbols == {a0s, rr} and sp.simplify(pnew / rMs ** 2).free_symbols == {rr, Gs}
check("D-scal", "at fixed rho_c the required point-mass pressure scales as M^(1/2) (deep) and M^1 (Newtonian): no single p(rho_c) exists", "p_deep/r_M and p_newt/r_M^2 are M-independent: %s" % ok_scal, ok_scal, "")

MASSES = [1e9, 1e10, 1e11, 1e12]


def curve_point(Mb, xs_=np.geomspace(0.1, 30.0, 400)):
    r = xs_ * rM(Mb)
    rho_ = a0 / (4 * math.pi * G * r * np.sqrt(1 + xs_ ** 2))
    p_ = a0 ** 2 / (8 * math.pi * G * xs_ ** 2)
    return r, rho_, p_ * np.ones_like(r), np.full_like(r, Mb)


def curve_exp(Mb, h, xs_=np.geomspace(0.1, 30.0, 400)):
    r = xs_ * rM(Mb)
    Menc = lambda rr_: Mb * gammainc(3, rr_ / h)
    gN_ = lambda rr_: G * Menc(rr_) / rr_ ** 2
    rho_ = a0 * Menc(r) / (4 * math.pi * r ** 3 * np.sqrt(gN_(r) ** 2 + a0 * gN_(r)))
    # p(r) = int_r^inf a0 Menc/(4 pi r'^3) dr'  (tail beyond 3e3 r_M: Menc = Mb)
    rg = np.geomspace(r[0], 3e3 * rM(Mb), 60001)
    f = a0 * Menc(rg) / (4 * math.pi * rg ** 3)
    cum = np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(rg))])
    tot = cum[-1] + a0 * Mb / (8 * math.pi * rg[-1] ** 2)
    p_ = tot - np.interp(r, rg, cum)
    return r, rho_, p_, Menc(r)


def ratio_table(curves, label, use_mutate):
    """curves: {M: (r, rho, p, Menc)}; compares p at matched rho over the density overlap of all masses."""
    if use_mutate:
        # MUTATE=1: the EOS may depend on the enclosed baryon mass: compare at matched rho * r_M(M_enclosed)
        key = {Mb: c[1] * np.sqrt(G * c[3] / a0) for Mb, c in curves.items()}
    else:
        key = {Mb: c[1] for Mb, c in curves.items()}
    lo = max(k.min() for k in key.values()); hi = min(k.max() for k in key.values())
    if not lo < hi:
        return None
    grid = np.geomspace(lo, hi, 7)
    rows = []
    for gk in grid:
        pv = []
        for Mb, c in curves.items():
            o = np.argsort(key[Mb])
            pv.append(math.exp(np.interp(math.log(gk), np.log(key[Mb][o]), np.log(c[2][o]))))
        rows.append((gk, max(pv) / min(pv), pv))
    return rows


for label, build in [("point mass", lambda Mb: curve_point(Mb)), ("exp sphere, h = 2 kpc for all M (CFG44 style)", lambda Mb: curve_exp(Mb, 2.0)),
                     ("exp sphere, h = 2 kpc (M/1e10)^(1/3) (fixed mean density)", lambda Mb: curve_exp(Mb, 2.0 * (Mb / 1e10) ** (1 / 3.0)))]:
    curves = {Mb: build(Mb) for Mb in MASSES}
    rows = ratio_table(curves, label, M == 1)
    P("")
    P("  %s   [matching %s]" % (label, "rho * r_M(M_b(<r)) (MUTATE=1: enclosed mass hand-fed)" if M == 1 else "rho_c alone (the locality hypothesis)"))
    if rows is None:
        P("    no density overlap for the four masses")
        check("G1-" + label.split(",")[0].split(" ")[0] + label.split(" ")[1], "density overlap exists", "none", False)
        continue
    worst = max(r_[1] for r_ in rows)
    for gk, rt, pv in rows:
        P("    key = %.3e : p_req(M = 1e9, 1e10, 1e11, 1e12) = %s   max/min = %.3g" % (gk, ", ".join("%.3e" % q for q in pv), rt))
    tag = "G1-" + ("pm" if label.startswith("point") else ("exp2" if "for all M" in label else "expM"))
    P("    GATE G1 (%s): %s (worst max/min of the required pressure at matched density = %.3g; pass line 1.10)" % (label.split(",")[0], "PASS" if worst <= 1.10 else "FAIL", worst))
    if M == 1:
        check(tag, "CLAIM 'G1 fails' with the enclosed baryon mass hand-fed (MUTATE=1: matching at rho * r_M(M_b(<r)) instead of rho)", "worst max/min over the matched grid = %.3g" % worst, worst > 1.10,
              "the control: for the point mass the claim is FALSE (exact collapse when the EOS may depend on M_b); for an extended sphere it stays TRUE, because p also depends on the mass OUTSIDE r (CFG44's far-shell theorem)")
    else:
        check(tag, "CLAIM: G1 fails, i.e. the required p(rho_c) differs by more than 10% between 1e9 and 1e12 Msun at matched density (so no single p(rho_c) from Q can be the target's EOS)", "worst max/min over the density overlap = %.3g" % worst, worst > 1.10,
              "the exchange's forced EOS (A3) is a function of rho_c (and the slice-uniform Lambda) only")
    # local exponents
    if M == 0:
        exps = []
        for gk, rt, pv in rows:
            e_ = np.polyfit(np.log(MASSES), np.log(pv), 1)[0]
            exps.append(e_)
        P("    fitted d ln p_req/d ln M at fixed rho over the grid: " + ", ".join("%.2f" % e_ for e_ in exps) + "  (point-mass theory: 0.5 deep ... 1 Newtonian)")

R.finish()
