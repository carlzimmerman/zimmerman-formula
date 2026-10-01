"""CFG263 / NG-S61: independent re-derivation of the sol61 canonical-clock coefficient bound and BBN rejection.
Written without opening sol61_push/clock_bbn.py, clock_coefficient_bound.py or their runs. c = hbar = 1, M^2 = 1/(8 pi G).

 S1  minisuperspace Friedmann constraint of (M^2/2)(K_ij K^ij - lambda K^2) - U0  =>  H^2 = 2 U0 / (3 M^2 (3 lambda - 1))
 S2  Lambda_geom = 16 pi G U0/(3 lambda - 1); G_cosm = 2G/(3 lambda - 1)
 S3  auxiliary stationarity: a = P + 12 pi G K q P^2
 S4  C = Lambda_geom/a0_N^2 = 4D(1+D)^2/(3(3 lambda - 1)) from the stated G_N, a0_N, q0, U0, D (static law taken as the lane's premise)
 S5  R = 2D/((1+D)(3 lambda - 1)); C = (2/3) R (1+D)^3; lambda > 1 <=> D(1-R) > R
 S6  C > (2/3) R/(1-R)^3, increasing in R; at R >= 0.92: C > 1197.9 = 11.92 x 32 pi
 S7  at C = 32 pi: D_min (1+D_min)^2 = 48 pi, R < D_min/(1+D_min) = 0.82387, H/H_std < 0.90768
 S8  kinetic branches; S9 the radiation diagnostics
"""
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 40


