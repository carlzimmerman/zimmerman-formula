#!/usr/bin/env python3
"""AC21 iter_3: wider blend family for the 3D-admissible smoothing (criteria FROZEN_CRITERIA.md, f5b0b7270d).
f'' = A q^4 on (0, tau], degree-D polynomial on [tau, 1] (C^4 knots, two moments), 1 above 1; free directions by LP
(max min Bernstein coefficient), rational rounding, exact re-solve, exact Bernstein positivity.
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_3_wide_blend/ac21_i3.py
Outputs ac21_i3.json/.out and form.json (the certified member, exact rationals, for iter_2 and Lean).
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
from fractions import Fraction
import numpy as np
import sympy as sp
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
q, sv = sp.symbols("q s")
KK = 4


def system(tau, D):
    A = sp.Symbol("A"); cs = list(sp.symbols(f"p0:{D + 1}"))
    p = sum(ci * q ** i for i, ci in enumerate(cs)); left = A * q ** 4
    eqs = [sp.diff(p, q, j).subs(q, tau) - sp.diff(left, q, j).subs(q, tau) for j in range(KK + 1)]
    eqs += [p.subs(q, 1) - 1] + [sp.diff(p, q, j).subs(q, 1) for j in range(1, KK + 1)]
    eqs += [sp.integrate(left, (q, 0, tau)) + sp.integrate(p, (q, tau, 1)) - 1,
            sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * p, (q, tau, 1)) - sp.Rational(1, 2)]
    vars_ = [A] + cs
    E, rhs = sp.linear_eq_to_matrix([sp.expand(e) for e in eqs], vars_)
    ps = sp.Poly(sp.expand(p.subs(q, tau + (1 - tau) * sv)), sv)
    a_c = [ps.coeff_monomial(sv ** i) for i in range(D + 1)]
    bern = [sp.expand(sum(sp.binomial(j, i) / sp.binomial(D, i) * a_c[i] for i in range(j + 1))) for j in range(D + 1)]
    Bm, _ = sp.linear_eq_to_matrix(bern, vars_)
    return vars_, E, rhs, Bm, p


def attempt(tau, D):
    vars_, E, rhs, Bm, p = system(tau, D)
    n = len(vars_)
    Ef = np.array(E.tolist(), float); rf = np.array(rhs.tolist(), float).ravel(); Bf = np.array(Bm.tolist(), float)
    # variables x (n) and t; maximize t: minimize -t; Bern x >= t  ->  -Bf x + t <= 0
    c = np.zeros(n + 1); c[-1] = -1.0
    A_ub = np.hstack([-Bf, np.ones((Bf.shape[0], 1))]); b_ub = np.zeros(Bf.shape[0])
    A_eq = np.hstack([Ef, np.zeros((Ef.shape[0], 1))])
    bounds = [(-1e6, 1e6)] * n + [(None, 1e6)]
    lp = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=rf, bounds=bounds, method="highs")
    rec = dict(tau=str(tau), D=D, lp_status=int(lp.status), lp_t=(float(-lp.fun) if lp.status == 0 else None))
    if lp.status != 0 or -lp.fun <= 0:
        rec["certified"] = False; return rec, None
    x = lp.x[:n]
    # exact: free = last (n - rank) coordinates rounded; basic re-solved
    nfree = n - E.rank()
    for basic_start in range(0, n - (n - nfree) + 1):
        basic = list(range(basic_start, basic_start + (n - nfree)))
        free = [i for i in range(n) if i not in basic]
        Eb = E[:, basic]
        if Eb.rank() < len(basic):
            continue
        xf = {vars_[i]: sp.Rational(Fraction(float(x[i])).limit_denominator(10 ** 6).numerator,
                                    Fraction(float(x[i])).limit_denominator(10 ** 6).denominator) for i in free}
        eqs = [sp.expand(sum(E[r, j] * vars_[j] for j in range(n)) - rhs[r]) for r in range(E.shape[0])]
        sol = sp.solve([e.subs(xf) for e in eqs], [vars_[i] for i in basic], dict=True)
        if len(sol) != 1:
            continue
        full = dict(xf); full.update(sol[0])
        Avalue = full[vars_[0]]
        bern = [sp.nsimplify(sum(Bm[j, i] * full[vars_[i]] for i in range(n))) for j in range(Bm.shape[0])]
        pos = all(b_ > 0 for b_ in bern) and Avalue > 0
        rec.update(certified=bool(pos), min_bern=str(min(bern)), min_bern_float=float(min(bern)), A=str(Avalue))
        if pos:
            pv = sp.expand(p.subs(full))
            return rec, dict(tau=tau, D=D, A=Avalue, p=pv, bern=bern)
        return rec, None
    rec["certified"] = False; rec["note"] = "no nonsingular basic set"
    return rec, None


tried, win = [], None
for D in (12, 14, 16, 18, 20):
    for tau in (sp.Rational(1, 2), sp.Rational(1, 3)):
        rec, w = attempt(tau, D); tried.append(rec); print(rec, flush=True)
        if w is not None:
            win = w; break
    if win is not None:
        break

ok, res = {}, dict(tried=tried)
ok["T4p_certified_member"] = win is not None
if win is not None:
    tau, Av, pv, D = win["tau"], win["A"], win["p"], win["D"]
    # exact re-verification of every constraint
    left = Av * q ** 4
    chk = [sp.simplify(sp.diff(pv, q, j).subs(q, tau) - sp.diff(left, q, j).subs(q, tau)) == 0 for j in range(KK + 1)]
    chk += [sp.simplify(pv.subs(q, 1) - 1) == 0] + [sp.simplify(sp.diff(pv, q, j).subs(q, 1)) == 0 for j in range(1, KK + 1)]
    m1 = sp.integrate(left, (q, 0, tau)) + sp.integrate(pv, (q, tau, 1))
    m2 = sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * pv, (q, tau, 1))
    chk += [sp.simplify(m1 - 1) == 0, sp.simplify(m2 - sp.Rational(1, 2)) == 0]
    ok["T4p_constraints_exact"] = all(chk)
    roots = [r for r in sp.Poly(pv, q).real_roots() if tau <= r <= 1]
    ok["T4p_no_root_in_layer"] = len(roots) == 0
    f1_mid = Av * tau ** 5 / 5 + sp.integrate(pv, (q, tau, q))
    qq = np.linspace(0, 1, 40001)
    f1n = np.where(qq <= float(tau), float(Av) * qq ** 5 / 5, sp.lambdify(q, f1_mid, "numpy")(qq))
    dev = float(np.max(np.abs(f1n - qq)))
    ok["T5_Sb_dev"] = dev <= 1.0
    ok["T7_Fprime_nonneg_layer"] = bool(np.all(f1n >= -1e-15))
    fpp_n = np.where(qq <= float(tau), float(Av) * qq ** 4, sp.lambdify(q, pv, "numpy")(qq))
    res["winner"] = dict(tau=str(tau), D=D, A=str(Av), A_float=float(Av), fpp_layer=str(pv),
                         bernstein=[str(b_) for b_ in win["bern"]], min_bern_float=float(min(win["bern"])),
                         max_abs_fprime_minus_q=dev, min_fpp_layer=float(np.min(fpp_n[qq >= float(tau)])),
                         fpp_max=float(np.max(fpp_n)))
    json.dump(dict(tau=str(tau), D=D, A=str(Av), p_coeffs=[str(sp.Poly(pv, q).coeff_monomial(q ** i)) for i in range(D + 1)],
                   bernstein=[str(b_) for b_ in win["bern"]]), open(os.path.join(HERE, "form.json"), "w"), indent=1)
i1 = json.load(open(os.path.join(HERE, "..", "iter_1_3d_symbol", "ac21_i1.json")))
ok["T5_statics_iter1"] = i1["checks"]["T5_statics"]; ok["T6_iter1"] = i1["checks"]["T6_g1_g2"] and i1["checks"]["T6_factor"]
label = ("3D-admissible smoothing EXISTS (v3s b = rho_DE, AC2q b = X); 3D PASS pending iter_2 numerics"
         if all(ok.values()) else "NO-GO for the iter_3 family (label stays FAIL as frozen)")
out = dict(label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, "ac21_i3.json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items()) + f"\nLABEL: {label}\n"
open(os.path.join(HERE, "ac21_i3.out"), "w").write(json.dumps(tried, default=str) + "\n" + txt)
print(txt)
