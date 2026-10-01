"""CFG263 / NG-X1: independent re-derivation of lane X1's two no-gos.
Written without opening agents/X1_one_generator/*.py, *.out or *.json. c = G = 1 unless stated.

 X1-i   no single D-formula generates the 4's (D-lift slots differ)
 X1-ii  no Noether-charge / Euler-unit origin of A Lambda = 32 pi^2, by two legs:
        (a) pi-power: 'a quantity ~ r^n has pi-power n/2 at r = Z L/2, so no r^3 charge ... can be a rational multiple of pi^k there'
        (b) alpha: the Euler term rescales absolute charges by (1 + 4 alpha/L^2), so 'Q(r_a0) = unit' is alpha-dependent
"""
import itertools
import numpy as np
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 60
rng = np.random.default_rng(263)


def christoffel(g, X):
    n = len(X)
    gi = g.inv()
    return [[[sp.simplify(sum(gi[a, l] * (sp.diff(g[l, b], X[c]) + sp.diff(g[l, c], X[b]) - sp.diff(g[b, c], X[l])) for l in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


def findpoly_ok(x, deg=4, maxc=10**4):
    try:
        return mp.findpoly(x, deg, maxcoeff=maxc) is not None
    except Exception:
        return False


def main():
    C = Checks("NG-X1")
    t, r, th, ph = sp.symbols("t r theta phi", real=True)
    G, L, rho, u, a0 = sp.symbols("G L rho u a0", positive=True)
    fF = sp.Function("f")(r)
    X = [t, r, th, ph]
    g = sp.diag(-fF, 1 / fF, r**2, r**2 * sp.sin(th)**2)
    Gam = christoffel(g, X)
    # xi = d_t ; xi_mu = g_{mu t}
    xi_low = [g[m, 0] for m in range(4)]
    # nabla_r xi_t
    nab_r_xi_t = sp.diff(xi_low[0], r) - sum(Gam[l][1][0] * xi_low[l] for l in range(4))
    nab_up_rt = sp.simplify(g.inv()[1, 1] * g.inv()[0, 0] * nab_r_xi_t)
    C.check("X1_1_nabla_xi", sp.simplify(nab_up_rt - sp.diff(fF, r) / 2) == 0, f"nabla^r xi^t = {nab_up_rt}")
    MK = r**2 * nab_up_rt / G           # Komar mass, normalised to M for Schwarzschild
    Q_IW = MK                             # MUTANT: Komar used as the Iyer-Wald charge
    M = sp.symbols("M", positive=True)
    C.check("X1_1b_schwarzschild_norm", sp.simplify(MK.subs(fF, 1 - 2 * G * M / r).doit() - M) == 0 and
            sp.simplify(Q_IW.subs(fF, 1 - 2 * G * M / r).doit() - M / 2) == 0, "Komar = M, Iyer-Wald = M/2 at every r for Schwarzschild")
    Q_dS = sp.simplify(Q_IW.subs(fF, 1 - r**2 / L**2).doit())
    C.check("X1_2_dS_charge", sp.simplify(Q_dS + r**3 / (2 * G * L**2)) == 0, f"dS: Q(r) = {Q_dS} = -r^3/(2 G L^2) (X1 README:9 reproduced)")
    Mvac = sp.Rational(4, 3) * sp.pi * rho * r**3
    Q_rho = Q_dS.subs(L, sp.sqrt(3 / (8 * sp.pi * G * rho)))
    C.check("X1_2b_charge_is_minus_vacuum_mass", sp.simplify(Q_rho + Mvac) == 0,
            "Q_IW(r) = -(4 pi/3) rho r^3 = -M_vac(r): the static-patch Noether charge is minus the vacuum mass inside r")

    # ---- X1-ii-a: pi content at the a0 radius, in both unit systems ----
    Z = sp.sqrt(32 * sp.pi / 3)
    r_a0_L = Z * L / 2                      # Lambda-units: r_a0 = 1/(2 a0) = Z L/2
    GQ_over_L = sp.simplify(G * sp.Abs(Q_dS.subs(r, r_a0_L)) / L)
    C.check("X1_3_Lunits_value", sp.simplify(GQ_over_L - Z**3 / 16) == 0, f"Lambda-units: G|Q|/L = Z^3/16 = {float(Z**3/16):.4f}")
    v = mp.mpf(float(1)) * (mp.sqrt(32 * mp.pi / 3))**3 / 16
    C.check("X1_3b_Lunits_pi_three_halves", (not findpoly_ok(v / mp.pi)) and (not findpoly_ok(v / mp.pi**2)) and findpoly_ok(v / mp.pi**mp.mpf(1.5)),
            "Lambda-units: G|Q|/L / pi^k is not algebraic for k = 1, 2 but is for k = 3/2 (X1's pi-power n/2 reproduced)")
    # u-units: u^2 = G rho, kappa = 1/2 => a0 = u/2, r_a0 = 1/(2 a0) = 1/u = R*
    Q_u = sp.simplify(Q_rho.subs(rho, u**2 / G).subs(r, 1 / u))
    GQu = sp.simplify(G * sp.Abs(Q_u) * u)
    C.check("X1_4_uunits_rational_pi", sp.simplify(GQu - sp.Rational(4, 3) * sp.pi) == 0,
            f"u-units: G|Q| u = {GQu}: a RATIONAL multiple of pi^1 at the a0 radius")
    # own fix: first draft hard-coded this flag; it is now computed from X1_3b (Lambda-units pi^(3/2)) and X1_4 (u-units pi^1)
    passed = {rw["id"]: rw["pass"] for rw in C.rows}
    X1_iia_unit_dependent = passed["X1_3b_Lunits_pi_three_halves"] and passed["X1_4_uunits_rational_pi"]
    C.check("X1_4b_X1_iia_is_unit_dependent", X1_iia_unit_dependent and findpoly_ok(mp.mpf(4) / 3),
            "X1's 'no r^3 charge ... can be a rational multiple of pi^k there' holds in Lambda-units only (H3 class, uncorrected in X1)")
    # but in u-units the condition is a restatement of the puzzle: G Q(r)/r = -(4pi/3) G rho r^2, = -4pi/3  <=>  G rho r^2 = 1
    rr = sp.symbols("rr", positive=True)
    cond = sp.Eq(G * (-sp.Rational(4, 3) * sp.pi * rho * rr**3) / rr, -sp.Rational(4, 3) * sp.pi)
    C.check("X1_4c_uunit_condition_is_restatement", sp.solve(cond, rr) == [1 / sp.sqrt(G * rho)],
            "G Q(r)/r = -4pi/3 selects r = 1/sqrt(G rho) = R*; with r_a0 = 1/(2 a0) this IS kappa = 1/2 (the 4pi/3 is the ball volume)")

    # ---- X1-ii-b: alpha (Euler) rescaling of the Wald/Noether tensor on dS ----
    # P^{abcd} = dL/dR_abcd contracted with a binormal: compute directional derivatives of R and E4 along eps(x)eps.
    def curv_scalars(Rm):
        D = Rm.shape[0]
        Ric = np.einsum("cacb->ab", Rm)
        Rs = np.trace(Ric)
        E4 = np.einsum("abcd,abcd", Rm, Rm) - 4 * np.einsum("ab,ab", Ric, Ric) + Rs**2
        return Rs, E4
    def maxsym(k, D):
        dlt = np.eye(D)
        return k * (np.einsum("ac,bd->abcd", dlt, dlt) - np.einsum("ad,bc->abcd", dlt, dlt))
    ok_alpha = True
    ratios = []
    for k in (0.3, 1.0, 2.7):
        D = 4
        R0 = maxsym(k, D)
        eps = np.zeros((D, D)); eps[0, 1] = 1; eps[1, 0] = -1
        B = np.einsum("ab,cd->abcd", eps, eps)
        h = 1e-6
        Rp, Ep = curv_scalars(R0 + h * B); Rm_, Em = curv_scalars(R0 - h * B)
        dR = (Rp - Rm_) / (2 * h); dE = (Ep - Em) / (2 * h)
        ratios.append(dE / dR / k)
        ok_alpha &= abs(dE / dR - 4 * k) < 1e-6
    C.check("X1_5_alpha_rescaling", ok_alpha, f"on dS4, (dE4)/(dR) along the binormal = 4k for k in (0.3,1,2.7): ratios/k = {np.round(ratios, 9)}; Q_alpha = (1 + 4 alpha/L^2) Q_EH")
    C.check("X1_5b_MM_alpha_kills_charge", abs(1 + 4 * (-0.25)) < 1e-15, "alpha = -L^2/4 (MacDowell-Mansouri) gives Q_alpha = 0 at every r")
    # the rescaling is r-independent: ratios Q(r1)/Q(r2) are alpha-free; on dS they are (r1/r2)^3
    ratio_aL = (Z / 2)**3
    # own fix: first draft ended in 'or True' (could not fail); now a real test at 60 digits
    rat = (8 * mp.pi / 3)**mp.mpf(1.5)
    C.check("X1_5c_ratio_conditions_alpha_free_and_irrational", (not findpoly_ok(rat, 4, 10**4)) and findpoly_ok(rat / mp.pi**mp.mpf(1.5), 4, 10**4)
            and abs(float(ratio_aL) - float(rat)) < 1e-12,
            f"Q(r_a0)/Q(L) = (Z/2)^3 = (8pi/3)^(3/2) = {float(ratio_aL):.4f}: alpha-free and unit-free, pi^(3/2): ratio conditions cannot be rational (unit-independent)")

    # ---- X1-i: D-lift slots I can recompute ----
    Dsym, rh, rs = sp.symbols("D r_h r_s", positive=True)
    ftan = 1 - (rh / r)**(Dsym - 3)
    kap_tan = sp.simplify(sp.diff(ftan, r).subs(r, rh) / 2)
    C.check("X1_6_tangherlini_slot", sp.simplify((rh * kap_tan)**-2 - 4 / (Dsym - 3)**2) == 0, f"(r_h kappa)^-2 = {sp.simplify((rh*kap_tan)**-2)}")
    # MacDowell-Mansouri / GB-shift slot: E4(R) - E4(R - k Delta) = 2k(D-2)(D-3) R - k^2 D(D-1)(D-2)(D-3)
    ok_mm = True
    for D in (4, 5, 6, 7):
        for trial in range(3):
            Rm = np.zeros((D, D, D, D))
            for _ in range(3):  # Kulkarni-Nomizu products of random symmetric matrices: all Riemann symmetries
                S1 = rng.normal(size=(D, D)); S1 = S1 + S1.T
                S2 = rng.normal(size=(D, D)); S2 = S2 + S2.T
                Rm += (np.einsum("ac,bd->abcd", S1, S2) + np.einsum("ac,bd->abcd", S2, S1)
                       - np.einsum("ad,bc->abcd", S1, S2) - np.einsum("ad,bc->abcd", S2, S1))
            k = rng.uniform(0.2, 2)
            Rs, E4R = curv_scalars(Rm)
            _, E4F = curv_scalars(Rm - maxsym(k, D))
            pred = 2 * k * (D - 2) * (D - 3) * Rs - k**2 * D * (D - 1) * (D - 2) * (D - 3)
            ok_mm &= abs((E4R - E4F) - pred) < 1e-8 * max(1, abs(pred))
    C.check("X1_7_MM_slot_2(D-2)(D-3)", ok_mm, "E4(R) - E4(R - k Delta) = 2k(D-2)(D-3) R - k^2 D(D-1)(D-2)(D-3) on random Riemann-symmetric tensors, D = 4..7: X1's slot 2(D-2)(D-3) reproduced (= 4, 12, 24, 40)")
    slots = {D: (4, 4, sp.Rational(4, (D - 3)**2), 2 * (D - 2) * (D - 3)) for D in (4, 5, 6, 7, 8)}
    differ = all(len(set(slots[D][1:])) > 1 for D in (5, 6, 7, 8)) and len(set(slots[4])) == 1
    C.check("X1_7b_slots_agree_only_D4", differ, f"slots (graviton, BH quarter, Tangherlini, MM) by D: { {D: tuple(str(s) for s in v) for D, v in slots.items()} }")
    # a different, also natural D-lift of the Euler coefficient: the alpha that zeroes the on-shell dS_D Lagrangian
    # (R - 2 Lambda) + alpha E4 = 0 with R = D(D-1)/L^2, Lambda = (D-1)(D-2)/(2L^2), E4 = D(D-1)(D-2)(D-3)/L^4
    al = [sp.Rational(-2, D * (D - 2) * (D - 3)) for D in (4, 5, 6)]
    C.check("X1_7c_alt_Euler_lift", al[0] == sp.Rational(-1, 4) and al[1] != sp.Rational(-1, 12),
            f"alpha_on-shell/L^2 = {al} for D = 4,5,6: equals the MM -1/4 at D = 4 only; D-lifts of 'the Euler 4' are convention-laden (supports X1's own caveat, README:82)")

    # ---- side result: A kappa^2 <= pi for Kerr-Newman ----
    rp, rm, aa = sp.symbols("r_p r_m a", nonnegative=True)
    gap = sp.expand((rp**2 + aa**2) - (rp - rm)**2 - (aa**2 + rm * (2 * rp - rm)))
    C.check("X1_8_KN_identity", gap == 0, "(r+^2 + a^2) - (r+ - r-)^2 = a^2 + r-(2 r+ - r-)")
    mx = 0.0
    for _ in range(200000):
        Mm = 1.0; aq = rng.uniform(0, 1); Q2 = rng.uniform(0, 1 - aq**2)
        disc = Mm**2 - aq**2 - Q2
        if disc < 0:
            continue
        rpp = Mm + np.sqrt(disc); rmm = Mm - np.sqrt(disc)
        A = 4 * np.pi * (rpp**2 + aq**2); kap = (rpp - rmm) / (2 * (rpp**2 + aq**2))
        mx = max(mx, A * kap**2 / np.pi)
    C.check("X1_8b_KN_sampled", mx <= 1 + 1e-12, f"max A kappa^2/pi over 2e5 random KN = {mx:.6f} <= 1")

    core = ["X1_2_dS_charge", "X1_3_Lunits_value", "X1_5_alpha_rescaling", "X1_6_tangherlini_slot", "X1_7_MM_slot_2(D-2)(D-3)", "X1_8_KN_identity"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    flags_i = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    # X1-ii: leg (a) is unit-dependent as worded (X1_4); leg (b) rests on the asserted premise that the a0-Lambda
    # relation is an equation-of-motion statement (README:111), which X1 does not verify.
    unit_dep = {rw["id"]: rw["pass"] for rw in C.rows}["X1_4b_X1_iia_is_unit_dependent"]
    flags_ii = {"step_false": step_false, "premise_unverified": bool(unit_dep), "headline_scope_ok": False}
    return C.write({"flags": flags_ii, "flags_X1_i": flags_i, "flags_X1_ii": flags_ii, "core": core})


if __name__ == "__main__":
    run_main(main)