def main():
    C = Checks("NG-S61")
    a, ad, N, M2, lam, U0, G = sp.symbols("a adot N M2 lambda U0 G", positive=True)
    # S1: h_ij = a^2 delta_ij, K_ij = (1/2N) dh_ij/dt = a adot/N delta_ij; K^i_j = adot/(a N) delta
    KK = 3 * (ad / (a * N))**2
    Ktr = 3 * ad / (a * N)
    Lmini = a**3 * N * (M2 / 2 * (KK - lam * Ktr**2) - U0)
    constraint = sp.diff(Lmini, N).subs(N, 1)
    Hs = sp.symbols("H", positive=True)
    # own fix: the first draft's extraction squared H^2 a second time; solve for H > 0 and square once
    Hsol = sp.solve(sp.Eq(constraint.subs(ad, Hs * a), 0), Hs)
    H2val = sp.simplify(Hsol[0]**2)
    C.check("S1_friedmann_constraint", sp.simplify(H2val - 2 * U0 / (3 * M2 * (3 * lam - 1))) == 0,
            f"dL/dN = 0 at N = 1: H^2 = {sp.simplify(H2val)}")
    Lam_geom = sp.simplify(3 * H2val.subs(M2, 1 / (8 * sp.pi * G)))
    C.check("S2_lambda_geom", sp.simplify(Lam_geom - 16 * sp.pi * G * U0 / (3 * lam - 1)) == 0, f"Lambda_geom = 3H^2 = {Lam_geom}")
    Gc = sp.simplify(Lam_geom / (8 * sp.pi * U0))
    C.check("S2b_G_cosm", sp.simplify(Gc - 2 * G / (3 * lam - 1)) == 0, f"G_cosm = Lambda_geom/(8 pi U0) = {Gc}")

    # S3 auxiliary polarization: stationarity in P of 2 M^2 (P a - P^2/2) - K q P^3
    P, acc, Kc, q = sp.symbols("P a_acc K_c q", positive=True)
    Laux = 2 * (1 / (8 * sp.pi * G)) * (P * acc - P**2 / 2) - Kc * q * P**3
    accsol = sp.solve(sp.diff(Laux, P), acc)[0]
    C.check("S3_aux_stationarity", sp.simplify(accsol - (P + 12 * sp.pi * G * Kc * q * P**2)) == 0, f"a = {sp.simplify(accsol)}")

    # S4 C from the stated static law (premises of CANONICAL_CLOCK_RESULTS.md:57-59)
    A, B, D = sp.symbols("A B D", positive=True)
    q0 = (A / B)**sp.Rational(1, 4)
    U0v = 2 * sp.sqrt(A * B)
    Dv = 12 * sp.pi * G * (2 * A * Kc**2)**sp.Rational(1, 3)
    a0N = (Dv / (1 + Dv)) / (12 * sp.pi * G * Kc * q0)
    Cval = sp.simplify((16 * sp.pi * G * U0v / (3 * lam - 1)) / a0N**2)
    Cform = 4 * Dv * (1 + Dv)**2 / (3 * (3 * lam - 1))
    C.check("S4_C_formula", sp.simplify(Cval - Cform) == 0, "Lambda_geom/a0_N^2 = 4D(1+D)^2/(3(3 lambda - 1)) (from the stated q0, U0, D, a0_N)")
    # also check U0 = 2 sqrt(AB) is the minimum of A/q^2 + B q^2 at q0 = (A/B)^(1/4)
    qq = sp.symbols("qq", positive=True)
    Uq = A / qq**2 + B * qq**2
    C.check("S4b_vacuum_min", sp.simplify(sp.diff(Uq, qq).subs(qq, q0)) == 0 and sp.simplify(Uq.subs(qq, q0) - U0v) == 0, "q0 = (A/B)^(1/4), U0 = 2 sqrt(AB)")

    # S5 elimination
    GN = G * (1 + D) / D
    R = sp.simplify((2 * G / (3 * lam - 1)) / GN)
    Cd = 4 * D * (1 + D)**2 / (3 * (3 * lam - 1))
    C.check("S5_R_formula", sp.simplify(R - 2 * D / ((1 + D) * (3 * lam - 1))) == 0, f"R = G_cosm/G_N = {R}")
    C.check("S5b_elimination", sp.simplify(Cd - sp.Rational(2, 3) * R * (1 + D)**3) == 0, "C = (2/3) R (1+D)^3 (lambda eliminated, no target imposed)")
    lam_of = sp.solve(sp.Eq(sp.Symbol("Rr"), R), lam)[0]
    Rr = sp.symbols("Rr", positive=True)
    cond = sp.simplify(lam_of.subs(sp.Symbol("Rr"), Rr) - 1)
    # lambda - 1 > 0  <=>  D(1-R) > R  (for R > 0)
    test = all(((float(cond.subs({Rr: rv, D: dv})) > 0) == (dv * (1 - rv) > rv)) for rv in (0.1, 0.5, 0.8, 0.95) for dv in (0.05, 0.5, 2, 9, 40))
    C.check("S5c_lambda_gt_1_iff", test, "lambda > 1 <=> D(1 - R) > R on a 4 x 5 grid (and the sign algebra)")

    # S6 bound
    Rv = sp.symbols("R_v", positive=True)
    lb = sp.Rational(2, 3) * Rv / (1 - Rv)**3
    dlb = sp.simplify(sp.diff(lb, Rv) - sp.Rational(2, 3) * (1 + 2 * Rv) / (1 - Rv)**4)
    C.check("S6_lower_bound_increasing", dlb == 0, "d/dR [(2/3) R/(1-R)^3] = (2/3)(1+2R)/(1-R)^4 > 0")
    val = lb.subs(Rv, sp.Rational(92, 100))
    C.check("S6b_at_0p92", abs(float(val) - 1197.9166667) < 1e-6 and abs(float(val / (32 * sp.pi)) - 11.9158974) < 1e-6,
            f"(2/3)(0.92)/(0.08)^3 = {float(val):.7f} = {float(val/(32*sp.pi)):.7f} x 32 pi")
    # strictness: C - (2/3) R/(1-R)^3 > 0 whenever lambda > 1 (sampled) -- the analytic chain is 1 + D > 1/(1-R)
    ok = True
    for dv in (0.3, 1.0, 4.7, 12.0, 50.0):
        for lv in (1.0001, 1.2, 2.0, 7.0):
            Rn = float(R.subs({D: dv, lam: lv})); Cn = float(Cd.subs({D: dv, lam: lv}))
            ok &= Cn > float(lb.subs(Rv, Rn))
    C.check("S6c_bound_holds_samples", ok, "C > (2/3) R/(1-R)^3 on 20 (D, lambda > 1) samples")

    # S7 target 32 pi
    Dmin = mp.findroot(lambda d: d * (1 + d)**2 - 48 * mp.pi, 4.7)
    Rmax = Dmin / (1 + Dmin)
    C.check("S7_Rmax", abs(Rmax - mp.mpf("0.8238740919142051")) < 1e-14 and abs(mp.sqrt(Rmax) - mp.mpf("0.907675102618886")) < 1e-14 and abs(Dmin - mp.mpf("4.67775639")) < 1e-7,
            f"D_min = {mp.nstr(Dmin, 10)}, R < {mp.nstr(Rmax, 16)}, H/H_std < {mp.nstr(mp.sqrt(Rmax), 15)} (sol61: 0.8238740919142051, 0.907675102618886)")
    C.check("S7b_below_bbn", Rmax < mp.mpf("0.92"), "R_max < 0.92 = lower end of G_BBN/G_0 = 0.98 +- 0.06 (95.4%, as transferred)")
    C.value("R_max", Rmax)

    # S8 kinetic branches
    kin = lambda l: 2 * (3 * l - 1) / (l - 1)
    C.check("S8_kinetic_branches", kin(2.0) > 0 and kin(0.5) < 0 and kin(0.2) > 0 and 2 / (3 * 0.2 - 1) < 0,
            "lambda > 1: healthy; 1/3 < lambda < 1: negative kinetic; lambda < 1/3: positive kinetic but G_cosm < 0")

    # S9 radiation diagnostics
    alpha = mp.mpf(7) / 8 * (mp.mpf(4) / 11)**(mp.mpf(4) / 3)
    dN_early = mp.mpf(43) / 7 * (1 / Rmax - 1)
    dN_late = (1 / alpha + 3) * (1 / Rmax - 1)
    late_ratio_if_early = Rmax * (1 + alpha * (3 + dN_early)) / (1 + 3 * alpha)
    early_ratio_if_late = Rmax * (mp.mpf(43) / 4 + mp.mpf(7) / 4 * dN_late) / (mp.mpf(43) / 4)
    C.check("S9_radiation", abs(dN_early - mp.mpf("1.31320587")) < 1e-7 and abs(dN_late - mp.mpf("1.58264006")) < 1e-7
            and abs(late_ratio_if_early - mp.mpf("0.97001571")) < 1e-7 and abs(early_ratio_if_late - mp.mpf("1.03613625")) < 1e-7,
            f"deltaN early {mp.nstr(dN_early, 9)}, late {mp.nstr(dN_late, 9)}; cross ratios {mp.nstr(late_ratio_if_early, 9)}, {mp.nstr(early_ratio_if_late, 9)}")

    core = ["S1_friedmann_constraint", "S2b_G_cosm", "S4_C_formula", "S5b_elimination", "S6_lower_bound_increasing", "S7_Rmax"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": True}
    return C.write({"flags": flags, "core": core, "premise_not_rederived": "static law G_N = G(1+D)/D, a0_N (CANONICAL_CLOCK_RESULTS.md:55-59)"})


if __name__ == "__main__":
    run_main(main)
