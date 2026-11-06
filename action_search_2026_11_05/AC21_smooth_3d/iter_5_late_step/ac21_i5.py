#!/usr/bin/env python3
"""AC21 iter_5: late-step structural blend (criteria FROZEN_CRITERIA.md, iter_5).
f'' = A q^4 (0, tau];  A q^4 (1 - S(x)) + S(x) + B x^5 (1-x)^n on [tau, 1];  1 above 1.  (A, B) from the two moments.
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_5_late_step/ac21_i5.py
Outputs ac21_i5.json/.out and form.json (exact winner for iter_2 and Lean). kappa = 1/2 FITTED; not theory closed.
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


def layer(tau, n, x0):
    """Piecewise in x: before x0 the late step is 0. Returned as (g_before, g_after, q_split)."""
    xq = (q - tau) / (1 - tau); yq = (xq - x0) / (1 - x0)
    base = A * q ** 4 * (1 - S.subs(x, xq)) + B * xq ** 5 * (1 - xq) ** n
    return sp.expand(base), sp.expand(base + S.subs(x, yq)), tau + x0 * (1 - tau)


tried, win = [], None
import itertools
for tau, x0, n in itertools.product((sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)),
                                    (sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(4, 5)), (5, 10)):
    if True:
        g1, g2, qs = layer(tau, n, x0); left = A * q ** 4
        g = sp.Piecewise((g1, q <= qs), (g2, True))
        m1 = sp.integrate(left, (q, 0, tau)) + sp.integrate(g1, (q, tau, qs)) + sp.integrate(g2, (q, qs, 1)) - 1
        m2 = (sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * g1, (q, tau, qs))
              + sp.integrate((1 - q) * g2, (q, qs, 1)) - sp.Rational(1, 2))
        sol = sp.solve([m1, m2], [A, B], dict=True)
        rec = dict(tau=str(tau), x0=str(x0), n=n, solved=len(sol) == 1)
        if len(sol) == 1:
            rec.update(A=str(sol[0][A]), B=str(sol[0][B]), A_float=float(sol[0][A]), B_float=float(sol[0][B]),
                       qualifies=bool(sol[0][A] > 0 and sol[0][B] >= 0))
        tried.append(rec); print(rec, flush=True)
        if rec.get("qualifies"):
            win = dict(tau=tau, n=n, x0=x0, A=sol[0][A], B=sol[0][B], g1=g1.subs(sol[0]), g2=g2.subs(sol[0]), qs=qs); break
res["tried"] = tried
ok["T4pp_qualifying_pair"] = win is not None
if win is not None:
    tau, Av, Bv = win["tau"], win["A"], win["B"]; g1, g2, qs = sp.expand(win["g1"]), sp.expand(win["g2"]), win["qs"]
    gv = sp.Piecewise((g1, q <= qs), (g2, True))
    left = Av * q ** 4
    chk = [sp.simplify(sp.diff(g1, q, j).subs(q, tau) - sp.diff(left, q, j).subs(q, tau)) == 0 for j in range(5)]
    chk += [sp.simplify(sp.diff(g2 - g1, q, j).subs(q, qs)) == 0 for j in range(5)]          # C^4 at the step start
    chk += [sp.simplify(g2.subs(q, 1) - 1) == 0] + [sp.simplify(sp.diff(g2, q, j).subs(q, 1)) == 0 for j in range(1, 5)]
    m1 = sp.integrate(left, (q, 0, tau)) + sp.integrate(g1, (q, tau, qs)) + sp.integrate(g2, (q, qs, 1))
    m2 = (sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * g1, (q, tau, qs))
          + sp.integrate((1 - q) * g2, (q, qs, 1)))
    chk += [sp.simplify(m1 - 1) == 0, sp.simplify(m2 - sp.Rational(1, 2)) == 0]
    ok["T4pp_C4_and_moments_exact"] = all(bool(c) for c in chk)
    qq = np.linspace(0, 1, 40001)
    g1n, g2n = sp.lambdify(q, g1, "numpy"), sp.lambdify(q, g2, "numpy")
    fpp = np.where(qq <= float(tau), float(Av) * qq ** 4, np.where(qq <= float(qs), g1n(qq), g2n(qq)))
    ok["T4pp_fpp_positive_numeric"] = bool(np.all(fpp[1:] > 0))
    f1n = np.concatenate([[0.0], np.cumsum(0.5 * (fpp[1:] + fpp[:-1]) * np.diff(qq))])   # f' by trapezoid (S-b, T7 only)
    dev = float(np.max(np.abs(f1n - qq)))
    ok["T5_Sb_dev"] = dev <= 1.0
    ok["T7_Fprime_nonneg_layer"] = bool(np.all(f1n >= -1e-15))
    res["winner"] = dict(tau=str(tau), n=win["n"], x0=str(win["x0"]), q_step_start=str(qs), A=str(Av), B=str(Bv), A_float=float(Av), B_float=float(Bv),
                         min_fpp_on_layer=float(np.min(fpp[qq >= float(tau)])), max_fpp=float(np.max(fpp)),
                         max_abs_fprime_minus_q=dev)
    json.dump(dict(tau=str(tau), n=win["n"], x0=str(win["x0"]), A=str(Av), B=str(Bv),
                   S="x^5 (126 - 420 x + 540 x^2 - 315 x^3 + 70 x^4)",
                   fpp="A q^4 on (0,tau]; A q^4 (1-S(x)) + B x^5 (1-x)^n + S(y) on [tau,1], x = (q-tau)/(1-tau), y = max(x-x0,0)/(1-x0); 1 above 1"),
              open(os.path.join(HERE, "form.json"), "w"), indent=1)
i1 = json.load(open(os.path.join(HERE, "..", "iter_1_3d_symbol", "ac21_i1.json")))
ok["T5_statics_iter1"] = i1["checks"]["T5_statics"]; ok["T6_iter1"] = i1["checks"]["T6_g1_g2"] and i1["checks"]["T6_factor"]
label = ("3D-admissible smoothing EXISTS (v3s b = rho_DE, AC2q b = X); 3D PASS pending iter_2 numerics"
         if all(ok.values()) else "NO-GO for the iter_5 family (3D label stays FAIL as frozen)")
out = dict(label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, "ac21_i5.json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = json.dumps(tried) + "\n" + "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items()) + f"\nLABEL: {label}\n"
open(os.path.join(HERE, "ac21_i5.out"), "w").write(txt)
print(txt)
