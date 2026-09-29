#!/usr/bin/env python3
"""CFG152 POST-HOC side finding (written after all frozen runs and after reading CFG124_T0_field_equations.py).
Not a pass line of CFG152; it checks one line of CFG124 found while comparing control C2 (CMV eq. 80).

CFG124 T0.4a prints: 'eps = -2 lam = (3/8piG)(1 - 3 gt/2) H^2 - V'.  Its background Lagrangian (copied below from
CFG124_T0_field_equations.py, line 91) writes the gamma term as (gamma/2) N a^3 (9 H^2 / N^2), i.e. box phi = -K with
K = 3H/N.  For phi = t and ds^2 = -N^2 dt^2 + a^2 dx^2, box phi = -3H/N^2 + N'/N^3 (checked below), so that form has the
wrong lapse dependence, which matters for the N-variation (the lambda equation).
"""
import sys

import sympy as sp

import cfg152_common as C

NAME = "cfg152_posthoc_T04_lambda"
rep = C.Report(NAME, "main")
C.header(rep)
t = sp.Symbol("t", real=True)
gt, Mp2 = sp.symbols("gt Mp2", positive=True)
a = sp.Function("a", positive=True)(t)
N = sp.Function("N", positive=True)(t)
lam, V = sp.Function("lam")(t), sp.Function("V")(t)
H = sp.diff(a, t) / a
Hd = sp.diff(H, t)
G8 = 1 / Mp2
gamma = gt * Mp2

# 1. box phi with a lapse, from the covariant definition
sqrtg = N * a**3
box = sp.simplify(sp.diff(sqrtg * (-1 / N**2) * 1, t) / sqrtg)
rep.p(f"box phi (phi = t, lapse N) = {box}")
ok_box = sp.simplify(box - (-3 * H / N**2 + sp.diff(N, t) / N**3)) == 0
rep.check("box phi = -3H/N^2 + N'/N^3 (so box phi = -K only at N = 1)", ok_box, kind="reported, post-hoc")


def lam_from(Lbg):
    """N-variation at N = 1 (with the N' term), solved for lambda, then the a-equation at N = 1 used to remove V."""
    Nd = sp.diff(N, t)
    EN = sp.diff(Lbg, N) - sp.diff(sp.diff(Lbg, Nd), t)
    EN = EN.subs({sp.Derivative(N, (t, 2)): 0}).subs({Nd: 0}).subs(N, 1).doit()
    lsol = sp.solve(EN, lam)[0]
    L1 = Lbg.subs(N, 1).doit()
    ad = sp.diff(a, t)
    Ea = sp.diff(L1, a) - sp.diff(sp.diff(L1, ad), t)
    Vsol = sp.solve(Ea.subs(lam, 0), V)[0]
    return sp.simplify(lsol.subs(V, Vsol)), sp.simplify(Vsol)


# 2. CFG124's background Lagrangian, as written (line 91 of its T0 script, with G8 = 8 pi G = 1/Mp2, g = gt)
L_cfg124 = N * a**3 * ((1 / (2 * G8)) * (-6 + 9 * gt) * sp.diff(a, t)**2 / (a**2 * N**2) - V) + lam * N * a**3 * (1 - 1 / N**2)
# 3. the same with the covariant box phi (lapse dependence kept); EH part unchanged: -3 Mp2 a a'^2 / N
L_cov = (-3 * Mp2 * a * sp.diff(a, t)**2 / N + (gamma / 2) * N * a**3 * box**2 - N * a**3 * V
         + lam * N * a**3 * (1 - 1 / N**2))
l124, V124 = lam_from(L_cfg124)
lcov, Vcov = lam_from(L_cov)
rep.p(f"lambda from CFG124's background Lagrangian (on its a-equation): {sp.factor(l124)}")
rep.p(f"lambda with the lapse-dependent box phi:                        {sp.factor(lcov)}")
rep.p(f"V from the a-equation, both Lagrangians: {sp.factor(V124)} | {sp.factor(Vcov)}")
same_V = sp.simplify(V124 - Vcov) == 0
rep.check("the a-equation (hence 2H' + 3H^2 = 2V/((2 - 3gt) M_P^2)) is the same in both", same_V, kind="reported, post-hoc")
ok_cfg = sp.simplify(l124 - (1 - sp.Rational(3, 2) * gt) * Mp2 * Hd) == 0
ok_cov = sp.simplify(lcov - (1 - 3 * gt) * Mp2 * Hd) == 0
rep.check("CFG124's Lagrangian gives lambda = (1 - 3gt/2) M_P^2 H'", ok_cfg, kind="reported, post-hoc")
rep.check("the covariant box phi gives lambda = (1 - 3gt) M_P^2 H' = CFG152 M2 brute force = CMV eq. 80 (mapped)", ok_cov,
          kind="reported, post-hoc")
# 4. what CFG124's eps expression is: the conserved first integral, = -2 lambda - 3 gt M_P^2 H'
eps124 = 3 * Mp2 * (1 - sp.Rational(3, 2) * gt) * H**2 - Vcov
ok_eps = sp.simplify(eps124 - (-2 * lcov - 3 * gt * Mp2 * Hd)) == 0
rep.p(f"CFG124's eps = (3/8piG)(1 - 3gt/2)H^2 - V  equals  -2 lambda - 3 gt M_P^2 H' : {ok_eps}")
rep.check("CFG124's eps expression = -2 lambda_bar - 3 gt M_P^2 H' (CMV eq. 78's momentum-density coefficient), "
          "not -2 lambda_bar, when gt != 0", ok_eps, kind="reported, post-hoc")
rep.results.update(lambda_cfg124=str(l124), lambda_covariant=str(lcov))
sys.exit(rep.finish())
