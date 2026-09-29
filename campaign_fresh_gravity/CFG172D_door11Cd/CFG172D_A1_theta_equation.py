#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG172D_A1 -- the theta equation of 11C-d, re-derived (not assumed): H-i, H-ii, T-d1, the d2 pincer formula, O3 (a,b,c), C7.

WHAT THIS SCRIPT DOES (frozen criteria section 6, A1; nothing here is tuned):
  S1 [sympy, spherical, exact] The khronon's tau-variation of V0's covariant brace with f = F(theta): tau = t + eps*pi(t,r) on the
     metric -N^2 dt^2 + a(t)^2 A(r)^2 (dr^2 + r^2 dOmega^2), all leafwise auxiliaries generic functions of (t,r).  L1 = dL/deps at
     eps = 0 is split into the theta channel (dL/dTheta * delta theta: gives the conjugate Pi and the operator
     div[h grad Pi / sqrt(-X)]) and the REST (every other tau-dependence: leafwise Laplacians, projected gradients, the
     4-acceleration, eps_d = u u T).  H-i (criteria 1.3) says REST = 0.  It is tested (i) in the static, non-expanding limit and
     (ii) with adot != 0 (quasi-static fields).  H-ii says alpha_c enters only through time derivatives: tested by extracting the
     alpha_c-dependence of REST.
  S2 [sympy] T-d1 (Pi constant on a leaf when REST = 0 => the same theta on both plateaus) and the d2 reduction: integrate out
     delta-theta, the interaction energy, c_gate^2, and the pincer formula -c_s^2/c^2 = 3 c2 Delta^2 eps_L/eps_b.
  S3 [numeric] C7: any C^2 flat-flat gate has f'' of both signs; W'' extrema.
  O3a [sympy] the NR Lagrangian's Euler-Lagrange equations with f = f(r) generic (Phi = u + f P, lam = -f Psi, kernel reads w).
  O3b [numeric] homogeneous background off-plateau for u_theta, w in {0.25, 1}, z in [-0.5..20] (criteria O3b).
  O3c [sympy] the local Hessian of the constraint system with the theta row (Schur complement on theta).
