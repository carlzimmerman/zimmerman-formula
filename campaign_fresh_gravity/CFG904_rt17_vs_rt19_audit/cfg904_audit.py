#!/usr/bin/env python3
r"""CFG904 -- RT-17 versus RT-19 (CFG894 prerequisite P4), recomputed in sympy.

RT-17 = reviews/mi_kernel_measure_from_desitter_2026.py: KMS at T_GH, identification I1 'w = x' -> Z = 2 pi,
        kappa = sqrt(2/(3 pi)) = 0.4607, presented as a prediction with no data.
RT-19 = reviews/mi_dsunruh_kernel_package_2026.py: dS-Unruh Delta-T construction -> a0 = 2 c H_Lambda (Z = 1/2);
        RT-17 withdrawn as 'wrong by 4 pi'.

Criteria: FROZEN_CRITERIA.md (committed alone before this script). Tests T1-T6, verdict classes V-A..V-E.
Law: a0 = kappa c sqrt(G rho_DE), H_Lambda^2 = 8 pi G rho_DE / 3, Z = c H_Lambda / a0 = sqrt(8 pi/3)/kappa.
kappa = 1/2 is FITTED. This lane derives nothing; it audits two records.

Normal run: exit 0 when every test was evaluated and every reproduction check held; 2 on an internal failure.
MUTATE=1: runs controls M1 (thermal 2 pi -> 4 pi), M2 (8 pi G -> 4 pi G), M3 (lambda 1 -> 1/2); exit 1 when all bite as
predicted (chain6 convention), 3 if any fails to bite. Outputs: cfg904_audit[_MUTATE].json (stdout -> .out).
"""
from __future__ import annotations

import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
STEM = "cfg904_audit" + ("_MUTATE" if MUTATE else "")

internal: list[tuple[bool, str]] = []   # reproduction / bookkeeping checks (must all hold)
tests: dict[str, dict] = {}             # T1..T6 outcomes (PASS/FAIL are findings, not errors)


def need(cond, msg):
    cond = bool(cond)
    internal.append((cond, msg))
    print(f"  [{'ok' if cond else 'INTERNAL FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 110 + f"\n  {t}\n" + "=" * 110)


def pi_weight(expr):
    """Exponent k of pi when expr = (pi-free factor) * pi^k; None if expr is not a monomial in pi."""
    e = sp.powsimp(sp.expand_power_base(sp.factor(sp.nsimplify(expr)), force=True), force=True)
    k = sp.Integer(0)
    for f in sp.Mul.make_args(e):
        b, ex = f.as_base_exp()
        if b == sp.pi:
            k += ex
        elif f.has(sp.pi):
            return None
    return k


# ---------------------------------------------------------------- symbols (no measured value enters any test)
om, H, hb, kB, c, G, rho, a, adS, x, u, lam = sp.symbols(
    "omega H_Lambda hbar k_B c G rho_DE a a_dS x u lambda", positive=True)
Zs = sp.Symbol("Z", positive=True)
TWO_PI = 2 * sp.pi            # the thermal 2 pi (T_GH and the Unruh prefactor)
EINSTEIN = 8 * sp.pi          # Friedmann coupling H^2 = EINSTEIN G rho / 3


def kappa_of_Z(Z, einstein=EINSTEIN):
    """kappa from Z via a0 = c H / Z = kappa c sqrt(G rho), H^2 = einstein G rho / 3 (derived, not typed)."""
    Hf = sp.sqrt(einstein * G * rho / 3)
    return sp.simplify((c * Hf / Z) / (c * sp.sqrt(G * rho)))


# ---------------------------------------------------------------- the RT-17 chain, step by step
def rt17_chain(two_pi=TWO_PI, einstein=EINSTEIN, lam_val=sp.Integer(1)):
    T_GH = hb * H / (two_pi * kB)                          # S1
    x_kms = sp.simplify(hb * om / (kB * T_GH))             # S2  KMS variable
    w_ker = sp.simplify(om * Zs / H)                       # S3  w = omega c / a0, a0 = c H / Z
    Zsol = sp.solve(sp.Eq(w_ker, lam_val * x_kms), Zs)     # S4  identification w = lambda x
    assert len(Zsol) == 1
    Z = sp.simplify(Zsol[0])
    kap = kappa_of_Z(Z, einstein)                          # S5
    return dict(T_GH=T_GH, x=x_kms, w=w_ker, Z=Z, kappa=kap)


def unruh_T(acc, two_pi=TWO_PI):
    return hb * acc / (two_pi * c * kB)


# ---------------------------------------------------------------- the RT-19 chain, from the temperatures
def rt19_chain(two_pi=TWO_PI, einstein=EINSTEIN):
    T_a = hb / (two_pi * c * kB) * sp.sqrt(a**2 + adS**2)  # dS-Unruh temperature
    T_0 = T_a.subs(a, 0)                                   # ambient (inertial) = Gibbons-Hawking
    mu_a = sp.simplify((T_a - T_0) / unruh_T(a, two_pi))   # Milgrom-1999 ansatz: inertia ~ excess temperature
    mu_u = sp.simplify(mu_a.subs(a, u * adS))              # u = a / a_dS
    mu1 = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)            # alpha = 1 kernel, x = g / a0
    trial = mu_u.subs(u, lam * x)
    s_trial = sp.series(trial, x, 0, 4).removeO()
    s_mu1 = sp.series(mu1, x, 0, 4).removeO()
    eq1 = sp.Eq(s_trial.coeff(x, 1), s_mu1.coeff(x, 1))
    lam_roots = sp.solve(eq1, lam)
    lam_star = lam_roots[0] if len(lam_roots) == 1 else None
    resid = sp.simplify(trial.subs(lam, lam_star) - mu1) if lam_star is not None else None
    Z = sp.Rational(1, 1) / lam_star if lam_star is not None else None   # a0 = lam* a_dS = lam* c H  ->  Z = 1/lam*
    return dict(T_a=T_a, mu_a=mu_a, mu_u=mu_u, mu1=mu1, lam_roots=lam_roots, lam_star=lam_star,
                resid=resid, Z=Z, kappa=kappa_of_Z(Z, einstein) if Z is not None else None)


