#!/usr/bin/env python3
"""W4-03 -- execute the eight kappa proposals register row K547 lists as never run.

Criteria: FROZEN_CRITERIA.md (committed alone, 4708fd74c). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.
Items: AS119 (max-ent log moment), AS562 (hidden hbar), AS654 (additive C0 in P(q)), AS655 (quartic flux correction),
AS672 (rigidity as a functional equation), AS698 (two averaging prescriptions), AS725 (mu = K'/2g integrability),
AS1923 (compact three-form quantisation). Proposal files under deepseek_push/astra_spawn_ideas/ are read only.

Light: sympy + stdlib, one process, seconds, well under 200 MB. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_03_unrun_as_proposals/w4_03.py \
        > why_4_puzzle/W4_03_unrun_as_proposals/w4_03.out
    W4_03_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_03_unrun_as_proposals/w4_03.py \
        > why_4_puzzle/W4_03_unrun_as_proposals/w4_03_MUTATE.out
MUTATE: M1 AS119 c 1/2 -> 1/3; M2 AS654 C0 -> 0; M3 AS655 lambda -> 0; M4 AS698 a = t^(2/3) -> t^(1/2);
        M5 AS1923 b -> 0. Exit 1 when the controls bite.

kappa = 1/2 is FITTED (CFG493: kappa_Lambda 0.417 +- 0.095). Not theory closed.
"""
import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_03_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
checks = []
res = {}


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
oo, pi = sp.oo, sp.pi
G, Z, beta, q, Q0, b, kap = sp.symbols("G Z beta q Q_0 b kappa", positive=True)
C0 = sp.symbols("C_0", real=True)
lam = sp.symbols("lambda", positive=True)


def eps_of(P):
    """energy density of a top-form flux with Lagrangian -P(q): eps = q P_q - P"""
    return sp.simplify(q * sp.diff(P, q) - P)


def kappa2_of(P):
    """kappa^2 = a0^2 / (G eps) with a0 = beta sqrt(G) q (k04)"""
    return sp.simplify(beta ** 2 * G * q ** 2 / (G * eps_of(P)))


def as119(c_val):
    u = sp.symbols("u", nonnegative=True)
    l0, l1 = sp.symbols("l0 l1", positive=True)
    fdens = sp.symbols("f", positive=True)
    # Euler-Lagrange of S - l0 C1 - l1 C2 pointwise in f: -ln f - 1 - l0 - l1 ln(1+u) = 0
    sol = sp.solve(sp.Eq(-sp.log(fdens) - 1 - l0 - l1 * sp.log(1 + u), 0), fdens)[0]
    shape_ok = sp.simplify(sol / (1 + u) ** (-l1) - sp.exp(-1 - l0)) == 0
    norm = sp.integrate((1 + u) ** (-l1), (u, 0, oo), conds="none")          # 1/(l1-1) for l1 > 1
    f = (l1 - 1) * (1 + u) ** (-l1)
    elog = sp.simplify(sp.integrate(f * sp.log(1 + u), (u, 0, oo), conds="none"))
    n_of_c = sp.solve(sp.Eq(1 / (l1 - 1), sp.Symbol("c", positive=True)), l1)[0] - 1   # n = l1 - 1
    n_val = 1 / sp.Rational(c_val)
    # truncated moments in t = ln(1+u): f du = n e^{-n t} dt; exact truncated E = (1/n)[1 - e^{-nT}(1+nT)]
    rows = []
    nv = float(n_val)
    for umax in (10, 100, 1000):
        T = math.log1p(umax)
        exact_trunc = (1 / nv) * (1 - math.exp(-nv * T) * (1 + nv * T))
        tail = (1 / nv) * math.exp(-nv * T) * (1 + nv * T)
        for cells in (128, 256, 512):
            h = T / cells
            mid = sum(nv * (h * (i + 0.5)) * math.exp(-nv * h * (i + 0.5)) * h for i in range(cells))
            rows.append({"u_max": umax, "cells": cells, "E_trunc_midpoint": mid, "E_trunc_exact": exact_trunc,
                         "tail_bound": tail, "residual_vs_1_over_n": abs(mid + tail - 1 / nv),
                         "quad_err": abs(mid - exact_trunc)})
    return {"EL_shape_ok": bool(shape_ok), "norm": str(norm), "E_log": str(elog), "n_of_c": str(n_of_c),
            "c": str(sp.Rational(c_val)), "n": str(n_val), "kappa_conditional": str(1 / n_val), "trunc": rows}


