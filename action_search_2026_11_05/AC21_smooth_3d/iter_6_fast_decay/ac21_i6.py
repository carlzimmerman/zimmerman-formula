#!/usr/bin/env python3
"""AC21 iter_6: fast-decaying left piece (criteria FROZEN_CRITERIA.md, 3ed022ae9f).
f'' = A q^4 (0, tau];  A q^4 (1 - S(z)) + B x^5 (1-x)^n + S(y) on [tau, 1];  1 above 1.
x = (q-tau)/(1-tau), z = min(x/x1, 1), y = max(x-x0, 0)/(1-x0); S = C^4 smoothstep.
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/ac21_i6.py
Outputs ac21_i6.json/.out and form.json. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, itertools
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
q, x, A, B = sp.symbols("q x A B")
S = lambda t: t ** 5 * (126 - 420 * t + 540 * t ** 2 - 315 * t ** 3 + 70 * t ** 4)
R = sp.Rational


def pieces(tau, x1, x0, n):
    """[(lo, hi, expr)] covering (0, 1]; knots tau, q1, qs."""
    xq = (q - tau) / (1 - tau)
    q1, qs = tau + x1 * (1 - tau), tau + x0 * (1 - tau)
    bump = B * xq ** 5 * (1 - xq) ** n
    return [(0, tau, A * q ** 4),
            (tau, q1, A * q ** 4 * (1 - S(xq / x1)) + bump),
            (q1, qs, bump),
            (qs, 1, bump + S((xq - x0) / (1 - x0)))], (q1, qs)


ok, res, tried, win = {}, {}, [], None
for tau, x1, x0, n in itertools.product((R(1, 2), R(1, 3)), (R(1, 4), R(1, 8)), (R(1, 2), R(4, 5)), (5, 10)):
    P, (q1, qs) = pieces(tau, x1, x0, n)
    m1 = sum(sp.integrate(sp.expand(e), (q, lo, hi)) for lo, hi, e in P) - 1
    m2 = sum(sp.integrate(sp.expand((1 - q) * e), (q, lo, hi)) for lo, hi, e in P) - R(1, 2)
    sol = sp.solve([m1, m2], [A, B], dict=True)
    rec = dict(tau=str(tau), x1=str(x1), x0=str(x0), n=n, solved=len(sol) == 1)
    if len(sol) == 1:
        rec.update(A=str(sol[0][A]), B=str(sol[0][B]), A_float=float(sol[0][A]), B_float=float(sol[0][B]),
                   qualifies=bool(sol[0][A] > 0 and sol[0][B] >= 0))
    tried.append(rec); print(rec, flush=True)
    if rec.get("qualifies"):
        win = dict(tau=tau, x1=x1, x0=x0, n=n, A=sol[0][A], B=sol[0][B],
                   P=[(lo, hi, sp.expand(e.subs(sol[0]))) for lo, hi, e in P], knots=(q1, qs))
        break
res["tried"] = tried
ok["T4pp_qualifying"] = win is not None
if win is not None:
    P = win["P"]; tau = win["tau"]
    chk = []
    for (lo, hi, e), (lo2, hi2, e2) in zip(P[:-1], P[1:]):          # C^4 at each interior knot
        chk += [sp.simplify(sp.diff(e - e2, q, j).subs(q, hi)) == 0 for j in range(5)]
    eR = P[-1][2]
    chk += [sp.simplify(eR.subs(q, 1) - 1) == 0] + [sp.simplify(sp.diff(eR, q, j).subs(q, 1)) == 0 for j in range(1, 5)]
    m1 = sum(sp.integrate(e, (q, lo, hi)) for lo, hi, e in P)
    m2 = sum(sp.integrate((1 - q) * e, (q, lo, hi)) for lo, hi, e in P)
    chk += [sp.simplify(m1 - 1) == 0, sp.simplify(m2 - R(1, 2)) == 0]
    ok["T4pp_C4_all_knots_and_moments_exact"] = all(bool(c) for c in chk)
    qq = np.linspace(0, 1, 80001)
    fpp = np.zeros_like(qq)
    for lo, hi, e in P:
        msk = (qq >= float(lo)) & (qq <= float(hi)); fpp[msk] = sp.lambdify(q, e, "numpy")(qq[msk])
    ok["T4pp_fpp_positive_numeric"] = bool(np.all(fpp[1:] > 0))
    f1 = np.concatenate([[0.0], np.cumsum(0.5 * (fpp[1:] + fpp[:-1]) * np.diff(qq))])
    dev = float(np.max(np.abs(f1 - qq)))
    ok["T5_Sb_dev"] = dev <= 1.0
    ok["T7_Fprime_nonneg"] = bool(np.all(f1 >= -1e-12))
    res["winner"] = dict(tau=str(tau), x1=str(win["x1"]), x0=str(win["x0"]), n=win["n"], A=str(win["A"]), B=str(win["B"]),
                         A_float=float(win["A"]), B_float=float(win["B"]), knots=[str(k) for k in win["knots"]],
                         min_fpp_on_0_1=float(np.min(fpp[1:])), min_fpp_on_layer=float(np.min(fpp[qq >= float(tau)])),
                         max_fpp=float(np.max(fpp)), max_abs_fprime_minus_q=dev, fprime_at_1=float(f1[-1]))
    json.dump(dict(tau=str(tau), x1=str(win["x1"]), x0=str(win["x0"]), n=win["n"], A=str(win["A"]), B=str(win["B"]),
                   pieces=[[str(lo), str(hi), str(e)] for lo, hi, e in P]), open(os.path.join(HERE, "form.json"), "w"), indent=1)
i1 = json.load(open(os.path.join(HERE, "..", "iter_1_3d_symbol", "ac21_i1.json")))
ok["T5_statics_iter1"] = i1["checks"]["T5_statics"]; ok["T6_iter1"] = i1["checks"]["T6_g1_g2"] and i1["checks"]["T6_factor"]
label = ("3D-admissible smoothing EXISTS (v3s b = rho_DE, AC2q b = X); 3D PASS pending iter_2 numerics"
         if all(ok.values()) else "NO-GO for the iter_6 family; construction unresolved (3D label stays FAIL as frozen)")
out = dict(label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, "ac21_i6.json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = json.dumps(tried) + "\n" + "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items()) + f"\nLABEL: {label}\n"
open(os.path.join(HERE, "ac21_i6.out"), "w").write(txt)
print(txt[txt.index("\n") + 1:])
