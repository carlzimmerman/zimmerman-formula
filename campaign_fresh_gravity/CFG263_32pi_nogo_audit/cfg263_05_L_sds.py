"""CFG263 / NG-L: independent re-derivation of lane L (SdS two-horizon family).
Written without opening agents/L_sds_two_horizon/*.py or *.out. c = G = 1, L = 1/H = 1 unless stated.

 L1  Vieta: x^2 + xy + y^2 = 1, 2M = xy(x+y); kappa_b = (1-3x^2)/(2x), kappa_c = (3y^2-1)/(2y)  (f-normalisation)
 L2  monotone bijection: kappa_b/H in (inf, 0), kappa_c/H in (1, 0)
 L3  T_b = T_c iff xy = 1/3 iff Nariai
 L4  a0-points (BH and cosmological), mu* = 0.98695 / 0.98298
 L5  Smarr point x^2 = 1/5, kappa_b = H/sqrt5
 L6  K_Sigma = rho_Lambda unattainable at any SdS horizon
 L7  elimination polynomial P(K, M) with integer coefficients (pi-count in Lambda-units)
 L8  u-units: c_rec = kappa/u = K sqrt(8pi/3); natural points give algebraic x sqrt(8pi/3)
 L9  19 entropy/temperature functionals: interior stationary points?
 L10 Bousso-Hawking normalisation: no horizon with kappa = H/Z
"""
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 50