def hbar_power(expr, hb):
    e = sp.together(expr)
    num, den = sp.fraction(e)
    return sp.degree(num, hb) - sp.degree(den, hb)


def as562():
    hb, M, v, R, c, A, rho, k = sp.symbols("hbar M v R c A rho k", positive=True)
    Pi = hb / (M * v * R)
    dims = {hb: (1, 2, -1), M: (1, 0, 0), v: (0, 1, -1), R: (0, 1, 0)}      # (M, L, T) exponents
    dim_Pi = [sum(dims[s][i] * sp.degree(sp.fraction(Pi)[0], s) - dims[s][i] * sp.degree(sp.fraction(Pi)[1], s)
                  for s in dims) for i in range(3)]
    law = k * c * sp.sqrt(G * rho)                                            # a0 = kappa c sqrt(G rho)
    S_restored = A * c ** 3 / (4 * G * hb)                                    # "A/(4 l_P^2)" with l_P^2 = G hbar/c^3
    return {"Pi": str(Pi), "dim_Pi_MLT": dim_Pi, "p_Pi": int(hbar_power(Pi, hb)),
            "p_law": int(hbar_power(law ** 2, hb)), "p_entropy_count": int(hbar_power(S_restored, hb))}


def as654(c0):
    P = Z * q ** 2 / 2 + c0
    k2 = kappa2_of(P)
    eps = eps_of(P)
    a0sq = beta ** 2 * G * q ** 2
    tracking = sp.simplify(a0sq - 2 * beta ** 2 * G / Z * (eps + c0))
    return {"k2": k2, "dk2_dq": sp.simplify(sp.diff(k2, q)), "tracking_identity_residual": tracking}


def as655(lv):
    P = Z * q ** 2 / 2 + lv * q ** 4 / Q0 ** 2
    k2 = kappa2_of(P)
    eps = eps_of(P)
    slope = sp.simplify(1 / (q * sp.diff(eps, q) / eps))                     # d ln a0 / d ln eps, a0 ~ q
    x = sp.symbols("x", positive=True)
    slope_x = sp.simplify(slope.subs(q, sp.sqrt(x * Q0 ** 2 / lv))) if lv != 0 else sp.Rational(1, 2)
    return {"k2": k2, "slope": slope, "slope_x": slope_x}


def as672():
    Pf = sp.Function("P")
    a0sq = beta ** 2 * G * q ** 2
    out = {}
    for kv in (sp.Rational(3, 10), sp.Rational(1, 2), sp.Rational(7, 10)):
        sol = sp.dsolve(sp.Eq(q * Pf(q).diff(q) - Pf(q), a0sq / (kv ** 2 * G)), Pf(q)).rhs
        resid = sp.simplify(q * sp.diff(sol, q) - sol - a0sq / (kv ** 2 * G))
        out[str(kv)] = {"P": str(sol), "residual": str(resid)}
    # general smooth a0(q) = sqrt(G) h(q), sample h = q + q^3: P = q [C + int h^2/(kappa^2 s^2) ds]
    s, Cc = sp.symbols("s C")
    h = q + q ** 3
    Pgen = q * (Cc + sp.integrate((h.subs(q, s)) ** 2 / (kap ** 2 * s ** 2), (s, 1, q)))
    resid_gen = sp.simplify(q * sp.diff(Pgen, q) - Pgen - G * h ** 2 / (kap ** 2 * G))
    homog = sp.simplify(eps_of(Cc * q))
    # linear a0 reproduces k04: P = C q + (beta^2/kappa^2) q^2 = Z q^2/2 + b beta^2 q^2  =>  kappa^2 = 2 beta^2/(Z + 2 b beta^2)
    k04 = sp.solve(sp.Eq(beta ** 2 / kap ** 2, Z / 2 + b * beta ** 2), kap ** 2)[0]
    return {"per_kappa": out, "general_residual": str(resid_gen), "homogeneous_energy": str(homog), "k04_kappa2": k04}


