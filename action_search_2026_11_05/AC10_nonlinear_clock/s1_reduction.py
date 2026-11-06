#!/usr/bin/env python3
"""AC10 S1: AC7's PN Lagrangian (on-region) in 1D planar symmetry reduces to the label system of FROZEN_CRITERIA.

Checks (sympy, exact):
 E1  sigma-EL is a continuity law d_t Pi + d_x F = 0 with Pi = dL/d sigma_t; F + Pi sigma_x vanishes at s = 0 and is
     s^2 * O(eps) under PN scaling (sigma_t, phi ~ eps, sigma_x ~ sqrt eps): transport velocity v = -sigma_x.
 E2  v = -sigma_x and Bernoulli Xi = phi - sigma_t + sigma_x^2/2 give D_t v = Xi_x - phi_x identically; with the P-EL,
     a = K M P - gamma d_x(P_x + C2) - phi_x.
 E3  phi-EL: phi_xx = K(rho_b + P_x + s^2) + s^2 O(eps) + O(gamma s^2): Poisson sees D.P + clock density.
 E4  charge Pi_on = P_x + C2 = P_x + s^2 + s^2 O(eps), and Pi (momentum) - Pi_on = s^2 O(eps) + O(gamma s^2):
     P_x = Pi - s^2 to PN order, as stated.
Run from the repo root: python3 action_search_2026_11_05/AC10_nonlinear_clock/s1_reduction.py
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
sys.dont_write_bytecode = True
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
t, x = sp.symbols("t x", real=True)
K, M, s, g = sp.symbols("K M s gamma_L", positive=True)
rb = sp.Function("rho_b")(x)
phi = sp.Function("phi")(t, x); sig = sp.Function("sigma")(t, x); P = sp.Function("P")(t, x)
st, sx = sp.diff(sig, t), sp.diff(sig, x)
Xi = phi - st + sx ** 2 / 2
C2 = s ** 2 * ((1 + st) ** 2 / (1 + phi) ** 2 - sx ** 2)
L = (-sp.diff(phi, x) ** 2 / (2 * K) + P * sp.diff(Xi, x) - K * M * P ** 2 / 2
     - g / 2 * ((sp.diff(P, x) + C2) ** 2 - C2 ** 2) + C2 / 2 - rb * phi)
res, ok = {}, {}

# E1: momentum and flux of sigma (L depends on sigma only through sigma_t, sigma_x, and P*Xi_x contains sigma_tx, sigma_xx:
# integrate P*Xi_x by parts first: P Xi_x -> -P_x Xi (exact up to a total derivative)
L_ibp = L - P * sp.diff(Xi, x) - sp.diff(P, x) * Xi
Sx, St = sp.symbols("S_x S_t")
Lsym = L_ibp.subs({sp.diff(sig, x): Sx, sp.diff(sig, t): St})
Pi = sp.diff(Lsym, St).subs({Sx: sx, St: st})
F = sp.diff(Lsym, Sx).subs({Sx: sx, St: st})
R1 = sp.simplify(F + Pi * sx)
e = sp.Symbol("e", positive=True)
pn = lambda ex: ex.subs({sp.diff(sig, t): e * sp.Symbol("u"), sp.diff(sig, x): sp.sqrt(e) * sp.Symbol("w"),
                         phi: e * sp.Symbol("f"), sp.diff(P, x): sp.Symbol("D")})
R1pn = sp.series(pn(R1), e, 0, 2).removeO()
ok["E1"] = sp.simplify(R1.subs(s, 0)) == 0 and sp.simplify(R1pn.subs(e, 0)) == 0
res["E1"] = dict(Pi=str(sp.simplify(Pi)), F_plus_Pi_sigmax=str(R1), leading_PN=str(sp.simplify(R1pn)))

# E2: Euler identity
v = -sx
Dv = sp.diff(v, t) + v * sp.diff(v, x)
R2 = sp.simplify(Dv - (sp.diff(Xi, x) - sp.diff(phi, x)))
(elP,) = euler_equations(L, [P], (t, x))
Peq = sp.simplify(elP.lhs)                    # = Xi_x - K M P + gamma d_x(P_x + C2)
R2b = sp.simplify(Peq - (sp.diff(Xi, x) - K * M * P + g * sp.diff(sp.diff(P, x) + C2, x)))
ok["E2"] = R2 == 0 and R2b == 0
res["E2"] = dict(euler_residual=str(R2), P_EL_residual=str(R2b))

# E3: Poisson
(elphi,) = euler_equations(L, [phi], (t, x))
phixx = sp.solve(sp.Eq(elphi.lhs, 0), sp.diff(phi, x, 2))[0]
R3 = sp.simplify(phixx / K - (rb + sp.diff(P, x) + s ** 2))
R3pn = sp.series(pn(R3), e, 0, 1).removeO()
ok["E3"] = sp.simplify(R3.subs(s, 0)) == 0 and sp.simplify(R3pn.subs(g, 0)) == 0
res["E3"] = dict(phi_xx=str(phixx), residual=str(R3), leading_PN=str(sp.simplify(R3pn)))

# E4: charges
Pion = sp.diff(P, x) + C2
R4a = sp.series(pn(Pion - sp.diff(P, x) - s ** 2), e, 0, 1).removeO()
R4b = sp.series(pn(Pi - Pion), e, 0, 1).removeO()
ok["E4"] = sp.simplify(R4a) == 0 and sp.simplify(R4b.subs(g, 0)) == 0
res["E4"] = dict(Pi_on_minus_Px_minus_s2_leading=str(sp.simplify(R4a)), Pi_minus_Pi_on_leading=str(sp.simplify(R4b)))

ok["S1"] = all(ok.values())
for k_, v_ in ok.items():
    print(f"{k_} {'PASS' if v_ else 'FAIL'} {res.get(k_, '')}")
json.dump(dict(checks=ok, detail=res), open(os.path.join(HERE, "s1_reduction.json"), "w"), indent=1)
sys.exit(0 if ok["S1"] else 1)