def fnum(e, n=6):
    return None if e is None else round(float(e), n)


# ---------------------------------------------------------------- read the reruns of the two records (read-only)
def parse_rt17_rerun():
    path = os.path.join(HERE, "rt17_original_rerun.out")
    rows = {}
    with open(path) as fh:
        for line in fh:
            m = re.match(r"^  (I[1-4])  w = ", line)
            if m and len(line) >= 82 and re.match(r"^\s*-?\d", line[72:82]):
                rows[m.group(1)] = dict(Z=float(line[40:50]), kappa=float(line[72:82]))
    return rows


def parse_rt19_rerun():
    path = os.path.join(HERE, "rt19_original_rerun.out")
    txt = open(path).read()
    mz = re.search(r"i\.e\. Z = ([0-9/]+), kappa = .*? = ([0-9.]+)", txt)
    mr = re.search(r"they disagree by a factor (\S+) = ([0-9.]+)", txt)
    return dict(Z=sp.Rational(mz.group(1)), kappa=float(mz.group(2)), ratio=mr.group(1), ratio_f=float(mr.group(2)))


# ======================================================================================================== NORMAL
def normal_run():
    res: dict = {}
    banner("T1  RT-17 ARITHMETIC, step by step")
    ch = rt17_chain()
    print(f"  S1 T_GH            = {ch['T_GH']}")
    print(f"  S2 KMS variable x  = hbar omega/(k_B T_GH) = {ch['x']}      (hbar and k_B cancel: "
          f"{not ch['x'].has(hb) and not ch['x'].has(kB)})")
    print(f"  S3 kernel variable w = omega c/a0 = {ch['w']}   (a0 = c H_Lambda / Z)")
    print(f"  S4 identification w = lambda x  ->  Z = 2 pi lambda;  I1 (lambda = 1): Z = {ch['Z']}")
    print(f"  S5 kappa = sqrt(8 pi/3)/Z = {ch['kappa']} = {float(ch['kappa']):.6f}")
    need(not ch["x"].has(hb) and not ch["x"].has(kB), "hbar and k_B cancel inside x (declared in FROZEN_CRITERIA §3)")
    idents = {"I1": sp.Integer(1), "I2": sp.Rational(1, 2), "I3": sp.Integer(2), "I4": 1 / (2 * sp.pi)}
    menu = {k: rt17_chain(lam_val=v) for k, v in idents.items()}
    printed = parse_rt17_rerun()
    print(f"\n  {'id':<4}{'lambda':>10}{'Z (exact)':>12}{'kappa (exact)':>26}{'kappa':>10}{'RT-17 printed':>15}")
    t1_rows_ok = True
    for k, v in menu.items():
        pk = printed.get(k, {}).get("kappa")
        same = pk is not None and abs(float(v["kappa"]) - pk) < 6e-6 and abs(float(v["Z"]) - printed[k]["Z"]) < 6e-6
        t1_rows_ok &= same
        print(f"  {k:<4}{sp.sstr(idents[k]):>10}{sp.sstr(v['Z']):>12}{sp.sstr(v['kappa']):>26}"
              f"{float(v['kappa']):>10.5f}{(pk if pk is not None else float('nan')):>15.5f}  {'match' if same else 'MISMATCH'}")
    need(len(printed) == 4, "RT-17 rerun table parsed (4 identification rows)")
    t1 = (sp.simplify(ch["Z"] - 2 * sp.pi) == 0 and sp.simplify(ch["kappa"] - sp.sqrt(2 / (3 * sp.pi))) == 0
          and t1_rows_ok)
    tests["T1"] = dict(result="PASS" if t1 else "FAIL",
                       detail="I1 gives Z = 2 pi, kappa = sqrt(2/(3 pi)) exactly; I1-I4 reproduce RT-17's printed table"
                       if t1 else "arithmetic does not reproduce RT-17")
    print(f"  T1 {tests['T1']['result']}: {tests['T1']['detail']}")
    res["rt17"] = {k: dict(lam=sp.sstr(idents[k]), Z=sp.sstr(v["Z"]), kappa=sp.sstr(v["kappa"]),
                           kappa_f=fnum(v["kappa"])) for k, v in menu.items()}

    banner("T2  RT-17 DETERMINACY (KAPPA_CAMPAIGN_RULES §4)")
    Z_lam = rt17_chain(lam_val=lam)["Z"]
    print(f"  without a chosen lambda the chain gives Z(lambda) = {Z_lam}; dZ/dlambda = {sp.diff(Z_lam, lam)}")
    chain_eqs = [ch["T_GH"], ch["x"], ch["w"]]
    lam_in_chain = any(e.has(lam) for e in chain_eqs)
    print(f"  does any of S1-S3 contain or fix lambda?  {lam_in_chain}")
    kvals = [float(v["kappa"]) for v in menu.values()]
    spread = max(kvals) - min(kvals)
    W_LO, W_HI = 0.227, 0.607          # report-only window, KAPPA_CAMPAIGN_RULES §7 (rho_DE)
    width = W_HI - W_LO
    print(f"  kappa over RT-17's own I1-I4: {', '.join(f'{v:.4f}' for v in kvals)}; spread {spread:.3f} vs W_data "
          f"width {width:.3f}  (ratio of extremes {max(kvals)/min(kvals):.2f} = 4 pi: "
          f"{abs(max(kvals)/min(kvals) - float(4*sp.pi)) < 1e-9})")
    print("  RT-17's own text, line 95: 'The identification is an ADDED AXIOM ... not a theorem.'")
    inside = [k for k, v in menu.items() if W_LO <= float(v["kappa"]) <= W_HI]
    print(f"  report-only: menu entries inside today's W_data [{W_LO}, {W_HI}]: {inside}")
    t2 = lam_in_chain or spread < width
    tests["T2"] = dict(result="PASS" if t2 else "FAIL",
                       detail=("lambda fixed by the chain" if lam_in_chain else
                               f"no equation of S1-S3 fixes lambda; Z = 2 pi lambda is a one-parameter family; "
                               f"spread over I1-I4 {spread:.3f} > window width {width:.3f} -> MENU"),
                       menu_inside_window=inside)
    print(f"  T2 {tests['T2']['result']}: {tests['T2']['detail']}")

    banner("T3  RT-17 INTERNAL CONSISTENCY: is I1 'a0 is the de Sitter-Unruh scale'?")
    a0_I1 = c * H / ch["Z"]
    ratio_T = sp.simplify(unruh_T(a0_I1) / ch["T_GH"])
    a0_U = sp.solve(sp.Eq(unruh_T(a), ch["T_GH"]), a)[0]
    Z_U = sp.simplify(c * H / a0_U)
    print(f"  a0(I1) = {a0_I1};  T_U(a0(I1)) / T_GH = {ratio_T}")
    print(f"  the Unruh relation T_U(a0) = T_GH gives a0 = {a0_U}, Z = {Z_U}, kappa = {kappa_of_Z(Z_U)} = "
          f"{float(kappa_of_Z(Z_U)):.5f}  (= RT-17's own I4: {sp.simplify(Z_U - menu['I4']['Z']) == 0})")
    print(f"  equivalently: I1 sets a0/c = k_B T_GH/hbar (thermal angular frequency) = {sp.simplify(kB*ch['T_GH']/hb)},"
          f" while the Unruh rate of T_GH is 2 pi k_B T_GH/hbar = {sp.simplify(2*sp.pi*kB*ch['T_GH']/hb)}")
    t3 = sp.simplify(ratio_T - 1) == 0
    tests["T3"] = dict(result="PASS" if t3 else "FAIL",
                       detail=("I1 is Unruh-consistent" if t3 else
                               f"T_U(a0_I1)/T_GH = {sp.sstr(ratio_T)}: I1 makes a0 the Unruh acceleration of "
                               f"T_GH/(2 pi), not of T_GH; the Unruh-consistent reading is Z = {sp.sstr(Z_U)} "
                               f"(RT-17's I4, kappa {float(kappa_of_Z(Z_U)):.4f})"),
                       ratio=sp.sstr(ratio_T), Z_unruh=sp.sstr(Z_U))
    print(f"  T3 {tests['T3']['result']}: {tests['T3']['detail']}")

    banner("T4  RT-19 CHAIN, recomputed from the temperatures (scale solved, not assumed)")
    r19 = rt19_chain()
    print(f"  mu(a) = [T(a) - T(0)]/T_U(a) = {r19['mu_a']}")
    print(f"  mu_dS(u) = {r19['mu_u']}   (contains pi: {r19['mu_u'].has(sp.pi)}, hbar: {r19['mu_u'].has(hb)}, "
          f"k_B: {r19['mu_u'].has(kB)})")
    lim_hi = sp.limit(r19["mu_u"], u, sp.oo)
    slope0 = sp.limit(r19["mu_u"] / u, u, 0)
    print(f"  limits: u -> oo: {lim_hi};  mu_dS/u at u -> 0: {slope0}")
    print(f"  series match mu_dS(lambda x) = mu_1(x) at O(x): lambda roots = {r19['lam_roots']}")
    print(f"  full-function residual at lambda* = {r19['lam_star']}: {r19['resid']}")
    s3 = sp.series(r19["mu_u"].subs(u, r19["lam_star"] * x) - r19["mu1"], x, 0, 8).removeO()
    print(f"  residual series to O(x^7): {sp.simplify(s3)}")
    printed19 = parse_rt19_rerun()
    print(f"  => a0 = lambda* a_dS = {r19['lam_star']} c H_Lambda, Z = {r19['Z']}, kappa = {r19['kappa']} = "
          f"{float(r19['kappa']):.5f}   (RT-19 printed Z = {printed19['Z']}, kappa = {printed19['kappa']})")
    ratio_D5 = sp.simplify(ch["Z"] / r19["Z"])
    print(f"  D5: Z_RT17 / Z_RT19 = {ratio_D5}   (RT-19 printed '{printed19['ratio']}')")
    need(printed19["Z"] == r19["Z"] and abs(printed19["kappa"] - float(r19["kappa"])) < 6e-6,
         "RT-19 rerun's Z and kappa reproduced")
    need(sp.simplify(ratio_D5 - sp.sympify(printed19["ratio"])) == 0,
         "RT-19 rerun's D5 ratio reproduced")
    # report-only: deep limit for any kernel normalised mu -> x, and the alpha = 2 kernel
    mu2 = x / sp.sqrt(1 + x**2)
    s_mu2 = sp.series(mu2, x, 0, 4).removeO()
    s_tr = sp.series(r19["mu_u"].subs(u, lam * x), x, 0, 4).removeO()
    lam2_o1 = sp.solve(sp.Eq(s_tr.coeff(x, 1), s_mu2.coeff(x, 1)), lam)
    o3_ok = [sp.simplify(s_tr.coeff(x, 3).subs(lam, l_) - s_mu2.coeff(x, 3)) == 0 for l_ in lam2_o1]
    print(f"  report-only: deep limit mu_dS -> u/{1/slope0} fixes a0 = {1/slope0} a_dS for ANY kernel with mu -> x "
          f"(kernel-independent)")
    print(f"  report-only: alpha = 2 kernel: O(x) gives lambda = {lam2_o1}, O(x^3) consistent: {o3_ok} "
          f"-> no full-function identity; only the deep limit ties the scale")
    t4 = (r19["lam_star"] is not None and len(r19["lam_roots"]) == 1 and r19["resid"] == 0
          and sp.simplify(r19["Z"] - sp.Rational(1, 2)) == 0 and lim_hi == 1)
    tests["T4"] = dict(result="PASS" if t4 else "FAIL",
                       detail=(f"mu_dS(2x) == mu_1(x) identically at the unique scale lambda* = 2 -> a0 = 2 c H_Lambda "
                               f"(Z = 1/2, kappa = 2 sqrt(8 pi/3) = {float(r19['kappa']):.4f}); thermal 2 pi, hbar, k_B "
                               f"cancel in mu" if t4 else "RT-19 chain does not reproduce"),
                       alpha2_full_identity=any(o3_ok))
    print(f"  T4 {tests['T4']['result']}: {tests['T4']['detail']}")
    res["rt19"] = dict(mu_dS=sp.sstr(r19["mu_u"]), lam_star=sp.sstr(r19["lam_star"]), Z=sp.sstr(r19["Z"]),
                       kappa=sp.sstr(r19["kappa"]), kappa_f=fnum(r19["kappa"]), D5_ratio=sp.sstr(ratio_D5))

    banner("T5  IS THE 4 pi ONE ERROR IN RT-17's CHAIN?")
    # c1: S1 against the Gibbons-Hawking form T = hbar kappa_s/(2 pi c k_B), surface gravity kappa_s = c H for dS
    T_GH_ref = hb * (c * H) / (2 * sp.pi * c * kB)
    c1_err = sp.simplify(ch["T_GH"] - T_GH_ref) != 0
    Z_c1 = ch["Z"]
    # c2: S4 replaced by the Unruh-consistent reading T_U(a0) = T_GH
    Z_c2 = Z_U
    # c3: S2 replaced by the Unruh variable x_U = omega c / a_U(T_GH), a_U(T) = 2 pi c k_B T / hbar
    a_U = 2 * sp.pi * c * kB * ch["T_GH"] / hb
    x_U = sp.simplify(om * c / a_U)
    Z_c3 = sp.simplify(sp.solve(sp.Eq(ch["w"], x_U), Zs)[0])
    # c4: S5 against Friedmann, derived independently
    k_c4 = sp.simplify((c * H / ch["Z"]) / (c * sp.sqrt(G * rho))).subs(H, sp.sqrt(8 * sp.pi * G * rho / 3))
    c4_err = sp.simplify(k_c4 - ch["kappa"]) != 0
    c2_err = sp.simplify(ratio_T - 1) != 0                # S4 disagrees with the Unruh reading RT-17 invokes (T3)
    c3_err = sp.simplify(Z_c3 - ch["Z"]) != 0             # S2's thermal variable differs from the Unruh variable
    corrections = {"c1 (S1 T_GH vs Gibbons-Hawking)": (c1_err, Z_c1),
                   "c2 (S4 -> Unruh-consistent T_U(a0) = T_GH)": (c2_err, Z_c2),
                   "c3 (S2 -> Unruh variable omega c/a_U(T_GH))": (c3_err, Z_c3),
                   "c4 (S5 vs Friedmann)": (c4_err, ch["Z"])}
    for k, (is_err, Zc) in corrections.items():
        print(f"  {k:<48} step in error: {str(is_err):<5}  corrected Z = {sp.sstr(Zc):<6} kappa = "
              f"{float(kappa_of_Z(Zc)):.4f}   reaches Z = 1/2: {sp.simplify(Zc - sp.Rational(1, 2)) == 0}")
    hit = any(sp.simplify(Zc - sp.Rational(1, 2)) == 0 for _, Zc in corrections.values())
    f_2pi = sp.simplify(ch["Z"] / Z_c2)
    f_2 = sp.simplify(Z_c2 / r19["Z"])
    print(f"\n  factorisation: Z_RT17/Z_RT19 = {ratio_D5} = (Z_RT17/Z_Unruh) x (Z_Unruh/Z_RT19) = {f_2pi} x {f_2}")
    print(f"    {f_2pi}: carried by S4 -- I1 equates a0/c with k_B T_GH/hbar instead of the Unruh rate 2 pi k_B T_GH/hbar")
    print(f"    {f_2}  : carried by RT-19's Delta-T construction -- its deep-limit slope mu_dS -> u/2 (a0 = 2 a_dS); "
          f"no step of RT-17 contains it")
    need(sp.simplify(f_2pi * f_2 - ratio_D5) == 0, "factorisation multiplies back to the D5 ratio")
    tests["T5"] = dict(result="PASS" if hit else "FAIL",
                       detail=("a single corrected step gives Z = 1/2" if hit else
                               f"no single corrected step gives Z = 1/2; 4 pi = {f_2pi} (RT-17's S4, an error against "
                               f"the Unruh reading it invokes) x {f_2} (the Delta-T deep-limit slope, a different "
                               f"construction, not an error in RT-17)"),
                       factor_S4=sp.sstr(f_2pi), factor_construction=sp.sstr(f_2))
    print(f"  T5 {tests['T5']['result']}: {tests['T5']['detail']}")

    banner("T6  IDENTITY CHECKS")
    # I4 rename test: the law's kappa only enters comparison lines
    kl = sp.Symbol("kappa_law", positive=True)
    t6 = {}
    outs = {}
    for kv in (sp.Rational(1, 2), sp.Rational(2, 5)):
        Z_law = sp.sqrt(8 * sp.pi / 3) / kv                      # report-only comparison, built from the law's kappa
        o17 = rt17_chain()["kappa"]
        o19 = rt19_chain()["kappa"]
        outs[str(kv)] = dict(rt17=o17, rt19=o19, cmp17=sp.simplify(o17 / kv), cmp19=sp.simplify(o19 / kv),
                             rt19_eq_Zlaw=sp.simplify(o19 - Z_law) == 0)
        print(f"  I4 law kappa = {kv}: RT-17 kappa = {sp.sstr(o17)}, RT-19 kappa = {sp.sstr(o19)}; ratios to law "
              f"{float(o17/kv):.4f}, {float(o19/kv):.4f}; RT-19's kappa equals the law's Z: "
              f"{outs[str(kv)]['rt19_eq_Zlaw']}")
    i4 = (outs["1/2"]["rt17"] == outs["2/5"]["rt17"] and outs["1/2"]["rt19"] == outs["2/5"]["rt19"]
          and outs["1/2"]["cmp17"] != outs["2/5"]["cmp17"])
    print(f"  I4 {'PASS' if i4 else 'FAIL'}: outputs do not move with the law's kappa (both chains are predictions of "
          f"their own axioms, not consistency relations); only the comparison lines move. Note: 'RT-19's kappa = Z' "
          f"holds only at law kappa = 1/2 (2 sqrt(8pi/3) = sqrt(8pi/3)/kappa_law iff kappa_law = 1/2) -- a coincidence")
    t6["I4_rename"] = i4
    # convention rename: hbar -> h/2pi, omega -> 2 pi nu, k_B -> 1 (kernel variable carried consistently)
    h_, nu = sp.symbols("h nu", positive=True)
    T_GH_r = (h_ / (2 * sp.pi)) * H / (2 * sp.pi)               # k_B = 1
    x_r = sp.simplify(h_ * nu / T_GH_r)                          # h nu / T == hbar omega / (k_B T)
    w_r = sp.simplify(2 * sp.pi * nu * Zs / H)                   # omega c / a0 with omega = 2 pi nu
    Z_r = sp.simplify(sp.solve(sp.Eq(w_r, x_r), Zs)[0])
    T_a_r = (h_ / (2 * sp.pi)) / (2 * sp.pi * c) * sp.sqrt(a**2 + adS**2)
    mu_r = sp.simplify((T_a_r - T_a_r.subs(a, 0)) / ((h_ / (2 * sp.pi)) * a / (2 * sp.pi * c)))
    conv = sp.simplify(Z_r - ch["Z"]) == 0 and sp.simplify(mu_r - r19["mu_a"]) == 0
    print(f"  convention rename: RT-17 Z = {Z_r} (was {ch['Z']}); RT-19 mu = {mu_r} (unchanged: "
          f"{sp.simplify(mu_r - r19['mu_a']) == 0})  -> {'PASS' if conv else 'FAIL'} (no convention leak; the 2 pi of "
          f"RT-17 is an identification choice, not a units artefact)")
    t6["convention_rename"] = conv
    # I3 scaling
    l1, l2, l3 = sp.symbols("l_G l_rho l_c", positive=True)
    sc_ok = True
    for nm, Zv in (("RT-17", ch["Z"]), ("RT-19", r19["Z"])):
        a0e = c * sp.sqrt(8 * sp.pi * G * rho / 3) / Zv
        a0s = a0e.subs({G: l1 * G, rho: l2 * rho, c: l3 * c}, simultaneous=True)
        r = sp.simplify(a0s / a0e)
        k_s = sp.simplify(a0s / (l3 * c * sp.sqrt(l1 * G * l2 * rho)))
        ok_ = sp.simplify(r - l3 * sp.sqrt(l1 * l2)) == 0 and sp.simplify(k_s - kappa_of_Z(Zv)) == 0
        sc_ok &= ok_
        print(f"  I3 scaling {nm}: a0 -> {r} a0, kappa invariant: {ok_}")
    t6["I3_scaling"] = sc_ok
    # I8 pi-weight tracking
    print("  I8 pi-weight (exponent k in rational-ish x pi^k) of every intermediate:")
    pw17 = [("S1 T_GH", ch["T_GH"]), ("S2 x/omega", ch["x"] / om), ("S4 Z", ch["Z"]), ("S5 kappa", ch["kappa"]),
            ("kappa^2", ch["kappa"] ** 2)]
    pw19 = [("T(a) prefactor", r19["T_a"] / sp.sqrt(a**2 + adS**2)), ("T_U(a)/a", unruh_T(a) / a),
            ("mu_dS", r19["mu_u"]), ("lambda*", r19["lam_star"]), ("Z", r19["Z"]), ("kappa", r19["kappa"]),
            ("kappa^2", r19["kappa"] ** 2)]
    pw_out = {}
    dims = {hb: 1, kB: 1, c: 1, H: 1, om: 1}          # dimensional symbols carry no pi
    for tag, seq in (("RT-17", pw17), ("RT-19", pw19)):
        row = []
        for nm, e in seq:
            if e.free_symbols & {u, a, adS}:           # a function of u (mu_dS): only ask whether pi appears
                k_ = "0 (pi-free function)" if not e.has(sp.pi) else "pi inside a function"
            else:
                k_ = pi_weight(sp.simplify(e.subs(dims)))
            row.append(f"{nm}: {k_}")
            pw_out[f"{tag} {nm}"] = str(k_)
        print(f"    {tag}: " + "; ".join(row))
    k2_17 = pi_weight(ch["kappa"] ** 2)
    k2_19 = pi_weight(r19["kappa"] ** 2)
    odd = lambda k_: k_ is not None and k_.is_integer and int(k_) % 2 != 0
    i8 = odd(k2_17) and odd(k2_19)
    dZ = pi_weight(ratio_D5)
    print(f"  I8 {'PASS' if i8 else 'FAIL'}: kappa^2 pi-weights {k2_17} (RT-17) and {k2_19} (RT-19), both odd as "
          f"declared (a-and-H class; exact 1/2 impossible). Z_RT17/Z_RT19 carries pi^{dZ}: it enters at RT-17's S1 "
          f"(T_GH's 1/2pi, kept by S2's x) and cancels in RT-19's ratio mu.")
    t6["I8_pi_weight"] = i8
    # I1 grep of this script for the forbidden constants (tokens assembled at run time)
    forbidden = ["9.36" + "e-11", "9.3603" + "e-11", "1.13" + "e-10", "1.1312" + "e-10", "1.2" + "e-10",
                 "5.78" + "88", "0.17" + "27"]
    src = open(os.path.abspath(__file__)).read()
    hits = [f for f in forbidden if f in src]
    t6["I1_grep"] = not hits
    print(f"  I1 grep: forbidden constants in this script: {hits or 'none'} -> {'PASS' if not hits else 'FAIL'}")
    tests["T6"] = dict(result="PASS" if all(t6.values()) else "FAIL", detail=t6, pi_weights=pw_out)

    banner("VERDICT (frozen table, FROZEN_CRITERIA §6)")
    T = {k: tests[k]["result"] == "PASS" for k in ("T1", "T2", "T3", "T4", "T5", "T6")}
    rt17_ok = T["T1"] and T["T2"] and T["T3"]
    if not T["T6"]:
        verdict = "VOID (identity check failed)"
    elif rt17_ok:
        verdict = "V-A RT-17 STANDS"
    elif T["T4"] and T["T5"]:
        verdict = "V-B RT-19 STANDS IN FULL"
    elif T["T4"] and not T["T5"]:
        verdict = "V-C WITHDRAWAL STANDS, 4pi ATTRIBUTION DOES NOT"
    elif not T["T4"]:
        verdict = "V-D BOTH FAIL"
    else:
        verdict = "V-E INCONSISTENT"
    for k in ("T1", "T2", "T3", "T4", "T5", "T6"):
        print(f"  {k}: {tests[k]['result']}")
    print(f"\n  VERDICT: {verdict}")
    res["verdict"] = verdict
    return res