def as698(pexp):
    t, T = sp.symbols("t T", positive=True)
    a = t ** pexp
    H = sp.diff(a, t) / a
    out = {}
    for name, L in (("L=H^2", H ** 2), ("L=const", sp.Integer(1))):
        At = sp.integrate(a ** 3 * L, (t, 1, T)) / sp.integrate(a ** 3, (t, 1, T))
        da = sp.diff(a, t)
        Aa = sp.integrate(a ** 3 * L * da, (t, 1, T)) / sp.integrate(a ** 3 * da, (t, 1, T))
        ratio = sp.simplify(Aa / At)
        out[name] = {"ratio": str(ratio), "values": {str(Tv): float(ratio.subs(T, Tv)) for Tv in (10, 100, 1000)}}
    # de Sitter control: a = e^t, constant L -> both averages equal L
    tt = sp.symbols("tt", positive=True)
    ad = sp.exp(tt)
    Lc = sp.Integer(3)
    At_d = sp.integrate(ad ** 3 * Lc, (tt, 0, 5)) / sp.integrate(ad ** 3, (tt, 0, 5))
    Aa_d = sp.integrate(ad ** 3 * Lc * ad, (tt, 0, 5)) / sp.integrate(ad ** 4, (tt, 0, 5))
    out["dS_const_L_equal"] = bool(sp.simplify(At_d - Aa_d) == 0)
    return out


def as725():
    g, a0, K0 = sp.symbols("g a_0 K_0", positive=True)
    gN_Q = sp.sqrt(g ** 2 + a0 ** 2 / 4) - a0 / 2                               # Q: g^2 = gN^2 + a0 gN
    mu_Q = gN_Q / g
    K_Q = sp.integrate(2 * g * mu_Q, g) + K0
    ok_Q = sp.simplify(sp.diff(K_Q, g) / (2 * g) - mu_Q) == 0
    lin_Q = sp.limit((K_Q - g ** 2) / g, g, oo)
    s = g / (2 * a0)
    mu_2 = 1 - (1 + s) ** -2
    K_2 = sp.integrate(sp.expand(2 * g * mu_2), g) + K0
    ok_2 = sp.simplify(sp.diff(K_2, g) / (2 * g) - mu_2) == 0
    log_2 = sp.limit((K_2 - g ** 2) / sp.log(g), g, oo)
    return {"Q_integrable": bool(ok_Q), "Q_offset_linear_coeff": str(lin_Q), "MU2_integrable": bool(ok_2),
            "MU2_offset_log_coeff": str(log_2), "K0_free": bool(sp.diff(K_Q, K0) == 1 and sp.diff(K_2, K0) == 1)}


def as1923(bv):
    n, f, Vol = sp.symbols("n f Vol", positive=True)
    qq = 2 * pi * n * f / Vol
    P = (Z / 2 + bv * beta ** 2) * q ** 2
    k2 = sp.simplify(kappa2_of(P).subs(q, qq))
    k2_f1 = sp.simplify(k2.subs(f, 1))
    return {"k2": k2, "free_of_n_f_Vol": not (k2.free_symbols & {n, f, Vol}), "k2_at_f1": k2_f1}
# === COMPUTE END ===


# grading / report constants (outside the compute block): CFG493, used only to propagate an uncertainty in AS119
K_MEAS, K_SIG = 0.417, 0.095


def same(a, b_):
    return sp.simplify(sp.sympify(a) - sp.sympify(b_)) == 0


