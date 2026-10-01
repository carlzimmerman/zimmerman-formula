"""CFG263 / NG-E: independent re-derivation of lane E's computable claims.
Written without opening agents/E_literature_a0_coefficient/*.py or *.out. c = G = 1.

What can be re-derived from formulas (the literature reading itself cannot be re-done here without the papers):
 E1  T - T_Lambda family: 2 pi (T - T_L) = sqrt(a^2 + H^2) - H  =>  deep limit a^2 = (2H) g  (a0 = 2H); the a dT/da functional gives a0 = H
 E2  Verlinde: a_M = (d-3)/((d-2)(d-1)) a0  -> 1/6 at d = 4; Z_V = 6; kappa_V = sqrt(2 pi/27); equality with the framework iff pi = 27/8
 E3  van Putten: a0 = 2 c H/(1 + 2 pi sqrt2) = 0.2023 cH
 E4  pi-parity lemma: kappa^2 = 8 pi/(3 Z^2); Z = q pi^j (q algebraic) gives rational kappa^2 iff j = 1/2
 E5  the area form: at kappa = 1/2, a0^2 A_dS = 3/8 (no pi), and 1/A_dS = (2/3) G rho_Lambda  ("1/area" = density class)
 E6  Milgrom naturalness: a constant F0 in three normalisations; |F0| = 4 only in the a0^2/G one
 E7  Verlinde's d-continuation (d-1)(d-2)/(d-3) has minimum 3 + 2 sqrt2 > Z for real d > 3
"""
import sympy as sp
import mpmath as mp
from cfg263_lib import Checks, run_main

mp.mp.dps = 50


