# KF1 T7: R4 with the kinetic prefactor n and the length coefficient xi left free. Run: python3 kf1_r4.py
import json, os
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__))
G, c, rho, r, n, xi, a0 = sp.symbols("G c rho r n xi a_0", positive=True)
Phi = sp.Function("Phi")(r)
X = n * c**4 * (1 - 2 * Phi / c**2)          # n = 1/2 is the canonical prefactor
X0 = X.subs(Phi, 0)
gradX = sp.Abs(sp.diff(X, r)).subs(sp.Abs(sp.diff(Phi, r)), a0)
gradX = 2 * n * c**2 * a0                    # |dX/dr| at g = a0
lam = xi * c / sp.sqrt(G * rho)
sol = sp.solve(sp.Eq(lam * gradX, X0.doit()), a0)[0]
kappa = sp.simplify(sol / (c * sp.sqrt(G * rho)))
res = {"kappa(n, xi)": str(kappa), "depends_on_n": bool(kappa.has(n)), "depends_on_xi": bool(kappa.has(xi)),
       "xi_for_deSitter": str(kappa.subs(xi, sp.sqrt(3 / (8 * sp.pi)))), "label": "VOID as derivation, TRADE for xi"}
for k, v in res.items():
    print(k, v)
with open(os.path.join(here, "kf1_r4.json"), "w") as f:
    json.dump(res, f, indent=1)
