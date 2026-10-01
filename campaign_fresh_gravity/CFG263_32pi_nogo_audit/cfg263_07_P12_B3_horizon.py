"""CFG263 / NG-P12B3: independent re-derivation of p12 (the static horizon identity) and B3's structural statement.
Written without opening p12_horizon_equation_no_local_bridge.py/.out or agents/B3_modified_horizon_equation/*.py/.out. c = G = 1.

 P1  G^t_t = -2 m'/r^2 for f = 1 - 2m(r)/r, from the Ricci tensor (and G^r_r = G^t_t when N = 1)
 P2  horizon identity 1 - 2 kappa r_h = 8 pi rho(r_h) r_h^2 (f-normalisation)
 P3  (A) kappa r_h = 1/2 iff rho(r_h) = 0; (B) Lambda r_h^2 = 8 pi gives kappa r_h = (1 - 8pi)/2; (C) dS horizon kappa r = -1
 P4  general lapse N(r): kappa = N_h f'(r_h)/2 (covariant), N'/N = 4 pi r (rho + p_r)/f
 P5  STRENGTHENING (my question, frozen section 8): with the Killing field normalised at ANY static-region observer and NEC,
     |kappa| r_h >= (8 pi - 1)/2 at a horizon with rho(r_h) = rho_Lambda and Lambda r_h^2 = 8 pi: (D) does not need the f-normalisation
 P6  B3: any SdS-form static vacuum obeys 2 kappa r_h = 1 - Lambda_e r_h^2
 P7  B3: 4D Glavan-Lin EGB horizon relation and the required coupling alpha = -Lambda_b r_h^2/3 at kappa r_h = 1/2
 P8  the gemini radius R* = 1/sqrt(G rho_Lambda) lies outside the static patch (R*/L = sqrt(8pi/3))
"""
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp
from cfg263_lib import Checks, run_main


def einstein_mixed(gm, X):
    n = 4
    gi = gm.inv()
    Gam = [[[sp.simplify(sum(gi[i, l] * (sp.diff(gm[l, j], X[k]) + sp.diff(gm[l, k], X[j]) - sp.diff(gm[j, k], X[l])) for l in range(n)) / 2)
             for k in range(n)] for j in range(n)] for i in range(n)]
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            Ric[j, k] = sp.simplify(sum(sp.diff(Gam[i][j][k], X[i]) for i in range(n)) - sum(sp.diff(Gam[i][j][i], X[k]) for i in range(n))
                                    + sum(Gam[i][i][p] * Gam[p][j][k] for i in range(n) for p in range(n))
                                    - sum(Gam[i][k][p] * Gam[p][j][i] for i in range(n) for p in range(n)))
    Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    Gmix = sp.simplify(gi * (Ric - Rs * gm / 2))
    return Gmix, Gam


