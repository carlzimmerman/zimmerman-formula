#!/usr/bin/env python3
"""AC21 iter_4: structurally positive C^4 blend (criteria FROZEN_CRITERIA.md, 3b4cb45230).
f'' = A q^4 (0, tau];  A q^4 (1 - S(x)) + S(x) + B x^5 (1-x)^n on [tau, 1];  1 above 1.  (A, B) from the two moments.
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_4_structural_blend/ac21_i4.py
Outputs ac21_i4.json/.out and form.json (exact winner for iter_2 and Lean). kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
q, x, A, B = sp.symbols("q x A B")
S = x ** 5 * (126 - 420 * x + 540 * x ** 2 - 315 * x ** 3 + 70 * x ** 4)
ok, res = {}, {}
ok["S_endpoints"] = S.subs(x, 0) == 0 and S.subs(x, 1) == 1 and all(sp.diff(S, x, j).subs(x, 0) == 0 and sp.diff(S, x, j).subs(x, 1) == 0 for j in range(1, 5))
dS = sp.factor(sp.diff(S, x))
ok["S_monotone"] = sp.simplify(dS - 630 * x ** 4 * (1 - x) ** 4) == 0      # S' = 630 x^4 (1-x)^4 >= 0


def layer(tau, n):
    xq = (q - tau) / (1 - tau)
    return sp.expand(A * q ** 4 * (1 - S.subs(x, xq)) + S.subs(x, xq) + B * xq ** 5 * (1 - xq) ** n)


tried, win = [], None
for tau in (sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)):
    for n in (5, 10, 15, 20, 30):
        g = layer(tau, n); left = A * q ** 4
        m1 = sp.integrate(left, (q, 0, tau)) + sp.integrate(g, (q, tau, 1)) - 1
        m2 = sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * g, (q, tau, 1)) - sp.Rational(1, 2)
        sol = sp.solve([m1, m2], [A, B], dict=True)
        rec = dict(tau=str(tau), n=n, solved=len(sol) == 1)
        if len(sol) == 1:
            rec.update(A=str(sol[0][A]), B=str(sol[0][B]), A_float=float(sol[0][A]), B_float=float(sol[0][B]),
                       qualifies=bool(sol[0][A] > 0 and sol[0][B] >= 0))
        tried.append(rec); print(rec, flush=True)
        if rec.get("qualifies"):
            win = dict(tau=tau, n=n, A=sol[0][A], B=sol[0][B], g=g.subs(sol[0])); break
    if win is not None:
        break
res["tried"] = tried
ok["T4pp_qualifying_pair"] = win is not None
if win is not None:
    tau, Av, Bv, gv = win["tau"], win["A"], win["B"], sp.expand(win["g"])
    left = Av * q ** 4
    chk = [sp.simplify(sp.diff(gv, q, j).subs(q, tau) - sp.diff(left, q, j).subs(q, tau)) == 0 for j in range(5)]
    chk += [sp.simplify(gv.subs(q, 1) - 1) == 0] + [sp.simplify(sp.diff(gv, q, j).subs(q, 1)) == 0 for j in range(1, 5)]
    m1 = sp.integrate(left, (q, 0, tau)) + sp.integrate(gv, (q, tau, 1))
    m2 = sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * gv, (q, tau, 1))
    chk += [m1 == 1, m2 == sp.Rational(1, 2)]
    ok["T4pp_C4_and_moments_exact"] = all(bool(c) for c in chk)
    qq = np.linspace(0, 1, 40001)
    gnum = sp.lambdify(q, gv, "numpy")
    fpp = np.where(qq <= float(tau), float(Av) * qq ** 4, gnum(qq))
    ok["T4pp_fpp_positive_numeric"] = bool(np.all(fpp[1:] > 0))
    f1_mid = Av * tau ** 5 / 5 + sp.integrate(gv, (q, tau, q))
    f1n = np.where(qq <= float(tau), float(Av) * qq ** 5 / 5, sp.lambdify(q, f1_mid, "numpy")(qq))
    dev = float(np.max(np.abs(f1n - qq)))
    ok["T5_Sb_dev"] = dev <= 1.0
    ok["T7_Fprime_nonneg_layer"] = bool(np.all(f1n >= -1e-15))
    res["winner"] = dict(tau=str(tau), n=win["n"], A=str(Av), B=str(Bv), A_float=float(Av), B_float=float(Bv),
                         min_fpp_on_layer=float(np.min(fpp[qq >= float(tau)])), max_fpp=float(np.max(fpp)),
                         max_abs_fprime_minus_q=dev)
    json.dump(dict(tau=str(tau), n=win["n"], A=str(Av), B=str(Bv),
                   S="x^5 (126 - 420 x + 540 x^2 - 315 x^3 + 70 x^4)",
                   fpp="A q^4 on (0,tau]; A q^4 (1-S(x)) + S(x) + B x^5 (1-x)^n on [tau,1], x = (q-tau)/(1-tau); 1 above 1"),
              open(os.path.join(HERE, "form.json"), "w"), indent=1)
i1 = json.load(open(os.path.join(HERE, "..", "iter_1_3d_symbol", "ac21_i1.json")))
ok["T5_statics_iter1"] = i1["checks"]["T5_statics"]; ok["T6_iter1"] = i1["checks"]["T6_g1_g2"] and i1["checks"]["T6_factor"]
label = ("3D-admissible smoothing EXISTS (v3s b = rho_DE, AC2q b = X); 3D PASS pending iter_2 numerics"
         if all(ok.values()) else "NO-GO for the iter_4 family (3D label stays FAIL as frozen)")
out = dict(label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, "ac21_i4.json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = json.dumps(tried) + "\n" + "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items()) + f"\nLABEL: {label}\n"
open(os.path.join(HERE, "ac21_i4.out"), "w").write(txt)
print(txt)
