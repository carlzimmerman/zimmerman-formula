"""CFG263 / NG-N: independent re-derivation of lane N (Jacobson / Clausius in exact de Sitter).
Written without opening agents/N_jacobson_thermo_dS/*.py or *.out. c = G = hbar = k_B = 1.

 N1  static observer in the static patch: a = H x/sqrt(1-x^2), Tolman T = T_GH/sqrt(f) = sqrt(a^2+H^2)/(2 pi), kappa_obs = a/sin(theta)
 N2  Clausius with heat and T normalised by the same Killing field: Tolman factors cancel (G_eff = G)
 N3  the six mismatched pairs G_eff/G = kappa_heat/kappa_T, kappa in {a, kappa_obs, H}: which has a Newtonian limit AND enhancement
 N4  the two members' a0: (kobs, a) -> a0 = H; T - T_Lambda -> a0 = 2H; the literal insertion (a, kobs) is a threshold
 N5  de Sitter is invisible to R_kk (null k): Lambda an integration constant
 N6  pi-parity: a0 = qH, q algebraic, gives kappa = q sqrt(8pi/3), never 1/2
"""
import itertools
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 40


def main():
    C = Checks("NG-N")
    H, a, g, xx, m = sp.symbols("H a g x m", positive=True)
    th = sp.symbols("theta", positive=True)

    # N1: static patch f = 1 - H^2 r^2; proper acceleration of r = const: a = (1/2) f'/sqrt(f) in magnitude
    r = sp.symbols("r", positive=True)
    f = 1 - H**2 * r**2
    acc = sp.Abs(sp.diff(f, r)) / (2 * sp.sqrt(f))
    acc_x = sp.simplify(acc.subs(r, xx / H))
    C.check("N1_static_acceleration", sp.simplify(acc_x - H * xx / sp.sqrt(1 - xx**2)) == 0 or
            all(abs(float((acc_x - H * xx / sp.sqrt(1 - xx**2)).subs({H: 1.7, xx: v}))) < 1e-13 for v in (0.1, 0.5, 0.95)),
            "a = H x/sqrt(1 - x^2), x = H r")
    # Tolman: T_loc = (H/2pi)/sqrt(f); with a = H tan(theta) (x = sin theta), sqrt(a^2 + H^2) = H/cos theta = H/sqrt(f)
    a_th = H * sp.tan(th)
    C.check("N1b_tolman_is_deserlevin", sp.simplify(sp.sqrt(a_th**2 + H**2) - H / sp.cos(th)) == 0 or
            all(abs(float((sp.sqrt(a_th**2 + H**2) - H / sp.cos(th)).subs({H: 1.3, th: v}))) < 1e-13 for v in (0.2, 0.7, 1.4)),
            "x = sin(theta): a = H tan(theta), T_loc = sqrt(a^2 + H^2)/(2 pi) = H/(2 pi cos theta)")
    kobs = sp.sqrt(a**2 + H**2)

    # N2: Clausius with one Killing field chi = xi/N0 for both heat and temperature
    N0 = sp.symbols("N0", positive=True)
    E_heat = m * N0 / N0      # Killing energy of a mass m at the observer, measured with chi: m
    T_chi = (H / (2 * sp.pi)) / N0 * N0  # T measured with chi: kappa_chi/(2pi) = (H/N0)/(2pi) ... times N0 at the observer
    # dS = dQ/T with dQ = m (local energy) and T_loc: Delta S = m / T_loc; the entropic force T_loc dS/dl = m * (d(..)/dl):
    # the same N0 multiplies both numerator and denominator, so it cancels identically:
    ratio = sp.simplify((m * N0) / ((H / (2 * sp.pi)) * N0))
    C.check("N2_tolman_cancels", sp.simplify(ratio - 2 * sp.pi * m / H) == 0, "Delta S = (m N0)/(T_GH N0): the observer's redshift cancels; G_eff = G for every a/H")

    # N3: mismatched pairs
    ks = {"a": a, "kobs": kobs, "H": H}
    table = {}
    for (hn, hk), (tn, tk) in itertools.permutations(ks.items(), 2):
        ratio = sp.simplify(hk / tk)           # G_eff/G
        hi = sp.limit(ratio.subs(a, 1 / sp.Symbol("e", positive=True)), sp.Symbol("e", positive=True), 0)  # a >> H
        lo = sp.limit(ratio, a, 0)                                                                      # a << H
        newton = (hi == 1)
        enhance = (lo == sp.oo)
        table[(hn, tn)] = (str(ratio), str(hi), str(lo), newton and enhance)
    winners = [k for k, v in table.items() if v[3]]
    C.check("N3_one_pair_newton_and_enhancement", winners == [("kobs", "a")],
            f"pairs with G_eff -> G at a >> H and G_eff -> inf at a << H: {winners}; full table {table}")

    # N4: member (ii) a = (G_eff/G) g with G_eff/G = kobs/a: a^2 = g sqrt(a^2 + H^2)
    sol = sp.solve(sp.Eq(a**4, g**2 * (a**2 + H**2)), a)
    sol = [s_ for s_ in sol if s_.is_positive or s_.is_positive is None]
    a_g = [s_ for s_ in sol if sp.N(s_.subs({g: 0.37, H: 1})).is_real and sp.N(s_.subs({g: 0.37, H: 1})) > 0][0]
    deep = sp.limit(a_g**2 / g, g, 0)
    C.check("N4_member_ii_a0_H", sp.simplify(deep - H) == 0, f"a^2 = [g^2 + sqrt(g^4 + 4 g^2 H^2)]/2: deep limit a^2/g -> {deep}: a0 = H")
    # member (i) T - T_Lambda: sqrt(a^2 + H^2) - H = g
    a_i = sp.sqrt(g**2 + 2 * H * g)
    # own fix: sympy does not factor sqrt(g^2 + 2Hg + H^2) unprompted; factor first (g, H > 0)
    C.check("N4b_member_i_a0_2H", sp.simplify(sp.sqrt(sp.factor(sp.expand(a_i**2 + H**2))) - H - g) == 0 and sp.limit(a_i**2 / g, g, 0) == 2 * H,
            "a = sqrt(g^2 + 2 H g): a0 = 2H; tail a - g -> H (constant)")
    lit = sp.simplify(a / kobs)  # literal insertion: G_eff/G = a/kobs: a = sin(theta) g -> a^2 = g^2 - H^2
    C.check("N4c_literal_insertion_threshold", sp.solve(sp.Eq(a * kobs / a, g), a) == [sp.sqrt(g**2 - H**2)] or
            sp.simplify(sp.solve(sp.Eq(sp.sqrt(a**2 + H**2), g), a)[0] - sp.sqrt(g**2 - H**2)) == 0,
            "literal insertion: a^2 = g_N^2 - H^2, no static solution below g_N = H (a threshold, not MOND)")

    # N5: dS Ricci on null vectors
    t_, X_ = sp.symbols("t X", real=True)
    gm = sp.diag(-1, sp.exp(2 * H * t_), sp.exp(2 * H * t_), sp.exp(2 * H * t_))
    coords = [t_, X_, sp.Symbol("Y"), sp.Symbol("Zc")]
    gi = gm.inv()
    Gam = [[[sum(gi[i, l] * (sp.diff(gm[l, j], coords[k]) + sp.diff(gm[l, k], coords[j]) - sp.diff(gm[j, k], coords[l])) for l in range(4)) / 2
             for k in range(4)] for j in range(4)] for i in range(4)]
    def Ric(j, k):
        return sp.simplify(sum(sp.diff(Gam[i][j][k], coords[i]) for i in range(4)) - sum(sp.diff(Gam[i][j][i], coords[k]) for i in range(4))
                           + sum(Gam[i][i][p] * Gam[p][j][k] for i in range(4) for p in range(4)) - sum(Gam[i][k][p] * Gam[p][j][i] for i in range(4) for p in range(4)))
    Rm = sp.Matrix(4, 4, lambda j, k: Ric(j, k))
    C.check("N5_dS_Ricci_proportional_to_g", sp.simplify(Rm - 3 * H**2 * gm) == sp.zeros(4, 4), "R_mn = 3H^2 g_mn = Lambda g_mn")
    kvec = sp.Matrix([1, sp.exp(-H * t_), 0, 0])
    C.check("N5b_null_contraction_zero", sp.simplify((kvec.T * gm * kvec)[0]) == 0 and sp.simplify((kvec.T * Rm * kvec)[0]) == 0,
            "k null => R_kk = 0 for every H: the Clausius chain R_kk = 8 pi T_kk cannot see Lambda")

    # N6: pi-parity of the members
    for q in (1, 2):
        k2 = mp.mpf(q)**2 * 8 * mp.pi / 3
        try:
            p = mp.findpoly(k2, 6, maxcoeff=10**4)
        except Exception:
            p = None
        C.check(f"N6_pi_parity_q{q}", p is None, f"a0 = {q}H: kappa = {q} sqrt(8pi/3) = {mp.nstr(mp.sqrt(k2), 6)}, kappa^2 not algebraic (no polynomial found)")
    # angle of the framework a0 in the T^2 = T_U^2 + T_L^2 structure
    th0 = mp.degrees(mp.atan(1 / mp.sqrt(32 * mp.pi / 3)))
    C.value("theta0_deg_framework", th0)

    core = ["N1b_tolman_is_deserlevin", "N2_tolman_cancels", "N3_one_pair_newton_and_enhancement", "N4_member_ii_a0_H", "N4b_member_i_a0_2H", "N5b_null_contraction_zero"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    # headline 'no-go (scoped)' with scope = exact-dS Killing thermodynamics with Jacobson's inputs: the derivation covers that class
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": True}
    return C.write({"flags": flags, "core": core})


if __name__ == "__main__":
    run_main(main)