def main():
    C = Checks("NG-E")
    a, H, g, d = sp.symbols("a H g d", positive=True)
    Zfw = sp.sqrt(32 * sp.pi / 3)

    # E1: T - T_Lambda
    lhs = sp.sqrt(a**2 + H**2) - H
    ser = sp.series(lhs, a, 0, 4).removeO()
    C.check("E1_T_minus_TL_deep_limit", sp.simplify(ser - a**2 / (2 * H)) == 0, f"sqrt(a^2+H^2) - H = {ser} + O(a^4): a^2 = 2H g, a0 = 2H")
    adTda = a * sp.diff(sp.sqrt(a**2 + H**2), a)
    ser2 = sp.series(adTda, a, 0, 4).removeO()
    C.check("E1b_adTda_functional", sp.simplify(ser2 - a**2 / H) == 0, f"2 pi a dT/da = {ser2} + ...: a0 = H (coefficient 2 or 1 by choice of functional)")
    # a0 = q H gives kappa = q sqrt(8 pi/3): for q = 2, kappa = 2 sqrt(8pi/3) = Z_fw (lane E's 'coincidence of how Z is defined')
    C.check("E1c_2H_equals_Zfw_kappa", sp.simplify(2 * sp.sqrt(8 * sp.pi / 3) - Zfw) == 0,
            "a0 = 2H corresponds to kappa = 2 sqrt(8pi/3) = Z_fw: 11.6x the framework a0 (= 2Z x cH/Z)")

    # E2: Verlinde
    aM = (d - 3) / ((d - 2) * (d - 1))
    C.check("E2_verlinde_one_sixth", aM.subs(d, 4) == sp.Rational(1, 6), "a_M = a0/6 at d = 4 (a0 := cH0): Z_V = 6")
    kV = sp.sqrt(8 * sp.pi / 3) / 6
    C.check("E2b_kappa_V", sp.simplify(kV - sp.sqrt(2 * sp.pi / 27)) == 0, f"kappa_V = sqrt(2 pi/27) = {float(kV):.6f}")
    C.check("E2c_equal_iff_pi_27_8", sp.solve(sp.Eq(36, 32 * sp.Symbol('p') / 3), sp.Symbol('p'))[0] == sp.Rational(27, 8),
            "Z_V = Z_fw iff pi = 27/8")
    C.value("kappa_Verlinde", kV)

    # E3: van Putten
    vp = 2 / (1 + 2 * sp.pi * sp.sqrt(2))
    C.check("E3_vanPutten", abs(float(vp) - 0.2023) < 5e-5, f"2/(1 + 2 pi sqrt2) = {float(vp):.5f}")
    C.value("vanPutten_a0_over_cH", vp)

    # E4: pi-parity
    q, j = sp.symbols("q j", positive=True)
    k2 = sp.Rational(8, 3) * sp.pi / (q * sp.pi**j)**2
    expo = sp.simplify(sp.log(k2.subs(q, 1) / sp.Rational(8, 3), sp.pi))
    C.check("E4_pi_exponent", sp.simplify(sp.expand_log(expo, force=True) - (1 - 2 * j)) == 0, "kappa^2 = (8/(3q^2)) pi^(1-2j)")
    C.check("E4b_rational_iff_j_half", sp.solve(sp.Eq(1 - 2 * j, 0), j) == [sp.Rational(1, 2)],
            "for algebraic q, kappa^2 is algebraic iff j = 1/2 (Lindemann for integer j != 1/2); Z_fw = sqrt(32/3) pi^(1/2)")
    # integer-relation illustration for j in {-1,0,1,2} at q = 1
    hits = []
    for jj in (-1, 0, 1, 2):
        val = mp.mpf(8) / 3 * mp.pi**(1 - 2 * jj)
        try:
            p = mp.findpoly(val, 6, maxcoeff=1000)
        except Exception:
            p = None
        hits.append(p is not None)
    C.check("E4c_integer_j_no_relation", not any(hits), f"findpoly on kappa^2 for j = -1,0,1,2: {hits}")

    # E5: area form
    a0, Lam = sp.symbols("a0 Lambda", positive=True)
    L2 = 3 / Lam
    A_dS = 4 * sp.pi * L2
    expr = (a0**2 * A_dS).subs(Lam, 32 * sp.pi * a0**2)
    C.check("E5_area_form_pi_free", sp.simplify(expr - sp.Rational(3, 8)) == 0, "at Lambda = 32 pi a0^2: a0^2 A_dS = 3/8 (no pi)")
    rho = sp.symbols("rho", positive=True)
    C.check("E5b_inverse_area_is_density", sp.simplify((1 / A_dS).subs(Lam, 8 * sp.pi * rho) - sp.Rational(2, 3) * rho) == 0,
            "1/A_dS = (2/3) G rho_Lambda: '1/area' and 'density' are one u-algebraic class (E's 'or 1/area' is exact)")
    # contrast: radius form is pi-carrying
    expr_r = (a0**2 * L2).subs(Lam, 32 * sp.pi * a0**2)
    C.check("E5c_radius_form_pi", sp.simplify(expr_r - 3 / (32 * sp.pi)) == 0, "a0^2 L^2 = 3/(32 pi): a radius-first route needs a transcendental coefficient")

    # E6: Milgrom naturalness, three normalisations of the constant F0 in the a0-sector Lagrangian
    F0 = sp.symbols("F0")
    # (i) L = -(a0^2/G) F  [E's choice]   (ii) L = -(a0^2/(8 pi G)) F  [Poisson/K]   (iii) L = -(a0^2/(16 pi G)) F
    out = {}
    for name, norm in (("a0^2/G", 1), ("a0^2/(8piG)", 1 / (8 * sp.pi)), ("a0^2/(16piG)", 1 / (16 * sp.pi))):
        rhoF = norm * a0**2 * F0  # vacuum energy density of the constant
        kappa2 = sp.simplify(a0**2 / rhoF)
        sol = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), F0)
        out[name] = sol[0]
    C.check("E6_F0_normalisations", out == {"a0^2/G": 4, "a0^2/(8piG)": 32 * sp.pi, "a0^2/(16piG)": 64 * sp.pi},
            f"F0 needed for kappa = 1/2: {out} (E: |F0| = 4 in its normalisation; the 8 pi/16 pi of the coupling is the ambiguity)")

    # E7: Verlinde d-continuation
    Zd = (d - 1) * (d - 2) / (d - 3)
    crit = sp.solve(sp.diff(Zd, d), d)
    crit = [c for c in crit if c.is_real and c > 3]
    zmin = sp.simplify(Zd.subs(d, crit[0]))
    C.check("E7_verlinde_d_min", sp.simplify(zmin - (3 + 2 * sp.sqrt(2))) == 0 and float(zmin) > float(Zfw),
            f"min over d > 3 at d = {crit[0]}: {zmin} = {float(zmin):.4f} > Z_fw = {float(Zfw):.4f}")

    # Scope: E's headline 'no published route derives kappa = 1/2' covers the works listed; the README table row
    # 'horizon-first routes give rational Z' drops E's own '(or 1/area)' (E5b): an area-first route is pi-allowed.
    core = ["E1_T_minus_TL_deep_limit", "E2_verlinde_one_sixth", "E3_vanPutten", "E4b_rational_iff_j_half", "E5_area_form_pi_free", "E6_F0_normalisations", "E7_verlinde_d_min"]
    step_false = not all(r["pass"] for r in C.rows if r["id"] in core)
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    return C.write({"flags": flags, "core": core})


if __name__ == "__main__":
    run_main(main)
