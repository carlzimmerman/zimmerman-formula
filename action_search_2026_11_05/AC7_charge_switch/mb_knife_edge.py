"""AC7 control M-b: switch on D.P alone (v3s style) on FRW, where D.P bar = 0. Shows the longitudinal-P quadratic
action is not analytic: the integrated lapse coefficient differs for D.P > 0 and D.P < 0 perturbations.
Run from the repository root. Kappa = 1/2 FITTED; not theory closed."""
import json, os, sympy as sp
k, K, g, al, P = sp.symbols("k K gamma alpha P", positive=True)
def integ(stiff_on):
    L = k * P * al / 2 - K * P ** 2 / 4 - (g / 2 * k ** 2 * P ** 2 / 2 if stiff_on else 0)
    Ps = sp.solve(sp.diff(L, P), P)[0]
    return sp.simplify(L.subs(P, Ps))
pos, neg = integ(True), integ(False)
d = sp.simplify(pos - neg)
out = {"D.P>0 side": str(pos), "D.P<0 side": str(neg), "difference": str(d), "non_analytic": d != 0}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb_knife_edge.json"), "w"), indent=1)