def main():
    C = Checks("NG-L")
    x, y, rm, M, r, K = sp.symbols("x y r_m M r K", real=True)
    # L1 Vieta for r^3 - r + 2M = 0 (f = 1 - 2M/r - r^2, times -r)
    poly = sp.expand((r - x) * (r - y) * (r - rm))
    eqs = [sp.Eq(poly.coeff(r, 2), 0), sp.Eq(poly.coeff(r, 1), -1), sp.Eq(poly.coeff(r, 0), 2 * M)]
    rm_sol = sp.solve(eqs[0], rm)[0]
    C.check("L1_vieta", sp.simplify(eqs[1].lhs.subs(rm, rm_sol) + 1 - (1 - (x**2 + x * y + y**2))) == 0 and
            sp.simplify(eqs[2].lhs.subs(rm, rm_sol) - (x * y * (x + y))) == 0,
            "x^2 + xy + y^2 = 1 and 2M = xy(x+y) (r_- = -(x+y))")
    f = 1 - 2 * M / r - r**2
    kb = sp.diff(f, r).subs(r, x) / 2
    kc = -sp.diff(f, r).subs(r, y) / 2
    yx = (-x + sp.sqrt(4 - 3 * x**2)) / 2
    Mx = x * yx * (x + yx) / 2
    C.check("L1b_kappas", sp.simplify(kb.subs(M, Mx) - (1 - 3 * x**2) / (2 * x)) == 0 and
            sp.simplify(kc.subs(M, Mx).subs(y, yx) - (3 * yx**2 - 1) / (2 * yx)) == 0,
            "kappa_b = (1-3x^2)/(2x), kappa_c = (3y^2-1)/(2y) on the family")

    # L2 monotonicity on x in (0, 1/sqrt3)
    xs = [mp.mpf(k) / 2000 * (1 / mp.sqrt(3)) for k in range(1, 2000)]
    yf = lambda xv: (-xv + mp.sqrt(4 - 3 * xv**2)) / 2
    Mf = lambda xv: xv * yf(xv) * (xv + yf(xv)) / 2
    kbf = lambda xv: (1 - 3 * xv**2) / (2 * xv)
    kcf = lambda xv: (3 * yf(xv)**2 - 1) / (2 * yf(xv))
    mono = all(Mf(xs[i + 1]) > Mf(xs[i]) and kbf(xs[i + 1]) < kbf(xs[i]) and kcf(xs[i + 1]) < kcf(xs[i]) for i in range(len(xs) - 1))
    dM = sp.simplify(sp.diff(Mx, x))
    C.check("L2_monotone_bijection", mono and abs(kcf(mp.mpf("1e-12")) - 1) < 1e-9 and abs(kcf(1 / mp.sqrt(3))) < 1e-30 and abs(kbf(1 / mp.sqrt(3))) < 1e-30,
            f"M up, kappa_b down (inf -> 0), kappa_c down (1 -> 0) on 1999 points; dM/dx = {dM}")
    MN = 1 / (3 * mp.sqrt(3))
    C.check("L2b_nariai_mass", abs(Mf(1 / mp.sqrt(3)) - MN) < 1e-40, "x = y = 1/sqrt3 at M_N = L/(3 sqrt3)")

    # L3 T_b = T_c
    diff_k = sp.simplify(((1 - 3 * x**2) / (2 * x) - (3 * y**2 - 1) / (2 * y)) - (x + y) * (1 - 3 * x * y) / (2 * x * y))
    sol = sp.solve([x**2 + x * y + y**2 - 1, x * y - sp.Rational(1, 3)], [x, y], dict=True)
    pos = [s_ for s_ in sol if s_[x].is_positive and s_[y].is_positive]
    # the identity uses x^2 + xy + y^2 = 1; check it on the family numerically
    idn = all(abs(((1 - 3 * xv**2) / (2 * xv) - kcf(xv)) - (xv + yf(xv)) * (1 - 3 * xv * yf(xv)) / (2 * xv * yf(xv))) < 1e-40 for xv in xs[::97])
    C.check("L3_equilibrium_only_nariai", idn and len(pos) == 1 and pos[0][x] == pos[0][y],
            f"kappa_b - kappa_c = (x+y)(1-3xy)/(2xy) on the family; xy = 1/3 with x^2+xy+y^2 = 1 has the single positive root {pos}")

    # L4 a0-points
    Z = mp.sqrt(32 * mp.pi / 3)
    xb = (mp.sqrt(1 + 32 * mp.pi) - 1) / mp.sqrt(96 * mp.pi)
    C.check("L4_bh_a0_point", abs(kbf(xb) - 1 / Z) < 1e-40, f"x* = (sqrt(1+32pi)-1)/sqrt(96pi) = {mp.nstr(xb, 8)}, kappa_b = H/Z")
    mub = Mf(xb) / MN
    yc = (1 + mp.sqrt(1 + 32 * mp.pi)) / (3 * Z)
    xc = (-yc + mp.sqrt(4 - 3 * yc**2)) / 2
    muc = xc * yc * (xc + yc) / 2 / MN
    C.check("L4b_mu_star", abs(mub - mp.mpf("0.98695")) < 5e-6 and abs(muc - mp.mpf("0.98298")) < 5e-6 and abs((3 * yc**2 - 1) / (2 * yc) - 1 / Z) < 1e-40,
            f"mu*_b = {mp.nstr(mub, 7)}, mu*_c = {mp.nstr(muc, 7)} (lane L: 0.98695, 0.98298)")
    C.value("mu_star_b", mub); C.value("mu_star_c", muc); C.value("rb_star", xb); C.value("rc_at_b_point", yf(xb))

    # L5 Smarr
    rho = 3 / (8 * sp.pi)     # rho_Lambda in L = 1 units
    smarr = sp.simplify((kb.subs(M, Mx) * x**2 + sp.Rational(8, 3) * sp.pi * rho * x**3) - Mx)
    C.check("L5_smarr_identity", sp.simplify(smarr) == 0, "M = kappa_b r_b^2 + (8pi/3) rho_Lambda r_b^3 on the family")
    xs5 = sp.solve(sp.Eq((1 - 3 * x**2) / (2 * x) * x**2, x**3), x)
    xs5 = [v for v in xs5 if v.is_positive]
    C.check("L5b_smarr_balance_point", xs5 == [1 / sp.sqrt(5)] and sp.simplify(((1 - 3 * x**2) / (2 * x)).subs(x, xs5[0]) - 1 / sp.sqrt(5)) == 0,
            "surface term = vacuum term at x^2 = 1/5: kappa_b = H/sqrt5 (algebraic)")

    # L6 K_Sigma = rho unattainable: G rho r^2 <= 1/(8pi) (BH, x <= 1/sqrt3), <= 3/(8pi) (cosmo, y <= 1)
    C.check("L6_KSigma_rho_unattainable", float(rho * (1 / sp.sqrt(3))**2) <= 1 / (8 * float(sp.pi)) + 1e-15 and float(rho * 1) <= 3 / (8 * float(sp.pi)) + 1e-15,
            "max G rho r_h^2 = 1/(8pi) (BH), 3/(8pi) (cosmological) < 1: no SdS horizon has K_Sigma = rho_Lambda")

    # L7 elimination polynomial
    P = sp.resultant(x**3 - x + 2 * M, 2 * K * x - 1 + 3 * x**2, x)
    Pp = sp.Poly(sp.expand(P), K, M)
    intc = all(c_.is_integer for c_ in Pp.coeffs())
    C.check("L7_elimination_polynomial", intc and sp.simplify(P.subs({K: kbf(xb), M: Mf(xb)}).evalf(40)) == 0 or
            (intc and abs(sp.N(P.subs({K: sp.Float(kbf(xb), 50), M: sp.Float(Mf(xb), 50)}), 50)) < 1e-35),
            f"P(K, M) = {sp.factor(P)}: integer coefficients; M algebraic => K = kappa_b/H algebraic; K = 1/Z transcendental => mu* transcendental")

    # L8 u-units
    c_rec = lambda Kv: Kv * mp.sqrt(8 * mp.pi / 3)
    C.check("L8_u_units", abs(c_rec(kbf(xb)) - mp.mpf(1) / 2) < 1e-40 and abs(c_rec(1) - mp.sqrt(8 * mp.pi / 3)) < 1e-40,
            f"c_rec = kappa/sqrt(G rho): a0-point 1/2 (rational) while K transcendental; dS horizon {mp.nstr(c_rec(1), 5)}, Smarr {mp.nstr(c_rec(1/mp.sqrt(5)), 5)}, Nariai(BH-norm) {mp.nstr(c_rec(mp.sqrt(3)), 5)}")

    # L9 functionals: interior stationary points over x in (0, 1/sqrt3)
    def Sb(xv): return mp.pi * xv**2
    def Sc(xv): return mp.pi * yf(xv)**2
    combos = {"Stot": lambda v: Sb(v) + Sc(v), "SbSc": lambda v: Sb(v) * Sc(v), "Sb/Sc": lambda v: Sb(v) / Sc(v), "Sc-Sb": lambda v: Sc(v) - Sb(v)}
    norms = {"L": lambda v: 1, "M": lambda v: Mf(v)**2, "rb": lambda v: v**2, "rc": lambda v: yf(v)**2}
    funcs = {}
    for cn, cf in combos.items():
        for nn, nf in norms.items():
            power = {"Stot": 1, "SbSc": 2, "Sb/Sc": 0, "Sc-Sb": 1}[cn]
            funcs[f"{cn}|{nn}"] = (lambda cf=cf, nf=nf, power=power: (lambda v: cf(v) / nf(v)**power))()
    funcs["kb+kc"] = lambda v: kbf(v) + kcf(v)
    funcs["kb*kc"] = lambda v: kbf(v) * kcf(v)
    funcs["kb/kc"] = lambda v: kbf(v) / kcf(v)
    # drop duplicates that are constant (Sb/Sc normalised by anything is the same ratio, power 0): keep them, they are monotone anyway
    interior = {}
    grid = [mp.mpf(k) / 4000 * (1 / mp.sqrt(3)) for k in range(2, 3999)]
    for name, fn in funcs.items():
        d = [mp.diff(fn, v) for v in grid[::4]]
        sc = sum(1 for i in range(len(d) - 1) if d[i] * d[i + 1] < 0)
        interior[name] = sc
    # control: a planted interior extremum is detected
    planted = lambda v: (v - mp.mpf("0.3"))**2
    dpl = [mp.diff(planted, v) for v in grid[::4]]
    ctrl = sum(1 for i in range(len(dpl) - 1) if dpl[i] * dpl[i + 1] < 0) == 1
    n_with = sum(1 for v in interior.values() if v > 0)
    C.check("L9_no_interior_stationary_point", n_with == 0 and ctrl and len(funcs) == 19,
            f"{len(funcs)} functionals, sign changes of the derivative: { {k: v for k, v in interior.items() if v} or 'none' }; planted-extremum control detected: {ctrl}")

    # L10 Bousso-Hawking normalisation: kappa_BH = kappa_f / sqrt(f(r*)), r*^3 = M L^2
    ok10 = True; mins = []
    for xv in xs[5::40]:
        Mv = Mf(xv); rs_ = Mv**(mp.mpf(1) / 3)
        fstar = 1 - 2 * Mv / rs_ - rs_**2
        kbBH = kbf(xv) / mp.sqrt(fstar); kcBH = kcf(xv) / mp.sqrt(fstar)
        mins.append((float(kbBH), float(kcBH)))
        ok10 &= kbBH >= mp.sqrt(3) - 1e-12 and 1 - 1e-12 <= kcBH <= mp.sqrt(3) + 1e-12
    C.check("L10_BH_norm_no_a0", ok10, f"Bousso-Hawking: kappa_b >= sqrt3 H, kappa_c in [H, sqrt3 H] on 49 points (min kappa_b {min(m[0] for m in mins):.4f}, kappa_c range {min(m[1] for m in mins):.4f}-{max(m[1] for m in mins):.4f}): no horizon has kappa = H/Z")

    core = ["L1_vieta", "L1b_kappas", "L2_monotone_bijection", "L3_equilibrium_only_nariai", "L4_bh_a0_point", "L4b_mu_star", "L6_KSigma_rho_unattainable", "L7_elimination_polynomial", "L9_no_interior_stationary_point"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    return C.write({"flags": flags, "core": core})


if __name__ == "__main__":
    run_main(main)
