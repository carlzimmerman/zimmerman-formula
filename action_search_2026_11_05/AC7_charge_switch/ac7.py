"""AC7: AC2 with the stiffness switched on the khronon charge (candidate AC2q). Criteria FROZEN_CRITERIA.md (b0d44a6952).
Run from the repository root: PYTHONHASHSEED=0 python3 action_search_2026_11_05/AC7_charge_switch/ac7.py [--mutate-a]
Kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, itertools
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
MUT_A = "--mutate-a" in sys.argv
TAG = "_MUTATE_A" if MUT_A else ""
checks, res, lines = [], {"mutate_a": MUT_A}, []


def log(s=""):
    print(s, flush=True); lines.append(s)


def check(cid, ok, value, thr):
    checks.append({"id": cid, "pass": bool(ok), "value": value, "threshold": thr})
    log(f"  [{'PASS' if ok else 'FAIL'}] {cid}: {value} (line: {thr})")


# ---------------------------------------------------------------- Q1: FRW longitudinal P with the new term
def q1():
    log("Q1: FRW, longitudinal polarization integrated out (unitary gauge, X = s^2/(2N^2) exactly)")
    k, K, g, s, al, P = sp.symbols("k K gamma s alpha P", positive=True)
    # one Fourier mode: P_L = P cos(kz), lapse alpha sin(kz); D.P = -k P sin, A = d(alpha) = k alpha cos; averages 1/2
    dX = -s ** 2 * al                                   # delta X at linear order (exact X = s^2/(2N^2))
    avg = lambda c2, s2: (c2 + s2) / 2
    PA = k * P * al / 2                                  # <P.A>
    W = K * P ** 2 / 4                                   # <K |P|^2 / 2>, quadratic W
    DD = k ** 2 * P ** 2 / 2                             # <(D.P)^2>
    XD = (-s ** 2 * al) * (-k * P) / 2                   # <dX * D.P> = <(-s^2 al sin)(-k P sin)>
    L_new = PA - W - g / 2 * (DD + 4 * XD)               # -(g/2)[(D.P)^2 + 4 X D.P] at quadratic order (D.P bar = 0)
    L_old = PA - W - g / 2 * DD
    def integrate(L):
        Ps = sp.solve(sp.diff(L, P), P)[0]
        return sp.simplify(L.subs(P, Ps))
    eo, en = integrate(L_old), integrate(L_new)
    factor = sp.factor(sp.simplify(en / eo))
    log(f"  integrated: old {eo}; new {en}; ratio {factor}")
    pred_plus = (1 + 2 * g * s ** 2) ** 2
    pred_minus = (1 - 2 * g * s ** 2) ** 2
    which = "(1+2 gamma s^2)^2" if sp.simplify(factor - pred_plus) == 0 else ("(1-2 gamma s^2)^2" if sp.simplify(factor - pred_minus) == 0 else "other")
    log(f"  frozen prediction was (1+2 gamma s^2)^2; derived factor is {which}")
    res["Q1_factor"] = str(factor); res["Q1_factor_form"] = which
    check("Q1a", which != "other" and sp.simplify(factor.subs(s, 0) - 1) == 0,
          f"factor {factor} (a perfect square, = 1 at s = 0); frozen prediction sign {'matches' if which.startswith('(1+') else 'differs'}",
          "a non-negative perfect-square factor multiplying AC2's cY term; known answer factor(s=0) = 1")
    # AC2's FRW block with cY -> f cY: kinetic eps + f x^2/(1+l^2 x^2), gradient eps x^2 (units H = Mpl = 1)
    rows, ok = [], True
    for gs2 in (0.0, 1e-11, 0.1, 1.0):
        f = float(factor.subs({s: 1, g: gs2})) if gs2 else 1.0
        for E, ell, x in itertools.product((0.01, 0.5, 2.0), (0.001, 1.0, 100.0), (0.1, 1.0, 10.0, 1000.0)):
            with mp.workdps(40):
                E_, l_, x_, f_ = map(mp.mpf, (E, ell, x, f))
                kin = E_ + f_ * x_ ** 2 / (1 + l_ ** 2 * x_ ** 2)
                grad = E_ * x_ ** 2
                w2 = lambda xx: E_ * xx ** 2 / (E_ + f_ * xx ** 2 / (1 + l_ ** 2 * xx ** 2))
                cph = mp.sqrt(w2(x_)) / x_
                cgr = mp.diff(lambda xx: mp.sqrt(w2(xx)), x_)
                good = kin > 0 and grad > 0 and 0 < cph <= 1 + mp.mpf("1e-30") and 0 < cgr <= 1 + mp.mpf("1e-30")
                if gs2 <= 1e-11:
                    ok &= bool(good)
                rows.append({"gamma_s2": gs2, "eps": E, "ell": ell, "x": x, "f": float(f_), "kin": float(kin),
                             "c_phase": float(cph), "c_group": float(cgr), "healthy": bool(good)})
    # known answer: f = 1 reproduces AC2's analytic dispersion E x^2 (1+l^2x^2)/[E+(1+E l^2)x^2]
    E, l, x, f = sp.symbols("E ell x f", positive=True)
    mine = E * x ** 2 / (E + f * x ** 2 / (1 + l ** 2 * x ** 2))
    ka = sp.simplify(mine.subs(f, 1) - E * x ** 2 * (1 + l ** 2 * x ** 2) / (E + (1 + E * l ** 2) * x ** 2))
    check("Q1b", ok and ka == 0, f"{sum(r['healthy'] for r in rows if r['gamma_s2'] <= 1e-11)}/72 physical fixtures healthy; "
          f"stress (0.1, 1): {sum(r['healthy'] for r in rows if r['gamma_s2'] > 1e-11)}/72; known answer residual {ka}",
          "all physical fixtures: kinetic, gradient > 0, phase and group speeds in (0, 1]; AC2 identity")
    res["Q1_rows"] = rows


# ---------------------------------------------------------------- Q2: galaxies, PN WKB
def q2():
    log("Q2: galaxies, PN frozen-background WKB with the charge switch (on-region) and without stiffness (off-region)")
    t, x, y, z = X = sp.symbols("t x y z", real=True)
    K, s, M, D0 = sp.symbols("K s M D_0", positive=True)
    gL = -sp.Symbol("gamma_L", positive=True) if MUT_A else sp.Symbol("gamma_L", positive=True)
    gsym = sp.Symbol("gamma_L", positive=True)
    k, om, th, ML, MT = sp.symbols("k omega theta M_L M_T", positive=True)
    d0 = sp.Symbol("d0", real=True)                     # background divergence, either sign
    dphi, dsig, dXi = sp.symbols("dphi dsigma dXi"); dP = sp.symbols("dP0:3"); dPv = sp.Matrix(dP)
    kh = sp.Matrix([0, 0, 1]); Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    W2 = sp.Symbol("W2")

    def hand(gam, Hm, d0_):
        dC2 = s ** 2 * (-2 * sp.I * om * dsig - 2 * dphi)
        dD = sp.I * k * kh.dot(dPv)
        Peq = sp.I * k * kh * dXi - Hm * dPv - gam * k ** 2 * kh * (kh.dot(dPv)) + sp.I * gam * k * kh * dC2
        drt = (1 - 2 * gam * s ** 2) * dD + s ** 2 * (1 - 2 * gam * d0_) * (-sp.I * om * dsig - 2 * dphi)
        rx0 = d0_ + s ** 2 * (1 - 2 * gam * d0_)
        ce = -sp.I * om * drt + rx0 * k ** 2 * dsig
        pois = -k ** 2 * dphi - K * ((1 - 2 * gam * s ** 2) * dD + s ** 2 * (1 - 2 * gam * d0_) * (-2 * sp.I * om * dsig - 3 * dphi))
        be = dXi - (dphi + sp.I * om * dsig)
        Mx = sp.linear_eq_to_matrix([pois, ce, be] + list(Peq), [dphi, dsig, dXi] + list(dP))[0]
        return Mx

    def roots(Mx):
        det = sp.factor(sp.simplify(Mx.det()))
        return sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2), det

    # validation: automatic linearisation, isotropic quadratic W, background P = P0 + (d0/3) r, phi = sigma = 0
    eps_ = sp.Symbol("epsilon")
    phi = sp.Function("phi")(*X); sig = sp.Function("sigma")(*X); Pf = [sp.Function(f"P{i}")(*X) for i in range(3)]
    xs = (x, y, z)
    grad = lambda f: [sp.diff(f, v) for v in xs]; div = lambda F: sum(sp.diff(F[i], xs[i]) for i in range(3))
    Xi = phi - sp.diff(sig, t) + sum(d ** 2 for d in grad(sig)) / 2
    C2 = s ** 2 * ((1 + sp.diff(sig, t)) ** 2 / (1 + phi) ** 2 - sum(d ** 2 for d in grad(sig)))
    L = (-sum(d ** 2 for d in grad(phi)) / (2 * K) + sum(Pf[i] * sp.diff(Xi, xs[i]) for i in range(3))
         - K * M * sum(p ** 2 for p in Pf) / 2 - gsym / 2 * ((div(Pf) + C2) ** 2 - C2 ** 2) + C2 / 2)
    eqs = euler_equations(L, [phi, sig] + Pf, X)
    ph = sp.exp(sp.I * (k * z - om * t))
    P0 = sp.symbols("Pb0:3")
    sub = {phi: eps_ * dphi * ph, sig: eps_ * dsig * ph}
    for i in range(3):
        sub[Pf[i]] = P0[i] + d0 / 3 * xs[i] + eps_ * dP[i] * ph
    lin = []
    for e in eqs:
        ex = e.lhs.subs(sub).doit()
        ex = sp.diff(ex, eps_).subs(eps_, 0)
        ex = sp.simplify((ex / ph).subs({x: 0, y: 0, z: 0, t: 0}))
        lin.append(sp.expand(ex))
    Ma = sp.linear_eq_to_matrix(lin, [dphi, dsig] + list(dP))[0]
    ra, _ = roots(Ma)
    Mh = hand(gsym, K * M * sp.eye(3), d0)
    # eliminate dXi from the hand system (Bernoulli) to compare roots
    rh, _ = roots(Mh)
    diff_ = [min((sp.simplify(a - b) for b in rh), key=lambda v: 0 if v == 0 else 1) for a in ra] if len(ra) == len(rh) else ["count"]
    check("Q2a", len(ra) == len(rh) and all(v == 0 for v in diff_),
          f"automatic linearisation roots {len(ra)}, hand roots {len(rh)}, residuals {diff_}", "identical dispersion")
    res["Q2_validation"] = {"auto": [str(r) for r in ra], "hand": [str(r) for r in rh]}

    # graded: anisotropic, on-region
    Hm = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    rr, _ = roots(hand(gL, Hm, d0))
    uv = [sp.simplify(sp.limit(r / k ** 2, k, sp.oo)) for r in rr]
    log(f"  on-region UV limits omega^2/k^2: {uv}")
    res["Q2_uv_on"] = [str(u) for u in uv]
    # sign scan of the UV limit on the on-region: rho_q = d0 + s^2 >= 0, |2 gamma d0| < 1 (exact rational grid)
    neg = []
    grid_s2 = [sp.Rational(1, 10), 1, 10]
    grid_g = [sp.Rational(1, 10 ** 11), sp.Rational(1, 100), sp.Rational(1, 4)]
    for s2v, gv in itertools.product(grid_s2, grid_g):
        for fr in [-1, sp.Rational(-999, 1000), sp.Rational(-1, 2), 0, 1, 10]:
            d0v = fr * s2v                                    # rho_q = d0 + s^2 >= 0 for fr >= -1
            if abs(2 * gv * d0v) >= 1:
                continue
            for u in uv:
                val = sp.nsimplify(u.subs({s: sp.sqrt(s2v), gsym: gv, d0: d0v, K: 1}))
                if val.free_symbols:
                    val = val.subs({ML: 4, MT: 2, th: sp.Rational(1, 3)})
                if sp.N(val, 30) < 0:
                    neg.append({"s2": str(s2v), "gamma": str(gv), "d0": str(d0v), "uv": str(sp.N(val, 12))})
    res["Q2_on_negative_cases"] = neg
    check("Q2b", not neg, f"{len(neg)} on-region grid points with negative UV omega^2/k^2", "0 (no Gamma ~ k where the switch is on)")
    # off-region: no P stiffness; the +2 gamma X^2 term is the clock's own k-essence piece
    Moff = hand(0, Hm, d0)
    ro, _ = roots(Moff)
    uvo = [sp.simplify(sp.limit(r, k, sp.oo)) for r in ro]
    check("Q2c", all(sp.limit(r / k ** 2, k, sp.oo) == 0 for r in ro) and all(u.is_finite is not False for u in uvo),
          f"off-region omega^2(k->inf) = {uvo}", "finite, k-independent (bounded rate)")
    res["Q2_uv_off"] = [str(u) for u in uvo]


def q3_q4():
    log("Q3/Q4: sizes of 2 gamma D.P and of the static shift")
    G, c, PC, MSUN = 6.67430e-11, 2.99792458e8, 3.0856775814913673e16, 1.98847e30
    MSUN_PC3 = MSUN / PC ** 3
    K = 4 * 3.141592653589793 * G
    DP = {"Solar System screened min": 0.045, "H4 S2 LMC-MW median": 1.1e-4, "H4 S4 cluster pair": 1.5e-6,
          "dense core 1e3 Msun/pc^3 (stress)": 1e3}
    rho_de = {"canonical": 5.8424e-27, "alt": 8.5328e-27}        # AC6 values, kg/m^3
    out, ok = {}, True
    for Ls in (21.7, 22.9, 90.0):
        gam_over_c2 = K * (Ls * PC) ** 2 / 2 / c ** 2               # gamma times a density, dimensionless after /c^2
        for nm, v in DP.items():
            val = 2 * gam_over_c2 * v * MSUN_PC3
            out[f"Lstar={Ls}|{nm}"] = val
            if "stress" not in nm:
                ok &= val < 1e-3
    check("Q3", ok, f"max |2 gamma D.P| over record values {max(v for k_, v in out.items() if 'stress' not in k_):.2e} "
          f"(stress 1e3 Msun/pc^3 at 90 pc: {out['Lstar=90.0|dense core 1e3 Msun/pc^3 (stress)']:.2e})", "< 1e-3")
    res["Q3"] = out
    shift = {foot: 2 * 2 * r / (0.045 * MSUN_PC3) for foot, r in rho_de.items()}
    check("Q4", all(v < 1e-3 for v in shift.values()), f"static relative shift bound 2 phidot^2/D.P at the Solar-System value: {shift}",
          "< 1e-3 (Cassini margin 4.8e7)")
    res["Q4"] = shift


def main():
    log(f"AC7 (mutate-a = {MUT_A}); kappa = 1/2 FITTED; not theory closed")
    if not MUT_A:
        q1()
    q2()
    if not MUT_A:
        q3_q4()
    res["checks"] = checks
    res["label"] = ("AC2q SURVIVES Q1-Q4" if all(c["pass"] for c in checks) else "see failed checks") if not MUT_A else "mutate-a run"
    log(f"LABEL: {res['label']}")
    json.dump(res, open(os.path.join(HERE, f"ac7_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"ac7{TAG}.out"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