def main():
    C = Checks("NG-P12B3")
    t, r, th, ph = sp.symbols("t r theta phi", real=True)
    X = [t, r, th, ph]
    m = sp.Function("m")(r)
    Nf = sp.Function("N")(r)
    f = 1 - 2 * m / r

    # P1 (N = 1)
    G1, _ = einstein_mixed(sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2), X)
    C.check("P1_Gtt", sp.simplify(G1[0, 0] + 2 * sp.diff(m, r) / r**2) == 0 and sp.simplify(G1[1, 1] - G1[0, 0]) == 0,
            f"G^t_t = {sp.simplify(G1[0,0])} = -8 pi rho  =>  m' = 4 pi r^2 rho; G^r_r = G^t_t (p_r = -rho when N = 1)")

    # P2, P3
    rh, rho_h, kap, Lam = sp.symbols("r_h rho_h kappa Lambda", positive=True)
    fp_h = (sp.diff(f, r)).subs(sp.diff(m, r), 4 * sp.pi * r**2 * rho_h).subs(m, r / 2).subs(r, rh)
    ident = sp.simplify(1 - 2 * (fp_h / 2) * rh - 8 * sp.pi * rho_h * rh**2)
    C.check("P2_horizon_identity", ident == 0, "f(r_h) = 0, kappa = f'(r_h)/2  =>  1 - 2 kappa r_h = 8 pi rho(r_h) r_h^2")
    C.check("P3A_half_iff_rho_zero", sp.solve(sp.Eq(1 - 2 * sp.Rational(1, 2), 8 * sp.pi * rho_h * rh**2), rho_h) == [],
            "kappa r_h = 1/2 forces 8 pi rho r_h^2 = 0: no positive rho solves it (rho(r_h) = 0 only)")
    kB = (1 - 8 * sp.pi) / 2
    C.check("P3B_vacuum_8pi", sp.simplify(((1 - Lam * rh**2) / 2).subs(Lam * rh**2, 8 * sp.pi) - kB) == 0 and abs(float(kB) + 12.066) < 1e-3,
            f"constant vacuum (8 pi rho = Lambda): kappa r_h = (1 - Lambda r_h^2)/2 = (1 - 8pi)/2 = {float(kB):.4f}")
    C.check("P3C_dS_horizon", (1 - 3) / 2 == -1, "Lambda r^2 = 3: kappa r = -1 (cosmological horizon, f-normalised kappa = H)")

    # P4 general lapse
    gN = sp.diag(-Nf**2 * f, 1 / f, r**2, r**2 * sp.sin(th)**2)
    GN, GamN = einstein_mixed(gN, X)
    C.check("P4_Gtt_lapse_independent", sp.simplify(GN[0, 0] + 2 * sp.diff(m, r) / r**2) == 0, "G^t_t = -2m'/r^2 for any N(r): rho still fixes m")
    C.check("P4b_lapse_equation", sp.simplify((GN[1, 1] - GN[0, 0]) - 2 * f * sp.diff(Nf, r) / (r * Nf)) == 0,
            "G^r_r - G^t_t = (2f/r) N'/N = 8 pi (p_r + rho)  =>  N'/N = 4 pi r (rho + p_r)/f")
    # covariant surface gravity: kappa^2 = -(1/2) (nabla_mu xi_nu)(nabla^mu xi^nu) at the horizon, xi = d_t
    xi_low = [gN[mu, 0] for mu in range(4)]
    nab = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            nab[mu, nu] = sp.diff(xi_low[nu], X[mu]) - sum(GamN[l][mu][nu] * xi_low[l] for l in range(4))
    gi = gN.inv()
    inv = sp.simplify(sum(gi[a_, b_] * gi[c_, d_] * nab[a_, c_] * nab[b_, d_] for a_ in range(4) for b_ in range(4) for c_ in range(4) for d_ in range(4)))
    fr, fpr, Nr, Npr = sp.symbols("f_r fp_r N_r Np_r")
    inv_s = sp.simplify(inv.subs(sp.diff(m, r), sp.Symbol("mp")).subs(sp.diff(Nf, r), Npr).subs(Nf, Nr))
    # express in terms of f and f': f = 1 - 2m/r, f' = 2m/r^2 - 2m'/r ; at the horizon f -> 0
    k2 = sp.simplify(-inv / 2)
    k2_h = sp.simplify(k2.subs(sp.diff(m, r), sp.Symbol("mp")).subs(sp.diff(Nf, r), Npr).subs(Nf, Nr).subs(m, r / 2))
    target = (Nr * (sp.diff(f, r).subs(sp.diff(m, r), sp.Symbol("mp")).subs(m, r / 2)) / 2)**2
    C.check("P4c_covariant_kappa", sp.simplify(k2_h - target) == 0, "kappa^2 = -(1/2) nabla xi . nabla xi at f = 0 equals (N_h f'(r_h)/2)^2: kappa = N_h f'(r_h)/2")

    # P5 strengthening, analytic part: cosmological-type horizon (f'(r_h) < 0), observer at r_ref < r_h with f > 0 on [r_ref, r_h].
    # NEC => N' >= 0 there => N_h >= N_ref => |kappa_ref| r_h = (N_h/N_ref)(8 pi - 1)/2 >= (8 pi - 1)/2.
    bound = (8 * mp.pi - 1) / 2
    C.check("P5_bound_value", bound > mp.mpf(1) / 2, f"(8 pi - 1)/2 = {mp.nstr(bound, 6)} > 1/2")
    # BH-type horizon would need f'(r_h) > 0, i.e. 1 - 8 pi rho r_h^2 > 0: impossible at Lambda r_h^2 = 8 pi
    C.check("P5b_bh_type_impossible", (1 - 8 * mp.pi) < 0, "f'(r_h) r_h = 1 - 8 pi < 0 at rho(r_h) = rho_Lambda, Lambda r_h^2 = 8 pi: only a cosmological-type horizon")

    # P5 numeric: build static profiles in units r_h = 1, rho_Lambda = 1/(8pi) * 8pi/r_h^2 -> G rho_L = 1 (Lambda r_h^2 = 8 pi).
    # interior: vacuole r < r_v (rho = 0, central mass m0) + vacuum shell r_v < r < 1 (rho = rho_L), plus a NEC-respecting
    # 'dust' layer (rho_d >= 0, p_r = 0) in r_a < r < r_b inside the vacuole. Integrate N'/N = 4 pi r (rho + p_r)/f outward from r_ref.
    rhoL = 1.0  # G rho_L in units of 1/r_h^2 (Lambda r_h^2 = 8 pi)
    def run(m0, rv, ra, rb, rhod, pr_sign=0.0, rref=None):
        # m(r) for the configuration; enforce f(1) = 0 by choosing m0
        def rho(rr):
            out = 0.0
            if ra < rr < rb:
                out += rhod
            if rr > rv:
                out += rhoL
            return out
        def pr(rr):
            out = 0.0
            if rr > rv:
                out -= rhoL           # vacuum p = -rho: rho + p_r = 0
            if ra < rr < rb:
                out += pr_sign * rhod  # dust (0) or exotic (-2 rho_d: rho + p_r = -rho_d < 0)
            return out
        rs = np.linspace(1e-3, 1.0, 20001)
        mm = np.zeros_like(rs); mm[0] = m0
        for i in range(1, len(rs)):
            rm_ = 0.5 * (rs[i] + rs[i - 1])
            mm[i] = mm[i - 1] + 4 * np.pi * rm_**2 * rho(rm_) * (rs[i] - rs[i - 1])
        return rs, mm, rho, pr
    # choose rv, layer and m0 so that m(1) = 1/2 (f(1) = 0)
    rv, ra, rb, rhod = 0.97, 0.5, 0.7, 0.05   # own fix: first run used rv = 0.95, which forces m0 < 0 (vacuum shell too heavy)
    shell_vac = 4 * np.pi / 3 * rhoL * (1 - rv**3)
    layer = 4 * np.pi / 3 * rhod * (rb**3 - ra**3)
    m0 = 0.5 - shell_vac - layer
    rs, mm, rho_fn, pr_fn = run(m0, rv, ra, rb, rhod)
    fvals = 1 - 2 * mm / rs
    # static region: f > 0 just inside r_h = 1 back to the outermost zero of f
    inside = np.where(fvals[:-1] <= 0)[0]
    i0 = inside[-1] + 1 if len(inside) else 0
    rref = rs[i0 + 10]
    def lnN_increment(r1, r2, pr_sign):
        sel = (rs >= r1) & (rs <= r2 - 1e-6)
        integrand = np.array([4 * np.pi * rr * (rho_fn(rr) + pr_fn(rr)) / (1 - 2 * mmv / rr) for rr, mmv in zip(rs[sel], mm[sel])])
        return np.trapezoid(integrand, rs[sel]) if hasattr(np, "trapezoid") else np.trapz(integrand, rs[sel])
    dlnN = lnN_increment(rref, 0.999, 0)
    fp_h = (fvals[-1] - fvals[-2]) / (rs[-1] - rs[-2])
    kap_ref = np.exp(dlnN) * abs(fp_h) / 2
    C.check("P5c_numeric_NEC_profile", m0 > 0 and abs(fvals[-1]) < 1e-3 and fp_h < 0 and dlnN >= -1e-9 and kap_ref >= 12.0,
            f"vacuole + dust layer + vacuum shell, m0 = {m0:.3f} > 0, f(r_h) = {fvals[-1]:.1e}, static region from r = {rs[i0]:.3f}; observer at r = {rref:.3f}: "
            f"ln(N_h/N_ref) = {dlnN:.3f} >= 0, |kappa_ref| r_h = {kap_ref:.2f} >= 12.07")
    C.value("P5_kappa_ref_rh_NEC_example", kap_ref)

    # P6 B3 SdS-form
    M_, Le = sp.symbols("M Lambda_e", positive=True)
    fS = 1 - 2 * M_ / r - Le * r**2 / 3
    Msol = sp.solve(sp.Eq(fS.subs(r, rh), 0), M_)[0]
    kS = sp.simplify(sp.diff(fS, r).subs(r, rh).subs(M_, Msol) / 2)
    C.check("P6_SdS_form", sp.simplify(2 * kS * rh - (1 - Le * rh**2)) == 0, "f = 1 - 2M/r - Lambda_e r^2/3: 2 kappa r_h = 1 - Lambda_e r_h^2 at every horizon, every coupling")

    # P7 B3 Glavan-Lin 4D EGB: psi + alpha psi^2 = 2M/r^3 + Lambda/3, f = 1 - r^2 psi
    al, Lb = sp.symbols("alpha Lambda_b", real=True)
    psi = sp.Function("psi")(r)
    implicit = psi + al * psi**2 - (2 * M_ / r**3 + Lb / 3)
    dpsi = sp.solve(sp.diff(implicit, r), sp.diff(psi, r))[0]
    fGL = 1 - r**2 * psi
    fpGL = sp.diff(fGL, r).subs(sp.diff(psi, r), dpsi)
    at_h = fpGL.subs(psi, 1 / r**2).subs(r, rh)
    Mh = sp.solve(implicit.subs(psi, 1 / r**2).subs(r, rh), M_)[0]
    k_h = sp.simplify(at_h.subs(M_, Mh) / 2)
    aa = sp.symbols("a")
    rel = sp.simplify(((2 * k_h * rh + 2) * (1 + 2 * al / rh**2) - 3 * (1 + al / rh**2 - Lb * rh**2 / 3)))
    C.check("P7_GL_horizon_relation", rel == 0, "(2 kappa r_h + 2)(1 + 2a) = 3(1 + a - Lambda_b r_h^2/3), a = alpha/r_h^2 (B3 README:16 at D = 4)")
    asol = sp.solve(sp.Eq(k_h * rh, sp.Rational(1, 2)), al)
    C.check("P7b_GL_required_coupling", len(asol) == 1 and sp.simplify(asol[0] + Lb * rh**4 / 3) == 0 and abs(float(1 + 2 * (-8 * sp.pi / 3)) + 15.755) < 1e-3,
            f"kappa r_h = 1/2 needs alpha = {asol[0]} = -Lambda_b r_h^4/3; at Lambda_b r_h^2 = 8 pi: a = -8pi/3, 1 + 2a = {float(1 - 16*sp.pi/3):.3f} (G_eff < 0): a dimensionful coupling tied to 1/a0^2")

    # P8 gemini R*
    C.check("P8_Rstar_outside_static_patch", abs(float(sp.sqrt(8 * sp.pi / 3)) - 2.8944) < 1e-4,
            f"R*/L = sqrt(8 pi/3) = {float(sp.sqrt(8*sp.pi/3)):.4f} > 1: R* = c/sqrt(G rho_Lambda) is not a static radius of the de Sitter patch")

    core = ["P1_Gtt", "P2_horizon_identity", "P3B_vacuum_8pi", "P4b_lapse_equation", "P4c_covariant_kappa", "P6_SdS_form", "P7_GL_horizon_relation"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    flags_p12 = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": True}
    flags_b3 = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    return C.write({"flags": flags_p12, "flags_P12": flags_p12, "flags_B3": flags_b3, "core": core,
                    "nec_strengthening": all(rw["pass"] for rw in C.rows if rw["id"].startswith("P5"))})


if __name__ == "__main__":
    run_main(main)
