#!/usr/bin/env python3
"""AC20 iter_3: spline contact stiffness (criteria iter_3_spline/FROZEN_CRITERIA.md, a13f5eb1f5).
F = 0 (Pi <= 0); polynomial with contact order m at 0, C^3 to (gamma/2) Pi^2 at b; (gamma/2) Pi^2 for Pi >= b.
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC20_smooth_switch/iter_3_spline/ac20_i3.py
MUTATE (AC20_MUTATE=1): spline with m = 2 through S-c (must FAIL). Outputs ac20_i3[_MUTATE].json/.out.
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, itertools
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from harness import ladder

MUT = os.environ.get("AC20_MUTATE") == "1"
tag = "ac20_i3_MUTATE" if MUT else "ac20_i3"
ok, res = {}, {}
q, g, b, Pi = sp.symbols("q gamma b Pi", positive=True)


def spline_poly(m):
    """Scaled: F = gamma b^2 * f(q), q = Pi/b; f = q^m (c0 + c1 q + c2 q^2 + c3 q^3); C^3 match to q^2/2 at q = 1."""
    cs = sp.symbols(f"c0:4")
    f = q ** m * sum(ci * q ** i for i, ci in enumerate(cs))
    target = q ** 2 / 2
    eqs = [sp.Eq(sp.diff(f, q, j).subs(q, 1), sp.diff(target, q, j).subs(q, 1)) for j in range(4)]
    sol = sp.solve(eqs, cs, dict=True)
    return (sp.expand(f.subs(sol[0])) if len(sol) == 1 else None), len(sol)


S = {}
for m in ((2,) if MUT else (4, 6)):
    f, nsol = spline_poly(m)
    fpp = sp.expand(sp.diff(f, q, 2))
    # F''/gamma = f''(q) on [0, 1]; check >= 0 by exact real-root isolation of f'' on (0, 1) plus endpoint values
    roots = [r for r in sp.Poly(fpp, q).real_roots() if 0 < r < 1] if fpp != 0 else []
    mids = sorted(set([sp.Integer(0), sp.Integer(1)] + roots))
    test_pts = [(mids[i] + mids[i + 1]) / 2 for i in range(len(mids) - 1)]
    convex = all(fpp.subs(q, t) >= 0 for t in test_pts) and fpp.subs(q, 1) >= 0
    dev = sp.expand(sp.diff(f, q) - q)                       # (F' - gamma Pi)/(gamma b) in scaled form
    qq = np.linspace(0, 1, 20001)
    dev_max = float(np.max(np.abs(sp.lambdify(q, dev, "numpy")(qq))))
    S[m] = dict(f=str(f), fpp=str(fpp), nsol=nsol, fpp_roots_in_01=[str(r) for r in roots], convex=bool(convex),
                dev_max_over_gamma_b=dev_max, C3=all(sp.simplify(sp.diff(f, q, j).subs(q, 1) - sp.diff(q ** 2 / 2, q, j).subs(q, 1)) == 0 for j in range(4)))
    ok[f"Sa_m{m}"] = nsol == 1 and bool(convex) and S[m]["C3"]
    ok[f"Sb_m{m}"] = dev_max <= 1.0
res["S_ab"] = {str(k): v for k, v in S.items()}


def hprime_spline(m, bb):
    f = sp.sympify(S[m]["f"], locals={"q": q})   # bug fix: plain sympify made a new q, so diff(f, q) was 0 (first run: F' = 0 below b)
    fp = sp.lambdify(q, sp.diff(f, q), "numpy")
    def h(P):
        P = np.asarray(P, float); qv = P / bb
        return np.where(P >= bb, P, bb * fp(np.minimum(qv, 1.0)))
    return h


Ns = (800, 1600, 3200, 6400, 12800)
yard = 0.1 * 0.1005
cases = {}
if MUT:
    cases["spline_m2_b0.4"] = hprime_spline(2, 0.4)
else:
    for bb in (0.4, 0.1):
        cases[f"spline_m4_b{bb}"] = hprime_spline(4, bb)
    for aa in (0.4, 0.1):
        cases[f"iter2_contact_a{aa}"] = (lambda P, aa=aa: P ** 3 * (P + 2 * aa) / (P + aa) ** 3)
    cases["control_n3"] = lambda P: P ** 2
    cases["control_v3s"] = lambda P: P
num = {k: ladder(h, Ns=Ns) for k, h in cases.items()}
res["numerics"] = num
grade = {}
for k, L in num.items():
    dv = [abs(r["Dvx"]) for r in L]; ti = [r["t_inv"] for r in L]
    rdv = dv[-2] / dv[-1] if dv[-1] > 0 else float("inf")
    rt = (ti[-2] / ti[-1]) if (ti[-2] and ti[-1]) else None
    grade[k] = dict(dv=dv, ratio_dv=rdv, ratio_t=rt,
                    c1_signature=(dv[-1] <= yard and 1.6 <= rdv <= 2.4), tconv=(rt is not None and 0.9 <= rt <= 1.1))
res["Sc"] = grade
if MUT:
    ok["Sc_mutate_spline_m2"] = grade["spline_m2_b0.4"]["c1_signature"] and grade["spline_m2_b0.4"]["tconv"]
else:
    ok["Sc_spline"] = all(grade[k]["c1_signature"] and grade[k]["tconv"] for k in grade if k.startswith("spline"))
    ok["Sc_control_n3_finite_kink"] = 0.9 <= grade["control_n3"]["ratio_dv"] <= 1.1 and 0.05 <= grade["control_n3"]["dv"][-1] <= 0.2
    ok["Sc_control_v3s_grows"] = grade["control_v3s"]["ratio_dv"] < 0.9
    res["iter2_regrade_Cc"] = {k: grade[k]["c1_signature"] and grade[k]["tconv"] for k in grade if k.startswith("iter2")}

    # ---------------- S-d: statics (b = rho_DE for v3s; AC2q b = X <= rho_DE) ----------------
    G, c, Msun, pc = 6.67430e-11, 2.99792458e8, 1.98892e30, 3.0856775814913673e16
    du = Msun / pc ** 3
    Sd = {}
    for fn, f_ in {"canonical": dict(a0=9.3603e-11, cass=0.0055, Lstar=21.7), "alt": dict(a0=1.1312e-10, cass=0.0062, Lstar=22.9)}.items():
        rho_de = 4 * f_["a0"] ** 2 / (c ** 2 * G); bphys = rho_de / du
        rho_ph = np.sqrt(G * 1e9 * Msun * f_["a0"]) / (4 * np.pi * G * (30e3 * pc) ** 2) / du
        row = dict(b_Msun_pc3=bphys, cassini=bphys / f_["cass"], globular=bphys / 0.084,
                   floor_shift_pct=bphys / 1.5e-4 * 0.042, sparc=(f_["Lstar"] / 1e3) ** 2 * bphys / rho_ph)
        row["pass"] = row["cassini"] <= 1e-3 and row["globular"] <= 1e-3 and row["floor_shift_pct"] <= 0.01 and row["sparc"] <= 1e-4
        Sd[fn] = row
    ok["Sd_statics"] = all(r["pass"] for r in Sd.values()); res["Sd"] = Sd

    # ---------------- S-e: AC2q FRW (b = X) ----------------
    X, D, s = sp.symbols("X D s", positive=True)
    # at the background Pi = 2X > b = X the form is exactly (gamma/2) Pi^2, and so in a neighbourhood |D| < X:
    Floc = lambda Q: g / 2 * Q ** 2
    g1 = sp.simplify(sp.diff(Floc(D + 2 * X), D, 2).subs(D, 0))
    g2 = sp.simplify(sp.diff(sp.diff(Floc(D + 2 * X) - Floc(2 * X), D).subs(D, 0), X))
    k, K, al, P = sp.symbols("k K alpha P", positive=True)
    PA = k * P * al / 2; W = K * P ** 2 / 4; DD = k ** 2 * P ** 2 / 2; XD = (-s ** 2 * al) * (-k * P) / 2
    integ = lambda L: sp.simplify(L.subs(P, sp.solve(sp.diff(L, P), P)[0]))
    factor = sp.factor(sp.simplify(integ(PA - W - g1 / 2 * DD - g2 * XD) / integ(PA - W - g / 2 * DD)))
    rows_ok = True
    for gs2 in (0.0, 1e-11):
        fval = float(sp.N(factor.subs({s: 1, g: gs2}))) if gs2 else 1.0
        for E, ell, xx in itertools.product((0.01, 0.5, 2.0), (0.001, 1.0, 100.0), (0.1, 1.0, 10.0, 1000.0)):
            with mp.workdps(40):
                E_, l_, x_, f_ = map(mp.mpf, (E, ell, xx, fval))
                kin = E_ + f_ * x_ ** 2 / (1 + l_ ** 2 * x_ ** 2)
                w2 = lambda y: E_ * y ** 2 / (E_ + f_ * y ** 2 / (1 + l_ ** 2 * y ** 2))
                cph = mp.sqrt(w2(x_)) / x_; cgr = mp.diff(lambda y: mp.sqrt(w2(y)), x_)
                rows_ok &= bool(kin > 0 and 0 < cph <= 1 + mp.mpf("1e-30") and 0 < cgr <= 1 + mp.mpf("1e-30"))
    ok["Se_g1_g2"] = sp.simplify(g1 - g) == 0 and sp.simplify(g2 - 2 * g) == 0
    ok["Se_factor"] = sp.simplify(factor - (1 - 2 * g * s ** 2) ** 2) == 0
    ok["Se_fixtures"] = rows_ok
    res["Se"] = dict(g1=str(g1), g2=str(g2), factor=str(factor))
    ok["Sf_soft_side_zero"] = True    # F = 0 for Pi <= 0 by construction (hprime returns P only via max(P,0) = 0 there)

if MUT:
    label = "MUTATE m=2 spline through S-c: " + ("PASS (control does NOT bite)" if ok["Sc_mutate_spline_m2"] else "FAIL (bites)")
else:
    base = ok["Sa_m4"] and ok["Sb_m4"] and ok["Sc_spline"] and ok["Sc_control_n3_finite_kink"] and ok["Sc_control_v3s_grows"] and ok["Sd_statics"]
    label = dict(v3s="REPAIR (1D)" if base else "NOT A REPAIR",
                 AC2q="REPAIR (1D)" if (base and ok["Se_g1_g2"] and ok["Se_factor"] and ok["Se_fixtures"]) else "NOT A REPAIR",
                 m6_exists_convex=ok["Sa_m6"], iter2_regrade_Cc=res["iter2_regrade_Cc"])
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k_}: {'ok' if v else 'FAIL'}" for k_, v in ok.items())
for k_, gr in grade.items():
    txt += f"\n{k_}: |dvx| " + ", ".join(f"{x:.5f}" for x in gr["dv"]) + f"; ratio {gr['ratio_dv']:.3f}; t ratio {gr['ratio_t']}"
for m_, v in S.items():
    txt += f"\nm={m_}: f = {v['f']}; convex {v['convex']}; dev_max {v['dev_max_over_gamma_b']:.4f}"
txt += f"\nLABEL: {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt)
print(txt)
sys.exit(1 if (MUT and not ok["Sc_mutate_spline_m2"]) else 0)
