"""AC8: AC2q's static limit against v3s's (H4 A1 Lagrangian at mu_K = 0). Criteria FROZEN_CRITERIA.md.
Run from the repository root: PYTHONHASHSEED=0 python3 action_search_2026_11_05/AC8_static_limit/ac8.py [--mutate]
Kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import sympy as sp
from sympy.calculus.euler import euler_equations
MUT = "--mutate" in sys.argv
x, y, z = xs = sp.symbols("x y z", real=True)
K, gL, s = sp.symbols("K gamma_L s", positive=True)
phi = sp.Function("phi")(*xs); Pf = [sp.Function(f"P{i}")(*xs) for i in range(3)]
rhom = sp.Function("rho_m")(*xs); Wf = sp.Function("W")
grad = lambda f: [sp.diff(f, v) for v in xs]; div = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
modP = sp.sqrt(sum(p ** 2 for p in Pf))
Xi = phi                                              # static, sigma = 0
base = -sum(d ** 2 for d in grad(phi)) / (2 * K) - rhom * phi + sum(Pf[i] * sp.diff(Xi, xs[i]) for i in range(3))
L_v3s = base - Wf(K * modP) - gL / 2 * div(Pf) ** 2                       # H4 A1 at mu_K = 0, static
C2 = s ** 2 / (1 + phi) ** 2                                               # 2X static
wsign = -1 if MUT else 1
L_q = base - wsign * Wf(K * modP) - gL / 2 * ((div(Pf) + C2) ** 2 - C2 ** 2) + C2 / 2
e1 = euler_equations(L_v3s, [phi] + Pf, xs); e2 = euler_equations(L_q, [phi] + Pf, xs)
diffs = [sp.simplify(sp.expand(a.lhs - b.lhs)) for a, b in zip(e1, e2)]
at0 = [sp.simplify(d.subs(s, 0)) for d in diffs]
# sigma equation in statics: time-dependent Lagrangian, evaluated at sigma = 0, static fields
t = sp.Symbol("t", real=True); X4 = (t, x, y, z)
sig = sp.Function("sigma")(*X4); phi4 = sp.Function("phi")(*X4); P4 = [sp.Function(f"P{i}")(*X4) for i in range(3)]
g4 = lambda f: [sp.diff(f, v) for v in xs]; d4 = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
Xi4 = phi4 - sp.diff(sig, t) + sum(d ** 2 for d in g4(sig)) / 2
C24 = s ** 2 * ((1 + sp.diff(sig, t)) ** 2 / (1 + phi4) ** 2 - sum(d ** 2 for d in g4(sig)))
L4 = (-sum(d ** 2 for d in g4(phi4)) / (2 * K) + sum(P4[i] * sp.diff(Xi4, xs[i]) for i in range(3))
      - wsign * Wf(K * sp.sqrt(sum(p ** 2 for p in P4))) - gL / 2 * ((d4(P4) + C24) ** 2 - C24 ** 2) + C24 / 2)
es = euler_equations(L4, [sig], X4)[0].lhs
stat = {sig: 0, phi4: sp.Function("phi")(*xs)}
for i in range(3):
    stat[P4[i]] = sp.Function(f"P{i}")(*xs)
sig_static = sp.simplify(es.subs(stat).doit())
out = {"mutate": MUT, "differences": [str(d) for d in diffs], "differences_at_s0": [str(d) for d in at0],
       "sigma_eq_at_static_sigma0": str(sig_static)}
transfers = all(d == 0 for d in at0) and sig_static == 0
out["label"] = ("TRANSFERS (corrections proportional to s^2)" if transfers else "DOES NOT TRANSFER") if not MUT else \
    ("control bites: difference survives at s = 0" if any(d != 0 for d in at0) else "control did NOT bite")
for k_, v in out.items():
    print(k_, ":", v)
H = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(H, "ac8_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
