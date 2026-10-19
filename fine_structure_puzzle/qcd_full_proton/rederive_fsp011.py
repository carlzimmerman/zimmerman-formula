#!/usr/bin/env python3
"""FSP-011 independent re-derivation of the critical step.

Written and run as a separate pass that does NOT import compute_fsp011.py and
does not reuse its closed-form tables or its Born kernel.  Only after its own
results are produced does it (optionally) open the author output and compare.

R1  Contraction-class charge weights by explicit enumeration of current
    placements on the uud / udd valence lines and on flavoured sea loops, with
    SYMBOLIC charges (sympy).  Tests: p-n vanishes identically for same-loop and
    two-loop sea classes; every p-n weight is divisible by (Q_u - Q_d);
    isoscalar weights are symmetric under Q_u <-> Q_d.
R2  Isospin (Wigner-Eckart) route: J_ud = (Q_u+Q_d)/2 S + (Q_u-Q_d)/2 V3.
    Three independent reduced amplitudes (SS, {S,V3}, V3V3); p-n sees only the
    {S,V3} one.  Cross-check of R1 in a different basis.
R3  SU(3) colour algebra behind heavy-quark (charm) decoupling: a quark loop
    with one photon and two gluons vanishes (Tr[T^a,T^b]=0 after Furry), while
    the d^{abc} three-gluon structure survives.
R4  Born normalisation by a different numerical route: full 2-D (Q, angle)
    integration of T1^B, T2^B for p and n (no use of the 1-D kernel B(z)),
    plus the point-Dirac sharp-cutoff constant from the same 2-D code.
R5  Path dependence: universal scale shifts cancel in R_u = A_u/M^3 - 3 A M_u/M^4;
    a quark-mass path change does not.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad

Qu, Qd, Qs, Qc = sp.symbols("Q_u Q_d Q_s Q_c")
QSYM = {"u": Qu, "d": Qd, "s": Qs, "c": Qc}
PHYS = {Qu: sp.Rational(2, 3), Qd: sp.Rational(-1, 3), Qs: sp.Rational(-1, 3), Qc: sp.Rational(2, 3)}


# ------------------------------------------------------------------ R1
def enumerate_weights(valence, majority):
    """Sum of Q(site1)*Q(site2) over all placements of two currents, grouped by
    the isospin-invariant amplitude class.  Sites: valence line index, or a sea
    loop (label A or B) of flavour g.  Isospin symmetry identifies a u and a d
    sea loop (same propagator), so light loops are labelled 'l' in the class
    name but keep their own symbolic charge."""
    sea_flav = ["u", "d", "s", "c"]
    sites = [("v", i) for i in range(3)] + [("loop", L, g) for L in ("A", "B") for g in sea_flav]
    classes = {}
    def role(i):
        return "maj" if valence[i] == majority else "min"
    def lbl(g):
        return "l" if g in ("u", "d") else g
    for s1, s2 in itertools.product(sites, repeat=2):
        q1 = QSYM[valence[s1[1]]] if s1[0] == "v" else QSYM[s1[2]]
        q2 = QSYM[valence[s2[1]]] if s2[0] == "v" else QSYM[s2[2]]
        if s1[0] == "v" and s2[0] == "v":
            if s1[1] == s2[1]:
                key = f"X_{role(s1[1])}"
            else:
                key = "Y_" + "".join(sorted([role(s1[1]), role(s2[1])]))
        elif s1[0] == "v" or s2[0] == "v":
            v, l = (s1, s2) if s1[0] == "v" else (s2, s1)
            if l[1] != "A":           # one-current loop: count it once (label A)
                continue
            key = f"Z_{role(v[1])}_{lbl(l[2])}"
        else:
            if s1[1] == s2[1]:
                if s1[2] != s2[2] or s1[1] != "A":
                    continue          # a single closed loop has one flavour
                key = f"W_{lbl(s1[2])}"
            else:
                if s1[1] != "A":      # ordered pair (A,B) represents both orderings
                    continue
                key = "V_" + "".join(sorted([lbl(s1[2]), lbl(s2[2])]))
        classes[key] = sp.expand(classes.get(key, 0) + q1 * q2)
    return classes


def r1():
    wp = enumerate_weights("uud", "u")
    wn = enumerate_weights("ddu", "d")
    keys = sorted(set(wp) | set(wn))
    out, tests = {}, {}
    for k in keys:
        p, n = wp.get(k, 0), wn.get(k, 0)
        diff = sp.factor(sp.expand(p - n))
        iso = sp.expand((p + n) / 2)
        sym_ok = sp.simplify(iso - iso.subs({Qu: Qd, Qd: Qu}, simultaneous=True)) == 0
        div_ok = sp.simplify(sp.cancel(diff / (Qu - Qd))).is_polynomial(Qu, Qd, Qs, Qc) if diff != 0 else True
        out[k] = {"p": str(p), "n": str(n), "p-n": str(diff), "(p+n)/2": str(iso),
                  "p_phys": str(p.subs(PHYS)) if p != 0 else "0",
                  "n_phys": str(n.subs(PHYS)) if n != 0 else "0",
                  "p-n_phys": str(sp.nsimplify(diff.subs(PHYS))) if diff != 0 else "0",
                  "(p+n)/2_phys": str(iso.subs(PHYS))}
        tests[k] = {"isoscalar_symmetric_under_u<->d": bool(sym_ok), "p-n_divisible_by_(Qu-Qd)": bool(div_ok)}
    sea_cancel = all(sp.expand(wp[k] - wn[k]) == 0 for k in keys if k.startswith(("W_", "V_")))
    ymm = sp.expand(wp["Y_majmin"] - wn["Y_majmin"]) == 0
    return out, tests, sea_cancel, ymm


# ------------------------------------------------------------------ R2
def r2():
    a, b, c, e_s, e_c, f_s, f_c, g_ss, g_cc, g_sc = sp.symbols("a b c e_s e_c f_s f_c g_ss g_cc g_sc")
    # J = alpha0 S + beta1 V3 + Qs O_s + Qc O_c ; nucleon matrix elements:
    # <SS>=a, <{S,V3}>=b tau3, <V3V3>=c (rank-2 part zero for I=1/2),
    # <{S,O_g}>=e_g, <{V3,O_g}>=f_g tau3, <O_g O_h>=g_gh (isoscalar)
    alpha0 = (Qu + Qd) / 2
    beta1 = (Qu - Qd) / 2
    def m(tau3):
        return sp.expand(alpha0 ** 2 * a + alpha0 * beta1 * b * tau3 + beta1 ** 2 * c
                         + alpha0 * (Qs * e_s + Qc * e_c) + beta1 * tau3 * (Qs * f_s + Qc * f_c)
                         + Qs ** 2 * g_ss + Qc ** 2 * g_cc + Qs * Qc * g_sc)
    p, n = m(1), m(-1)
    diff = sp.factor(sp.expand(p - n))
    iso = sp.expand((p + n) / 2)
    seen_in_diff = sorted(str(s) for s in diff.free_symbols if s not in (Qu, Qd, Qs, Qc))
    seen_in_iso = sorted(str(s) for s in iso.free_symbols if s not in (Qu, Qd, Qs, Qc))
    return {"p-n": str(diff), "(p+n)/2": str(iso),
            "reduced_amplitudes_in_p-n": seen_in_diff,
            "reduced_amplitudes_in_isoscalar": seen_in_iso,
            "isoscalar_needs_amplitudes_absent_from_p-n": sorted(set(seen_in_iso) - set(seen_in_diff))}


# ------------------------------------------------------------------ R3
def gell_mann():
    l = np.zeros((8, 3, 3), dtype=complex)
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1], l[1][1, 0] = -1j, 1j
    l[2][0, 0], l[2][1, 1] = 1, -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2], l[4][2, 0] = -1j, 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2], l[6][2, 1] = -1j, 1j
    l[7] = np.diag([1, 1, -2]) / math.sqrt(3)
    return l / 2


def r3():
    T = gell_mann()
    comm_tr = max(abs(np.trace(T[a] @ T[b] - T[b] @ T[a])) for a in range(8) for b in range(8))
    sym_tr = max(abs(np.trace(T[a] @ T[b]) - 0.5 * (a == b)) for a in range(8) for b in range(8))
    d = np.zeros((8, 8, 8))
    for a, b, cc in itertools.product(range(8), repeat=3):
        d[a, b, cc] = 2 * np.real(np.trace((T[a] @ T[b] + T[b] @ T[a]) @ T[cc]))
    dsq = float(np.sum(d * d))
    return {"max|Tr[T^a,T^b]|": float(comm_tr), "max|Tr(T^aT^b)-delta/2|": float(sym_tr),
            "sum_abc d_abc^2": dsq, "expected_sum_d2_(N^2-4)(N^2-1)/N": 40.0 / 3.0,
            "photon+2gluon loop (Furry: Tr T^aT^b - Tr T^bT^a)": "vanishes" if comm_tr < 1e-12 else "nonzero",
            "photon+3gluon d-symbol coupling": "survives" if dsq > 1 else "vanishes"}


# ------------------------------------------------------------------ R4
def r4(inp):
    kin = inp["nucleon_kinematics"]
    c = inp["form_factor_parametrisations"]["BBBA05"]
    def rat(a, bb, t):
        return sum(x * t ** k for k, x in enumerate(a)) / (1 + sum(x * t ** (k + 1) for k, x in enumerate(bb)))
    def ff(nuc, t):
        if nuc == "p":
            return rat(c["GEp"]["a"], c["GEp"]["b"], t), kin["mu_p"] * rat(c["GMp_over_mu_p"]["a"], c["GMp_over_mu_p"]["b"], t)
        return rat(c["GEn"]["a"], c["GEn"]["b"], t), kin["mu_n"] * rat(c["GMn_over_mu_n"]["a"], c["GMn_over_mu_n"]["b"], t)
    # Cottingham, re-derived: M_u = 1/(32 pi^3 M) int dQ^2 int_-1^1 dx sqrt(1-x^2) [-3T1 + (1-x^2) T2]
    # with Q^2 = 4 M^2 z^2 => M_u/M = 1/(4 pi^3) int z dz int dx sqrt(1-x^2)[...]
    def inner(z, GE, GM, pole_only=False):
        t = z * z
        F1 = (GE + t * GM) / (1 + t)
        A = (GE * GE + t * GM * GM) / (1 + t)
        def g(x):
            T1 = 2 * (t * GM * GM / (t + x * x) - (0.0 if pole_only else F1 * F1))
            T2 = 2 * A / (t + x * x)
            return math.sqrt(max(0.0, 1 - x * x)) * (-3 * T1 + (1 - x * x) * T2)
        v, _ = quad(g, 0.0, 1.0, points=[min(z, 0.9)], limit=300, epsabs=1e-13, epsrel=1e-11)
        return 2 * v
    res = {}
    for nuc, MeV in (("p", kin["M_p_MeV"]), ("n", kin["M_n_MeV"])):
        M = MeV / 1000.0
        for pole_only in (False, True):
            def f(z):
                GE, GM = ff(nuc, z * z)
                return z * inner(z, GE, GM, pole_only)
            tot = 0.0
            edges = [0, 0.02, 0.1, 0.3, 0.7, 1.5, 4, 12, 60]
            for lo, hi in zip(edges[:-1], edges[1:]):
                tot += quad(f, lo, hi, limit=200, epsabs=1e-13, epsrel=1e-10)[0]
            tot += quad(f, 60, math.inf, limit=200)[0]
            key = f"{nuc}_{'poleonly' if pole_only else 'fullBorn'}_MeV_per_e2"
            res[key] = tot / (4 * math.pi ** 3) * MeV
    # point Dirac with sharp cutoff, same 2-D code: F1=1, F2=0 => GE=GM=1
    def dirac(Lm):
        Z = Lm / 2
        f = lambda z: z * inner(z, 1.0, 1.0)
        edges = [0, 0.1, 1, 10, 100, 1000, Z]
        edges = [e for e in edges if e <= Z]
        if edges[-1] != Z:
            edges.append(Z)
        tot = sum(quad(f, lo, hi, limit=300, epsabs=1e-12, epsrel=1e-11)[0] for lo, hi in zip(edges[:-1], edges[1:]))
        Mu_over_m = tot / (4 * math.pi ** 3)
        return 16 * math.pi ** 2 * Mu_over_m - 3 * math.log(Lm ** 2)
    res["dirac_constant_Lambda_over_m_1e3"] = dirac(1e3)
    res["dirac_constant_Lambda_over_m_1e4"] = dirac(1e4)
    return res


# ------------------------------------------------------------------ R5
def r5():
    A, M, Au, Mu, cg, u = sp.symbols("A M A_u M_u c u")
    Ru = Au / M ** 3 - 3 * A * Mu / M ** 4
    # universal scale shift at O(u): A -> A(1+3 c u), M -> M(1+c u)
    Au2, Mu2 = Au + 3 * cg * A, Mu + cg * M
    Ru2 = Au2 / M ** 3 - 3 * A * Mu2 / M ** 4
    scale_invariant = sp.simplify(Ru2 - Ru) == 0
    # quark-mass path change: A_u -> A_u + k a_m, M_u -> M_u + k sigma (a_m = m dA/dm, sigma = m dM/dm)
    k, am, sg = sp.symbols("k a_m sigma")
    Ru3 = (Au + k * am) / M ** 3 - 3 * A * (Mu + k * sg) / M ** 4
    shift = sp.simplify(Ru3 - Ru)
    return {"universal_scale_shift_changes_R_u": not scale_invariant,
            "quark_mass_path_change_shift_in_R_u": str(shift),
            "equals_k_times_m_dR/dm": str(sp.simplify(shift - k * (am / M ** 3 - 3 * A * sg / M ** 4))) == "0"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--author-result", default=None,
                    help="opened only AFTER the independent results are computed")
    args = ap.parse_args()
    raw = open(args.inputs, "rb").read()
    inp = json.loads(raw)
    w, wtests, sea_cancel, ymm = r1()
    out = {"script": "rederive_fsp011.py", "inputs_sha256": hashlib.sha256(raw).hexdigest(),
           "R1_enumerated_charge_weights": w, "R1_tests": wtests,
           "R1_sea_same_loop_and_two_loop_cancel_in_p-n": sea_cancel,
           "R1_Y_majmin_cancels_in_p-n": ymm,
           "R2_isospin_route": r2(), "R3_colour_algebra": r3(), "R4_born_2D": r4(inp), "R5_path": r5()}
    checks = [
        ("R1 sea same-loop/two-loop vanish identically in p-n", sea_cancel),
        ("R1 every p-n weight divisible by (Qu-Qd); isoscalar symmetric", all(all(v.values()) for v in wtests.values())),
        ("R2 isoscalar needs reduced amplitudes absent from p-n", len(out["R2_isospin_route"]["isoscalar_needs_amplitudes_absent_from_p-n"]) > 0),
        ("R3 photon+2gluon quark loop vanishes, d-symbol survives",
         out["R3_colour_algebra"]["photon+2gluon loop (Furry: Tr T^aT^b - Tr T^bT^a)"] == "vanishes"
         and abs(out["R3_colour_algebra"]["sum_abc d_abc^2"] - 40.0 / 3.0) < 1e-9),
        ("R4 point-Dirac constant 3/2 from 2-D code", abs(out["R4_born_2D"]["dirac_constant_Lambda_over_m_1e4"] - 1.5) < 1e-5),
        ("R5 scale shift cancels in R_u; mass path does not", (not out["R5_path"]["universal_scale_shift_changes_R_u"]) and out["R5_path"]["equals_k_times_m_dR/dm"]),
    ]
    out["checks_independent"] = [{"name": n, "pass": bool(p)} for n, p in checks]
    # ---- comparison with the author, only now
    if args.author_result:
        au = json.load(open(args.author_result))
        cmp = {}
        # The two passes normalise amplitudes differently (author: one total
        # amplitude per class; enumeration: one amplitude per placement), so a
        # class-dependent multiplicity factor is expected.  Convention-free
        # agreement = the SAME factor for proton and neutron, and identical
        # vanishing pattern in p-n.
        for k, v in au["D_charge_weights_author"].items():
            # label normalisation only: two-loop classes are named by their
            # flavour pair in sorted order here (V_cl == author's V_lc)
            kk = "V_" + "".join(sorted(k[2:])) if k.startswith("V_") else k
            mine = w.get(kk)
            if mine is None:
                cmp[k] = "class absent in enumeration"
                continue
            mp_, mn_ = sp.nsimplify(mine["p_phys"]), sp.nsimplify(mine["n_phys"])
            ap_, an_ = sp.nsimplify(v["p"]), sp.nsimplify(v["n"])
            if ap_ == 0 or an_ == 0:
                ok = (mp_ == 0) == (ap_ == 0) and (mn_ == 0) == (an_ == 0)
                factor = "n/a"
            else:
                ok = sp.simplify(mp_ / ap_ - mn_ / an_) == 0
                factor = str(sp.simplify(mp_ / ap_))
            zero_pattern = (sp.nsimplify(mine["p-n_phys"]) == 0) == (sp.nsimplify(v["p-n"]) == 0)
            cmp[k] = "agree (multiplicity factor %s)" % factor if (ok and zero_pattern) else f"DISAGREE mine={mine} author={v}"
        bb = au["B_born"]["BBBA05"]
        cmp["Born_p_fullBorn_rel_diff"] = abs(out["R4_born_2D"]["p_fullBorn_MeV_per_e2"] / bb["p"]["MuB_MeV_per_e2"] - 1)
        cmp["Born_n_fullBorn_rel_diff"] = abs(out["R4_born_2D"]["n_fullBorn_MeV_per_e2"] / bb["n"]["MuB_MeV_per_e2"] - 1)
        cmp["Born_p_poleonly_rel_diff"] = abs(out["R4_born_2D"]["p_poleonly_MeV_per_e2"] / bb["proton_poleonly_MeV_per_e2"] - 1)
        out["comparison_with_author"] = cmp
        out["checks_comparison"] = [
            {"name": "charge weights agree class by class (up to a p/n-common multiplicity convention)",
             "pass": all(str(v).startswith("agree") for k, v in cmp.items() if not k.startswith("Born"))},
            {"name": "Born p,n agree to 1e-6 relative", "pass": max(cmp["Born_p_fullBorn_rel_diff"], cmp["Born_n_fullBorn_rel_diff"], cmp["Born_p_poleonly_rel_diff"]) < 1e-6},
        ]
    allc = out["checks_independent"] + out.get("checks_comparison", [])
    out["all_checks_pass"] = all(c["pass"] for c in allc)
    json.dump(out, open(args.output, "w"), indent=1)
    print(json.dumps({"all_checks_pass": out["all_checks_pass"], "checks": [(c["name"], c["pass"]) for c in allc]}, indent=1))
    return 0 if out["all_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