# ======================================================================================================== MUTATE
def mutate_run():
    res: dict = {}
    bites = {}
    base17, base19 = rt17_chain(), rt19_chain()
    banner("M1  thermal 2 pi -> 4 pi in T_GH and in the Unruh prefactor")
    m17, m19 = rt17_chain(two_pi=4 * sp.pi), rt19_chain(two_pi=4 * sp.pi)
    a0_U_m = sp.solve(sp.Eq(unruh_T(a, 4 * sp.pi), m17["T_GH"]), a)[0]
    print(f"  RT-17 Z: {base17['Z']} -> {m17['Z']}  (kappa {float(base17['kappa']):.4f} -> {float(m17['kappa']):.4f})")
    print(f"  RT-19 mu_dS: {m19['mu_u']} (unchanged: {sp.simplify(m19['mu_u'] - base19['mu_u']) == 0}); "
          f"Z: {base19['Z']} -> {m19['Z']}")
    print(f"  Unruh-consistent a0 under M1: {a0_U_m} (unchanged: {sp.simplify(a0_U_m - c*H) == 0})")
    bites["M1_rt17_moves_to_4pi"] = sp.simplify(m17["Z"] - 4 * sp.pi) == 0
    bites["M1_rt19_fixed"] = (sp.simplify(m19["mu_u"] - base19["mu_u"]) == 0
                              and sp.simplify(m19["Z"] - base19["Z"]) == 0)
    banner("M2  Einstein coupling 8 pi G -> 4 pi G")
    e17, e19 = rt17_chain(einstein=4 * sp.pi), rt19_chain(einstein=4 * sp.pi)
    print(f"  Z: RT-17 {e17['Z']}, RT-19 {e19['Z']} (unchanged); kappa ratios "
          f"{sp.simplify(e17['kappa']/base17['kappa'])}, {sp.simplify(e19['kappa']/base19['kappa'])}")
    bites["M2_Z_fixed_kappa_over_sqrt2"] = (
        sp.simplify(e17["Z"] - base17["Z"]) == 0 and sp.simplify(e19["Z"] - base19["Z"]) == 0
        and sp.simplify(e17["kappa"] / base17["kappa"] - 1 / sp.sqrt(2)) == 0
        and sp.simplify(e19["kappa"] / base19["kappa"] - 1 / sp.sqrt(2)) == 0)
    banner("M3  identification lambda = 1 -> 1/2 (RT-17's I2)")
    l17 = rt17_chain(lam_val=sp.Rational(1, 2))
    print(f"  RT-17 Z -> {l17['Z']}, kappa -> {l17['kappa']} = {float(l17['kappa']):.4f}")
    bites["M3_rt17_to_pi"] = sp.simplify(l17["Z"] - sp.pi) == 0
    banner("MUTATE RESULT")
    for k, v in bites.items():
        print(f"  {k}: {'bites as predicted' if v else 'DID NOT BITE'}")
    res["bites"] = bites
    res["all_bite"] = all(bites.values())
    return res


if __name__ == "__main__":
    print("CFG904 -- RT-17 vs RT-19 audit" + ("  [MUTATE]" if MUTATE else ""))
    out = mutate_run() if MUTATE else normal_run()
    out["internal_checks"] = [dict(ok=o, msg=m) for o, m in internal]
    out["tests"] = tests
    with open(os.path.join(HERE, STEM + ".json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    bad = [m for o, m in internal if not o]
    if MUTATE:
        code = 1 if out["all_bite"] and not bad else 3
        print(f"\n  exit {code} ({'every control bites as predicted' if code == 1 else 'a control failed to bite'})")
        sys.exit(code)
    if bad:
        print("\n  INTERNAL FAILURES:\n    - " + "\n    - ".join(bad))
        sys.exit(2)
    print(f"\n  {len(internal)}/{len(internal)} internal checks held; exit 0.")
    sys.exit(0)