MUTATE=M6 (drop the leaf-mean offset): O3b must FAIL for w = 1.     MUTATE=M7 (c2 -> -c2, a ghost theta sector): the theta-theta
Hessian entry changes sign; the stability claim must FAIL.   exit 1 when the control bites.
Run:  ZF_REPO=<repo> python3 CFG172D_A1_theta_equation.py     (about 1 minute)
"""
import os, sys, time, math, json
import numpy as np
import sympy as sp
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG172D_common as C

MUT = os.environ.get("MUTATE")
R = C.Report("CFG172D_A1_theta_equation", MUT)
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip())
P(f"\n  repo: {C.rel(C.REPO)}   MUTATE={MUT}")

# ============================================================================================ S1
banner("S1  THE TAU-VARIATION OF V0 WITH f = F(theta), DERIVED SYMBOLICALLY (H-i, H-ii)")
t0 = time.time()
t, r, th_, ph_, eps = sp.symbols("t r vartheta varphi epsilon", real=True)
X = [t, r, th_, ph_]
N = sp.Function("N", positive=True)(r); A = sp.Function("A", positive=True)(r); a = sp.Function("a", positive=True)(t)
al, alc, c2, m2, sig, kd = sp.symbols("alpha alpha_c c_2 m2 sigma kappa_d", positive=True)
g = sp.diag(-N**2, a**2 * A**2, a**2 * A**2 * r**2, a**2 * A**2 * r**2 * sp.sin(th_)**2)
gi = g.inv()
sq = N * a**3 * A**3 * r**2 * sp.sin(th_)
Gam = [[[sum(gi[l, m] * (sp.diff(g[m, i], X[j]) + sp.diff(g[m, j], X[i]) - sp.diff(g[i, j], X[m])) for m in range(4)) / 2
         for j in range(4)] for i in range(4)] for l in range(4)]
pi = sp.Function("pi")(t, r)
tau = t + eps * pi
dtau = [sp.diff(tau, c) for c in X]
Xn = sum(gi[i, i] * dtau[i]**2 for i in range(4))
ul = [-d / sp.sqrt(-Xn) for d in dtau]
uu = [sum(gi[i, j] * ul[j] for j in range(4)) for i in range(4)]
theta = sum(sp.diff(sq * uu[i], X[i]) for i in range(4)) / sq
Th = sp.Symbol("Th")
grad = lambda f: [sp.diff(f, c) for c in X]


def hess(f):
    df = grad(f)
    return [[sp.diff(df[j], X[i]) - sum(Gam[l][i][j] * df[l] for l in range(4)) for j in range(4)] for i in range(4)]


hmat = [[gi[i, j] + uu[i] * uu[j] for j in range(4)] for i in range(4)]


def Delta_h(f):
    Hf = hess(f); df = grad(f)
    return sum(hmat[i][j] * Hf[i][j] for i in range(4) for j in range(4)) + theta * sum(uu[i] * df[i] for i in range(4))


def Dmu(f):
    df = grad(f); ud = sum(uu[i] * df[i] for i in range(4))
    return [df[i] + ul[i] * ud for i in range(4)]


def nabla_ul(nu, mu):
    return sp.diff(ul[mu], X[nu]) - sum(Gam[l][nu][mu] * ul[l] for l in range(4))


acc = [sum(uu[nu] * nabla_ul(nu, mu) for nu in range(4)) for mu in range(4)]
Uf, Vf, Yf, Wf, Wz, Psi, Lm, Ld, Ttt, Trr, Tb1, Tb2 = [sp.Function(n)(t, r) for n in
                                                       ("U", "V", "Y", "W", "Wz", "Psi", "Lm", "Ld", "Ttt", "Trr", "Tbtt", "Tbrr")]
tb = sp.Function("tb")(t); edb = sp.Function("edb")(t); ebb = sp.Function("ebb")(t)
Fg = sp.Function("F"); qf = sp.Function("q"); Hh = sp.Function("Hh")
kb, zeta = sp.symbols("kappa_b zeta")
DU = Dmu(Uf); DW = Dmu(Wf)
term1 = 2 * sum(hmat[i][j] * (DU[i] - acc[i]) * (DU[j] - acc[j]) for i in range(4) for j in range(4))
term2 = alc * sum(gi[i, i] * acc[i]**2 for i in range(4))
Zk = sum(hmat[i][j] * DW[i] * DW[j] for i in range(4) for j in range(4)) / al**2
Fq = Fg(Th)
G1 = 2 * al**2 * Fq * qf(Zk)
G2 = 2 * Psi * ((Delta_h(Yf) - m2 * (1 - Fq) * Yf) - Fq * Delta_h(Uf - Vf))
G3 = -2 * sig * m2 * (1 - Fq) * Yf**2
G0 = Lm * (Wz - Delta_h(Wf))
edd = ul[0]**2 * Ttt + ul[1]**2 * Trr                                  # eps_d = u_mu u_nu T_d^{mu nu}
ebar = ul[0]**2 * Tb1 + ul[1]**2 * Tb2                                 # eps_b = u_mu u_nu T_b^{mu nu}  (the baryons, d2's source)
G4 = 2 * Ld * (Delta_h(Vf) - kd * (edd - edb))
G5 = -kb * (ebar - ebb) * zeta * Hh(Th)                                # d2: -(16 pi G/c^4)(eps_b - <eps_b>) zeta h(vartheta)
Kt = -c2 * (Th - tb)**2
Lag = sq * (term1 + term2 + G1 + G2 + G3 + G0 + G4 + Kt + G5)
th0 = sp.simplify(theta.subs(eps, 0)); th1 = sp.simplify(sp.diff(theta, eps).subs(eps, 0))
dLdTh = sp.diff(Lag, Th).subs(eps, 0).subs(Th, th0)
Rest = sp.diff(Lag, eps).subs(eps, 0).subs(Th, th0)
P(f"  Lagrangian, theta channel and REST built ({time.time() - t0:.0f} s); theta_0 = {th0} (the background expansion 3 adot/(N a)), "
  f"theta_1 = -div of the tilt: {th1}")
ps = sp.symbols("p0 pt pr ptt ptr prr")


def lin_coeffs(expr):
    e = expr.doit()
    rep = [(sp.Derivative(pi, (r, 2)), ps[5]), (sp.Derivative(pi, t, r), ps[4]), (sp.Derivative(pi, r, t), ps[4]),
           (sp.Derivative(pi, (t, 2)), ps[3]), (sp.Derivative(pi, r), ps[2]), (sp.Derivative(pi, t), ps[1]), (pi, ps[0])]
    for a_, b_ in rep:
        e = e.subs(a_, b_)
    return [sp.diff(e, p) for p in ps]


def EL(expr):
    c0, ct, cr, ctt, ctr, crr = lin_coeffs(expr)
    return c0 - sp.diff(ct, t) - sp.diff(cr, r) + sp.diff(ctt, t, 2) + sp.diff(ctr, t, r) + sp.diff(crr, r, 2)


ELrest = EL(Rest) / sp.sin(th_)
ELth = sp.simplify(EL(dLdTh * th1) / sp.sin(th_))
P(f"  E-L operators built ({time.time() - t0:.0f} s)")
fields = (Uf, Vf, Yf, Wf, Wz, Psi, Lm, Ld, Ttt, Trr, Tb1, Tb2)


def kill_time(e, keep_adot=False):
    e = e.doit()
    for f_ in fields:
        e = e.replace(lambda ex, f_=f_: isinstance(ex, sp.Derivative) and ex.expr == f_ and any(v == t for v in ex.variables), lambda ex: 0)
    if not keep_adot:
        e = e.replace(lambda ex: isinstance(ex, sp.Derivative) and ex.expr == a, lambda ex: 0)
    return e


e_static = sp.simplify(kill_time(ELrest, keep_adot=False))
e_qs = sp.simplify(kill_time(ELrest, keep_adot=True))
P(f"  E-L[REST] in the static, non-expanding limit (all time derivatives and adot set to 0): {e_static}")
h_i_static = (e_static == 0)
check("H-i (static limit) the MOND-sector, C-H chassis, alpha_c, projected-gradient and eps_d terms give NO O(pi) source when "
      "the background is static and non-expanding", f"E-L[REST] = {e_static}", h_i_static)
adot = sp.Derivative(a, t)
Hs = sp.Symbol("Hs"); lam_s = sp.Symbol("lam_s")
e_qs_s = sp.simplify(e_qs.subs(sp.Derivative(a, t), lam_s * Hs * a).subs(sp.Derivative(a, (t, 2)), 0))
# adot -> lam*adot: polynomial in lam (F(theta_0) also carries adot; treat F, F' as symbols)
F0, F1 = sp.symbols("F0 F1")
e_qs_sym = e_qs.subs(sp.Subs(sp.Derivative(Fg(sp.Symbol("_xi_1")), sp.Symbol("_xi_1")), sp.Symbol("_xi_1"), th0), F1)
e_qs_sym = e_qs_sym.replace(lambda ex: isinstance(ex, sp.Subs), lambda ex: F1).replace(lambda ex: isinstance(ex, sp.Function) and ex.func == Fg, lambda ex: F0)
lam = sp.Symbol("lam")
poly = sp.expand(e_qs_sym.subs(sp.Derivative(a, t), lam * sp.Derivative(a, t)))
pl = sp.Poly(poly, lam)
P(f"  E-L[REST] with adot != 0 (fields static in comoving r): a polynomial in adot of degree {pl.degree()}; "
  f"lam^0 coefficient = {sp.simplify(pl.coeff_monomial(1))}")
check("H-i (expanding background, quasi-static fields): E-L[REST] = 0",
      f"FALSE as written: E-L[REST] is a polynomial of degree {pl.degree()} in adot with zero adot^0 part, i.e. an O(H) MOND-sector source of theta exists; "
      "H-i holds only in the static limit (its size is estimated in A2)", pl.degree() == 0, load_bearing=False)
R.num("H_i_static_zero", bool(h_i_static)); R.num("H_i_expanding_nonzero", bool(pl.degree() >= 1))
# H-ii: alpha_c dependence of REST
ac_part = sp.simplify(sp.diff(e_qs_sym, alc))
ac_static = sp.simplify(sp.diff(e_static, alc)) if e_static != 0 else 0
ac_poly = sp.Poly(sp.expand(ac_part.subs(sp.Derivative(a, t), lam * sp.Derivative(a, t))), lam)
P(f"  alpha_c dependence: d(E-L[REST])/d alpha_c has lam^0 coefficient {sp.simplify(ac_poly.coeff_monomial(1))} (i.e. zero without adot) and degree {ac_poly.degree()} in adot")
check("H-ii alpha_c enters the theta-equation's remainder only multiplied by adot (a time derivative)",
      f"lam^0 coefficient of dE/d(alpha_c) = {sp.simplify(ac_poly.coeff_monomial(1))}; nonzero adot-part: {ac_poly.degree() >= 1}",
      sp.simplify(ac_poly.coeff_monomial(1)) == 0)
# the theta channel: form of the operator
Pi_hat = sp.Function("Pihat")(t, r)
# EL[dLdTh*th1] with dLdTh = sq*Pihat: compare to  -d/dr( a N^2 A r^2 * dPihat/dr ) (up to the a-scaling)
ELth_gen = sp.simplify(EL((sq * Pi_hat) * th1) / sp.sin(th_))
expect = -sp.diff(a * N**2 * A * r**2 * sp.diff(Pi_hat, r), r)
diff_form = sp.simplify(ELth_gen - expect)
P(f"  theta channel: E-L[Pihat*sqrt(-g)*delta theta] = {ELth_gen}\n  compared with -d/dr(a N^2 A r^2 dPihat/dr): difference = {diff_form}")
check("the theta channel gives div[h grad Pi / sqrt(-X)] (the khronon's flow equation), Pi = dL/dtheta per unit sqrt(-g)", f"difference {diff_form}",
      sp.simplify(diff_form) == 0 or sp.simplify(diff_form.subs(sp.Derivative(Pi_hat, t), 0).doit()) == 0)
# weak-field, V = Lm = Ld = 0 form of the REST for A2 (source size estimate)
Nw, Aw = sp.Symbol("Nw"), sp.Symbol("Aw")
simp = e_qs.subs({Lm: 0, Ld: 0, Vf: 0}).doit()
simp = sp.simplify(kill_time(simp, keep_adot=True))
P(f"  REST with V = Lm = Ld = 0 (no dark component, no filter), quasi-static: {sp.count_ops(simp)} operations; saved for A2's size estimate")
open(os.path.join(C.HERE, "CFG172D_A1_rest_expr.txt"), "w").write(sp.srepr(simp))

# ============================================================================================ S2
banner("S2  T-d1 AND THE d2 PINCER (symbolic)")
th, thb, thL, rho, eps_L, z_, c2s, Bs, GN, cl = sp.symbols("theta thetabar thetaL rho epsL zeta c2 Bcal G c", positive=True)
Ff = sp.Function("f")
# leaf-local Lagrangian per unit (c^4/16 pi G):  L = -c2 (th-thb)^2 + B f(th) - (16 pi G rho/c^2) zeta h((th-thb)/thL)
hfun = sp.Function("h")
Lloc = -c2s * (th - thb)**2 + Bs * Ff(th) - (16 * sp.pi * GN * rho / cl**2) * z_ * hfun((th - thb) / thL)
Pi_loc = sp.diff(Lloc, th)
P(f"  Pi(theta) = {Pi_loc}")
# T-d1: with the source and the gate off (f' = 0 on plateaus), Pi = const => theta = const on each plateau
Pi_plateau = Pi_loc.subs({Bs: 0, z_: 0})
sol_plateau = sp.solve(sp.Eq(Pi_plateau, sp.Symbol("Pi0")), th)
P(f"  plateau (f' = 0, zeta = 0): Pi = Pi0 => theta = {sol_plateau}: independent of position => the same value on every plateau")
check("T-d1: on any plateau of f (f' = 0), Pi = Pi0 forces theta = thetabar - Pi0/(2 c2), the same number on the bound and the web plateaus "
      "(so d1 cannot be a region gate)", f"theta = {sol_plateau[0]}", len(sol_plateau) == 1 and not sol_plateau[0].has(rho))
# d2 (linear h): integrate out
dth = sp.Symbol("dth")
Llin = (Lloc.subs(hfun((th - thb) / thL), (th - thb) / thL).subs(Bs, 0)).subs(th, thb + dth)
dsol = sp.solve(sp.diff(Llin, dth), dth)[0]
Lstar = sp.simplify(Llin.subs(dth, dsol))
E_int = sp.simplify(-Lstar * cl**4 / (16 * sp.pi * GN))                  # energy density, static
P(f"  d2(lin): delta theta* = {dsol}; energy density E_int = {E_int}")
Lam_s = sp.Symbol("Lambda", positive=True)
E_int_L = sp.simplify(E_int.subs(thL, sp.sqrt(3 * Lam_s)))
S_coef = sp.simplify(sp.diff(E_int_L, rho, 2))                           # d^2E/drho^2 (negative)
cs2 = sp.simplify(rho * S_coef)                                          # c_s^2 = rho E''
P(f"  E_int (thetaL^2 = 3 Lambda) = {E_int_L};  c_s^2 = rho d2E/drho2 = {cs2}")
epsL_expr = Lam_s * cl**4 / (8 * sp.pi * GN)
cs2_over_c2 = sp.simplify((cs2 / cl**2).subs(Lam_s, 8 * sp.pi * GN * eps_L / cl**4))
P(f"  c_s^2/c^2 with rho -> eps_b/c^2: {sp.simplify(cs2_over_c2.subs(rho, sp.Symbol('epsb') / cl**2))}")
epsb = sp.Symbol("epsb", positive=True)
frozen = -z_**2 * epsb / (3 * c2s * eps_L)
got = sp.simplify(cs2_over_c2.subs(rho, epsb / cl**2))
check("d2 pincer (frozen criteria 3.2): c_s^2/c^2 = -zeta^2 eps_b/(3 c2 eps_Lambda)", f"derived {got}; frozen {frozen}", sp.simplify(got - frozen) == 0)
Dl = sp.Symbol("Delta", positive=True)
zeta_needed = sp.solve(sp.Eq(Dl, z_ * epsb / (3 * c2s * eps_L)), z_)[0]
pinch = sp.simplify(got.subs(z_, zeta_needed))
P(f"  eliminating zeta through the depletion Delta = |delta theta|/thetaL = zeta eps_b/(3 c2 eps_L): -c_s^2/c^2 = {sp.simplify(-pinch)}")
check("d2 pincer formula: -c_s^2/c^2 = 3 c2 Delta^2 eps_L/eps_b, independent of zeta", f"{sp.simplify(-pinch)}",
      sp.simplify(-pinch - 3 * c2s * Dl**2 * eps_L / epsb) == 0)
# with the gate's second variation (fold): S ~ 1/|L_thth|
Lthth = sp.simplify(sp.diff(Lloc, th, 2))
P(f"  L_thth = {Lthth} (the gate adds B f''; a fold where L_thth -> 0 divides c_gate^2 by |L_thth|)")

# ============================================================================================ S3 (C7)
banner("S3  C7: a smooth gate flat at both ends has f'' of both signs; W'' extrema")
tt = np.linspace(0.005, 0.995, 20001)
_, W1n, W2n = C.Wd(tt)
i1, i2 = np.argmax(W2n), np.argmin(W2n)
P(f"  W' max = {W1n.max():.4f} at t = {tt[np.argmax(W1n)]:.3f};  W'' max = {W2n.max():.3f} at t = {tt[i1]:.3f}; W'' min = {W2n.min():.3f} at t = {tt[i2]:.3f}")
check("C7 W'' takes both signs on (0,1), extrema +-9.84 at t = 0.218 / 0.782, W'(1/2) = 2", f"{W2n.max():.3f}, {W2n.min():.3f}, {W1n.max():.4f}",
      W2n.max() > 9.8 and W2n.min() < -9.8 and abs(W1n.max() - 2) < 1e-3)
R.num("Wpp_max", float(W2n.max())); R.num("Wp_max", float(W1n.max()))

# ============================================================================================ O3a
banner("O3a  PLATEAU REDUCTIONS: the NR Euler-Lagrange equations with f = f(r) generic (spherical)")
rr = sp.Symbol("rr", positive=True)
Ph, u_, v_, w_, Ps_, lm_, f_ = [sp.Function(n)(rr) for n in ("Phi", "u", "v", "w", "Psi", "lam", "f")]
rb, rd = sp.Function("rhob")(rr), sp.Function("rhod")(rr)
Gs, a0s, sg, mm = sp.symbols("G a0 sigma mm", positive=True)
qq = sp.Function("q")
lap = lambda F_: sp.diff(rr**2 * sp.diff(F_, rr), rr) / rr**2
M2 = mm * (1 - f_)
Lnr = (-(rb + rd) * Ph - (2 * sp.diff(Ph, rr) * sp.diff(u_, rr) - sp.diff(u_, rr)**2) / (8 * sp.pi * Gs)
       + a0s**2 * f_ * qq(sp.diff(w_, rr)**2 / a0s**2) / (8 * sp.pi * Gs)
       + Ps_ * (lap(w_) - M2 * w_ - f_ * lap(u_ - v_)) / (8 * sp.pi * Gs)
       + lm_ * (lap(v_) - 4 * sp.pi * Gs * rd) / (8 * sp.pi * Gs) - sg * M2 * w_**2 / (8 * sp.pi * Gs)) * rr**2


def EL_nr(L, fn):
    # Euler-Lagrange with derivatives up to 2nd order
    d0 = sp.diff(L, fn); d1 = sp.diff(L, sp.diff(fn, rr)); d2 = sp.diff(L, sp.diff(fn, rr, 2))
    return sp.simplify(d0 - sp.diff(d1, rr) + sp.diff(d2, rr, 2))


eqs = {n: EL_nr(Lnr, fn) for n, fn in (("Phi", Ph), ("u", u_), ("v", v_), ("w", w_), ("Psi", Ps_), ("lam", lm_))}
P("  Euler-Lagrange equations derived; checking the stated field equations:")
chk = []
# Phi: lap u = 4 pi G (rho_b + rho_d)
chk.append(("dPhi: lap u = 4 pi G (rho_b + rho_d)", sp.simplify(eqs["Phi"] - (-(rb + rd) * rr**2 + 2 * rr**2 * lap(u_) / (8 * sp.pi * Gs)))))
# u: lap(Phi - u - f Psi/2) = 0
lhs_u = sp.simplify(eqs["u"] - rr**2 * (2 * lap(Ph) - 2 * lap(u_) - lap(f_ * Ps_)) / (8 * sp.pi * Gs))
chk.append(("du: lap(Phi - u - f Psi/2) = 0", lhs_u))
chk.append(("dv: lap(lam + f Psi) = 0", sp.simplify(eqs["v"] - rr**2 * lap(lm_ + f_ * Ps_) / (8 * sp.pi * Gs))))
chk.append(("dlam: lap v = 4 pi G rho_d", sp.simplify(eqs["lam"] - rr**2 * (lap(v_) - 4 * sp.pi * Gs * rd) / (8 * sp.pi * Gs))))
chk.append(("dPsi: (lap - M^2) w = f lap(u - v)", sp.simplify(eqs["Psi"] - rr**2 * (lap(w_) - M2 * w_ - f_ * lap(u_ - v_)) / (8 * sp.pi * Gs))))
qpf = sp.Function("qp")
Zs = sp.diff(w_, rr)**2 / a0s**2
def _q_sub(e):
    d = e.args[0]                                      # Derivative(q(xi), xi) or Derivative(q(xi), (xi, 2))
    order = d.derivative_count
    return qpf(Zs) if order == 1 else sp.Subs(sp.Derivative(qpf(sp.Symbol("_xi")), sp.Symbol("_xi")), sp.Symbol("_xi"), Zs)
w_derived = eqs["w"].replace(lambda e: isinstance(e, sp.Subs), _q_sub)
w_stated = (-2 * sp.diff(rr**2 * f_ * qpf(Zs) * sp.diff(w_, rr), rr) + rr**2 * (lap(Ps_) - M2 * Ps_ - 2 * sg * M2 * w_)) / (8 * sp.pi * Gs)
chk.append(("dw: -2 div(f q' grad w) + lap Psi - M^2 Psi - 2 sigma M^2 w = 0", sp.simplify((w_derived - w_stated).doit())))
okA = all(d == 0 for _, d in chk)
for n_, d in chk:
    P(f"    {n_}: residual {d}")
check("O3a the NR E-L equations give: baryons feel Phi = u + f P (P = Psi/2), lam = -f Psi (the dark component feels u only), the kernel "
      "reads w with (lap - M^2) w = 4 pi G f (rho_b - <rho_b>)", "all residuals 0", okA)
# on-plateau (f = 1, M = 0) reduction
# the P equation on shell:  P = Psi/2:  lap P - M^2 P = div(f (nu-1) grad w) + sigma M^2 w   (stated for A2)
P("  the P equation used by A2:  (1/r^2)(r^2 P')' - M^2 P = (1/r^2)(r^2 f (nu - 1) w')' + sigma M^2 w,  nu = nu(|w'|/a0)  [from dw with q' = nu - 1]")
# check it symbolically from dw
# ============================================================================================ O3b
banner("O3b  THE HOMOGENEOUS BACKGROUND IS OFF-PLATEAU FOR u_theta (each other gate variable must show its own; CV2 A6)")
ok_b = True
rows = []
zgrid = np.concatenate([np.linspace(-0.5, 0.0, 6), np.linspace(0.0, 20.0, 81)])
for w in (0.25, 1.0):
    worst = -1e9
    for z in zgrid:
        E2z = 0.3138 * (1 + z)**3 + 0.6862
        if MUT == "M6":
            u = E2z**-1                                              # (H0/H)^{2p}: no leaf-mean offset
        else:
            th_bg = C.theta_bar(max(z, -0.5)) if z > -0.9 else 1.0
            u = C.u_theta(th_bg, max(z, -0.5) if z > -0.9 else 0.0)  # D = 0 on the background
            u = float(u)
        tt_ = C.t_of_u(u, w)
        worst = max(worst, tt_)
    rows.append((w, worst))
    P(f"    w = {w}: max over z in [-0.5, 20] of t(u_bg) = {worst:.4f}  (needs <= 0 for W = 0 with all derivatives)")
    ok_b &= worst <= 1e-12
check("O3b for w = 0.25 and w = 1 the background gate variable sits at or below the off-plateau edge t <= 0 for every z (W = W' = ... = 0)",
      {f"w={w}": round(v, 4) for w, v in rows}, ok_b)
R.num("O3b_tmax", {str(w): v for w, v in rows})

# ============================================================================================ O3c
banner("O3c  THE CONSTRAINT SYSTEM WITH THE THETA ROW: the local Hessian derived from the Lagrangian; the Schur complement on theta")
cval_g = -1 if MUT == "M7" else 1
xs = sp.Symbol("xs", real=True); kq = sp.Symbol("k", positive=True); ee = sp.Symbol("ee")
c2h, m2s, sigs, a0q = sp.symbols("c2 m2s sigs a0q", positive=True)
w0, gw, Psi0, Ssrc, f0, f1, f2, q0, q1, q2, th_b = sp.symbols("w0 gw Psi0 Ssrc f0 f1 f2 q0 q1 q2 thb", real=True)
dPh, dW, dT = sp.symbols("dPh dW dT"); dPc, dWc, dTc = sp.symbols("dPc dWc dTc")
Ex = sp.exp(sp.I * kq * xs)
pert = lambda A_, Ac_: ee * (A_ * Ex + Ac_ / Ex) / 2
Psi_l = Psi0 + pert(dPh, dPc)
w_l = w0 + gw * xs + pert(dW, dWc)
th_l = th_b + pert(dT, dTc)
f_l = f0 + f1 * (th_l - th_b) + f2 * (th_l - th_b)**2 / 2
Zl = sp.diff(w_l, xs)**2 / a0q**2
Z0 = gw**2 / a0q**2
q_l = q0 + q1 * (Zl - Z0) + q2 * (Zl - Z0)**2 / 2
M2l = m2s * (1 - f_l)
Lq = (a0q**2 * f_l * q_l + Psi_l * (sp.diff(w_l, xs, 2) - M2l * w_l - f_l * Ssrc) - sigs * M2l * w_l**2 - cval_g * c2h * (th_l - th_b)**2)
L2 = sp.expand(sp.diff(Lq, ee, 2).subs(ee, 0) / 2)
Es = sp.Symbol("Es")
L2 = sp.expand(sp.powsimp(sp.expand(L2.rewrite(sp.exp)).subs(sp.exp(sp.I * kq * xs), Es), combine="exp"))
L2 = sp.expand(L2.subs(sp.exp(-sp.I * kq * xs), 1 / Es).subs(sp.exp(2 * sp.I * kq * xs), Es**2).subs(sp.exp(-2 * sp.I * kq * xs), Es**-2))
L20 = sp.expand(L2).coeff(Es, 0)
L20 = sp.expand(L20.subs(xs, 0))
fl = [dPh, dW, dT]; flc = [dPc, dWc, dTc]
Hm = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L20, fl[i], flc[j])))
# substitute the on-shell background: q0/q1/q2 stay symbols; B = dL/df at the background
Bcal_bg = a0q**2 * q0 + Psi0 * (m2s * w0 - Ssrc) + sigs * m2s * w0**2
P("  Hermitian Hessian in (Psi, w, theta) derived from the Lagrangian (columns: dPsi, dw, dtheta):")
for i in range(3):
    P("    " + str([sp.simplify(Hm[i, j]) for j in range(3)]))
Hcon = Hm[:2, :2]
det_c = sp.simplify(Hcon.det())
P(f"  det of the (Psi, w) constraint block = {det_c}")
Cv = Hm[:2, 2]
schur = sp.simplify(Hm[2, 2] - (Cv.H * Hcon.inv() * Cv)[0, 0]) if False else sp.simplify(Hm[2, 2] - (Hm[2, :2] * Hcon.inv() * Hm[:2, 2])[0, 0])
P(f"  theta-theta entry = {sp.simplify(Hm[2, 2])}")
P(f"  Schur complement on theta (constraints eliminated) = {schur}")
theta_theta_expected = (-2 * cval_g * c2h + Bcal_bg * f2) / 4          # every entry carries the same period-average factor 1/4
check("O3c the theta-theta Hessian entry is -2 c2 + Bcal f'' with Bcal = dL/df = a0^2 q + Psi(m^2 w - lap(u - v)) + sigma m^2 w^2 (V0's own gate coefficient)",
      f"entry - expected = {sp.simplify(Hm[2, 2] - theta_theta_expected)}", sp.simplify(Hm[2, 2] - theta_theta_expected) == 0)
M2eff = m2s * (1 - f0)
ok_det = sp.simplify(det_c - (-(kq**2 + M2eff)**2 / 16)) == 0
check("O3c the (Psi, w) constraint block has determinant -(k^2 + M^2)^2 (times the common 1/16 of the period average) for every gate shape: no f'', no c2, no f' in it",
      f"det = {det_c}", ok_det and not det_c.has(f2, c2h, f1))
schur_hi = sp.limit(schur, kq, sp.oo)
P(f"  high-k limit of the Schur complement on theta: {sp.simplify(schur_hi)}")
check("O3c at high k the theta stiffness is -2 c2 + Bcal f'' (the constraint couplings drop out as 1/k^2)",
      f"limit - expected = {sp.simplify(schur_hi - theta_theta_expected)}", sp.simplify(schur_hi - theta_theta_expected) == 0)
R.num("schur_theta", str(schur)); R.num("theta_theta", str(sp.simplify(Hm[2, 2])))

# ============================================================================================ M7
banner("ghost check: the sign of the c2 part of the theta-theta entry (M7 flips it)")
c2_coeff = sp.simplify(sp.diff(schur_hi, c2h))
P(f"  d(high-k theta stiffness)/d c2 = {c2_coeff}   (negative = healthy theta sector for c2 > 0; positive = a ghost)")
ok_healthy = bool(c2_coeff < 0)
check("the theta sector is not a ghost: the c2 part of the theta stiffness is negative", f"coefficient {c2_coeff}", ok_healthy, load_bearing=(MUT == "M7"))

nf = R.write()
bitten = (MUT == "M6" and not ok_b) or (MUT == "M7" and not ok_healthy)
if MUT:
    P(f"\n  MUTATE={MUT}: control {'BITES' if bitten else 'DOES NOT BITE'}"); sys.exit(1 if bitten else 0)
sys.exit(0 if nf == 0 else 1)