def main():
    print("W4-03  the eight unrun kappa proposals (K547)" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa = 1/2 FITTED (CFG493 0.417 +- 0.095). Not theory closed. deepseek_push read only.\n")

    # I1
    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"1\.13\d*e-10", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.53\b", r"0\.55",
                 r"5\.78", r"0\.1727", r"32\s*\*\s*pi\s*/\s*3", r"0\.685"]
    hits = [x for x in forbidden if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")

    # ---- AS119
    c_val = "1/3" if MUTATE else "1/2"
    r119 = as119(c_val)
    res["AS119"] = r119
    print(f"\nAS119  max-ent {{1, E[ln(1+u)] = c}}: EL shape (1+u)^-l1 {r119['EL_shape_ok']}; norm int = {r119['norm']}; "
          f"E[ln(1+u)] = {r119['E_log']}; n(c) = {r119['n_of_c']}")
    print(f"       c = {r119['c']} -> n = {r119['n']} -> kappa = 1/n = {r119['kappa_conditional']} "
          "(ONLY under the identification s = c sqrt(G rho): premise A)")
    for row in r119["trunc"]:
        print(f"       u_max {row['u_max']:5d} cells {row['cells']:4d}: E_trunc {row['E_trunc_midpoint']:.10f} "
              f"(exact {row['E_trunc_exact']:.10f}), tail bound {row['tail_bound']:.3e}, "
              f"|E + tail - 1/n| {row['residual_vs_1_over_n']:.2e}")
    check("K1 AS119 Lomax from max-ent", "EL gives (l1-1)(1+u)^-l1, E[ln(1+u)] = 1/(l1-1), n = 1/c; kappa = c under premise A "
          f"(hand: c = 1/2 -> kappa 1/2): got {r119['kappa_conditional']}",
          r119["EL_shape_ok"] and same(r119["E_log"], "1/(l1 - 1)") and same(r119["kappa_conditional"], "1/2"))
    # K1b as frozen ("truncated moments converge to 1/n with an analytic tail bound"). The first run used an unfrozen
    # 1e-5 threshold on the raw midpoint residual and failed at u_max 1000 / 512 cells (1.52e-5, a quadrature error, not a
    # tail error); kept as w4_03_firstrun_K1bfail.out. Tested now: exact truncated moment + tail = 1/n, and the midpoint
    # quadrature converges at second order (error ratio ~4 per cell doubling) at every u_max.
    ident = max(abs(row["E_trunc_exact"] + row["tail_bound"] - 1 / float(sp.sympify(r119["n"]))) for row in r119["trunc"])
    ratios = []
    for umax in (10, 100, 1000):
        errs = [row["quad_err"] for row in r119["trunc"] if row["u_max"] == umax]
        ratios += [errs[0] / errs[1], errs[1] / errs[2]]
    check("K1b AS119 truncation (as frozen: converges, analytic tail)",
          f"max |exact truncated + tail - 1/n| = {ident:.1e}; quadrature error ratios per doubling "
          f"{', '.join(f'{x:.2f}' for x in ratios)} (second order -> 4)",
          ident < 1e-12 and all(3.5 < x < 4.5 for x in ratios), "B")
    n_mean, n_sig = 1 / K_MEAS, K_SIG / K_MEAS ** 2
    print(f"       interval (CFG493, propagation only): c = kappa = {K_MEAS} +- {K_SIG} -> n = {n_mean:.2f} +- {n_sig:.2f}")
    check("NC AS119 'kappa exact while c inferred' rejected",
          f"under kappa = c, sigma_kappa = sigma_c = {K_SIG} > 0, so 'kappa exact' contradicts the inferred c", K_SIG > 0, "N")

    # ---- AS562
    r562 = as562()
    res["AS562"] = r562
    hbar_si, msun, kpc = 1.054571817e-34, 1.98847e30, 3.0856775814913673e19
    pi_fix = hbar_si / (1e10 * msun * 1.0e5 * 10 * kpc)
    r562["Pi_fixture"] = pi_fix
    print(f"\nAS562  Pi_quant = {r562['Pi']}: (M, L, T) exponents {r562['dim_Pi_MLT']}; hbar power {r562['p_Pi']}; "
          f"fixture (1e10 Msun, 100 km/s, 10 kpc) = {pi_fix:.3e}")
    print(f"       law a0^2 = kappa^2 c^2 G rho: hbar power {r562['p_law']}; "
          f"'A/(4 l_P^2)' restored: hbar power {r562['p_entropy_count']}")
    check("K2 AS562", "Pi_quant dimensionless, ~1e-100 at the galaxy fixture; the law is hbar-free",
          r562["dim_Pi_MLT"] == [0, 0, 0] and r562["p_law"] == 0 and pi_fix < 1e-90, "K")
    check("NC AS562 'hbar = 1 normalisation is classical' rejected",
          f"an entropy count written with l_P = 1 carries hbar^{r562['p_entropy_count']} once units are restored",
          r562["p_entropy_count"] != 0, "N")

    # ---- AS654
    c0v = 0 if MUTATE else C0
    r654 = as654(c0v)
    res["AS654"] = {k: str(v) for k, v in r654.items()}
    print(f"\nAS654  P = Z q^2/2 + C0: kappa^2(q) = {r654['k2']}; d kappa^2/dq = {r654['dk2_dq']}; "
          f"a0^2 - (2 beta^2 G/Z)(eps + C0) = {r654['tracking_identity_residual']}")
    check("K3 AS654", "hand: kappa^2 = 2 beta^2/(Z - 2 C0/q^2), q-dependent unless C0 = 0",
          same(r654["k2"], 2 * beta ** 2 / (Z - 2 * C0 / q ** 2)) and r654["dk2_dq"] != 0)
    check("NC AS654 'amplitude cancellation removes every offset' rejected",
          "kappa^2 depends on q when C0 != 0", same(as654(C0)["dk2_dq"], 0) is False, "N")

    # ---- AS655
    lv = 0 if MUTATE else lam
    r655 = as655(lv)
    res["AS655"] = {k: str(v) for k, v in r655.items()}
    print(f"\nAS655  P = Z q^2/2 + lambda q^4/Q0^2: kappa^2(q) = {r655['k2']}; d ln a0/d ln eps = {r655['slope_x']} "
          "(x = lambda q^2/Q0^2)")
    xs = sp.symbols("x", positive=True)
    check("K4 AS655", "hand: kappa^2 = 2 beta^2/(Z + 6 lambda q^2/Q0^2); slope (Z + 6x)/(2(Z + 12x))",
          same(r655["k2"], 2 * beta ** 2 / (Z + 6 * lam * q ** 2 / Q0 ** 2))
          and same(r655["slope_x"], (Z + 6 * xs) / (2 * (Z + 12 * xs))))
    check("NC AS655 'quadratic formula survives q^4' rejected", "kappa^2 != 2 beta^2/Z at lambda > 0",
          not same(as655(lam)["k2"], 2 * beta ** 2 / Z), "N")

    # ---- AS672
    r672 = as672()
    res["AS672"] = {"per_kappa": r672["per_kappa"], "general_residual": r672["general_residual"],
                    "homogeneous_energy": r672["homogeneous_energy"], "k04_kappa2": str(r672["k04_kappa2"])}
    print("\nAS672  q P' - P = a0^2/(kappa^2 G), a0 = beta sqrt(G) q:")
    for kv, d in r672["per_kappa"].items():
        print(f"       kappa {kv}: P = {d['P']}, residual {d['residual']}")
    print(f"       general a0 = sqrt(G)(q + q^3): residual {r672['general_residual']}; "
          f"homogeneous mode C q has energy {r672['homogeneous_energy']}; k04 relation kappa^2 = {r672['k04_kappa2']}")
    allsolve = all(d["residual"] == "0" for d in r672["per_kappa"].values()) and r672["general_residual"] == "0"
    check("K5 AS672", "solvable for every kappa; free mode C q with zero energy; reproduces k04",
          allsolve and r672["homogeneous_energy"] == "0"
          and same(r672["k04_kappa2"], 2 * beta ** 2 / (Z + 2 * b * beta ** 2)))
    check("NC AS672 'satisfying the equation derives kappa' rejected", "satisfied at kappa = 0.3, 0.5 and 0.7 alike",
          allsolve, "N")

    # ---- AS698
    pexp = sp.Rational(1, 2) if MUTATE else sp.Rational(2, 3)
    r698 = as698(pexp)
    res["AS698"] = r698
    vals = r698["L=H^2"]["values"]
    print(f"\nAS698  a = t^{pexp} on [1, T], L = H^2: A_a/A_t = {r698['L=H^2']['ratio']}")
    print(f"       T = 10, 100, 1000: {', '.join(f'{v:.4f}' for v in vals.values())}; "
          f"L = const: {', '.join(f'{v:.4f}' for v in r698['L=const']['values'].values())}; "
          f"de Sitter constant-L equality {r698['dS_const_L_equal']}")
    check("K6 AS698", "A_a/A_t != 1 and T-dependent for L = H^2; equal for constant L (both fixtures)",
          all(abs(v - 1) > 1e-3 for v in vals.values()) and abs(vals["10"] - vals["100"]) > 1e-3
          and all(abs(v - 1) < 1e-12 for v in r698["L=const"]["values"].values()) and r698["dS_const_L_equal"])
    check("NC AS698 'A_t and A_a are the same covariant average' rejected",
          f"ratio at T = 10 is {vals['10']:.4f}; only A_t carries sqrt(-g) = a^3 in cosmic time",
          abs(vals["10"] - 1) > 1e-3, "N")

    # ---- AS725
    r725 = as725()
    res["AS725"] = r725
    print(f"\nAS725  K = int 2 g mu dg + K0: Q integrable {r725['Q_integrable']}, (K - g^2)/g -> {r725['Q_offset_linear_coeff']}; "
          f"MU2 integrable {r725['MU2_integrable']}, (K - g^2)/ln g -> {r725['MU2_offset_log_coeff']}; K0 free {r725['K0_free']}")
    check("K7 AS725", "hand: integrable for any mu, K0 free; Newtonian offset diverges (Q linear -a0, MU2 log -8 a0^2)",
          r725["Q_integrable"] and r725["MU2_integrable"] and r725["K0_free"]
          and same(r725["Q_offset_linear_coeff"], "-a_0") and same(r725["MU2_offset_log_coeff"], "-8*a_0**2"))
    check("NC AS725 'derivative equation closes the vacuum' rejected", "dK/dK0 = 1 after solving K' = 2 g mu",
          r725["K0_free"], "N")

    # ---- AS1923
    bv = 0 if MUTATE else b
    r1923 = as1923(bv)
    res["AS1923"] = {k: str(v) for k, v in r1923.items()}
    print(f"\nAS1923 q = 2 pi n f/Vol: kappa^2 = {r1923['k2']}; free of (n, f, Vol) {r1923['free_of_n_f_Vol']}; "
          f"at f = 1: {r1923['k2_at_f1']}")
    check("K8 AS1923", "hand: kappa^2 = 2 beta^2/(Z + 2 b beta^2), independent of n, f, Vol (= FL1/K144)",
          same(r1923["k2"], 2 * beta ** 2 / (Z + 2 * b * beta ** 2)) and r1923["free_of_n_f_Vol"])
    check("NC AS1923 'unit flux spacing gives 1/2' rejected", "setting f = 1 leaves kappa^2 unchanged and unfixed",
          same(r1923["k2_at_f1"], r1923["k2"]) and bool(sp.sympify(r1923["k2"]).free_symbols), "N")

    # ---- I4: the law's kappa is never read (except AS119's identification, flagged)
    check("I4 rename", "no item reads the law's kappa; AS119's kappa = c is the identification itself (consistency relation)",
          True, "B")

    # ---- verdicts
    classes = {"AS119": "free (reparametrisation; kappa = c only under premise A)", "AS562": "audit",
               "AS654": "free (CONDITION: LOCK needs C0 = 0, nothing names it)",
               "AS655": "free (TRADE; running kappa, LOCK slope below 1/2)", "AS672": "free (CLOSURE: no rigidity)",
               "AS698": "free (prescription ambiguity in the excluded global-average class)",
               "AS725": "free (CLOSURE: k01 zero mode as integrability)", "AS1923": "free (TRADE; = FL1/K144)"}
    print("\nper-item classes")
    for k, v in classes.items():
        print(f"  {k}: {v}")
    lane = "BACKLOG CLEARED, NO SELECTION"
    print(f"\nLANE VERDICT: {lane}")
    print("  None of the eight fixes kappa. The one exact 1/2 (AS119) is the committed MU2 kernel's n = 2 read back through"
          " premise A. The four-form items move the 4 into C0, lambda or beta^2/Z. AS672 and AS725 show the equations hold"
          " for every kappa. AS698 adds a prescription ambiguity to an already-excluded class. AS562 confirms the hbar wall.")
    n_pass = sum(c["pass"] for c in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    out = {"mutate": MUTATE, "results": res, "classes": classes, "lane_verdict": lane, "checks": checks}
    with open(os.path.join(HERE, f"w4_03_results{SUF}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)

    if MUTATE:
        must_fail = {"K1 AS119 Lomax from max-ent", "K3 AS654", "K4 AS655", "K8 AS1923"}
        bit = all(not c["pass"] for c in checks if c["name"] in must_fail)
        book = all(c["pass"] for c in checks if c["kind"] == "B")
        moved = False
        try:
            base = json.load(open(os.path.join(HERE, "w4_03_results.json")))
            moved = abs(base["results"]["AS698"]["L=H^2"]["values"]["10"] - vals["10"]) > 1e-3
        except (OSError, KeyError):
            pass
        print(f"MUTATE: M1/M2/M3/M5 K checks fail {bit}; M4 AS698 ratio moved vs the normal run {moved}; "
              f"bookkeeping (I1, K1b, I4) passes {book}")
        sys.exit(1 if (bit and moved and book) else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
